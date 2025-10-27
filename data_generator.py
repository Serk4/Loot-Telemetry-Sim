#!/usr/bin/env python3
"""
Loot Telemetry Data Generator

This script simulates multiple game clients sending stat sheet data to the server.
It generates realistic game session data and uploads it via the REST API.
"""

import json
import random
import time
import requests
from datetime import datetime, timedelta
import argparse


class LootTelemetryDataGenerator:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.session = requests.Session()
        
        # Game configuration
        self.items = ['rubber_duck', 'medkit', 'ammo_box', 'grenade', 'gold_coin']
        self.map_size = (100, 100)  # X, Y coordinates range
        
    def generate_stat_sheet(self, match_id, player_id):
        """Generate a realistic stat sheet for a player in a match."""
        # Random item counts (0-5 each)
        looted_items = {item: random.randint(0, 5) for item in self.items}
        
        # Generate locations for items that were looted
        locations = {}
        for item, count in looted_items.items():
            if count > 0:
                x = random.uniform(0, self.map_size[0])
                y = random.uniform(0, self.map_size[1])
                locations[item] = (x, y)
        
        return {
            "match_id": match_id,
            "player_id": player_id,
            "timestamp": datetime.now().isoformat(),
            "looted_items": looted_items,
            "locations": locations,
            "match_duration": random.randint(300, 1800),  # 5-30 minutes
            "player_level": random.randint(1, 50)
        }
    
    def test_server_connection(self):
        """Test if the server is available."""
        try:
            response = self.session.get(f"{self.server_url}/api/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def send_stat_sheet(self, stat_sheet):
        """Send a single stat sheet to the server."""
        try:
            response = self.session.post(
                f"{self.server_url}/api/submit", 
                json=stat_sheet, 
                timeout=10
            )
            if response.status_code == 201:
                return True, response.json()
            else:
                return False, f"HTTP {response.status_code}: {response.text}"
        except requests.RequestException as e:
            return False, f"Request error: {str(e)}"
    
    def generate_match_data(self, num_matches=50, players_per_match=4):
        """Generate stat sheets for multiple matches."""
        print(f"🎮 Generating data for {num_matches} matches ({players_per_match} players each)")
        
        stat_sheets = []
        for match_num in range(1, num_matches + 1):
            match_id = f"match_{match_num:03d}"
            
            for player_num in range(1, players_per_match + 1):
                player_id = f"player_{match_num}_{player_num}"
                stat_sheet = self.generate_stat_sheet(match_id, player_id)
                stat_sheets.append(stat_sheet)
        
        print(f"📊 Generated {len(stat_sheets)} stat sheets")
        return stat_sheets
    
    def upload_data_to_server(self, stat_sheets):
        """Upload all stat sheets to the server with progress tracking."""
        if not self.test_server_connection():
            print("❌ Cannot connect to server. Make sure it's running at", self.server_url)
            return False
        
        print("✅ Server connection verified")
        print(f"📤 Uploading {len(stat_sheets)} stat sheets...")
        
        success_count = 0
        failed_count = 0
        start_time = time.time()
        
        for i, stat_sheet in enumerate(stat_sheets):
            success, result = self.send_stat_sheet(stat_sheet)
            
            if success:
                success_count += 1
            else:
                failed_count += 1
                if failed_count <= 5:  # Show first 5 errors only
                    print(f"❌ Failed to send sheet {i+1}: {result}")
            
            # Progress update every 50 sheets
            if (i + 1) % 50 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                print(f"Progress: {i+1}/{len(stat_sheets)} sheets sent ({rate:.1f}/sec)")
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.01)
        
        elapsed = time.time() - start_time
        print(f"\n📊 Upload completed in {elapsed:.1f} seconds")
        print(f"✅ Successfully sent: {success_count} stat sheets")
        print(f"❌ Failed: {failed_count} stat sheets")
        
        # Get final server stats
        try:
            response = self.session.get(f"{self.server_url}/api/aggregate", timeout=5)
            if response.status_code == 200:
                stats = response.json()['data']
                print(f"\n🎯 Server now contains:")
                print(f"   📋 {stats['total_stat_sheets']} total stat sheets")
                print(f"   🎮 {stats['total_matches']} unique matches")
                print(f"   👥 {stats['total_players']} unique players")
                print(f"   🎁 Total items: {stats['total_items']}")
        except requests.RequestException:
            print("⚠️  Could not retrieve server statistics")
        
        return success_count > 0


def main():
    parser = argparse.ArgumentParser(description='Generate and upload loot telemetry data')
    parser.add_argument('--matches', type=int, default=50, help='Number of matches to generate')
    parser.add_argument('--players', type=int, default=4, help='Number of players per match')
    parser.add_argument('--server', default='http://localhost:5000', help='Server URL')
    parser.add_argument('--generate-only', action='store_true', help='Generate data but don\'t upload')
    
    args = parser.parse_args()
    
    print("🎯 Loot Telemetry Data Generator")
    print("=" * 40)
    
    generator = LootTelemetryDataGenerator(args.server)
    
    # Generate the data
    stat_sheets = generator.generate_match_data(args.matches, args.players)
    
    if args.generate_only:
        print("📁 Saving data to files...")
        # Save to JSON files for inspection
        with open('generated_stat_sheets.json', 'w') as f:
            json.dump(stat_sheets, f, indent=2)
        print("✅ Data saved to generated_stat_sheets.json")
    else:
        # Upload to server
        success = generator.upload_data_to_server(stat_sheets)
        if success:
            print("🎉 Data generation and upload completed successfully!")
        else:
            print("💥 Data upload failed. Check server status.")


if __name__ == "__main__":
    main()