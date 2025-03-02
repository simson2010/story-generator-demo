# pip install zhipuai 请先在终端进行安装
from zhipuai import ZhipuAI
import os 

import sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)
from logger import LOG

class ZhipuImageGenerator:
    def __init__(self, api_key):
        self.client = ZhipuAI(api_key=api_key)
    
    def generate_image(self, prompt, model="cogview-3-plus"):
        """生成文生图
        参数：
            prompt: 中文提示词
            model: 模型版本（默认cogview-4）
        返回：
            (image_url, revised_prompt) 元组
        """

        LOG.info(f"正在生成图片，prompt: {prompt}")
        try:
            response = self.client.images.generations(
                model=model,
                prompt=prompt,
            )
            return response.data[0].url, prompt  # 智谱暂不返回优化后的prompt
        except Exception as e:
            raise RuntimeError(f"图片生成失败: {str(e)}")