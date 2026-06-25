# 🔗 URL Shortener

A simple and efficient URL shortener service built with Python and Flask.

## ✨ Features
- Shorten long URLs instantly
- Custom aliases for short URLs
- Click tracking and analytics
- QR code generation
- Rate limiting
- URL expiration
- REST API

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite (easily switchable to PostgreSQL)
- **QR Code:** qrcode library
- **Frontend:** HTML, CSS, JavaScript

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/url-shortener.git

# Navigate to directory
cd url-shortener

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000`

## 📡 API Endpoints

### Shorten URL
```http
POST /api/shorten
Content-Type: application/json

{
  "url": "https://example.com/very/long/url",
  "custom_alias": "my-link",
  "expires_in_days": 30
}
```

Response:
```json
{
  "short_url": "http://localhost:5000/my-link",
  "original_url": "https://example.com/very/long/url",
  "expires_at": "2024-02-15T10:00:00Z"
}
```

### Get URL Stats
```http
GET /api/stats/my-link
```

Response:
```json
{
  "short_url": "my-link",
  "original_url": "https://example.com/very/long/url",
  "clicks": 142,
  "created_at": "2024-01-15T10:00:00Z"
}
```

### Generate QR Code
```http
GET /api/qr/my-link
```

Returns QR code image.

## 📁 Project Structure
```
url-shortener/
├── app.py              # Main Flask application
├── models.py           # Database models
├── utils.py            # Utility functions
├── requirements.txt    # Dependencies
├── templates/
│   ├── index.html      # Home page
│   └── stats.html      # Stats page
├── static/
│   ├── css/
│   └── js/
└── database.db         # SQLite database
```

## 🔧 Configuration

Create a `.env` file:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///database.db
BASE_URL=http://localhost:5000
```

## 📊 Features Detail

### URL Analytics
- Total clicks
- Clicks over time
- Referrer tracking
- Browser/device stats

### Security Features
- Rate limiting (100 requests/hour)
- Input validation
- SQL injection prevention
- XSS protection

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License
MIT License - see [LICENSE](LICENSE)

---

Made with ❤️ by [Your Name]
