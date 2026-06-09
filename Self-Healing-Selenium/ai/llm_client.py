import os
from openai import OpenAI


class LLMClient:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def suggest_locator(self, html, element):
        prompt = f"""
        You are a QA automation expert.

        HTML:
        {html}

        Task:
        Find the best Selenium locator for: {element}

        Return only one locator in this exact format (choose one):
        id=...
        name=...
        xpath=...
        css=...
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
