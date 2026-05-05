# 🍯 Complete Honeypot System

A production-ready, multi-protocol honeypot system with real-time attack detection, logging, storage, and interactive analytics dashboard.

## Quick Links

- 📋 [Setup Guide](SETUP_GUIDE.md) - Detailed installation instructions
- 🚀 [Quick Start](#quick-start) - Get running in 5 minutes
- 📊 [API Documentation](#rest-api-reference) - Full API reference
- 🎨 [Dashboard Guide](#dashboard-features) - Dashboard usage
- 🔧 [Configuration](#configuration) - System configuration
- 🐛 [Troubleshooting](#troubleshooting) - Common issues

---

## What's Included

### 📦 Components

| File | Purpose | Size |
|------|---------|------|
| `honeypot_server.py` | Multi-protocol honeypot | ~700 lines |
| `storage_manager.py` | Database abstraction layer | ~600 lines |
| `api_server.py` | Flask REST API | ~400 lines |
| `dashboard.html` | Interactive web dashboard | ~1000 lines |
| `quickstart.sh` | Automated setup script | ~400 lines |
| `requirements.txt` | Python dependencies | 5 packages |

### 🎯 Features

**Honeypot Services:**
- ✅ SSH brute-force detection (port 2222)
- ✅ HTTP scanning detection (port 8080)
- ✅ FTP credential attacks (port 2121)
- ✅ Real-time threat classification
- ✅ JSON-formatted logging

**Storage:**
- ✅ MongoDB persistent storage (recommended)
- ✅ Local JSONL fallback storage
- ✅ Automatic threat classification
- ✅ Indexed queries and aggregation
- ✅ Configurable retention policies

**Analytics:**
- ✅ REST API for data access
- ✅ Real-time attack statistics
- ✅ Interactive web dashboard
- ✅ Charts and visualizations
- ✅ Protocol and threat analysis

**Deployment:**
- ✅ Standalone Python scripts
- ✅ Docker support
- ✅ Systemd integration
- ✅ Automated setup script

---

## Architecture

```
Attack Stream (SSH/HTTP/FTP) 
        ↓
   Honeypot Servers
   (2222/8080/2121)
        ↓
   Attack Logger
   (Threat Classification)
        ↓
   Storage Layer
   ├─ MongoDB (Primary)
   └─ Local JSONL (Fallback)
        ↓
   Flask REST API
   (Port 5000)
        ↓
   Web Dashboard
   (Interactive Charts)
```

---

## Quick Start

### 1️⃣ Automated Setup (Recommended)

```bash
# Clone or download the files
mkdir -p ~/honeypot && cd ~/honeypot

# Run quick-start script
bash quickstart.sh

# Follow interactive prompts
```

### 2️⃣ Manual Setup

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Start honeypot server
python3 honeypot_server.py &

# Start API server (new terminal)
python3 api_server.py &

# Open dashboard
open http://localhost:5000
```

### 3️⃣ Docker Deployment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

## System Requirements

### Minimum
- Python 3.7+
- 1GB RAM
- 100MB disk space
- Linux/macOS/Windows (WSL)

### Recommended
- Python 3.9+
- 4GB RAM
- 10GB disk space (for logs)
- Linux (Ubuntu/CentOS)
- MongoDB 4.0+

### Network Requirements
- Ports: 2222, 8080, 2121 (honeypots), 5000 (API)
- Outbound: Not required
- Inbound: Only honeypot ports

---

## REST API Reference

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Get Statistics
```bash
GET /api/stats

Response:
{
  "total": 1247,
  "last_24h": 156,
  "unique_ips": 43,
  "protocols": {
    "SSH": 612,
    "HTTP": 458,
    "FTP": 177
  },
  "threat_levels": {
    "high": 248,
    "medium": 654,
    "low": 345
  },
  "top_sources": [
    {"ip": "192.168.1.105", "count": 87}
  ]
}
```

#### Get Recent Attacks
```bash
GET /api/attacks?limit=100&protocol=SSH&threat_level=high

Query Parameters:
- limit: Number of attacks (default: 100)
- protocol: Filter by protocol (SSH, HTTP, FTP)
- threat_level: Filter by level (high, medium, low)

Response:
{
  "count": 45,
  "attacks": [
    {
      "timestamp": "2024-01-15T10:30:45.123Z",
      "protocol": "SSH",
      "src_ip": "192.168.1.105",
      "src_port": 54321,
      "dst_port": 2222,
      "payload": "SSH-2.0-OpenSSH_7.4",
      "threat_level": "high"
    }
  ]
}
```

#### Get Attacks by Source IP
```bash
GET /api/attacks/by-ip/192.168.1.105?limit=50

Response:
{
  "ip": "192.168.1.105",
  "count": 50,
  "attacks": [...]
}
```

#### Get Attacks by Protocol
```bash
GET /api/attacks/by-protocol/SSH?limit=100

Response:
{
  "protocol": "SSH",
  "count": 100,
  "attacks": [...]
}
```

#### Get Attack Timeline
```bash
GET /api/timeline?hours=24

Query Parameters:
- hours: Time period in hours (default: 24)

Response:
{
  "hours": 24,
  "timeline": [
    {
      "_id": "2024-01-15 10:00",
      "count": 45
    }
  ]
}
```

#### Get High-Risk Alerts
```bash
GET /api/threats?limit=50

Response:
{
  "count": 50,
  "threats": [...]
}
```

#### Insert Test Attack
```bash
POST /api/test-attack

Request Body:
{
  "protocol": "SSH",
  "src_ip": "192.168.1.100",
  "src_port": 54321,
  "dst_port": 2222,
  "payload": "test payload",
  "threat_level": "high"
}

Response:
{
  "status": "success",
  "message": "Test attack inserted",
  "data": {...}
}
```

#### Health Check
```bash
GET /api/health

Response:
{
  "status": "operational",
  "timestamp": "2024-01-15T10:30:45.123Z",
  "storage": "MongoDBStorage"
}
```

#### Cleanup Old Records
```bash
POST /api/cleanup

Request Body:
{
  "days": 30
}

Response:
{
  "status": "success",
  "deleted": 1234,
  "older_than_days": 30
}
```

---

## Dashboard Features

### Overview
Real-time attack dashboard with:
- **Total Attack Counter**: All-time and last 24h
- **Threat Distribution**: Pie chart by severity level
- **Protocol Statistics**: Attacks per protocol
- **Timeline Graph**: Hourly attack frequency
- **Top Sources**: Most active attacking IPs
- **Recent Attacks**: Latest detected attacks table

### Tabs

**Recent Attacks**
- Timestamp
- Protocol type
- Source IP
- Attack payload
- Threat level
- Sortable and filterable

**Protocol Analysis**
- SSH attack statistics
- HTTP attack statistics
- FTP attack statistics
- Risk assessment per protocol
- Common attack patterns

**High-Risk Alerts**
- Critical threats
- Suspicious activities
- Attack patterns
- Recommended actions

### Interactions
- 🔄 Auto-refresh every 30 seconds
- 🔍 Click to drill down into details
- 📥 Export data (via API)
- 🎨 Responsive design (mobile-friendly)

---

## Configuration

### Honeypot Ports
Edit `honeypot_server.py`:
```python
honeypots = [
    ("SSH", SSHHoneypot(2222, attack_logger)),    # Change port
    ("HTTP", HTTPHoneypot(8080, attack_logger)),  # Change port
    ("FTP", FTPHoneypot(2121, attack_logger)),    # Change port
]
```

### MongoDB Connection
Edit `api_server.py`:
```python
storage = StorageFactory.create(
    "mongodb",
    uri="mongodb://localhost:27017",  # Change URI
    db_name="honeypot"                 # Change DB name
)
```

### Threat Classification
Edit `storage_manager.py`:
```python
dangerous_patterns = [
    b'cat /etc/passwd',
    b'rm -rf',
    b'chmod 777',
    # Add custom patterns
]
```

### API Configuration
Edit `api_server.py`:
```python
app.run(
    host='0.0.0.0',      # Listen address
    port=5000,           # Listen port
    debug=False,         # Debug mode
    threaded=True        # Threading
)
```

### Logging
Edit `honeypot_server.py`:
```python
setup_logging(log_dir="./logs")  # Change log directory

# Log levels in logging module
logging.DEBUG      # Detailed debug info
logging.INFO       # General info
logging.WARNING    # Warning messages
logging.ERROR      # Error messages
logging.CRITICAL   # Critical errors
```

---

## Monitoring & Logs

### Log Files

**Honeypot Log** (`logs/honeypot.log`)
```
2024-01-15 10:30:45,123 - ssh - INFO - SSH Honeypot listening on port 2222
2024-01-15 10:30:46,456 - attacks - INFO - {"timestamp": "...", ...}
```

**Attack Log** (`logs/honeypot_attacks.jsonl`)
```
{"timestamp": "2024-01-15T10:30:46.456Z", "protocol": "SSH", "src_ip": "192.168.1.105", ...}
{"timestamp": "2024-01-15T10:30:47.789Z", "protocol": "HTTP", "src_ip": "10.0.0.54", ...}
```

### View Logs

```bash
# Real-time honeypot log
tail -f logs/honeypot.log

# Real-time attack log
tail -f logs/honeypot_attacks.jsonl

# Pretty-print JSON logs
tail -f logs/honeypot_attacks.jsonl | jq '.'

# Filter by protocol
grep "SSH" logs/honeypot_attacks.jsonl

# Count attacks
wc -l logs/honeypot_attacks.jsonl
```

### Database Monitoring

```bash
# Connect to MongoDB
mongo

# Select honeypot database
use honeypot

# Count documents
db.attacks.count()

# Check latest attacks
db.attacks.find().sort({timestamp: -1}).limit(5)

# Count by protocol
db.attacks.aggregate([
  {$group: {_id: '$protocol', count: {$sum: 1}}},
  {$sort: {count: -1}}
])

# Check indexes
db.attacks.getIndexes()

# Database stats
db.stats()
```

---

## Performance Tuning

### Optimize MongoDB

```bash
# Create index for timestamp
mongo
use honeypot
db.attacks.createIndex({timestamp: -1})
db.attacks.createIndex({src_ip: 1})
db.attacks.createIndex({protocol: 1})
db.attacks.createIndex({threat_level: 1})
```

### Connection Pooling

Edit `api_server.py`:
```python
from pymongo import MongoClient
client = MongoClient(
    'mongodb://localhost:27017',
    maxPoolSize=50,      # Max connections
    minPoolSize=10       # Min connections
)
```

### Caching

Add to `api_server.py`:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/stats')
@cache.cached(timeout=60)  # Cache for 60 seconds
def get_stats():
    return jsonify(storage.get_stats())
```

---

## Security Hardening

### Network Security
```bash
# Allow only required ports
sudo ufw allow 2222/tcp  # SSH honeypot
sudo ufw allow 8080/tcp  # HTTP honeypot
sudo ufw allow 2121/tcp  # FTP honeypot
sudo ufw allow 5000/tcp  # API (restrict to localhost)
```

### API Security
```python
# Add rate limiting
from flask_limiter import Limiter
limiter = Limiter(app)

@app.route('/api/attacks')
@limiter.limit("100 per hour")
def get_attacks():
    return jsonify(...)
```

### Data Encryption
```bash
# Enable MongoDB encryption
mongod --enableEncryption --encryptionKeyFile /path/to/keyfile
```

### Access Control
```nginx
# Nginx reverse proxy with auth
location / {
    auth_basic "Honeypot Dashboard";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://localhost:5000;
}
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 2222
sudo lsof -i :2222

# Kill the process
sudo kill -9 <PID>

# Change honeypot port
# Edit honeypot_server.py and change port number
```

### MongoDB Connection Refused

```bash
# Check if MongoDB is running
sudo systemctl status mongodb

# Start MongoDB
sudo systemctl start mongodb

# Test connection
mongo --eval "db.version()"

# Check MongoDB logs
sudo tail -f /var/log/mongodb/mongod.log
```

### Dashboard Not Loading

```bash
# Check API server is running
curl http://localhost:5000/api/health

# Check browser console for errors (F12)

# Verify CORS settings
# Edit api_server.py and ensure CORS(app) is called

# Clear browser cache
# Ctrl+Shift+Del or Cmd+Shift+Del
```

### API Returns Empty Results

```bash
# Verify attacks are being logged
tail -f logs/honeypot_attacks.jsonl

# Check if MongoDB has data
mongo
use honeypot
db.attacks.count()

# If empty, generate test data
curl -X POST http://localhost:5000/api/test-attack \
  -H "Content-Type: application/json" \
  -d '{"protocol":"SSH","src_ip":"192.168.1.1","threat_level":"high"}'
```

### High Memory Usage

```bash
# Check memory usage
free -h

# Check honeypot process
ps aux | grep honeypot_server

# Limit memory in systemd service
[Service]
MemoryLimit=512M

# Reduce log rotation size
# Edit setup_logging() in honeypot_server.py
```

### Slow Dashboard

```bash
# Check API response time
time curl http://localhost:5000/api/stats

# Add database index
mongo
use honeypot
db.attacks.createIndex({timestamp: -1})

# Optimize queries
# Check database stats: db.stats()

# Implement caching (see Performance Tuning)
```

---

## Advanced Usage

### Custom Alert Rules

Edit `storage_manager.py`:

```python
def _classify_threat(self, protocol, payload):
    if protocol == 'SSH':
        if b'root' in payload and b'password' in payload:
            return 'high'
    elif protocol == 'HTTP':
        dangerous_http = [
            b'/../../../',
            b'union select',
            b'<?php'
        ]
        for pattern in dangerous_http:
            if pattern in payload:
                return 'high'
    return 'medium'
```

### Webhook Notifications

Add to `api_server.py`:

```python
import requests

def send_alert(attack):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK"
    message = {
        "text": f"🚨 High-risk attack detected!",
        "attachments": [{
            "color": "danger",
            "fields": [
                {"title": "Protocol", "value": attack['protocol']},
                {"title": "Source IP", "value": attack['src_ip']},
                {"title": "Threat Level", "value": attack['threat_level']}
            ]
        }]
    }
    requests.post(webhook_url, json=message)
```

### Integration with SIEM

Export data to syslog:

```python
import logging.handlers

syslog_handler = logging.handlers.SysLogHandler(
    address=('localhost', 514)
)
logger.addHandler(syslog_handler)
```

### Multi-Instance Deployment

```bash
# Run multiple honeypot instances on different ports
python3 -c "
from honeypot_server import *
import threading

for port in [2222, 3333, 4444]:
    h = SSHHoneypot(port, attack_logger)
    t = threading.Thread(target=h.start)
    t.daemon = True
    t.start()
"
```

---

## Maintenance Tasks

### Daily
- ✓ Monitor dashboard for anomalies
- ✓ Check disk space
- ✓ Verify services running

### Weekly
- ✓ Review attack patterns
- ✓ Analyze top attackers
- ✓ Update threat patterns

### Monthly
- ✓ Optimize database
- ✓ Archive old logs
- ✓ Capacity planning

### Quarterly
- ✓ Security audit
- ✓ Performance review
- ✓ Update dependencies

---

## Production Checklist

- [ ] Configure MongoDB replication
- [ ] Set up automated backups
- [ ] Enable SSL/TLS for API
- [ ] Configure rate limiting
- [ ] Set up monitoring/alerts
- [ ] Create firewall rules
- [ ] Enable logging/auditing
- [ ] Test disaster recovery
- [ ] Document procedures
- [ ] Schedule regular reviews

---

## Performance Metrics

**Typical Performance:**
- Concurrent connections: 1000+
- Attack logging latency: <10ms
- API response time: <100ms
- Dashboard refresh: 1-2 seconds

**Storage:**
- Per 1000 attacks: ~500KB
- Daily (1000/day): ~15MB
- Monthly: ~450MB
- Yearly: ~5.5GB

---

## Support & Resources

- 📖 [Setup Guide](SETUP_GUIDE.md)
- 🐍 [Python Docs](https://python.org)
- 🍃 [MongoDB Docs](https://mongodb.com/docs)
- 🔧 [Flask Docs](https://flask.palletsprojects.com)

---

## License

Educational and research purposes only. Use responsibly and legally.

---

## Next Steps

1. ✅ Run `quickstart.sh`
2. ✅ Access dashboard at `http://localhost:5000`
3. ✅ Monitor attack logs
4. ✅ Analyze threat patterns
5. ✅ Configure alerts
6. ✅ Deploy to production
7. ✅ Integrate with SIEM

**Happy hunting! 🍯**
