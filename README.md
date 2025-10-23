# 🎮 Loot Telemetry Simulator

A Python-based game telemetry simulation system that generates, processes, and analyzes loot data from simulated gaming sessions. This project demonstrates how game telemetry systems work in practice, complete with data generation, API server, and visualization components.

## 🌟 Features

- **Data Generation**: Simulate realistic game loot data for multiple matches and players
- **REST API Server**: Flask-based server for receiving and storing telemetry data
- **Database Storage**: SQLite database for persistent data storage
- **Data Visualization**: Generate charts and heatmaps from collected data
- **Interactive Notebook**: Jupyter notebook for data analysis and visualization
- **Real-time Analytics**: Aggregate statistics and location-based heatmaps

## 📁 Project Structure

```
loot-telemetry-sim/
├── simulator.ipynb      # Main Jupyter notebook for data generation & analysis
├── server.py           # Flask REST API server
├── db_handler.py       # Database operations and data management
├── test_server.py      # Test suite for server functionality
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Virtual environment support

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/loot-telemetry-sim.git
   cd loot-telemetry-sim
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Option 1: Full Simulation (Recommended)

1. **Start the API server**

   ```bash
   python server.py
   ```

   Server will be available at: http://localhost:5000

2. **Run the simulation notebook**
   - Open `simulator.ipynb` in Jupyter/VS Code
   - Execute all cells in order
   - Watch as data is generated, sent to server, and visualized

#### Option 2: Server Testing

```bash
python test_server.py
```

## 📊 What It Does

### 1. Data Generation

- Simulates 50 matches with 4 players each (200 total stat sheets)
- Generates random loot data for 5 item types:
  - 🦆 Rubber Duck
  - 🏥 Medkit
  - 📦 Ammo Box
  - 💣 Grenade
  - 🪙 Gold Coin
- Includes location coordinates for heatmap generation

### 2. API Endpoints

| Method | Endpoint              | Description                           |
| ------ | --------------------- | ------------------------------------- |
| GET    | `/`                   | API documentation homepage            |
| POST   | `/api/submit`         | Submit stat sheet data                |
| GET    | `/api/stats`          | Retrieve stat sheets (with filtering) |
| GET    | `/api/aggregate`      | Get aggregated statistics             |
| GET    | `/api/heatmap/{item}` | Get location data for heatmaps        |
| GET    | `/api/health`         | Server health check                   |

### 3. Data Analysis

- Aggregate loot statistics across all matches
- Location-based heatmaps showing where items are found
- Comparison between local simulation and server data
- Export charts as PNG files

## 🖼️ Generated Visualizations

The system generates several charts:

- `loot_totals.png` - Bar chart of total items looted
- `duck_heatmap.png` - Heatmap of rubber duck locations
- `local_vs_server_comparison.png` - Local vs server data comparison
- `server_duck_heatmap.png` - Server-based heatmap

## 🔧 Technical Details

### Database Schema

```sql
CREATE TABLE stat_sheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    looted_items TEXT NOT NULL,  -- JSON
    locations TEXT,              -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sample Data Structure

```json
{
	"match_id": "match_001",
	"player_id": "player_1_1",
	"timestamp": "2025-10-23T10:30:00",
	"looted_items": {
		"rubber_duck": 3,
		"medkit": 1,
		"ammo_box": 2
	},
	"locations": {
		"rubber_duck": [25.5, 75.2],
		"medkit": [10.0, 50.0]
	}
}
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python test_server.py
```

Tests include:

- Database operations (insert, retrieve, aggregate)
- API endpoint functionality
- Data integrity verification
- Server health checks

## 🛠️ Development

### Adding New Item Types

1. Update the `items` list in `simulator.ipynb`
2. Restart the server to handle new item types
3. Run the notebook to generate data with new items

### Extending the API

- Add new endpoints in `server.py`
- Update database schema in `db_handler.py` if needed
- Add corresponding tests in `test_server.py`

## 📈 Use Cases

This project demonstrates concepts useful for:

- **Game Analytics**: Understanding player behavior and item distribution
- **Telemetry Systems**: How games collect and process player data
- **Data Pipeline**: From generation → API → storage → analysis
- **Real-time Analytics**: Processing streaming game data
- **A/B Testing**: Comparing different game configurations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Future Enhancements

- [ ] Add player progression tracking
- [ ] Implement real-time websocket updates
- [ ] Add more visualization types (scatter plots, time series)
- [ ] Support for multiple game modes
- [ ] Player behavior clustering analysis
- [ ] Export data to different formats (CSV, JSON, Parquet)

---

Built with ❤️ using Python, Flask, SQLite, and Jupyter Notebooks
