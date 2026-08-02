import os
from icrawler.builtin import GoogleImageCrawler

class GoogleImages:
    def __init__(self):
        pass

    def get_image(self, query, save_dir):
        """
        Downloads ONE image from Google Images using icrawler.
        Returns the local file path.
        """

        target_dir = os.path.join(save_dir, "images")
        os.makedirs(target_dir, exist_ok=True)

        crawler = GoogleImageCrawler(storage={"root_dir": target_dir})

       
        crawler.crawl(keyword=query, max_num=1)

        
        for file in os.listdir(target_dir):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                return os.path.join(target_dir, file)

        raise Exception("No image downloaded from Google.")
