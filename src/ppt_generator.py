
class PPTGenerator:
    def __init__(self, openai_service, max_pages=5):
        self.openai_service = openai_service  # 注入OpenAI服务
        self.max_pages = max_pages

    def generate_outline(self, user_prompt, max_pages):
        """生成PPT大纲"""
        return self.openai_service.generate_ppt_outline(user_prompt, max_pages)

    def generate_description(self, title, points):
        """生成页面描述"""
        return self.openai_service.generate_page_description(title, points)

    def parse_ppt_content(self, response_text):
        pages = []
        current_page = {"title": "", "points": []}
        
        for line in response_text.split('\n'):
            line = line.strip()
            if line.startswith('# '):
                if current_page["title"]:
                    pages.append(current_page)
                    current_page = {"title": "", "points": []}
                current_page["title"] = line[2:].strip()
            elif line.startswith('## '):
                if not current_page["title"]:
                    current_page["title"] = line[3:].strip()
                else:
                    current_page["points"].append(line[3:].strip())
            elif line.startswith('-'):
                current_page["points"].append(line[1:].strip())
        
        if current_page["title"] or current_page["points"]:
            pages.append(current_page)
        return pages

    def parse_desc_content(self, text):
        """解析描述生成结果"""
        try:
            summary_part = text.split('摘要：')[1].split('提示：')[0].strip()
            prompt_part = text.split('提示：')[1].strip()
        except IndexError:
            summary_part = "无法解析摘要内容"
            prompt_part = "无法解析提示词"
        
        return {
            "summary": summary_part,
            "image_prompt": prompt_part
        } 