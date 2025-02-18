from openai import OpenAI
import os

class OpenAIService:
    def __init__(self, outline_template, desc_template):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.default_model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.desc_model = os.getenv('DESC_MODEL', 'gpt-4o-mini')
        self.outline_template = outline_template
        self.desc_template = desc_template
    
    def generate_ppt_outline(self, user_prompt, max_pages):
        """生成PPT大纲"""
        full_prompt = self.outline_template.format(max_pages=max_pages) + user_prompt
        return self._generate_content(full_prompt)
    
    def generate_page_description(self, title, points):
        """生成页面描述"""
        formatted_prompt = self.desc_template.format(
            title=title,
            points='\n'.join(points)
        )
        return self._generate_content(formatted_prompt, self.desc_model)
    
    def _generate_content(self, prompt, model=None):
        """通用生成方法"""
        try:
            completion = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(e)
            raise RuntimeError(f"API调用失败: {str(e)}") 