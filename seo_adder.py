import requests
from typing import List, Dict

class DuckDuckGoSearch:
    def __init__(self):
        self.api_url = "https://api.duckduckgo.com/"
    
    def perform_search(self, query: str) -> List[Dict]:
        """
        Fetch search results from DuckDuckGo Instant Answer API.
        """
        try:
            params = {
                "q": query,
                "format": "json",
                "pretty": 1,
                "no_html": 1
            }
            print("\nPerforming search...\n")
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract meaningful search results
            results = []
            if "RelatedTopics" in data:
                for topic in data["RelatedTopics"]:
                    if "Text" in topic and "FirstURL" in topic:
                        results.append({"text": topic["Text"], "url": topic["FirstURL"]})
            return results
        except Exception as e:
            print(f"Error while performing search: {e}")
            return [{"error": str(e)}]

# Test the DuckDuckGoSearch class
if __name__ == "__main__":
    search_tool = DuckDuckGoSearch()
    topic = "The role of AI in education"
    results = search_tool.perform_search(topic)

    print("\nSearch Results:\n")
    for idx, result in enumerate(results):
        print(f"{idx + 1}. {result['text']} ({result['url']})")
