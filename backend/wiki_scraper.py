import wikipediaapi
import json
import os
import time

class WikiSkiScraper:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='SkiSageSummit/1.0 (contact@skisage.com)'
        )
        
        # Core skiing topics to start with
        self.seed_topics = [
            "Skiing",
            "Alpine skiing",
            "Ski resort",
            "Ski equipment",
            "Ski binding",
            "Ski boot",
            "Ski pole",
            "Snowboarding",
            "List of ski areas and resorts",
            "Ski touring",
            "Ski mountaineering",
            "Cross-country skiing",
            "Freestyle skiing",
            "Ski jumping",
            "Snow conditions",
            "Ski wax",
            "Ski technique",
            "Ski trail rating",
            "Ski lift",
            "Avalanche safety",
        ]
        
    def get_related_pages(self, page):
        """Extract links to related skiing pages"""
        if not page.exists():
            return []
        
        related = []
        for link in page.links.values():
            # Filter relevant skiing-related pages
            if any(term in link.title.lower() for term in ['ski', 'snow', 'winter sport', 'mountain']):
                related.append(link.title)
        return related

    def scrape_page(self, title):
        """Scrape content from a single Wikipedia page"""
        page = self.wiki.page(title)
        if not page.exists():
            return None
            
        content = {
            'title': page.title,
            'text': page.text,
            'summary': page.summary,
            'url': page.fullurl,
            'categories': list(page.categories.keys())
        }
        return content

    def save_as_text_file(self, content, output_dir):
        """Save article content as a text file"""
        # Create a filename-safe version of the title
        filename = content['title'].replace('/', '_').replace('\\', '_')
        filename = ''.join(c for c in filename if c.isalnum() or c in (' ', '_', '-'))
        filepath = os.path.join(output_dir, f"{filename}.txt")
        
        # Create the text content with metadata
        text_content = f"""Title: {content['title']}
URL: {content['url']}
Categories: {', '.join(content['categories'])}

Summary:
{content['summary']}

Full Article:
{content['text']}
"""
        
        # Save the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        return filepath

    def scrape_all(self, output_dir='data/texts', max_pages=100):
        """Scrape all skiing-related content and save as text files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Set to keep track of processed pages
        processed_pages = set()
        metadata = []
        
        # Start with seed topics
        pages_to_process = self.seed_topics.copy()
        
        print("Starting Wikipedia scraping for ski-related content...")
        
        while pages_to_process and len(metadata) < max_pages:
            current_page = pages_to_process.pop(0)
            
            if current_page in processed_pages:
                continue
                
            print(f"Processing: {current_page}")
            
            # Scrape current page
            content = self.scrape_page(current_page)
            if content:
                # Save as text file
                filepath = self.save_as_text_file(content, output_dir)
                
                # Add to metadata
                metadata.append({
                    'title': content['title'],
                    'file': os.path.basename(filepath),
                    'url': content['url'],
                    'categories': content['categories']
                })
                
                processed_pages.add(current_page)
                
                # Get related pages
                related = self.get_related_pages(self.wiki.page(current_page))
                pages_to_process.extend([p for p in related if p not in processed_pages])
                
            # Rate limiting to be nice to Wikipedia
            time.sleep(1)
            
            # Save metadata periodically
            if len(metadata) % 10 == 0:
                self._save_metadata(metadata, output_dir)
                
        # Final metadata save
        self._save_metadata(metadata, output_dir)
        print(f"Scraping complete! Processed {len(metadata)} pages.")
        
    def _save_metadata(self, metadata, output_dir):
        """Save metadata about all scraped articles"""
        metadata_file = os.path.join(output_dir, 'metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    scraper = WikiSkiScraper()
    scraper.scrape_all() 