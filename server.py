"""
Flask Server for Loot Telemetry Simulator
REST API for receiving and serving loot data
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime
from db_handler import DatabaseHandler

app = Flask(__name__)
CORS(app)  # Enable CORS for web client access

# Initialize database
db = DatabaseHandler()

@app.route('/')
def home():
    """Simple home page with API documentation"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Game Loot Telemetry Simulator API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f4f4f4; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #007bff; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🎮 Loot Telemetry Simulator API</h1>
        <p>Welcome to the Loot Telemetry Simulator server!</p>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <span class="method">POST</span> <strong>/api/submit</strong><br>
            Submit a stat sheet from a game client<br>
            <em>Body: JSON stat sheet data</em>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <strong>/api/stats</strong><br>
            Get all stat sheets (with optional filtering)<br>
            <em>Query params: match_id, player_id, limit</em>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <strong>/api/aggregate</strong><br>
            Get aggregated statistics across all matches
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <strong>/api/heatmap/{item_name}</strong><br>
            Get location data for heatmap visualization
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <strong>/api/health</strong><br>
            Server health check
        </div>
        
        <p><a href="/api/aggregate">View Current Stats</a> | <a href="/api/stats">View All Data</a></p>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Loot Telemetry Server is running'
    })

@app.route('/api/submit', methods=['POST'])
def submit_stat_sheet():
    """Receive and store a stat sheet from game client"""
    try:
        # Get JSON data from request
        stat_sheet = request.get_json()
        
        if not stat_sheet:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['match_id', 'player_id', 'looted_items']
        for field in required_fields:
            if field not in stat_sheet:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Add timestamp if not provided
        if 'timestamp' not in stat_sheet:
            stat_sheet['timestamp'] = datetime.now().isoformat()
        
        # Insert into database
        sheet_id = db.insert_stat_sheet(stat_sheet)
        
        if sheet_id:
            return jsonify({
                'success': True,
                'message': 'Stat sheet received successfully',
                'id': sheet_id,
                'timestamp': datetime.now().isoformat()
            }), 201
        else:
            return jsonify({'error': 'Failed to store stat sheet'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/stats')
def get_stats():
    """Retrieve stat sheets with optional filtering"""
    try:
        # Get query parameters
        match_id = request.args.get('match_id')
        player_id = request.args.get('player_id')
        limit = request.args.get('limit', type=int)
        
        # Retrieve from database
        stat_sheets = db.get_stat_sheets(match_id=match_id, player_id=player_id, limit=limit)
        
        return jsonify({
            'success': True,
            'count': len(stat_sheets),
            'data': stat_sheets
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/aggregate')
def get_aggregate_stats():
    """Get aggregated statistics across all matches"""
    try:
        stats = db.get_aggregate_stats()
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/heatmap/<item_name>')
def get_heatmap_data(item_name):
    """Get location data for heatmap visualization"""
    try:
        locations = db.get_heatmap_data(item_name)
        
        # Convert to format suitable for frontend
        heatmap_data = {
            'item_name': item_name,
            'locations': locations,
            'count': len(locations)
        }
        
        return jsonify({
            'success': True,
            'data': heatmap_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/clear', methods=['POST'])
def clear_database():
    """Clear all data (useful for testing)"""
    try:
        db.clear_database()
        return jsonify({
            'success': True,
            'message': 'Database cleared successfully'
        })
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🎮 Starting Loot Telemetry Simulator Server...")
    print("📊 Database initialized")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API documentation at: http://localhost:5000")
    
    # Run the server
    app.run(
        host='0.0.0.0',  # Accept connections from any IP
        port=5000,
        debug=True  # Enable debug mode for development
    )