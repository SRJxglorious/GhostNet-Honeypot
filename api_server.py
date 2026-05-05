#!/usr/bin/env python3
"""
Flask API Server for Honeypot Dashboard
Provides REST endpoints for the dashboard to fetch attack data
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys

# Import storage module
try:
    from storage_manager import StorageFactory
except ImportError:
    print("Error: storage_manager.py not found in same directory")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('api')

# Initialize storage
storage = StorageFactory.create("mongodb")
logger.info(f"Storage backend: {type(storage).__name__}")

# === ROUTES ===

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get comprehensive attack statistics"""
    try:
        stats = storage.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/attacks', methods=['GET'])
def get_attacks():
    """Get recent attacks with optional filters"""
    try:
        limit = request.args.get('limit', default=100, type=int)
        protocol = request.args.get('protocol', default=None)
        threat_level = request.args.get('threat_level', default=None)
        
        filters = {}
        if protocol:
            filters['protocol'] = protocol
        if threat_level:
            filters['threat_level'] = threat_level
        
        attacks = storage.get_attacks(filters=filters if filters else None, limit=limit)
        
        # Remove MongoDB _id field for JSON serialization
        for attack in attacks:
            if '_id' in attack:
                attack['_id'] = str(attack['_id'])
        
        return jsonify({
            "count": len(attacks),
            "attacks": attacks
        }), 200
    except Exception as e:
        logger.error(f"Error getting attacks: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/attacks/by-ip/<ip>', methods=['GET'])
def get_attacks_by_ip(ip):
    """Get all attacks from a specific IP"""
    try:
        limit = request.args.get('limit', default=100, type=int)
        attacks = storage.get_attacks_by_ip(ip, limit=limit)
        
        for attack in attacks:
            if '_id' in attack:
                attack['_id'] = str(attack['_id'])
        
        return jsonify({
            "ip": ip,
            "count": len(attacks),
            "attacks": attacks
        }), 200
    except Exception as e:
        logger.error(f"Error getting attacks by IP: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/attacks/by-protocol/<protocol>', methods=['GET'])
def get_attacks_by_protocol(protocol):
    """Get all attacks for a specific protocol"""
    try:
        limit = request.args.get('limit', default=100, type=int)
        attacks = storage.get_attacks_by_protocol(protocol.upper(), limit=limit)
        
        for attack in attacks:
            if '_id' in attack:
                attack['_id'] = str(attack['_id'])
        
        return jsonify({
            "protocol": protocol,
            "count": len(attacks),
            "attacks": attacks
        }), 200
    except Exception as e:
        logger.error(f"Error getting attacks by protocol: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/timeline', methods=['GET'])
def get_timeline():
    """Get attack timeline for the last N hours"""
    try:
        hours = request.args.get('hours', default=24, type=int)
        timeline = storage.get_timeline(hours=hours)
        
        return jsonify({
            "hours": hours,
            "timeline": timeline
        }), 200
    except Exception as e:
        logger.error(f"Error getting timeline: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/threats', methods=['GET'])
def get_threats():
    """Get high and medium threat attacks"""
    try:
        limit = request.args.get('limit', default=50, type=int)
        threats = storage.get_attacks(
            filters={'threat_level': {'$in': ['high', 'medium']}},
            limit=limit
        )
        
        for threat in threats:
            if '_id' in threat:
                threat['_id'] = str(threat['_id'])
        
        return jsonify({
            "count": len(threats),
            "threats": threats
        }), 200
    except Exception as e:
        logger.error(f"Error getting threats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "storage": type(storage).__name__
    }), 200

@app.route('/api/test-attack', methods=['POST'])
def test_attack():
    """Insert a test attack (for testing purposes)"""
    try:
        attack_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "protocol": request.json.get('protocol', 'TEST'),
            "src_ip": request.json.get('src_ip', '127.0.0.1'),
            "src_port": request.json.get('src_port', 12345),
            "dst_port": request.json.get('dst_port', 8080),
            "payload": request.json.get('payload', 'test'),
            "threat_level": request.json.get('threat_level', 'low')
        }
        
        if storage.insert_attack(attack_data):
            logger.info(f"Test attack inserted: {attack_data['protocol']}")
            return jsonify({
                "status": "success",
                "message": "Test attack inserted",
                "data": attack_data
            }), 201
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to insert test attack"
            }), 500
    except Exception as e:
        logger.error(f"Error inserting test attack: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup_old_records():
    """Delete records older than N days"""
    try:
        days = request.json.get('days', 30) if request.json else 30
        count = storage.delete_old_records(days=days)
        
        return jsonify({
            "status": "success",
            "deleted": count,
            "older_than_days": days
        }), 200
    except Exception as e:
        logger.error(f"Error cleaning up records: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API documentation"""
    return jsonify({
        "name": "Honeypot API",
        "version": "1.0",
        "endpoints": {
            "GET /api/stats": "Get comprehensive statistics",
            "GET /api/attacks": "Get recent attacks (limit, protocol, threat_level params)",
            "GET /api/attacks/by-ip/<ip>": "Get attacks from specific IP",
            "GET /api/attacks/by-protocol/<protocol>": "Get attacks for protocol",
            "GET /api/timeline": "Get attack timeline (hours param)",
            "GET /api/threats": "Get high/medium threat attacks",
            "GET /api/health": "Health check",
            "POST /api/test-attack": "Insert test attack",
            "POST /api/cleanup": "Delete old records (days param)"
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

# === MAIN ===

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("Honeypot API Server Starting")
    logger.info("=" * 60)
    logger.info(f"Storage: {type(storage).__name__}")
    logger.info("Listening on http://0.0.0.0:5000")
    logger.info("Dashboard: http://localhost:5000/dashboard.html")
    logger.info("API Docs: http://localhost:5000/api")
    logger.info("=" * 60)
    
    # Run Flask server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
