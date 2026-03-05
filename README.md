# Auto Web Scraper

A lightweight Flask-based web scraping application that extracts links, images, and text content from websites with a simple, intuitive interface.

## Features

✨ **Core Features**
- User authentication (registration & login)
- Web scraping with BeautifulSoup
- Extract links, images, and text content
- Export scraped data to CSV format
- Responsive Bootstrap 5 UI
- No database required (in-memory storage)

## Prerequisites

- Python 3.7 or higher
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sayanntani/autowebscrapper.git
cd autowebscrapper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

Start the application:
```bash
python app.py
```

Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Register** - Create a new account with email and password
2. **Login** - Sign in with your credentials
3. **Enter URL** - Input any website URL (e.g., example.com)
4. **Scrape** - Click "Start Scraping" to extract content
5. **Download** - Download the results as CSV file

## Technologies

- **Backend**: Flask 2.3.3
- **Scraping**: BeautifulSoup4, Requests
- **Frontend**: Bootstrap 5, HTML/CSS/JavaScript
- **Parser**: Python's built-in html.parser

## Project Structure

```
autowebscrapper/
├── app.py                 # Flask application & routes
├── scraper.py             # Web scraping logic
├── requirements.txt       # Project dependencies
├── templates/             # HTML templates
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── downloads/             # CSV exports (generated)
├── README.md              # This file
├── LICENSE                # MIT License
└── .gitignore            # Git ignore rules
```

## Example URLs to Test

- `https://example.com`
- `https://www.python.org`
- `https://news.ycombinator.com`

## CSV Export

Scraped data is exported as CSV with the following sections:
- Page metadata (URL, title)
- Links (URLs and anchor text)
- Images (sources and alt text)
- Text content sample

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Author

**Sayantani Bhattacharjee**