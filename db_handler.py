"""
Database Handler for Loot Telemetry Simulator
Handles SQLite database operations for storing and retrieving stat sheets
"""

import sqlite3
import json
from datetime import datetime
import os

class DatabaseHandler:
    def __init__(self, db_path="loot_telemetry.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create stat_sheets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stat_sheets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    match_id TEXT NOT NULL,
                    player_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    looted_items TEXT NOT NULL,
                    locations TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_match_id ON stat_sheets(match_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_player_id ON stat_sheets(player_id)
            ''')
            
            conn.commit()
            print("Database initialized successfully")
    
    def insert_stat_sheet(self, stat_sheet):
        """Insert a single stat sheet into the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO stat_sheets (match_id, player_id, timestamp, looted_items, locations)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    stat_sheet['match_id'],
                    stat_sheet['player_id'],
                    stat_sheet['timestamp'],
                    json.dumps(stat_sheet['looted_items']),
                    json.dumps(stat_sheet.get('locations', {}))
                ))
                
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error inserting stat sheet: {e}")
            return None
    
    def get_stat_sheets(self, match_id=None, player_id=None, limit=None):
        """Retrieve stat sheets with optional filtering"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM stat_sheets WHERE 1=1"
                params = []
                
                if match_id:
                    query += " AND match_id = ?"
                    params.append(match_id)
                
                if player_id:
                    query += " AND player_id = ?"
                    params.append(player_id)
                
                query += " ORDER BY created_at DESC"
                
                if limit:
                    query += " LIMIT ?"
                    params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                stat_sheets = []
                for row in rows:
                    stat_sheet = {
                        'id': row[0],
                        'match_id': row[1],
                        'player_id': row[2],
                        'timestamp': row[3],
                        'looted_items': json.loads(row[4]),
                        'locations': json.loads(row[5]) if row[5] else {},
                        'created_at': row[6]
                    }
                    stat_sheets.append(stat_sheet)
                
                return stat_sheets
        except Exception as e:
            print(f"Error retrieving stat sheets: {e}")
            return []
    
    def get_aggregate_stats(self):
        """Get aggregated loot statistics across all matches"""
        try:
            stat_sheets = self.get_stat_sheets()
            
            # Aggregate totals
            all_loots = {}
            total_matches = set()
            total_players = set()
            
            for sheet in stat_sheets:
                total_matches.add(sheet['match_id'])
                total_players.add(sheet['player_id'])
                
                for item, count in sheet['looted_items'].items():
                    all_loots[item] = all_loots.get(item, 0) + count
            
            return {
                'total_items': all_loots,
                'total_matches': len(total_matches),
                'total_players': len(total_players),
                'total_stat_sheets': len(stat_sheets)
            }
        except Exception as e:
            print(f"Error getting aggregate stats: {e}")
            return {}
    
    def get_heatmap_data(self, item_name):
        """Get location data for heatmap visualization"""
        try:
            stat_sheets = self.get_stat_sheets()
            
            locations = []
            for sheet in stat_sheets:
                if item_name in sheet['locations'] and sheet['looted_items'].get(item_name, 0) > 0:
                    x, y = sheet['locations'][item_name]
                    count = sheet['looted_items'][item_name]
                    locations.extend([(x, y)] * count)  # Repeat based on count
            
            return locations
        except Exception as e:
            print(f"Error getting heatmap data: {e}")
            return []
    
    def clear_database(self):
        """Clear all stat sheets (useful for testing)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM stat_sheets")
                conn.commit()
                print("Database cleared successfully")
        except Exception as e:
            print(f"Error clearing database: {e}")
    
    def close(self):
        """Close database connection (if needed for cleanup)"""
        pass  # Using context managers, so no explicit close needed