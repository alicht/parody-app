def is_tragedy(article_title: str) -> bool:
    keywords = [
        'deadly', 'attack', 'crash', 'explosion',
        'earthquake', 'flood', 'disaster',
        'massacre', 'tragedy', 'shooting'
    ]
    return any(word in article_title.lower() for word in keywords)