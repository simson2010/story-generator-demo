
# AI PPT 生成器

![应用截图](docs/screenshot.png)

基于AI技术的故事型PPT自动生成工具，支持动态内容生成和智能配图

## 功能特性

- 🔒 用户身份认证（密码哈希保护）
- 📝 AI智能生成PPT大纲（支持3-8页动态调整）
- ✨ 自动生成页面描述与配图提示词
- 🖼️ 集成智谱AI文生图服务
- 🌊 动态背景波浪效果
- 📱 响应式移动端适配

## 技术栈

- **后端框架**: Flask
- **AI服务**: 
  - OpenAI 内容生成
  - 智谱AI 图像生成
- **安全认证**: Werkzeug密码哈希
- **前端**: HTML5/CSS3 + 自适应布局
- **配置管理**: python-dotenv

## 快速开始

### 前置要求
- Python 3.8+
- OpenAI API密钥
- 智谱AI API密钥

### 安装步骤


#### 克隆仓库
```bash
git clone git@github.com:simson2010/story-generator-demo.git

```

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 配置环境变量
在项目根目录下创建 `.env` 文件，并添加以下内容：

```plaintext
OPENAI_API_KEY=your-openai-api-key
ZHIHUI_API_KEY=your-zhihui-api-key
```

#### 认证配置
```plaintext
AUTH_USERNAME=admin
AUTH_PASSWORD_HASH=pbkdf2:sha256:...
```

### 运行应用
```bash
python app.py
```

访问 `http://localhost:5000/` 查看效果。

## 使用指南
1. 访问 `http://localhost:5000/login`
2. 使用配置的用户名密码登录
3. 输入主题并选择页数（3-8页）
4. 生成后可按页生成详细描述和配图

## 项目结构
```plaintext
.env # 环境变量配置文件
├── app.py # 主应用入口
├── src/ # 核心模块
│ ├── ppt_generator.py # PPT生成逻辑
│ ├── openai_service.py # OpenAI服务封装
│ └── zhipu_image.py # 图像生成服务
├── templates/ # 前端模板
└── static/ # 静态资源
```

## 注意事项

- 请确保遵守OpenAI与智谱AI的使用条款和服务协议。
- 本工具仅为演示用途，实际应用中请谨慎使用敏感信息。

## 安全建议
1. 生产环境务必设置`FLASK_DEBUG=false`
2. 使用HTTPS加密传输
3. 定期轮换API密钥
4. 密码哈希应通过`generate_password_hash`生成

## 许可协议
MIT License © 2025 simson2010
