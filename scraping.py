import requests
from bs4 import BeautifulSoup


def scrape_quotes_by_tags(base_url, tags, quotes_per_tag=2):
    """Scrapes quotes from the given URL based on specified tags by accessing each tag's page."""
    try:
        quotes_data = {}
        unique_quotes = set()  # Set to store unique quotes globally across all tags

        for tag in tags:
            tag_url = f"{base_url}/tag/{tag}/"  # Construct URL for each tag
            response = requests.get(tag_url, timeout=(3, 10))
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            tag_quotes = []
            
            # Extract quotes from the tag-specific page
            for quote_block in soup.find_all("div", class_="quote"):
                quote_text = quote_block.find("span", class_="text").text.strip()
                
                # Ensure quotes are unique globally across all tags
                if quote_text not in unique_quotes:
                    tag_quotes.append(quote_text)
                    unique_quotes.add(quote_text)
                
                # Stop when we reach the required number of quotes
                if len(tag_quotes) == quotes_per_tag:
                    break
            
            quotes_data[tag] = tag_quotes

        return quotes_data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {}


if __name__ == "__main__":
    base_url = "http://quotes.toscrape.com"
    tags = ["love", "inspirational", "life", "humor", "books"]
    quotes_by_tag = scrape_quotes_by_tags(base_url, tags)
    
    # Print extracted quotes by tag
    for tag, quotes in quotes_by_tag.items():
        print(f"\nQuotes for tag: {tag}")
        for quote in quotes:
            print(f"- {quote}")
