# 🎮 Loot Telemetry Simulator

A Python-based game telemetry simulation system that generates, processes, and analyzes loot data from simulated gaming sessions. This project demonstrates how game telemetry systems work in practice, complete with data generation, API server, and visualization components.

## 🌟 Features

- **Data Generation**: Standalone script to simulate realistic game loot data for multiple matches and players
- **REST API Server**: Flask-based server for receiving and storing telemetry data
- **Database Storage**: SQLite database for persistent data storage
- **Data Visualization**: Generate comprehensive charts, heatmaps, and performance dashboards
- **Interactive Analysis**: Jupyter notebook focused on data analysis and visualization
- **Real-time Analytics**: Aggregate statistics and location-based heatmaps
- **Flexible Configuration**: Customizable match counts, player numbers, and server endpoints

## 📁 Project Structure

```
loot-telemetry-sim/
├── data_generator.py   # Standalone data generation and upload script
├── simulator.ipynb     # Jupyter notebook for data analysis & visualization
├── server.py          # Flask REST API server
├── db_handler.py      # Database operations and data management
├── test_server.py     # Test suite for server functionality
├── requirements.txt   # Python dependencies
├── .gitignore        # Git ignore rules
└── README.md         # This file
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

2. **Generate and upload mock data**

   ```bash
   # Generate default data (50 matches, 4 players each)
   python data_generator.py

   # Generate custom amount of data
   python data_generator.py --matches 100 --players 6

   # Generate data for a different server
   python data_generator.py --server http://localhost:8000

   # Generate data files without uploading to server
   python data_generator.py --generate-only
   ```

3. **Analyze data in Jupyter notebook**
   - Open `simulator.ipynb` in Jupyter/VS Code
   - Execute all cells to see comprehensive data analysis
   - View generated charts and performance dashboards

#### Option 2: Data Generator Options

The `data_generator.py` script supports several command-line options:

```bash
python data_generator.py [OPTIONS]

Options:
  --matches INTEGER    Number of matches to generate (default: 50)
  --players INTEGER    Number of players per match (default: 4)
  --server TEXT        Server URL (default: http://localhost:5000)
  --generate-only      Generate data but don't upload to server
  --help              Show help message and exit
```

**Examples:**

```bash
# Generate 200 matches with 8 players each
python data_generator.py --matches 200 --players 8

# Generate data for testing without server upload
python data_generator.py --matches 10 --generate-only

# Upload to a different server instance
python data_generator.py --server http://192.168.1.100:5000

# Large dataset generation
python data_generator.py --matches 500 --players 6
```

#### Option 3: Server Testing

```bash
python test_server.py
```

## 📊 What It Does

### 1. Data Generation (`data_generator.py`)

The standalone data generator simulates realistic game sessions:

- **Configurable Scale**: Generate any number of matches with custom player counts
- **Realistic Data**: Each player gets randomized loot counts (0-5 per item type)
- **Location Tracking**: Generates X,Y coordinates for collected items (used for heatmaps)
- **Performance Metrics**: Tracks upload speed and provides progress updates
- **Flexible Output**: Can save to files or upload directly to server

**Generated Item Types:**

- 🦆 Rubber Duck
- 🏥 Medkit
- 📦 Ammo Box
- 💣 Grenade
- 🪙 Gold Coin

**Sample Output:**

```
🎮 Generating data for 50 matches (4 players each)
📊 Generated 200 stat sheets
✅ Server connection verified
📤 Uploading 200 stat sheets...
Progress: 50/200 sheets sent (125.3/sec)
Progress: 100/200 sheets sent (127.8/sec)
Progress: 150/200 sheets sent (124.9/sec)

📊 Upload completed in 1.6 seconds
✅ Successfully sent: 200 stat sheets
❌ Failed: 0 stat sheets

🎯 Server now contains:
   📋 200 total stat sheets
   🎮 50 unique matches
   👥 200 unique players
   🎁 Total items: {'rubber_duck': 485, 'medkit': 523, ...}
```

### 2. Data Analysis (`simulator.ipynb`)

The Jupyter notebook provides comprehensive analysis:

- **Server Connectivity**: Tests connection and displays current data summary
- **Item Distribution**: Bar charts and pie charts of collected items
- **Location Heatmaps**: Visual maps showing where items are commonly found
- **Performance Dashboard**: Multi-panel view with key metrics
- **Export Charts**: Saves high-quality PNG files for reports

### 3. API Server (`server.py`)

| Method | Endpoint              | Description                           |
| ------ | --------------------- | ------------------------------------- |
| GET    | `/`                   | API documentation homepage            |
| POST   | `/api/submit`         | Submit stat sheet data                |
| GET    | `/api/stats`          | Retrieve stat sheets (with filtering) |
| GET    | `/api/aggregate`      | Get aggregated statistics             |
| GET    | `/api/heatmap/{item}` | Get location data for heatmaps        |
| GET    | `/api/health`         | Server health check                   |

### 4. Data Analysis Outputs

The Jupyter notebook creates comprehensive visualizations:

- **Item Distribution Analysis**: Shows which items are collected most frequently
- **Location-based Heatmaps**: Visual maps revealing popular loot locations
- **Performance Dashboard**: Multi-panel view combining statistics and metrics
- **Data Quality Metrics**: Coverage analysis and data completeness scores

## 🖼️ Generated Visualizations

The analysis system generates several high-quality charts:

- `item_distribution.png` - Bar chart showing item collection frequency with percentages
- `rubber_duck_heatmap.png` - Heatmap revealing popular rubber duck locations
- `performance_dashboard.png` - 4-panel dashboard with comprehensive metrics

**Sample Dashboard Panels:**

- **Item Distribution**: Pie chart showing percentage breakdown
- **Game Statistics**: Bar chart of matches, players, and stat sheets
- **Average Performance**: Items per player and items per match
- **Data Quality**: Coverage metrics and data completeness scores

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
	"timestamp": "2025-10-27T10:30:00",
	"looted_items": {
		"rubber_duck": 3,
		"medkit": 1,
		"ammo_box": 2,
		"grenade": 0,
		"gold_coin": 4
	},
	"locations": {
		"rubber_duck": [25.5, 75.2],
		"medkit": [10.0, 50.0],
		"ammo_box": [45.3, 30.1],
		"gold_coin": [80.7, 65.4]
	},
	"match_duration": 1250,
	"player_level": 23
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

### Architecture Overview

The project follows a clean separation of concerns:

1. **Data Generation Layer** (`data_generator.py`): Simulates game clients sending telemetry
2. **API Layer** (`server.py`): RESTful endpoints for data ingestion and retrieval
3. **Storage Layer** (`db_handler.py`): Database operations and data persistence
4. **Analysis Layer** (`simulator.ipynb`): Data visualization and insights generation

### Adding New Item Types

1. Update the `items` list in `data_generator.py`
2. Restart the server to handle new item types
3. Generate new data and run analysis notebook

### Scaling Data Generation

```bash
# Small dataset for testing
python data_generator.py --matches 10 --players 2

# Medium dataset for development
python data_generator.py --matches 100 --players 4

# Large dataset for performance testing
python data_generator.py --matches 1000 --players 8
```

### Extending the API

- Add new endpoints in `server.py`
- Update database schema in `db_handler.py` if needed
- Add corresponding tests in `test_server.py`
- Update analysis notebook for new data types

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

- [ ] **Multi-threaded Data Generation**: Parallel upload for faster bulk data creation
- [ ] **Real-time Streaming**: WebSocket support for live data feeds
- [ ] **Advanced Analytics**: Player behavior clustering and progression tracking
- [ ] **Multiple Game Modes**: Support different game types with varying item sets
- [ ] **Data Export**: CSV, JSON, and Parquet export options
- [ ] **Interactive Dashboards**: Web-based real-time visualization interface
- [ ] **A/B Testing Framework**: Compare different game balance configurations
- [ ] **Machine Learning**: Predictive analytics for player behavior
- [ ] **Performance Optimization**: Database indexing and query optimization
- [ ] **Docker Support**: Containerized deployment for easy scaling

## 🚀 Quick Examples

### Generate Large Dataset

```bash
# Generate 500 matches with 6 players each (3000 stat sheets)
python data_generator.py --matches 500 --players 6
```

### Test with Custom Server

```bash
# Point to a different server instance
python data_generator.py --server http://game-server.example.com:5000
```

### Development Workflow

```bash
# 1. Start server
python server.py

# 2. Generate test data
python data_generator.py --matches 20

# 3. Analyze in notebook
# Open simulator.ipynb and run all cells

# 4. Run tests
python test_server.py
```

---

Built with ❤️ using Python, Flask, SQLite, and Jupyter Notebooks
