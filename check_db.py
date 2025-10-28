#!/usr/bin/env python3
"""
Quick script to check stat_sheets table contents
"""

from db_handler import DatabaseHandler
import json

def check_stat_sheets():
    """Check the contents of the stat_sheets table"""
    db = DatabaseHandler()
    
    print("🔍 Checking stat_sheets table contents...\n")
    
    # Get all stat sheets
    stat_sheets = db.get_stat_sheets()
    
    if not stat_sheets:
        print("❌ No stat sheets found in database")
        return
    
    print(f"📊 Found {len(stat_sheets)} stat sheets")
    print("=" * 60)
    
    # Show first 5 entries as examples
    for i, sheet in enumerate(stat_sheets[:5]):
        print(f"\n📋 Entry #{i+1} (ID: {sheet['id']})")
        print(f"   🎮 Match: {sheet['match_id']}")
        print(f"   👤 Player: {sheet['player_id']}")
        print(f"   ⏰ Timestamp: {sheet['timestamp']}")
        print(f"   🎁 Items: {sheet['looted_items']}")
        if sheet['locations']:
            print(f"   📍 Locations: {sheet['locations']}")
        print(f"   📅 Created: {sheet['created_at']}")
    
    if len(stat_sheets) > 5:
        print(f"\n... and {len(stat_sheets) - 5} more entries")
    
    # Show aggregate stats
    print(f"\n📈 Aggregate Statistics:")
    stats = db.get_aggregate_stats()
    print(f"   🎮 Total matches: {stats['total_matches']}")
    print(f"   👥 Total players: {stats['total_players']}")
    print(f"   📋 Total stat sheets: {stats['total_stat_sheets']}")
    print(f"   🎁 Item totals: {stats['total_items']}")

def check_recent_entries(limit=10):
    """Show the most recent entries"""
    db = DatabaseHandler()
    
    print(f"🕒 Showing {limit} most recent entries:\n")
    
    stat_sheets = db.get_stat_sheets(limit=limit)
    
    for i, sheet in enumerate(stat_sheets):
        print(f"{i+1}. Match: {sheet['match_id']} | Player: {sheet['player_id']} | Items: {sum(sheet['looted_items'].values())} | Created: {sheet['created_at']}")

def check_by_match(match_id):
    """Show all entries for a specific match"""
    db = DatabaseHandler()
    
    print(f"🎮 Checking match: {match_id}\n")
    
    stat_sheets = db.get_stat_sheets(match_id=match_id)
    
    if not stat_sheets:
        print(f"❌ No stat sheets found for match {match_id}")
        return
    
    print(f"📊 Found {len(stat_sheets)} players in match {match_id}")
    
    for sheet in stat_sheets:
        print(f"   👤 {sheet['player_id']}: {sheet['looted_items']}")

if __name__ == "__main__":
    print("🗄️  Database Content Checker")
    print("=" * 40)
    
    # Show basic info
    check_stat_sheets()
    
    print("\n" + "=" * 60)
    
    # Show recent entries
    check_recent_entries()