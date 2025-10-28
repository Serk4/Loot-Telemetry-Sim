from db_handler import DatabaseHandler

# Quick stats
db = DatabaseHandler()
stats = db.get_aggregate_stats()
print(f"Total records: {stats['total_stat_sheets']}")
print(f"Matches: {stats['total_matches']}")
print(f"Players: {stats['total_players']}")
print(f"Items: {stats['total_items']}")

# Show latest 3 entries
print("\nLatest 3 entries:")
recent = db.get_stat_sheets(limit=3)
for i, sheet in enumerate(recent, 1):
    print(f"{i}. {sheet['match_id']} | {sheet['player_id']} | {sheet['looted_items']}")