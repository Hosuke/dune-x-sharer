# Dune Dashboard Sharer

A powerful tool for capturing and sharing Dune Analytics dashboard charts and data on Twitter/X.

## Features

- Automatically capture charts and data visualizations from Dune dashboards
- Smart detection of different visualization types (charts, tables, lists)
- Maintains original resolution and quality
- Supports various chart types (Canvas, SVG, ECharts, Highcharts, etc.)
- Automatic quality optimization for large visualizations
- Direct sharing to Twitter/X using your browser session

## Requirements

- Python 3.8+
- Google Chrome browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dune-x-sharer.git
cd dune-x-sharer
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright:
```bash
playwright install chromium
```

5. Copy environment variables file:
```bash
cp .env.example .env
```

## Usage

1. Start Chrome with remote debugging:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

2. Log into Dune Analytics and Twitter/X in Chrome
3. Start the service:
```bash
python -m flask run --port 5001
```
4. Open the Dune dashboard you want to share
5. Click the share button
6. Screenshots will be automatically shared to Twitter/X

## Configuration

Set the following environment variables in `.env`:

- `FLASK_APP`: Application entry point
- `FLASK_ENV`: Running environment
- `FLASK_DEBUG`: Debug mode
- `PORT`: Service port
- `HOST`: Service address
- `LOG_LEVEL`: Logging level

## Important Notes

- Ensure Chrome browser is logged into both Dune Analytics and Twitter/X
- Chart loading may take some time, please be patient
- Recommended screen resolution: 1920x1080 or higher

## Future Roadmap

### Planned Features

1. **Smart Thread Creation**
   - Automatic batch processing of dashboard content
   - Intelligent slicing of content into Twitter threads
   - Smart content organization for better storytelling

2. **AI-Powered Enhancements**
   - AI agent for optimal chart composition and layout
   - Smart caption generation for charts
   - Context-aware content organization
   - Automated chart styling and theme application

3. **Advanced Sharing Features**
   - Support for more social platforms
   - Customizable sharing templates
   - Scheduled posting
   - Analytics and engagement tracking

4. **Visualization Improvements**
   - Custom chart annotations
   - Interactive preview before sharing
   - Theme customization
   - Watermark and branding options

## Contributing

Contributions are welcome! Feel free to submit Pull Requests and Issues.

## License

MIT License
