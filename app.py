from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from src.zhipu_image import ZhipuImageGenerator
from src.openai_service import OpenAIService
from src.ppt_generator import PPTGenerator
from src.prompt_templates import DEFAULT_PROMPT_TEMPLATE, DESC_PROMPT
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
from functools import wraps

# 先加载环境变量
load_dotenv()

app = Flask(__name__)
app.config.update(
    DEFAULT_PROMPT_TEMPLATE=DEFAULT_PROMPT_TEMPLATE,
    DESC_PROMPT=DESC_PROMPT,
    MAX_PAGES=int(os.getenv('DEFAULT_MAX_PAGES', 5))
)

# 添加密钥配置
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-123')

image_gen = ZhipuImageGenerator(api_key=os.getenv('ZHIPU_API_KEY'))


# 初始化服务
openai_service = OpenAIService(
    outline_template=app.config['DEFAULT_PROMPT_TEMPLATE'],
    desc_template=app.config['DESC_PROMPT']
)

# 初始化PPT生成器时传入OpenAI服务
ppt_gen = PPTGenerator(
    openai_service=openai_service,
    max_pages=5
)

def parse_ppt_content(response_text):
    pages = []
    current_page = {"title": "", "points": []}
    
    for line in response_text.split('\n'):
        line = line.strip()
        # 检测页标题（支持 # 和 ## 两种标题标记）
        if line.startswith('# '):
            if current_page["title"]:
                pages.append(current_page)
                current_page = {"title": "", "points": []}
            current_page["title"] = line[2:].strip()
        elif line.startswith('## '):
            # 将二级标题作为第一个要点
            if not current_page["title"]:
                current_page["title"] = line[3:].strip()
            else:
                current_page["points"].append(line[3:].strip())
        elif line.startswith('-'):
            current_page["points"].append(line[1:].strip())
    
    if current_page["title"] or current_page["points"]:
        pages.append(current_page)
    return pages[:5]  # 最多5页

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username == os.getenv('AUTH_USERNAME') and 
            check_password_hash(os.getenv('AUTH_PASSWORD_HASH'), password)):
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error="无效凭证")
    return render_template('login.html')

# 注销路由
@app.route('/logout')
def logout():
    session.clear()  # 清空所有会话数据
    resp = redirect(url_for('login'))
    resp.delete_cookie('session')  # 删除客户端cookie
    return resp

# 认证装饰器
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated

# 保护现有路由
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
@login_required
def generate_ppt():
    user_prompt = request.form.get('prompt')
    max_pages = int(request.form.get('max_pages', 5))  # 获取用户选择的页数
    
    if not user_prompt:
        return jsonify({"error": "请输入主题内容"}), 400
    
    try:
        content = ppt_gen.generate_outline(user_prompt, max_pages)
        pages = ppt_gen.parse_ppt_content(content)
        return jsonify({"pages": pages})  # 不再截断
    
    except ValueError:
        return jsonify({"error": "无效的页数参数"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_desc', methods=['POST'])
def generate_page_desc():
    data = request.json
    try:
        content = ppt_gen.generate_description(
            title=data['title'],
            points=data['points'],
            phase=data['phase']  # 接收阶段参数
        )
        return jsonify(ppt_gen.parse_desc_content(content))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    try:
        image_url, _ = image_gen.generate_image(
            prompt=data['prompt']
        )
        return jsonify({
            "image_url": image_url,
            "revised_prompt": data['prompt']  # 智谱不返回优化后的prompt
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 