import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

# Class to extract m3u8 link
class EmturbovidExtractor:
    def __init__(self, url):
        self.url = url

    def get_page_content(self):
        """Fetches the HTML content of the page."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error if the request was unsuccessful
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def extract_m3u8_link(self):
        """Extracts the m3u8 link from the data-hash attribute in the page content."""
        html_content = self.get_page_content()
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Find the div with id "video_player" and extract the data-hash attribute
            video_player_div = soup.find('div', id='video_player')
            if video_player_div and video_player_div.has_attr('data-hash'):
                m3u8_url = video_player_div['data-hash']
                return m3u8_url
            else:
                print("Error: m3u8 link not found.")
                return None
        else:
            return None

# Initialize Flask app
app = Flask(__name__)

@app.route('/extract', methods=['GET'])
def extract_m3u8():
    # Get the URL from the query parameter
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    
    # Create an instance of the extractor with the provided URL
    extractor = EmturbovidExtractor(url)
    m3u8_link = extractor.extract_m3u8_link()
    
    if m3u8_link:
        return jsonify({"m3u8_link": m3u8_link}), 200
    else:
        return jsonify({"error": "Failed to extract the m3u8 link"}), 404

# Example of running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
