def build_locator_prompt(html, element_name):
    return f"""
    You are a QA automation expert.

    HTML Page Source:
    {html}

    Task:
    Find the most reliable Selenium locator for: '{element_name}'

    Rules:
    - Prefer id > name > css > xpath
    - Return ONLY one locator in this exact format:
      id=...  OR  name=...  OR  css=...  OR  xpath=...
    - No explanation. No extra text.
    """
