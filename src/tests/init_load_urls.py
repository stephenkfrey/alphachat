from src.scripts.db_add_data import add_url_list_to_collection

import os
print(os.system('tree -L 2'))

user_command = input("Enter which initial dataset to load into the db (TEST or FULL)(or a local txt list of files): ")

arxiv_vanity_links = []

if user_command.upper() == "TEST":
    arxiv_vanity_links = [
        "https://www.arxiv-vanity.com/papers/2204.06125/",
        "https://www.arxiv-vanity.com/papers/2201.03545/",
        "https://www.arxiv-vanity.com/papers/2208.12266/",
    ]
elif user_command.upper() == "FULL":
    arxiv_vanity_links = [
        "https://www.arxiv-vanity.com/papers/2204.06125/",
        "https://www.arxiv-vanity.com/papers/2201.03545/",
        "https://www.arxiv-vanity.com/papers/2204.02311/",
        "https://www.arxiv-vanity.com/papers/2103.14030/",
        "https://www.arxiv-vanity.com/papers/2103.00020/",
        "https://www.arxiv-vanity.com/papers/2010.11929/",
        "https://www.arxiv-vanity.com/papers/2104.14294/",
        "https://www.arxiv-vanity.com/papers/2005.14165/",
        "https://www.arxiv-vanity.com/papers/2004.10934/",
        "https://www.arxiv-vanity.com/papers/1910.10683/",
        "https://www.arxiv-vanity.com/papers/2006.07733/",
        "https://www.arxiv-vanity.com/papers/1706.03762/",
        "https://www.arxiv-vanity.com/papers/2308.09592/", 
        "https://www.arxiv-vanity.com/papers/1311.2901/", 
    ]


elif user_command.upper().endswith('.TXT'):
    with open(user_command, 'r') as file:
        arxiv_vanity_links = file.read().splitlines()
        print('avl',arxiv_vanity_links)


print ('\n loading ', len(arxiv_vanity_links), ' links into the database \n: ', arxiv_vanity_links)
r = add_url_list_to_collection(arxiv_vanity_links)
print(r)