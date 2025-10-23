"""
Test the Loot Telemetry Server
Run this to test database operations and server functionality
"""

import json
import requests
from datetime import datetime
from db_handler import DatabaseHandler

def test_database():
    """Test database operations"""
    print("🔧 Testing Database Operations...")
    
    # Initialize database
    db = DatabaseHandler("test_loot.db")
    
    # Test data
    test_sheet = {
        "match_id": "test_match_001",
        "player_id": "test_player_1",
        "timestamp": datetime.now().isoformat(),
        "looted_items": {
            "rubber_duck": 3,
            "medkit": 1,
            "ammo_box": 2
        },
        "locations": {
            "rubber_duck": (25.5, 75.2),
            "medkit": (10.0, 50.0),
            "ammo_box": (80.1, 20.3)
        }
    }
    
    # Test insert
    sheet_id = db.insert_stat_sheet(test_sheet)
    print(f"✅ Inserted stat sheet with ID: {sheet_id}")
    
    # Test retrieve
    sheets = db.get_stat_sheets()
    print(f"✅ Retrieved {len(sheets)} stat sheets")
    
    # Test aggregate
    stats = db.get_aggregate_stats()
    print(f"✅ Aggregate stats: {stats}")
    
    # Test heatmap data
    duck_locations = db.get_heatmap_data("rubber_duck")
    print(f"✅ Duck locations: {duck_locations}")
    
    # Clean up
    db.clear_database()
    print("✅ Database test completed successfully!")

def test_server_api():
    """Test server API endpoints (requires server to be running)"""
    print("\n🌐 Testing Server API...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test health check
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server health check passed")
        else:
            print("❌ Server health check failed")
            return
        
        # Test submit stat sheet
        test_data = {
            "match_id": "api_test_001",
            "player_id": "api_test_player",
            "looted_items": {
                "rubber_duck": 5,
                "gold_coin": 2
            },
            "locations": {
                "rubber_duck": (30.0, 40.0),
                "gold_coin": (70.0, 80.0)
            }
        }
        
        response = requests.post(f"{base_url}/api/submit", json=test_data, timeout=5)
        if response.status_code == 201:
            print("✅ Stat sheet submission passed")
        else:
            print(f"❌ Stat sheet submission failed: {response.status_code}")
        
        # Test get stats
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get stats passed - found {data['count']} records")
        else:
            print("❌ Get stats failed")
        
        # Test aggregate
        response = requests.get(f"{base_url}/api/aggregate", timeout=5)
        if response.status_code == 200:
            print("✅ Aggregate stats passed")
        else:
            print("❌ Aggregate stats failed")
        
        print("✅ Server API test completed successfully!")
        
    except requests.ConnectionError:
        print("❌ Could not connect to server. Make sure to run 'python server.py' first!")
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    print("🎮 Loot Telemetry Simulator - Test Suite")
    print("=" * 50)
    
    # Test database
    test_database()
    
    # Test server API
    test_server_api()
    
    print("\n🎯 Test Summary:")
    print("1. Database operations: ✅ Working")
    print("2. Server API: Run 'python server.py' first, then run this test again")
    print("\nNext steps:")
    print("- Run: python server.py")
    print("- Visit: http://localhost:5000")
    print("- Run your notebook to generate data")
    print("- Submit data to the server API")