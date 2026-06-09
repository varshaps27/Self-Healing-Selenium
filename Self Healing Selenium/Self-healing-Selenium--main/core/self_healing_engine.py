from bs4 import BeautifulSoup


class SelfHealingEngine:

    def find_best_locator(self, html, tag_type="input"):
        """
        Parse page HTML and return the most specific
        locator, skipping hidden/irrelevant elements.
        """
        soup = BeautifulSoup(html, "lxml")
        elements = soup.find_all(tag_type)

        for el in elements:

            # ── SKIP hidden, submit, button, checkbox type inputs ──
            input_type = el.get("type", "").lower()
            if input_type in ["hidden", "submit", "button", "checkbox", "radio", "file"]:
                continue

            # ── SKIP elements with no visible role ──
            if el.get("name") in ["_token", "csrf_token", "csrf", "__RequestVerificationToken"]:
                continue

            # PRIORITY 1: NAME attribute (most reliable for forms)
            if el.get("name"):
                return {"type": "name", "value": el.get("name")}

            # PRIORITY 2: ID attribute
            if el.get("id"):
                return {"type": "id", "value": el.get("id")}

            # PRIORITY 3: Placeholder-based xpath
            if el.get("placeholder"):
                return {
                    "type": "xpath",
                    "value": f"//{tag_type}[@placeholder='{el.get('placeholder')}']"
                }

            # PRIORITY 4: CSS with class
            if el.get("class"):
                return {"type": "css", "value": f"{tag_type}.{el.get('class')[0]}"}

        # FALLBACK
        return {"type": "xpath", "value": f"//{tag_type}[not(@type='hidden')]"}