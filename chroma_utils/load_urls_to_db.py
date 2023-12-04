from extract_images import extract_image_caption_sets_from_url
from add_query import add_list_of_dicts_to_collection

####### 
def load_urls_to_db(url_list):
    print (f"---- Loading images and captions from URLs ---- ")
    results = []
    data_list = [] 

    for url in url_list:
        # print ('\n\nadding to db from ', url)
        list_of_image_dicts = extract_image_caption_sets_from_url(url)
        # print('\n\n---- list of image dicts', list_of_image_dicts)
        for single_image_dict in list_of_image_dicts:
            print ('item',single_image_dict)
            data = {
                "prompt": single_image_dict['caption'],
                "metadata": {
                    "page_url": url, 
                    "image_url":single_image_dict['image_url'],
                    "page_title": single_image_dict['page_title']
                    }
            }
            data_list.append(data)

    results.append(add_list_of_dicts_to_collection(data_list))
    return results 

#######  Run ####### 

# url_list = [
#     "https://www.arxiv-vanity.com/papers/2308.09592/", 
#     "https://www.arxiv-vanity.com/papers/1311.2901/", 
#     "https://www.arxiv-vanity.com/papers/2208.12266/"
#     ] 

# results = load_urls_to_db(url_list)