"""
Definition of top industry news feeds covering marketing, branding, and advertising.
"""

CATEGORIES = {
    "BRANDING": {
        "title": "Branding & Visual Identity",
        "description": "Rebrands, identity redesigns, brand positioning, packaging, and creative case studies.",
        "badge_color": "#4338CA"  # Indigo
    },
    "ADVERTISING": {
        "title": "Advertising & Creative Campaigns",
        "description": "Breakthrough ad campaigns, agency moves, creative leadership, and award-winning commercials.",
        "badge_color": "#E11D48"  # Rose / Crimson
    },
    "MARKETING_TECH": {
        "title": "Marketing Strategy, Social & AdTech",
        "description": "Digital marketing trends, search marketing (SEO/SEM), platform updates, newsletters, and consumer behavior.",
        "badge_color": "#0D9488"  # Teal
    }
}

NEWS_SOURCES = [
    # --- 1. Advertising & Creative Campaigns ---
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
        "name": "The Drum",
        "url": "https://news.google.com/rss/search?q=site:thedrum.com&hl=en-US&gl=US&ceid=US:en",
        "category": "ADVERTISING",
        "priority": 1
    },
    {
        "name": "Ads of the World",
        "url": "https://news.google.com/rss/search?q=site:adsoftheworld.com&hl=en-US&gl=US&ceid=US:en",
        "category": "ADVERTISING",
        "priority": 1
    },

    # --- 2. Branding & Visual Identity ---
    {
        "name": "Brand New (UnderConsideration)",
        "url": "https://www.underconsideration.com/brandnew/atom.xml",
        "category": "BRANDING",
        "priority": 1
    },
    {
        "name": "BP&O (Branding, Packaging & Opinion)",
        "url": "https://bpando.org/feed/",
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
        "name": "Marketing Examples",
        "url": "https://news.google.com/rss/search?q=site:marketingexamples.com&hl=en-US&gl=US&ceid=US:en",
        "category": "BRANDING",
        "priority": 2
    },
    {
        "name": "Brand Identity & Rebrands Feed",
        "url": "https://news.google.com/rss/search?q=branding+rebrand+logo+identity+packaging&hl=en-US&gl=US&ceid=US:en",
        "category": "BRANDING",
        "priority": 2
    },

    # --- 3. Marketing Strategy, Newsletters & MarTech ---
    {
        "name": "Marketing Dive",
        "url": "https://www.marketingdive.com/feeds/news/",
        "category": "MARKETING_TECH",
        "priority": 1
    },
    {
        "name": "Marketing Brew",
        "url": "https://news.google.com/rss/search?q=%22Marketing+Brew%22&hl=en-US&gl=US&ceid=US:en",
        "category": "MARKETING_TECH",
        "priority": 1
    },
    {
        "name": "TLDR Marketing",
        "url": "https://tldr.tech/api/rss/marketing",
        "category": "MARKETING_TECH",
        "priority": 1
    },
    {
        "name": "Stacked Marketer",
        "url": "https://news.google.com/rss/search?q=site:stackedmarketer.com&hl=en-US&gl=US&ceid=US:en",
        "category": "MARKETING_TECH",
        "priority": 1
    },
    {
        "name": "Search Engine Land",
        "url": "https://news.google.com/rss/search?q=site:searchengineland.com&hl=en-US&gl=US&ceid=US:en",
        "category": "MARKETING_TECH",
        "priority": 1
    },
    {
        "name": "Digiday",
        "url": "https://digiday.com/feed/",
        "category": "MARKETING_TECH",
        "priority": 2
    },
    {
        "name": "Social Media Today",
        "url": "https://www.socialmediatoday.com/feeds/news/",
        "category": "MARKETING_TECH",
        "priority": 2
    }
]
