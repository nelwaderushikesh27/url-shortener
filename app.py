#!/usr/bin/env python3
"""
🔗 URL Shortener
A simple URL shortener built with Flask.
"""

from flask import Flask, render_template, request, redirect, jsonify, send_file
from models import db, URL
from utils import generate_short_code, generate_qr_code
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
app.config['BASE_URL'] = os.environ.get('BASE_URL', 'http://localhost:5000')

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """Shorten a URL."""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    original_url = data['url']
    custom_alias = data.get('custom_alias')
    expires_in_days = data.get('expires_in_days')
    
    # Validate URL
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url
    
    # Check if custom alias is available
    if custom_alias:
        existing_url = URL.query.filter_by(short_code=custom_alias).first()
        if existing_url:
            return jsonify({'error': 'Custom alias already in use'}), 409
        short_code = custom_alias
    else:
        short_code = generate_short_code()
        while URL.query.filter_by(short_code=short_code).first():
            short_code = generate_short_code()
    
    # Calculate expiration
    expires_at = None
    if expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    # Create URL record
    url = URL(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at
    )
    
    db.session.add(url)
    db.session.commit()
    
    short_url = f"{app.config['BASE_URL']}/{short_code}"
    
    return jsonify({
        'short_url': short_url,
        'original_url': original_url,
        'expires_at': expires_at.isoformat() if expires_at else None
    }), 201


@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """Get URL statistics."""
    url = URL.query.filter_by(short_code=short_code).first()
    
    if not url:
        return jsonify({'error': 'URL not found'}), 404
    
    return jsonify({
        'short_url': url.short_code,
        'original_url': url.original_url,
        'clicks': url.clicks,
        'created_at': url.created_at.isoformat(),
        'expires_at': url.expires_at.isoformat() if url.expires_at else None
    })


@app.route('/api/qr/<short_code>')
def get_qr_code(short_code):
    """Generate QR code for a short URL."""
    url = URL.query.filter_by(short_code=short_code).first()
    
    if not url:
        return jsonify({'error': 'URL not found'}), 404
    
    short_url = f"{app.config['BASE_URL']}/{short_code}"
    qr_code = generate_qr_code(short_url)
    
    return send_file(qr_code, mimetype='image/png')


@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to original URL."""
    url = URL.query.filter_by(short_code=short_code).first()
    
    if not url:
        return render_template('404.html'), 404
    
    # Check expiration
    if url.expires_at and url.expires_at < datetime.utcnow():
        return render_template('expired.html'), 410
    
    # Increment click counter
    url.clicks += 1
    db.session.commit()
    
    return redirect(url.original_url)


if __name__ == '__main__':
    app.run(debug=True)
