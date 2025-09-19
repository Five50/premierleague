"""
Translation content for views.
This provides a simple way to manage multilingual content without a database.
"""

# Page translations
PAGE_CONTENT = {
    "home": {
        "sv": {
            "title": "Jämför lån, sparande och försäkringar",
            "subtitle": "Vi hjälper dig hitta de bästa finansiella produkterna",
            "description": "Oberoende jämförelser av lån, sparkonton, kreditkort och försäkringar från Sveriges största aktörer.",
        },
        "en": {
            "title": "Compare loans, savings and insurance",
            "subtitle": "We help you find the best financial products",
            "description": "Independent comparisons of loans, savings accounts, credit cards and insurance from Sweden's largest providers.",
        },
    },
    "savings": {
        "sv": {
            "title": "Bästa sparräntan 2025",
            "subtitle": "Jämför sparkonton och maximera din avkastning",
            "description": "Vi hjälper dig hitta det sparkonto med högst ränta. Jämför aktuella erbjudanden från Sveriges största banker.",
            "features": [
                "Jämför räntor från 20+ banker",
                "Uppdateras dagligen",
                "Helt kostnadsfritt",
                "Säker jämförelse",
            ],
        },
        "en": {
            "title": "Best Savings Rates 2025",
            "subtitle": "Compare savings accounts and maximize your returns",
            "description": "We help you find the savings account with the highest interest rate. Compare current offers from Sweden's largest banks.",
            "features": [
                "Compare rates from 20+ banks",
                "Updated daily",
                "Completely free",
                "Secure comparison",
            ],
        },
    },
    "loans": {
        "sv": {
            "title": "Jämför lån och hitta lägsta räntan",
            "subtitle": "Vi hjälper dig hitta rätt lån med bästa villkoren",
            "description": "Jämför erbjudanden från över 30 långivare. Få svar direkt och välj det lån som passar din ekonomi bäst.",
            "features": [
                "Jämför 30+ långivare",
                "Svar inom minuter",
                "Ingen UC-påverkan",
                "Personliga erbjudanden",
            ],
        },
        "en": {
            "title": "Compare loans and find the lowest rate",
            "subtitle": "We help you find the right loan with the best terms",
            "description": "Compare offers from over 30 lenders. Get instant answers and choose the loan that best suits your finances.",
            "features": [
                "Compare 30+ lenders",
                "Answer within minutes",
                "No credit impact",
                "Personal offers",
            ],
        },
    },
}

# Menu translations
MENU_TRANSLATIONS = {
    "sv": {
        "loans": "Lån",
        "savings": "Sparande",
        "credit_cards": "Kreditkort",
        "business_loans": "Företagslån",
        "blog": "Blogg",
        "about": "Om oss",
    },
    "en": {
        "loans": "Loans",
        "savings": "Savings",
        "credit_cards": "Credit Cards",
        "business_loans": "Business Loans",
        "blog": "Blog",
        "about": "About Us",
    },
}

# Common UI translations
UI_TRANSLATIONS = {
    "sv": {
        "compare_now": "Jämför nu",
        "apply_now": "Ansök nu",
        "read_more": "Läs mer",
        "learn_more": "Läs mer",
        "get_started": "Kom igång",
        "contact_us": "Kontakta oss",
        "back_to_top": "Till toppen",
    },
    "en": {
        "compare_now": "Compare now",
        "apply_now": "Apply now",
        "read_more": "Read more",
        "learn_more": "Learn more",
        "get_started": "Get started",
        "contact_us": "Contact us",
        "back_to_top": "Back to top",
    },
}
