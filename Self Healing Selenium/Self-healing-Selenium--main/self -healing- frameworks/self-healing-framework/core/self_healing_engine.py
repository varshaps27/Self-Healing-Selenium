from bs4 import BeautifulSoup


class SelfHealingEngine:

    def find_best_locator(self, html, tag_type="input"):
        """
        Parse the page HTML and find the best locator
        for the given tag type using priority order:
        id > name > css (class) > xpath fallback
        """
        soup = BeautifulSoup(html, "lxml")
        elements = soup.find_all(tag_type)

        for el in elements:

            # PRIORITY 1: ID (most stable)
            if el.get("id"):
                return {"type": "id", "value": el.get("id")}

            # PRIORITY 2: NAME
            if el.get("name"):
                return {"type": "name", "value": el.get("name")}

            # PRIORITY 3: CSS selector via class
            if el.get("class"):
                css = f"{tag_type}.{el.get('class')[0]}"
                return {"type": "css", "value": css}

        # FALLBACK: generic xpath
        return {"type": "xpath", "value": f"//{tag_type}"}
