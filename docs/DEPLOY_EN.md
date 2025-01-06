# Dune Dashboard Sharer - Deployment Guide

## Project Overview
Dune Dashboard Sharer is a web service that allows users to input a Dune Analytics dashboard URL, automatically capture all charts, and share them on Twitter as a thread.

## System Requirements
- Python 3.8+
- Chrome browser
- Twitter API credentials
- Sufficient disk space for temporary image storage

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd dune-x-sharer
```

2. Create virtual environment:
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

4. Configure environment variables:
```bash
cp .env.example .env
```
Edit `.env` file with your credentials:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

5. Run development server:
```bash
flask run
```

## Production Deployment

### Using Docker (Recommended)

1. Create Dockerfile:
```dockerfile
FROM python:3.8-slim

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

2. Build and run Docker container:
```bash
docker build -t dune-sharer .
docker run -p 8000:8000 --env-file .env dune-sharer
```

### Direct Server Deployment

1. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv chromium-browser chromium-chromedriver
```

2. Set up application directory:
```bash
mkdir -p /opt/dune-sharer
cd /opt/dune-sharer
```

3. Copy project files to server

4. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file with necessary configurations
```

7. Use Supervisor for process management (recommended):
```
[program:dune-sharer]
directory=/opt/dune-sharer
command=/opt/dune-sharer/venv/bin/gunicorn --bind 0.0.0.0:8000 app:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/dune-sharer/err.log
stdout_logfile=/var/log/dune-sharer/out.log
```

8. Configure Nginx reverse proxy:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Security Considerations

1. Keep `.env` file secure, never commit to version control
2. Use HTTPS for encrypted transmission
3. Implement rate limiting to prevent abuse
4. Regularly update dependencies for security patches
5. Configure appropriate firewall rules

## Monitoring and Maintenance

1. Set up log rotation
2. Monitor server resource usage
3. Regularly backup configuration files
4. Set up monitoring alert system

## Troubleshooting

Common issues:

1. Chrome driver issues:
   - Ensure Chrome and ChromeDriver versions match
   - Verify Chrome installation

2. Twitter API limitations:
   - Monitor API usage quotas
   - Implement retry mechanisms

3. Memory usage:
   - Regular cleanup of temporary files
   - Monitor memory consumption

## Support

For issues or questions, please contact: [Contact Information]
