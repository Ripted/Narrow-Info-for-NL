# 🎯 Narrow Arrow Leaderboard Viewer

A web application and CLI tool for viewing Narrow Arrow game leaderboards with detailed run information.

## 🌟 Features

- **Web Interface**: Beautiful, responsive web UI for viewing leaderboards
- **Level Details**: Display level name, creator, creation date, and likes
- **Complete Leaderboards**: View all runs with player names, times, arrows used, and finish dates
- **Real-time Data**: Fetches live data from the Narrow Arrow API
- **CLI Tool**: Command-line interface also available

## 🚀 Quick Start

### Web Version

1. Run the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser to `http://localhost:5000`

3. Enter a level ID (try `1743661104278` for Tower of Hell)

### CLI Version

Run the command-line version:
```bash
python cli.py
```

Then enter level IDs when prompted.

## 📋 Requirements

- Python 3.11+
- Flask
- Requests
- Rich (for CLI)

Install dependencies:
```bash
pip install flask requests rich
```

Or with uv:
```bash
uv add flask requests rich
```

## 🎮 Example Levels

- **1743661104278** - Tower of Hell

## 📡 API Endpoints

### Level Details
`GET https://api.narrowarrow.xyz/level-details/{level_id}?isCustomLevel=true`

### Leaderboard
`GET https://api.narrowarrow.xyz/leaderboard?levelId={level_id}`

### Run Details
`GET https://api.narrowarrow.xyz/runs/{run_id}`

## 🗂️ Project Structure

```
.
├── app.py              # Flask web application
├── cli.py              # Command-line interface
├── templates/
│   ├── index.html      # Homepage
│   ├── leaderboard.html # Leaderboard display
│   └── error.html      # Error page
├── static/             # Static assets
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 💻 Development

The web application uses Flask with server-side rendering. The leaderboard page dynamically fetches run completion dates via AJAX to improve initial load times.

## 🤝 Contributing

Feel free to fork this project and submit pull requests!

## 📄 License

This project is open source and available for personal and educational use.

---

Made with ❤️ for the Narrow Arrow community
