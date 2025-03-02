class PPTGenerator:
    def __init__(self, openai_service, max_pages=5):
        self.openai_service = openai_service  # 注入OpenAI服务
        self.max_pages = max_pages
        self.story_arc = self._adjust_story_arc(max_pages)  # 初始化故事弧线

    def generate_outline(self, user_prompt, max_pages):
        """生成PPT大纲"""
        self.max_pages = max_pages
        self.story_arc = self._adjust_story_arc(max_pages)  # 更新故事结构
        return self.openai_service.generate_ppt_outline(
            user_prompt=user_prompt,
            max_pages=max_pages
        )

    def generate_description(self, title, points, phase):
        """生成页面描述"""
        return self.openai_service.generate_page_description(
            title=title,
            points=points,
            phase=phase
        )

    def parse_ppt_content(self, response_text):
        pages = []
        current_page = {"title": "", "points": [], "phase": ""}
        
        for line in response_text.split('\n'):
            line = line.strip()
            if line.startswith('# '):
                if current_page["title"]:
                    pages.append(current_page)
                    current_page = {"title": "", "points": [], "phase": ""}
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
        
        # 自动填充阶段信息
        for idx, page in enumerate(pages):
            if not page.get('phase') and idx < len(self.story_arc):
                page['phase'] = self.story_arc[idx]
        return pages[:self.max_pages]

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

    def _adjust_story_arc(self, max_pages):
        arc_map = {
            3: ["开端", "对抗", "解决"],
            5: ["日常", "变故", "探索", "危机", "新生"],
            8: ["平静", "异动", "抉择", "挫折", "启悟", "对决", "代价", "终局"]
        }
        return arc_map.get(max_pages, arc_map[5]) 