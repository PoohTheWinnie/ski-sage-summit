import os
import json
import requests

def load_books(books_directory: str):
    """Load all books from a directory into the RAG system"""
    for filename in os.listdir(books_directory):
        if filename.endswith('.txt'):  # Assuming books are in txt format
            with open(os.path.join(books_directory, filename), 'r') as f:
                content = f.read()
                
                # Create metadata for the book
                metadata = {
                    'title': filename.replace('.txt', ''),
                    'author': 'Unknown',  # Add actual metadata as available
                    'year': 0,
                    'publisher': 'Unknown',
                    'category': 'skiing'
                }
                
                # Upload to the API
                files = {
                    'file': ('book.txt', content, 'text/plain'),
                    'metadata': (None, json.dumps(metadata))
                }
                
                response = requests.post(
                    'http://localhost:8000/api/upload-book',
                    files=files
                )
                
                print(f"Uploaded {filename}: {response.json()}")

if __name__ == "__main__":
    load_books('path/to/your/books') 