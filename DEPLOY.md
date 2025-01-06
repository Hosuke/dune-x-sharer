# Dune Dashboard Sharer - Deployment Guide | 部署指南

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

### Project Overview
Dune Dashboard Sharer is a web service that allows users to input a Dune Analytics dashboard URL, automatically capture all charts, and share them on Twitter/X.

### System Requirements
- Python 3.8+
- Google Chrome browser
- Sufficient disk space for temporary screenshots

### Local Development Setup

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

5. Run development server:
```bash
flask run
```

### Production Deployment

#### Using Docker (Recommended)

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

#### Direct Server Deployment

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
```ini
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

### Security Considerations

1. Keep `.env` file secure and never commit to version control
2. Use HTTPS for data transmission
3. Implement rate limiting to prevent abuse
4. Regularly update dependencies for security patches
5. Configure appropriate firewall rules

### Monitoring and Maintenance

1. Set up log rotation
2. Monitor server resource usage
3. Regularly backup configuration files
4. Set up monitoring alert system

### Troubleshooting

Common issues:

1. Chrome driver issues:
   - Ensure Chrome and ChromeDriver versions match
   - Verify Chrome installation

2. Memory usage:
   - Regular cleanup of temporary files
   - Monitor memory consumption

### Support

For issues, please contact: [contact information]

---

<a name="chinese"></a>
## 中文

### 项目简介
Dune Dashboard Sharer 是一个Web服务，允许用户输入Dune Analytics dashboard的URL，自动截取所有图表并发布到Twitter/X上。

### 系统要求
- Python 3.8+
- Chrome浏览器
- 足够的磁盘空间用于临时存储截图

### 本地开发环境设置

1. 克隆代码库：
```bash
git clone <repository-url>
cd dune-x-sharer
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
```

5. 运行开发服务器：
```bash
flask run
```

### 生产环境部署

#### 使用 Docker 部署（推荐）

1. 创建 Dockerfile：
```dockerfile
FROM python:3.8-slim

# 安装 Chrome 和依赖
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

2. 构建并运行 Docker 容器：
```bash
docker build -t dune-sharer .
docker run -p 8000:8000 --env-file .env dune-sharer
```

#### 直接部署到服务器

1. 在服务器上安装系统依赖：
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv chromium-browser chromium-chromedriver
```

2. 设置应用目录：
```bash
mkdir -p /opt/dune-sharer
cd /opt/dune-sharer
```

3. 复制项目文件到服务器

4. 创建并激活虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate
```

5. 安装依赖：
```bash
pip install -r requirements.txt
```

6. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件添加必要的配置
```

7. 使用 Supervisor 管理进程（推荐）：
```ini
[program:dune-sharer]
directory=/opt/dune-sharer
command=/opt/dune-sharer/venv/bin/gunicorn --bind 0.0.0.0:8000 app:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/dune-sharer/err.log
stdout_logfile=/var/log/dune-sharer/out.log
```

8. 配置 Nginx 反向代理：
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

### 安全注意事项

1. 确保 `.env` 文件安全，不要提交到版本控制系统
2. 使用 HTTPS 加密传输
3. 实施速率限制以防止滥用
4. 定期更新依赖包以修复安全漏洞
5. 配置适当的防火墙规则

### 监控和维护

1. 设置日志轮转
2. 监控服务器资源使用情况
3. 定期备份配置文件
4. 设置监控告警系统

### 故障排除

常见问题：

1. Chrome驱动问题：
   - 确保Chrome和ChromeDriver版本匹配
   - 检查Chrome是否正确安装

2. 内存使用：
   - 定期清理临时文件
   - 监控内存使用情况

### 支持

如有问题，请联系：[联系方式]
