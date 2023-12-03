from load_urls_to_db import load_urls_to_db

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

r = load_urls_to_db(arxiv_vanity_links)
print(r)