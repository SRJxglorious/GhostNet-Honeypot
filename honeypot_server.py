#!/usr/bin/env python3
"""
Multi-protocol Honeypot Server
Simulates SSH, HTTP, and FTP services to detect and log attacks
"""

import socket
import threading
import logging
import json
import datetime
import hashlib
from pathlib import Path
from logging.handlers import RotatingFileHandler
import base64

# === LOGGING SETUP ===

def setup_logging(log_dir="./logs"):
    Path(log_dir).mkdir(exist_ok=True)
    
    # JSON logger for structured data
    json_handler = RotatingFileHandler(
        f"{log_dir}/honeypot_attacks.jsonl",
        maxBytes=10*1024*1024,
        backupCount=5
    )
    json_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # Standard logger
    file_handler = RotatingFileHandler(
        f"{log_dir}/honeypot.log",
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    
    return json_handler, file_handler, console_handler

# === ATTACK LOGGER ===

class AttackLogger:
    def __init__(self, json_handler):
        self.json_handler = json_handler
        self.logger = logging.getLogger('attacks')
        self.logger.addHandler(json_handler)
        self.logger.setLevel(logging.INFO)
    
    def log_attack(self, protocol, src_ip, src_port, payload, response, port):
        attack_data = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "protocol": protocol,
            "src_ip": src_ip,
            "src_port": src_port,
            "dst_port": port,
            "payload": payload[:200] if payload else "",  # Truncate for safety
            "payload_hash": hashlib.sha256(payload.encode() if isinstance(payload, str) else payload).hexdigest(),
            "response_sent": response,
            "threat_level": self._classify_threat(protocol, payload)
        }
        self.logger.info(json.dumps(attack_data))
        print(f"[{protocol.upper()}] Attack from {src_ip}:{src_port} logged")
        return attack_data
    
    def _classify_threat(self, protocol, payload):
        """Simple threat classification"""
        if not payload:
            return "low"
        
        dangerous_patterns = [
            b'cat /etc/passwd', b'rm -rf', b'chmod', b'bash',
            b'<?php', b'eval', b'exec', b'system'
        ]
        
        if isinstance(payload, str):
            payload = payload.encode()
        
        for pattern in dangerous_patterns:
            if pattern in payload:
                return "high"
        
        return "medium" if len(payload) > 100 else "low"

# === SSH HONEYPOT ===

class SSHHoneypot:
    def __init__(self, port, attack_logger):
        self.port = port
        self.attack_logger = attack_logger
        self.banner = b"SSH-2.0-OpenSSH_7.4\r\n"
    
    def handle_connection(self, client_socket, addr):
        try:
            # Send SSH banner
            client_socket.send(self.banner)
            
            # Receive client banner
            data = client_socket.recv(1024)
            payload = data.decode('utf-8', errors='ignore').strip()
            
            # Send fake key exchange
            response = "SSH-2.0-OpenSSH_7.4_HoneyPot\r\n"
            client_socket.send(response.encode())
            
            # Log attempt
            self.attack_logger.log_attack(
                "SSH", addr[0], addr[1], payload, response, self.port
            )
            
            # Keep connection open briefly for key exchange
            client_socket.settimeout(2)
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    self.attack_logger.log_attack(
                        "SSH", addr[0], addr[1], 
                        data.decode('utf-8', errors='ignore'),
                        "SSH Protocol Sequence", self.port
                    )
            except socket.timeout:
                pass
        
        except Exception as e:
            logging.error(f"SSH handler error: {e}")
        finally:
            client_socket.close()
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.port))
        server.listen(5)
        logger = logging.getLogger('ssh')
        logger.info(f"SSH Honeypot listening on port {self.port}")
        
        try:
            while True:
                client_socket, addr = server.accept()
                thread = threading.Thread(
                    target=self.handle_connection,
                    args=(client_socket, addr)
                )
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            logger.info("SSH Honeypot shutting down")
        finally:
            server.close()

# === HTTP HONEYPOT ===

class HTTPHoneypot:
    def __init__(self, port, attack_logger):
        self.port = port
        self.attack_logger = attack_logger
    
    def handle_connection(self, client_socket, addr):
        try:
            request_data = client_socket.recv(4096)
            payload = request_data.decode('utf-8', errors='ignore')
            
            # Parse request
            lines = payload.split('\r\n')
            request_line = lines[0] if lines else ""
            
            # Log the attack
            self.attack_logger.log_attack(
                "HTTP", addr[0], addr[1], request_line, "HTTP/1.1 404", self.port
            )
            
            # Send response
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                "Content-Length: 153\r\n"
                "Connection: close\r\n"
                "\r\n"
                "<html><body><h1>404 Not Found</h1>"
                "<p>The requested resource was not found on this server.</p>"
                "</body></html>"
            )
            client_socket.send(response.encode())
        
        except Exception as e:
            logging.error(f"HTTP handler error: {e}")
        finally:
            client_socket.close()
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.port))
        server.listen(5)
        logger = logging.getLogger('http')
        logger.info(f"HTTP Honeypot listening on port {self.port}")
        
        try:
            while True:
                client_socket, addr = server.accept()
                thread = threading.Thread(
                    target=self.handle_connection,
                    args=(client_socket, addr)
                )
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            logger.info("HTTP Honeypot shutting down")
        finally:
            server.close()

# === FTP HONEYPOT ===

class FTPHoneypot:
    def __init__(self, port, attack_logger):
        self.port = port
        self.attack_logger = attack_logger
    
    def handle_connection(self, client_socket, addr):
        try:
            # Send FTP banner
            banner = b"220 FTP Server Ready\r\n"
            client_socket.send(banner)
            
            self.attack_logger.log_attack(
                "FTP", addr[0], addr[1], "connection", "220 FTP Ready", self.port
            )
            
            client_socket.settimeout(5)
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                command = data.decode('utf-8', errors='ignore').strip()
                self.attack_logger.log_attack(
                    "FTP", addr[0], addr[1], command, "530 Not Logged In", self.port
                )
                
                response = b"530 Not Logged In\r\n"
                client_socket.send(response)
        
        except socket.timeout:
            pass
        except Exception as e:
            logging.error(f"FTP handler error: {e}")
        finally:
            client_socket.close()
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.port))
        server.listen(5)
        logger = logging.getLogger('ftp')
        logger.info(f"FTP Honeypot listening on port {self.port}")
        
        try:
            while True:
                client_socket, addr = server.accept()
                thread = threading.Thread(
                    target=self.handle_connection,
                    args=(client_socket, addr)
                )
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            logger.info("FTP Honeypot shutting down")
        finally:
            server.close()

# === MAIN ===

def main():
    # Setup logging
    json_handler, file_handler, console_handler = setup_logging()
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    root_logger.info("=" * 60)
    root_logger.info("Honeypot Server Starting")
    root_logger.info("=" * 60)
    
    # Create attack logger
    attack_logger = AttackLogger(json_handler)
    
    # Start honeypots
    honeypots = [
        ("SSH", SSHHoneypot(2222, attack_logger)),
        ("HTTP", HTTPHoneypot(8080, attack_logger)),
        ("FTP", FTPHoneypot(2121, attack_logger)),
    ]
    
    threads = []
    for name, honeypot in honeypots:
        thread = threading.Thread(target=honeypot.start, daemon=True)
        thread.start()
        threads.append(thread)
        root_logger.info(f"{name} honeypot started")
    
    root_logger.info("\nHoneypot system is active. Press Ctrl+C to stop.\n")
    
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        root_logger.info("\nShutting down honeypot system...")

if __name__ == "__main__":
    main()
