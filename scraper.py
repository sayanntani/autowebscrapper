import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape(self, url):
        """Simple scraping function"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            response = requests.get(url, timeout=10, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove scripts and styles
            for tag in soup(['script', 'style']):
                tag.decompose()

            result = {
                'url': url,
                'title': soup.title.string if soup.title else 'No title',
                'links': [],
                'images': [],
                'text_sample': soup.get_text()[:500] if soup.get_text() else '',
                'status': 'success'
            }

            # Get links
            for link in soup.find_all('a', href=True)[:50]:  # Limit to 50
                href = link.get('href')
                text = link.get_text(strip=True)[:100]
                if href:
                    result['links'].append({
                        'url': href,
                        'text': text
                    })

            # Get images
            for img in soup.find_all('img')[:20]:  # Limit to 20
                src = img.get('src')
                alt = img.get('alt', '')[:100]
                if src:
                    result['images'].append({
                        'src': src,
                        'alt': alt
                    })

            return result

        except requests.exceptions.MissingSchema:
            return {'status': 'error', 'message': 'Invalid URL format'}
        except requests.exceptions.ConnectionError:
            return {'status': 'error', 'message': 'Could not connect to website'}
        except requests.exceptions.Timeout:
            return {'status': 'error', 'message': 'Request timeout - website too slow'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)[:100]}

    def export_csv(self, data, filename):
        """Export data to CSV"""
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        filepath = os.path.join('downloads', filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow(['Web Scraper Export'])
            writer.writerow(['URL', data.get('url', '')])
            writer.writerow(['Title', data.get('title', '')])
            writer.writerow([])

            # Links
            writer.writerow(['LINKS'])
            writer.writerow(['URL', 'Text'])
            for link in data.get('links', []):
                writer.writerow([link['url'], link['text']])
            writer.writerow([])

            # Images
            writer.writerow(['IMAGES'])
            writer.writerow(['Source', 'Alt Text'])
            for img in data.get('images', []):
                writer.writerow([img['src'], img['alt']])
            writer.writerow([])

            # Text sample
            writer.writerow(['TEXT SAMPLE'])
            writer.writerow([data.get('text_sample', '')])

        return filepath
