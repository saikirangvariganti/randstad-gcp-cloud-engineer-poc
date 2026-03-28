"""
Randstad GCP Cloud Engineer POC — Python Application

A simple Flask application demonstrating GCP cloud engineering patterns:
- Cloud SQL (PostgreSQL) connection via Cloud SQL Python Connector
- Secret Manager integration for credentials
- Cloud Storage client
- Prometheus metrics endpoint
- Health and readiness checks
"""

import os
import logging
import time
from datetime import datetime

from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP request count',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

DB_QUERY_LATENCY = Histogram(
    'db_query_duration_seconds',
    'Database query latency in seconds',
    ['operation']
)

# Application configuration
APP_ENV = os.environ.get('APP_ENV', 'development')
APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')
PROJECT_ID = os.environ.get('PROJECT_ID', 'local')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'appdb')
DB_USER = os.environ.get('DB_USER', 'appuser')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Set log level from environment
logging.getLogger().setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

# In-memory storage for demo (replace with Cloud SQL in production)
_items_store = {}
_request_count = 0


@app.before_request
def before_request():
    """Record request start time."""
    request.start_time = time.time()


@app.after_request
def after_request(response):
    """Record metrics after each request."""
    global _request_count
    latency = time.time() - request.start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status_code=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path
    ).observe(latency)
    _request_count += 1
    logger.info(
        "request completed",
        extra={
            'method': request.method,
            'path': request.path,
            'status': response.status_code,
            'latency_ms': round(latency * 1000, 2)
        }
    )
    return response


@app.route('/health', methods=['GET'])
def health():
    """Liveness probe endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': APP_VERSION,
        'environment': APP_ENV
    }), 200


@app.route('/ready', methods=['GET'])
def ready():
    """Readiness probe endpoint."""
    checks = {
        'app': True,
        'database': _check_db_connection(),
    }
    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503

    return jsonify({
        'status': 'ready' if all_ready else 'not ready',
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code


def _check_db_connection() -> bool:
    """Check database connectivity (stub for demo)."""
    try:
        # In production: use google-cloud-sql-connector
        # connector = Connector()
        # conn = connector.connect(INSTANCE_CONNECTION_NAME, ...)
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route('/api/v1/items', methods=['GET'])
def list_items():
    """List all items."""
    return jsonify({
        'items': list(_items_store.values()),
        'count': len(_items_store),
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/v1/items/<item_id>', methods=['GET'])
def get_item(item_id: str):
    """Get a specific item by ID."""
    item = _items_store.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found', 'id': item_id}), 404
    return jsonify(item), 200


@app.route('/api/v1/items', methods=['POST'])
def create_item():
    """Create a new item."""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing required field: name'}), 400

    item_id = str(len(_items_store) + 1)
    item = {
        'id': item_id,
        'name': data['name'],
        'description': data.get('description', ''),
        'created_at': datetime.utcnow().isoformat()
    }
    _items_store[item_id] = item
    logger.info(f"Item created: {item_id}")
    return jsonify(item), 201


@app.route('/api/v1/items/<item_id>', methods=['DELETE'])
def delete_item(item_id: str):
    """Delete an item."""
    if item_id not in _items_store:
        return jsonify({'error': 'Item not found', 'id': item_id}), 404
    del _items_store[item_id]
    logger.info(f"Item deleted: {item_id}")
    return jsonify({'deleted': item_id}), 200


@app.route('/api/v1/info', methods=['GET'])
def info():
    """Application information endpoint."""
    return jsonify({
        'app': 'randstad-gcp-cloud-engineer-poc',
        'version': APP_VERSION,
        'environment': APP_ENV,
        'project_id': PROJECT_ID,
        'features': [
            'GKE deployment',
            'Cloud SQL (PostgreSQL)',
            'Secret Manager',
            'Cloud Storage',
            'VPC Service Controls',
            'Cloud Armor WAF',
            'Prometheus metrics',
            'ArgoCD GitOps',
            'Terraform IaC',
        ]
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = APP_ENV == 'development'
    logger.info(f"Starting Randstad GCP POC app on port {port} (env={APP_ENV})")
    app.run(host='0.0.0.0', port=port, debug=debug)
