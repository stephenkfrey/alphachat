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

def extract_image_caption_sets_from_url(url, save_directory="./downloaded_images"):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Unable to fetch the webpage. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')
    list_of_image_dicts = []
    page_title = soup.title.string if soup.title else "No title"

    print (f"\n ===== Extracting images from {page_title} =====\n")

    for index, img in enumerate(images):
        image_url = img['src']
        if image_url.startswith('data:image'):  # Base64 encoded image
            continue  
        image_url = f"https://ar5iv.labs.arxiv.org{image_url}" # for legit ones, 

        image_name = f"image_{index}.png"
        # download_image(url, image_url, image_name, save_directory)

        # Check for a figure parent and find the caption
        figure = img.find_parent('figure')
        caption = figure.figcaption.get_text().strip() if figure and figure.figcaption else "No caption"

        # text_before, text_after = extract_text_around_image(img)
        # references = "(placeholder) References to the image"

        list_of_image_dicts.append({
            'image_url': image_url, 
            'caption': caption,
            'page_title':page_title,
            # 'image_name': image_name,
            # 'text_before': text_before,
            # 'text_after': text_after,
            # 'references': references
        })

    pprint (list_of_image_dicts)

    return list_of_image_dicts

###### Example ###### 

url = "https://ar5iv.labs.arxiv.org/html/1412.1897/"
save_directory = "downloaded_images" 

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

image_caption_pairs = extract_image_caption_sets_from_url(url)

pprint(image_caption_pairs)

# {'caption': 'Figure 13: Images found by maximizing the softmax output for '
#              'classes via gradient ascent\xa0[11, 26]. Optimization begins at '
#              'the ImageNet mean (plus small Gaussian noise to break symmetry) '
#              'and continues until the DNN confidence for the target class '
#              'reaches 99.99%.\n'
#              'Images are shown with the mean subtracted.\n'
#              'Adding regularization makes images more recognizable but results '
#              'in slightly lower confidence scores (see supplementary '
#              'material).',
#   'image_url': '/html/1412.1897/assets/images/gradient_descent_nodecay_less.jpg',
#   'page_title': '[1412.1897] Deep Neural Networks are Easily Fooled: High '
#                 'Confidence Predictions for Unrecognizable Images'},


# https://ar5iv.labs.arxiv.org/html/1412.1897/assets/x5.png
