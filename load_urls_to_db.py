from extract_images import extract_image_caption_sets_from_url
from add_to_chroma import add_to_collection




def load_urls_to_db(url_list):
    results = []

    for url in url_list:
        image_dict = extract_image_caption_sets_from_url(url)
        data = {"metadata": {"url": url}, "image_dict": image_dict}
        results.append(add_to_collection(data))

    return results 


url_list = ["url1", "url2", "url3"]  # replace with your actual list of URLs
results = load 
