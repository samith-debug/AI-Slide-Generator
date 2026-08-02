import os
import requests
from utils import load_config


class SerpAPIImageFetcher:
    def __init__(self):
        self.config = load_config()
        self.api_key = self.config.get("serpapi_key", "")

   
    def clear_folder(self, folder):
        if not os.path.exists(folder):
            return

        for f in os.listdir(folder):
            try:
                os.remove(os.path.join(folder, f))
            except:
                pass

  
    def fetch_image_result(self, query):
        try:
            url = "https://serpapi.com/search.json"

            params = {
                "engine": "google",
                "q": query,
                "tbm": "isch",
                "api_key": self.api_key,
                "num": 1
            }

            resp = requests.get(url, params=params, timeout=15)

            if resp.status_code != 200:
                print("SerpAPI HTTP error:", resp.text)
                return None

            data = resp.json()
            images = data.get("images_results", [])

            if images:
                return images[0].get("original")

        except Exception as e:
            print("SerpAPI error:", e)

        return None

    
    def download_image(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=10)

            if resp.status_code == 200:
                return resp.content
        except Exception as e:
            print("Download error:", e)

        return None

    
    def get_image(self, query, save_dir):
        images_dir = os.path.join(save_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        self.clear_folder(images_dir)

        img_url = self.fetch_image_result(query)
        if not img_url:
            return None

        img_bytes = self.download_image(img_url)
        if not img_bytes:
            return None

        filename = os.path.join(images_dir, "image.jpg")

        with open(filename, "wb") as f:
            f.write(img_bytes)

        return filename



class UnsplashFallback:
    def get_image(self, query, save_dir):
        return None
