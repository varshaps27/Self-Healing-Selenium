from bs4 import BeautifulSoup


class SelfHealingEngine:

    def find_best_locator(self, html, tag_type="input"):
        """
        Parses page HTML and returns the best available locator.

        Priority:
          1. name attribute
          2. id attribute
          3. placeholder-based xpath
          4. css via class
          5. fallback xpath

        Skips hidden, submit, CSRF/token fields.
        """
        soup = BeautifulSoup(html, "lxml")
        elements = soup.find_all(tag_type)

        for el in elements:

            # Skip non-interactable input types
            input_type = el.get("type", "").lower()
            if input_type in ["hidden", "submit", "button", "checkbox", "radio", "file"]:
                continue

            # Skip known CSRF / security token fields
            if el.get("name") in ["_token", "csrf_token", "csrf",
                                   "__RequestVerificationToken"]:
                continue

            # PRIORITY 1: NAME
            if el.get("name"):
                return {"type": "name", "value": el.get("name")}

            # PRIORITY 2: ID
            if el.get("id"):
                return {"type": "id", "value": el.get("id")}

            # PRIORITY 3: Placeholder xpath
            if el.get("placeholder"):
                return {
                    "type": "xpath",
                    "value": f"//{tag_type}[@placeholder='{el.get('placeholder')}']"
                }

            # PRIORITY 4: CSS via class
            if el.get("class"):
                return {"type": "css", "value": f"{tag_type}.{el.get('class')[0]}"}

        # FALLBACK
        return {"type": "xpath", "value": f"//{tag_type}[not(@type='hidden')]"}
