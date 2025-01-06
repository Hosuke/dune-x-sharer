# Dune Dashboard Sharer

一个用于捕获 Dune Analytics 仪表板图表和数据的工具。

## 功能特点

- 自动捕获仪表板中的图表和数据列表
- 智能识别不同类型的可视化内容（图表、表格、列表等）
- 保持原始分辨率和质量
- 支持多种图表类型（Canvas, SVG, ECharts, Highcharts等）
- 自动优化大尺寸图表的质量

## 安装要求

- Python 3.8+
- Chrome 浏览器

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/dune-x-sharer.git
cd dune-x-sharer
```

2. 创建并激活虚拟环境：
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

4. 安装 Playwright：
```bash
playwright install chromium
```

5. 复制环境变量文件：
```bash
cp .env.example .env
```

## 启动说明

1. 启动 Chrome 浏览器并登录 Dune Analytics
2. 启动服务：
```bash
python -m flask run --port 5001
```
3. 在浏览器中打开要分享的 Dune 仪表板
4. 点击分享按钮
5. 截图将保存在 `output/screenshots` 目录中

## 配置说明

在 `.env` 文件中设置以下环境变量：

- `FLASK_APP`: 应用入口文件
- `FLASK_ENV`: 运行环境
- `FLASK_DEBUG`: 调试模式
- `PORT`: 服务端口
- `HOST`: 服务地址
- `LOG_LEVEL`: 日志级别

## 注意事项

- 确保 Chrome 浏览器已经登录 Dune Analytics
- 图表加载可能需要一些时间，请耐心等待
- 建议使用 1920x1080 或更高的屏幕分辨率

## 贡献指南

欢迎提交 Pull Requests 和 Issues！

## 许可证

MIT License
