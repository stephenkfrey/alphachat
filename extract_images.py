import requests
from bs4 import BeautifulSoup
import os
import base64
import urllib.parse
from pprint import pprint

###### Helpers ######

def download_image(base_url, image_url, image_name, save_directory):
    if image_url.startswith('http'):
        # Standard URL
        full_url = urllib.parse.urljoin(base_url, image_url)
        response = requests.get(full_url)
        if response.status_code == 200:
            with open(os.path.join(save_directory, image_name), 'wb') as file:
                file.write(response.content)
    elif image_url.startswith('data:image'):
        # Base64 encoded image
        header, image_data = image_url.split(',', 1)
        with open(os.path.join(save_directory, image_name), 'wb') as file:
            file.write(base64.b64decode(image_data))

def extract_text_around_image(img_tag):
    # This part is highly dependent on the HTML structure of the webpage

    text_before = ""
    text_after = ""
    current_element = img_tag

    # Traverse backwards to find text before the image
    while current_element.previous_sibling:
        current_element = current_element.previous_sibling
        if current_element.name == 'p':  # Assuming text is in <p> tags
            text_before = current_element.get_text() + " " + text_before

    current_element = img_tag

    # Traverse forwards to find text after the image
    while current_element.next_sibling:
        current_element = current_element.next_sibling
        if current_element.name == 'p':
            text_after += " " + current_element.get_text()

    return text_before, text_after

###### Main ###### 

def extract_image_caption_sets_from_url(url, save_directory="downloaded_images"):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Unable to fetch the webpage. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')
    data = []

    for index, img in enumerate(images):
        image_url = img['src']
        if image_url.startswith('data:image'):  # Base64 encoded image
            continue 

        image_name = f"image_{index}.png"
        # download_image(url, image_url, image_name, save_directory)

        # Check for a figure parent and find the caption
        figure = img.find_parent('figure')
        caption = figure.figcaption.get_text().strip() if figure and figure.figcaption else "No caption"

        text_before, text_after = extract_text_around_image(img)
        # references = "(placeholder) References to the image"

        data.append({
            'image_url': image_url, 
            'caption': caption,
            # 'image_name': image_name,
            # 'text_before': text_before,
            # 'text_after': text_after,
            # 'references': references
        })

    return data

###### Example ###### 

url = "https://www.arxiv-vanity.com/papers/2208.12266/"
save_directory = "downloaded_images" 

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

image_caption_pairs = extract_image_caption_sets_from_url(url)

pprint(image_caption_pairs)

