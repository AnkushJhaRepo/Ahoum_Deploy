from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from datetime import datetime
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load .env
load_dotenv()

# -------------------- CONFIGURE LOGGING --------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crm_notifications.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# -------------------- INIT APP --------------------
app = Flask(__name__)
CORS(app)

# -------------------- CONFIGURATION --------------------
app.config['CRM_NOTIFY_TOKEN'] = os.getenv('CRM_AUTH_TOKEN', 'your-static-bearer-token-here')
app.config['NOTIFICATION_LOG_FILE'] = os.getenv('NOTIFICATION_LOG_FILE', 'notifications.json')

# -------------------- VALIDATION FUNCTIONS --------------------
def validate_notification_payload(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    required_fields = ['booking_id', 'user', 'event', 'facilitator_id']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    if not isinstance(data['booking_id'], int) or data['booking_id'] <= 0:
        return False, "booking_id must be a positive integer"

    if not isinstance(data['user'], dict):
        return False, "user must be an object"
    for field in ['id', 'name', 'email']:
        if field not in data['user']:
            return False, f"Missing user.{field}"
    
    if not isinstance(data['user']['id'], int) or data['user']['id'] <= 0:
        return False, "user.id must be a positive integer"
    if not isinstance(data['user']['name'], str) or not data['user']['name'].strip():
        return False, "user.name must be a non-empty string"
    if not isinstance(data['user']['email'], str) or not data['user']['email'].strip():
        return False, "user.email must be a non-empty string"

    if not isinstance(data['event'], dict):
        return False, "event must be an object"
    for field in ['id', 'title', 'start_date']:
        if field not in data['event']:
            return False, f"Missing event.{field}"

    if not isinstance(data['event']['id'], int) or data['event']['id'] <= 0:
        return False, "event.id must be a positive integer"
    if not isinstance(data['event']['title'], str) or not data['event']['title'].strip():
        return False, "event.title must be a non-empty string"
    if not isinstance(data['event']['start_date'], str) or not data['event']['start_date'].strip():
        return False, "event.start_date must be a non-empty string"

    if not isinstance(data['facilitator_id'], int) or data['facilitator_id'] <= 0:
        return False, "facilitator_id must be a positive integer"

    return True, None

def validate_bearer_token(auth_header: str) -> bool:
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
    token = auth_header.replace("Bearer ", "").strip()
    return token == app.config['CRM_NOTIFY_TOKEN']

# -------------------- LOGGING & STORAGE --------------------
def log_notification(data: Dict[str, Any]) -> None:
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'booking_id': data['booking_id'],
        'user': data['user'],
        'event': data['event'],
        'facilitator_id': data['facilitator_id']
    }
    logger.info(f"Notification received: {json.dumps(log_entry, indent=2)}")

def store_notification(data: Dict[str, Any]) -> None:
    log_path = app.config['NOTIFICATION_LOG_FILE']
    notification_record = {
        'timestamp': datetime.utcnow().isoformat(),
        'data': data
    }

    notifications = []
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r') as f:
                notifications = json.load(f)
        except Exception:
            notifications = []

    notifications.append(notification_record)

    with open(log_path, 'w') as f:
        json.dump(notifications, f, indent=2)

    logger.info(f"Stored booking_id {data['booking_id']}")

# -------------------- ROUTES --------------------
@app.route('/notify', methods=['POST'])
def notify():
    auth_header = request.headers.get('Authorization')
    if not validate_bearer_token(auth_header or ''):
        return jsonify({'error': 'Unauthorized'}), 401

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Empty JSON payload'}), 400

    is_valid, error = validate_notification_payload(data)
    if not is_valid:
        return jsonify({'error': error}), 400

    try:
        log_notification(data)
        store_notification(data)
        return jsonify({
            'message': 'Notification processed successfully',
            'booking_id': data['booking_id'],
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'crm-notification-service'
    }), 200

@app.route('/notifications', methods=['GET'])
def get_notifications():
    log_path = app.config['NOTIFICATION_LOG_FILE']
    if not os.path.exists(log_path):
        return jsonify({'notifications': []}), 200
    try:
        with open(log_path, 'r') as f:
            notifications = json.load(f)
        return jsonify({'notifications': notifications, 'count': len(notifications)}), 200
    except Exception as e:
        logger.error(f"Error loading notifications: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Serve the notifications dashboard HTML page"""
    try:
        with open('notifications.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Dashboard file not found", 404
    except Exception as e:
        logger.error(f"Error serving dashboard: {str(e)}")
        return "Internal server error", 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# -------------------- MAIN ENTRY --------------------
if __name__ == '__main__':
    logger.info("✅ CRM Notification Service starting...")
    logger.info(f"Token loaded: {'✅' if app.config['CRM_NOTIFY_TOKEN'] != 'your-static-bearer-token-here' else '❌ Default token used'}")
    logger.info(f"Log file path: {app.config['NOTIFICATION_LOG_FILE']}")

    port = int(os.getenv('CRM_PORT', 5001))
    debug = os.getenv('CRM_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
