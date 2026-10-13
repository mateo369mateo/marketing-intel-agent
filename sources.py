"""
Definition of top industry news feeds covering marketing, branding, and advertising.
"""

CATEGORIES = {
    "BRANDING": {
        "title": "Branding & Visual Identity",
        "description": "Rebrands, identity redesigns, brand positioning, packaging, and equity.",
        "badge_color": "#4338CA"  # Indigo
    },
    "ADVERTISING": {
        "title": "Advertising & Creative Campaigns",
        "description": "Breakthrough ad campaigns, agency moves, creative leadership, and media buying.",
        "badge_color": "#E11D48"  # Rose / Crimson
    },
    "MARKETING_TECH": {
        "title": "Marketing Strategy, Social & AdTech",
        "description": "Digital marketing trends, social media platform updates, AI in marketing, and consumer behavior.",
        "badge_color": "#0D9488"  # Teal
    }
}

NEWS_SOURCES = [
    # Advertising & Agencies
    {
        "name": "Adweek",
        "url": "https://www.adweek.com/feed/",
        "category": "ADVERTISING",
        "priority": 1
    },
    {
        "name": "Campaign Live",
        "url": "https://www.campaignlive.com/rss/news",
        "category": "ADVERTISING",
        "priority": 1
    },
    {
        "name": "Industry Ads & Agency Intel",
        "url": "https://news.google.com/rss/search?q=advertising+campaign+agency+commercial&hl=en-US&gl=US&ceid=US:en",
        "category": "ADVERTISING",
        "priority": 2
    },

    # Branding & Visual Identity
    {
        "name": "Brand New (UnderConsideration)",
        "url": "https://www.underconsideration.com/brandnew/atom.xml",
        "category": "BRANDING",
        "priority": 1
    },
    {
        "name": "Retail & Brand Strategy (Retail Dive)",
        "url": "https://www.retaildive.com/feeds/news/",
        "category": "BRANDING",
        "priority": 2
    },
    {
        "name": "Brand Identity & Rebrands",
        "url": "https://news.google.com/rss/search?q=branding+rebrand+logo+identity+packaging&hl=en-US&gl=US&ceid=US:en",
        "category": "BRANDING",
        "priority": 2
    },

    # Marketing, Social & MarTech
    {
        "name": "Marketing Dive",
        "url": "https://www.marketingdive.com/feeds/news/",
        "category": "MARKETING_TECH",
        "priority": 1
    },
    {
        "name": "Digiday",
        "url": "https://digiday.com/feed/",
        "category": "MARKETING_TECH",
        "priority": 1
    },
    {
        "name": "Social Media Today",
        "url": "https://www.socialmediatoday.com/feeds/news/",
        "category": "MARKETING_TECH",
        "priority": 2
    }
]
