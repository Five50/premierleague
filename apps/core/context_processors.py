from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


def site_context(request):
    """Add site-wide context variables."""
    current_language = get_language()

    # Define navigation items with proper structure
    # Using # for all URLs that don't have corresponding views yet
    personal_loan_items = [
        {
            "text": _("Borrow Money"),
            "href": "#",
            "has_submenu": True,
            "submenu": [
                {"text": _("Borrow Money Quickly"), "href": "#"},
            ],
        },
        {
            "text": _("Car Loan"),
            "href": "#",
            "has_submenu": True,
            "submenu": [
                {"text": _("Car Loans for Students"), "href": "#"},
                {"text": _("Environment Car Loan"), "href": "#"},
                {"text": _("Car Loan with Payment Notice"), "href": "#"},
            ],
        },
        {"text": _("Unsecured Loan"), "href": "#"},
        {
            "text": _("Quick Loan"),
            "href": "#",
            "has_submenu": True,
            "submenu": [
                {"text": _("SMS Loan"), "href": "#"},
                {"text": _("Microloans"), "href": "#"},
                {"text": _("Small Loans"), "href": "#"},
            ],
        },
        {"text": _("Debt Financing"), "href": "#"},
        {
            "text": _("Credit Loan"),
            "href": "#",
            "has_submenu": True,
            "submenu": [
                {"text": _("Account Credit"), "href": "#"},
            ],
        },
        {"text": _("Loans for Specific Situations"), "href": "#"},
        {"text": _("Loan Broker"), "href": "#"},
        {
            "text": _("Other Loans"),
            "href": "#",
            "has_submenu": True,
            "submenu": [
                {"text": _("New Loans"), "href": "#"},
                {"text": _("Student Loans"), "href": "#"},
                {
                    "text": _("Energy Loan"),
                    "href": "#",
                    "has_submenu": True,
                    "submenu": [
                        {"text": _("Loan for Replacement Window"), "href": "#"},
                        {"text": _("Solar Cell Loan"), "href": "#"},
                        {"text": _("Loans for Geothermal Heating"), "href": "#"},
                    ],
                },
                {"text": _("Loan Forms"), "href": "#"},
                {"text": _("Emergency Loan"), "href": "#"},
            ],
        },
    ]

    corporate_loan_items = [
        {"text": _("Corporate Credit"), "href": "#"},
        {
            "text": _("Start-up Loan"),
            "href": "#",
            "has_submenu": True,
            "submenu": [
                {"text": _("Start-your-own Loan"), "href": "#"},
                {"text": _("Business Loans for Start-up Companies"), "href": "#"},
            ],
        },
        {"text": _("Group Loans for Companies"), "href": "#"},
        {"text": _("Loan Broker for Business Loans"), "href": "#"},
        {"text": _("Loans for Different Company Types"), "href": "#"},
        {"text": _("Other Corporate Loans"), "href": "#"},
    ]

    credit_card_items = [
        {
            "text": _("Gas Card"),
            "href": (
                f"/{current_language}/credit-cards/gas/"
                if current_language == "en"
                else "/kreditkort/bensin/"
            ),
        },
        {
            "text": _("Food Card"),
            "href": (
                f"/{current_language}/credit-cards/food/"
                if current_language == "en"
                else "/kreditkort/mat/"
            ),
        },
        {
            "text": _("Travel Card"),
            "href": (
                f"/{current_language}/credit-cards/travel/"
                if current_language == "en"
                else "/kreditkort/resa/"
            ),
        },
        {
            "text": _("Credit Card"),
            "href": (
                f"/{current_language}/credit-cards/standard/"
                if current_language == "en"
                else "/kreditkort/standard/"
            ),
            "has_submenu": True,
            "submenu": [
                {
                    "text": _("Credit Cards Without Annual Fee"),
                    "href": (
                        f"/{current_language}/credit-cards/no-annual-fee/"
                        if current_language == "en"
                        else "/kreditkort/utan-arsavgift/"
                    ),
                },
            ],
        },
        {
            "text": _("Cashback Credit Cards"),
            "href": (
                f"/{current_language}/credit-cards/cashback/"
                if current_language == "en"
                else "/kreditkort/cashback/"
            ),
        },
        {
            "text": _("Cheap Credit Cards"),
            "href": (
                f"/{current_language}/credit-cards/cheap/"
                if current_language == "en"
                else "/kreditkort/billiga/"
            ),
            "has_submenu": True,
            "submenu": [
                {
                    "text": _("Credit Card Without Annual Fee"),
                    "href": (
                        f"/{current_language}/credit-cards/cheap/no-annual-fee/"
                        if current_language == "en"
                        else "/kreditkort/billiga/ingen-arsavgift/"
                    ),
                },
                {
                    "text": _("Credit Card Without Withdrawal Fee"),
                    "href": (
                        f"/{current_language}/credit-cards/cheap/no-withdrawal-fee/"
                        if current_language == "en"
                        else "/kreditkort/billiga/ingen-uttagsavgift/"
                    ),
                },
                {
                    "text": _("Credit Cards Without Currency Surcharges"),
                    "href": (
                        f"/{current_language}/credit-cards/cheap/no-currency-fee/"
                        if current_language == "en"
                        else "/kreditkort/billiga/ingen-valutapaslag/"
                    ),
                },
            ],
        },
        {
            "text": _("Business Card"),
            "href": (
                f"/{current_language}/credit-cards/business/"
                if current_language == "en"
                else "/kreditkort/foretag/"
            ),
        },
        {
            "text": _("Digital Credit Cards"),
            "href": (
                f"/{current_language}/credit-cards/digital/"
                if current_language == "en"
                else "/kreditkort/digitala/"
            ),
        },
    ]

    save_money_items = [
        # This one exists - link to the real savings best rate page
        {
            "text": _("Best Savings Interest Rate Right Now"),
            "href": (
                f"/{current_language}/savings/best-interest-rate/"
                if current_language == "en"
                else "/spara/basta-rantan-just-nu/"
            ),
        },
        {
            "text": _("Savings Accounts"),
            "href": "#",
            "has_submenu": True,
            "submenu": [
                {"text": _("Children's Savings Accounts"), "href": "#"},
                {"text": _("Buffer Savings Account"), "href": "#"},
                {"text": _("Fixed Interest Account"), "href": "#"},
                {
                    "text": _("High-Interest Account"),
                    "href": "#",
                    "has_submenu": True,
                    "submenu": [
                        {"text": _("High Interest Savings Account"), "href": "#"},
                    ],
                },
            ],
        },
        {"text": _("Savings Apps"), "href": "#"},
    ]

    # Legacy items for backward compatibility
    if current_language == "en":
        loan_items = [
            {"text": _("Personal Loans"), "href": "/en/loans/"},
            {"text": _("Business Loans"), "href": "/en/business-loans/unsecured/"},
            {"text": _("Car Loans"), "href": "/en/loans/"},
            {"text": _("Debt Consolidation"), "href": "/en/loans/"},
        ]
        savings_items = [
            {"text": _("Savings Account"), "href": "/en/savings/best-interest-rate/"},
            {"text": _("ISK"), "href": "#"},
            {"text": _("Robo-Advisor"), "href": "#"},
            {"text": _("Stocks"), "href": "#"},
        ]
    else:
        loan_items = [
            {"text": "Privatlån", "href": "/lan/"},
            {"text": "Företagslån", "href": "/foretagslan/utan-sakerhet/"},
            {"text": "Billån", "href": "/lan/"},
            {"text": "Samlingslån", "href": "/lan/"},
        ]
        savings_items = [
            {"text": "Sparkonto", "href": "/spara/basta-rantan-just-nu/"},
            {"text": "ISK", "href": "#"},
            {"text": "Fondrobot", "href": "#"},
            {"text": "Aktier", "href": "#"},
        ]

    # Sample blog posts data - 12 posts per section
    popular_posts = [
        {
            "title": _("Can You Get a Loan When Everyone Says No?"),
            "url": "#",
            "image_name": "kan-man-fa-lan-nar-alla-sager-nej",
            "author": "Jenny Magnusson",
            "author_url": "#",
            "date": _("July 30, 2025") if current_language == "en" else "juli 30, 2025",
            "date_iso": "2025-07-30",
        },
        {
            "title": _("Difficult to Get a Loan: Here's How You Can Still Borrow"),
            "url": "#",
            "image_name": "svart-att-fa-lan",
            "author": "Jenny Magnusson",
            "author_url": "#",
            "date": _("July 30, 2025") if current_language == "en" else "juli 30, 2025",
            "date_iso": "2025-07-30",
        },
        {
            "title": _("Which Car Insurance Do I Have?"),
            "url": "#",
            "image_name": "vilken-bilforsakring-har-jag",
            "author": "Anna Rask",
            "author_url": "#",
            "date": (
                _("August 28, 2024") if current_language == "en" else "augusti 28, 2024"
            ),
            "date_iso": "2024-08-28",
        },
        {
            "title": _("Which Home Insurance Do I Have?"),
            "url": "#",
            "image_name": "vilken-hemforsakring-har-jag",
            "author": "Anna Rask",
            "author_url": "#",
            "date": (
                _("November 29, 2024")
                if current_language == "en"
                else "november 29, 2024"
            ),
            "date_iso": "2024-11-29",
        },
        {
            "title": _("Save Money in Everyday Life"),
            "url": "#",
            "image_name": "spara-pengar-i-vardagen",
            "author": "Anna Rask",
            "author_url": "#",
            "date": (
                _("January 11, 2025")
                if current_language == "en"
                else "januari 11, 2025"
            ),
            "date_iso": "2025-01-11",
        },
        {
            "title": _("How to Create, Buy and Sell NFT [Crypto]?"),
            "url": "#",
            "image_name": "hur-skapar-koper-och-saljer-man-nfts",
            "author": "Bob Vargas",
            "author_url": "#",
            "date": (
                _("February 23, 2025")
                if current_language == "en"
                else "februari 23, 2025"
            ),
            "date_iso": "2025-02-23",
        },
        {
            "title": _("How Does Tax on Cryptocurrencies Work?"),
            "url": "#",
            "image_name": "behover-man-betala-skatt-pa-kryptovalutor",
            "author": "Bob Vargas",
            "author_url": "#",
            "date": _("May 19, 2025") if current_language == "en" else "maj 19, 2025",
            "date_iso": "2025-05-19",
        },
        {
            "title": _("Which Cryptocurrency is Best 2025?"),
            "url": "#",
            "image_name": "vilken-kryptovaluta-ar-bast",
            "author": "Bob Vargas",
            "author_url": "#",
            "date": (
                _("April 26, 2025") if current_language == "en" else "april 26, 2025"
            ),
            "date_iso": "2025-04-26",
        },
        {
            "title": _("What Uses the Most Electricity at Home?"),
            "url": "#",
            "image_name": "vad-drar-mest-el-i-hemmet",
            "author": "Anna Rask",
            "author_url": "#",
            "date": (
                _("November 29, 2024")
                if current_language == "en"
                else "november 29, 2024"
            ),
            "date_iso": "2024-11-29",
        },
        {
            "title": _("Which Electricity Company Do I Have?"),
            "url": "#",
            "image_name": "vilket-elbolag-har-jag",
            "author": "Jenny Magnusson",
            "author_url": "#",
            "date": (
                _("November 6, 2024")
                if current_language == "en"
                else "november 6, 2024"
            ),
            "date_iso": "2024-11-06",
        },
        {
            "title": _("What is KALP and How Do You Calculate It?"),
            "url": "#",
            "image_name": "kalp-kvar-att-leva-pa",
            "author": "Anna Rask",
            "author_url": "#",
            "date": _("May 11, 2025") if current_language == "en" else "maj 11, 2025",
            "date_iso": "2025-05-11",
        },
        {
            "title": _("Important Considerations Before Taking an SMS Loan"),
            "url": "#",
            "image_name": "viktiga-overvaganden-innan-du-tar-ett-sms-lan",
            "author": "Johan Karlsson",
            "author_url": "#",
            "date": _("May 11, 2025") if current_language == "en" else "maj 11, 2025",
            "date_iso": "2025-05-11",
        },
    ]

    latest_posts = [
        {
            "title": _("Save Money in Everyday Life"),
            "url": "#",
            "image_name": "spara-pengar-i-vardagen",
            "author": "Anna Rask",
            "author_url": "#",
            "date": (
                _("January 11, 2025")
                if current_language == "en"
                else "januari 11, 2025"
            ),
            "date_iso": "2025-01-11",
        },
        {
            "title": _("How to Identify a Crypto Scam"),
            "url": "#",
            "image_name": "krypto-scam",
            "author": "Bob Vargas",
            "author_url": "#",
            "date": (
                _("August 29, 2024") if current_language == "en" else "augusti 29, 2024"
            ),
            "date_iso": "2024-08-29",
        },
        {
            "title": _("Save for Wedding - 11 Steps to Get Started"),
            "url": "#",
            "image_name": "spara-till-brollop",
            "author": "Anna Rask",
            "author_url": "#",
            "date": _("May 11, 2025") if current_language == "en" else "maj 11, 2025",
            "date_iso": "2025-05-11",
        },
        {
            "title": _("7 Ways Renovation Can Increase Your Property Value"),
            "url": "#",
            "image_name": "7-tips-nar-du-renoverar",
            "author": "Anna Rask",
            "author_url": "#",
            "date": (
                _("April 18, 2025") if current_language == "en" else "april 18, 2025"
            ),
            "date_iso": "2025-04-18",
        },
        {
            "title": _("What is a Debt Trap?"),
            "url": "#",
            "image_name": "vad-ar-skuldfalla",
            "author": "Anna Rask",
            "author_url": "#",
            "date": _("May 11, 2025") if current_language == "en" else "maj 11, 2025",
            "date_iso": "2025-05-11",
        },
        {
            "title": _("What is the Snowball Method for Debt Financing?"),
            "url": "#",
            "image_name": "snobollsmetoden",
            "author": "Johan Karlsson",
            "author_url": "#",
            "date": _("May 11, 2025") if current_language == "en" else "maj 11, 2025",
            "date_iso": "2025-05-11",
        },
        {
            "title": _("Which Savings Form is Best?"),
            "url": "#",
            "image_name": "vilken-sparform-ar-bast",
            "author": "Anna Rask",
            "author_url": "#",
            "date": _("July 8, 2025") if current_language == "en" else "juli 8, 2025",
            "date_iso": "2025-07-08",
        },
        {
            "title": _("Important Considerations Before Taking an SMS Loan"),
            "url": "#",
            "image_name": "viktiga-overvaganden-innan-du-tar-ett-sms-lan",
            "author": "Johan Karlsson",
            "author_url": "#",
            "date": _("May 11, 2025") if current_language == "en" else "maj 11, 2025",
            "date_iso": "2025-05-11",
        },
        {
            "title": _("What is MiCA (Markets in Crypto-Assets)?"),
            "url": "#",
            "image_name": "vad-ar-mica",
            "author": "Bob Vargas",
            "author_url": "#",
            "date": _("July 26, 2024") if current_language == "en" else "juli 26, 2024",
            "date_iso": "2024-07-26",
        },
        {
            "title": _("Which Cryptocurrency is Best 2025?"),
            "url": "#",
            "image_name": "vilken-kryptovaluta-ar-bast",
            "author": "Bob Vargas",
            "author_url": "#",
            "date": (
                _("April 26, 2025") if current_language == "en" else "april 26, 2025"
            ),
            "date_iso": "2025-04-26",
        },
        {
            "title": _("What Uses the Most Electricity at Home?"),
            "url": "#",
            "image_name": "vad-drar-mest-el-i-hemmet",
            "author": "Anna Rask",
            "author_url": "#",
            "date": (
                _("November 29, 2024")
                if current_language == "en"
                else "november 29, 2024"
            ),
            "date_iso": "2024-11-29",
        },
        {
            "title": _("How Does Tax on Cryptocurrencies Work?"),
            "url": "#",
            "image_name": "behover-man-betala-skatt-pa-kryptovalutor",
            "author": "Bob Vargas",
            "author_url": "#",
            "date": _("May 19, 2025") if current_language == "en" else "maj 19, 2025",
            "date_iso": "2025-05-19",
        },
    ]

    return {
        "site_name": "PayUp",
        "debug": settings.DEBUG,
        "lang": current_language,
        "current_language": current_language,
        "personal_loan_items": personal_loan_items,
        "corporate_loan_items": corporate_loan_items,
        "credit_card_items": credit_card_items,
        "save_money_items": save_money_items,
        "loan_items": loan_items,
        "savings_items": savings_items,
        "popular_posts": popular_posts,
        "latest_posts": latest_posts,
        "default_lenders": [
            {
                "name": "Nordea",
                "initials": "N",
                "rating": 4,
                "reviews": "1,234",
                "rate": "4.95",
                "monthly": "1,886",
                "max_amount": "600k",
                "response_time": "2 min",
                "apply_url": "#",
                "details_url": "#",
            },
            {
                "name": "Swedbank",
                "initials": "S",
                "rating": 5,
                "reviews": "2,156",
                "rate": "5.25",
                "monthly": "1,925",
                "max_amount": "500k",
                "response_time": "5 min",
                "apply_url": "#",
                "details_url": "#",
            },
            {
                "name": "Santander",
                "initials": "S",
                "rating": 4,
                "reviews": "987",
                "rate": "4.75",
                "monthly": "1,862",
                "max_amount": "750k",
                "response_time": "1 min",
                "apply_url": "#",
                "details_url": "#",
            },
        ],
        # Popular Loans Tab Data
        "popular_loans": [
            {
                "name": "Creditstar",
                "type": _("Quick loan"),
                "rate": "20.00",
                "selected_count": 199,
                "url": "#",
            },
            {
                "name": "Northmill",
                "type": _("Personal loan"),
                "rate": "6.95",
                "selected_count": 342,
                "url": "#",
            },
            {
                "name": "Lendo",
                "type": _("Consolidation loan"),
                "rate": "4.90",
                "selected_count": 287,
                "url": "#",
            },
            {
                "name": "Santander",
                "type": _("Bank loan"),
                "rate": "5.45",
                "selected_count": 156,
                "url": "#",
            },
        ],
        "popular_corporate_loans": [
            {
                "name": "Qred",
                "type": _("Business loan"),
                "rate": "8.90",
                "selected_count": 89,
                "url": "#",
            },
            {
                "name": "Froda",
                "type": _("Growth capital"),
                "rate": "7.50",
                "selected_count": 124,
                "url": "#",
            },
            {
                "name": "Capcito",
                "type": _("Invoice financing"),
                "rate": "6.20",
                "selected_count": 76,
                "url": "#",
            },
            {
                "name": "Wayler",
                "type": _("Equipment loan"),
                "rate": "9.95",
                "selected_count": 45,
                "url": "#",
            },
        ],
        "popular_credit_cards": [
            {
                "name": "Norwegian",
                "type": _("Travel card"),
                "feature": _("1% Cashback"),
                "selected_count": 523,
                "url": "#",
            },
            {
                "name": "Coop",
                "type": _("Shopping card"),
                "feature": _("0 kr fee"),
                "selected_count": 412,
                "url": "#",
            },
            {
                "name": "SEB",
                "type": _("Premium card"),
                "feature": _("2% Points"),
                "selected_count": 234,
                "url": "#",
            },
            {
                "name": "ICA",
                "type": _("Grocery card"),
                "feature": _("5% Bonus"),
                "selected_count": 189,
                "url": "#",
            },
        ],
        "popular_savings_accounts": [
            {
                "name": "Klarna",
                "type": _("Flexible savings"),
                "rate": "5.25",
                "selected_count": 892,
                "url": "#",
            },
            {
                "name": "Collector",
                "type": _("Fixed savings"),
                "rate": "4.95",
                "selected_count": 654,
                "url": "#",
            },
            {
                "name": "Avanza",
                "type": _("Investment savings"),
                "rate": "4.85",
                "selected_count": 445,
                "url": "#",
            },
            {
                "name": "SBAB",
                "type": _("Goal savings"),
                "rate": "4.75",
                "selected_count": 321,
                "url": "#",
            },
        ],
        # Current Interest Rates Data
        "top_interest_rates": [
            {
                "name": "Coop MedMera",
                "rate": "4.20",
                "type": _("Personal Loan"),
            },
            {
                "name": "Santander",
                "rate": "4.45",
                "type": _("Personal Loan"),
            },
            {
                "name": "Lendo",
                "rate": "4.90",
                "type": _("Personal Loan"),
            },
            {
                "name": "Multitude Bank",
                "rate": "3.00",
                "type": _("Savings Account"),
            },
            {
                "name": "Klarna",
                "rate": "2.85",
                "type": _("Savings Account"),
            },
        ],
        "loan_rate_changes": [
            {
                "lender": "Avida",
                "previous_rate": "9.22–21.22%",
                "new_rate": "6.29–21.22%",
                "change": "-2.93% " + str(_("points")),
                "is_decrease": True,
                "date": "2025-07-30",
                "url": "#",
            },
            {
                "lender": "Equilo",
                "previous_rate": "17.27%",
                "new_rate": "16.90–19.47%",
                "change": "+2.20% " + str(_("points")),
                "is_decrease": False,
                "date": "2025-08-02",
                "url": "#",
            },
            {
                "lender": "ViaConto",
                "previous_rate": "23.00%",
                "new_rate": "22.00%",
                "change": "-1.00% " + str(_("points")),
                "is_decrease": True,
                "date": "2025-07-22",
                "url": "#",
            },
        ],
        "savings_rate_changes": [
            {
                "bank": "Swedbank",
                "binding_time": _("2 years"),
                "previous_rate": "1.62%",
                "new_rate": "1.56%",
                "change": "-0.06% " + str(_("points")),
                "date": "2025-08-05",
            },
            {
                "bank": "Swedbank",
                "binding_time": _("3 years"),
                "previous_rate": "1.72%",
                "new_rate": "1.65%",
                "change": "-0.07% " + str(_("points")),
                "date": "2025-08-05",
            },
            {
                "bank": "Swedbank",
                "binding_time": _("4 years"),
                "previous_rate": "1.81%",
                "new_rate": "1.74%",
                "change": "-0.07% " + str(_("points")),
                "date": "2025-08-05",
            },
            {
                "bank": "Swedbank",
                "binding_time": _("5 years"),
                "previous_rate": "1.90%",
                "new_rate": "1.82%",
                "change": "-0.08% " + str(_("points")),
                "date": "2025-08-05",
            },
            {
                "bank": "Handelsbanken",
                "binding_time": _("1 year"),
                "previous_rate": "1.66%",
                "new_rate": "1.61%",
                "change": "-0.05% " + str(_("points")),
                "date": "2025-08-05",
            },
            {
                "bank": "Handelsbanken",
                "binding_time": _("2 years"),
                "previous_rate": "1.82%",
                "new_rate": "1.71%",
                "change": "-0.11% " + str(_("points")),
                "date": "2025-08-05",
            },
            {
                "bank": "Handelsbanken",
                "binding_time": _("3 years"),
                "previous_rate": "1.98%",
                "new_rate": "1.87%",
                "change": "-0.11% " + str(_("points")),
                "date": "2025-08-05",
            },
            {
                "bank": "Handelsbanken",
                "binding_time": _("5 years"),
                "previous_rate": "2.28%",
                "new_rate": "2.15%",
                "change": "-0.13% " + str(_("points")),
                "date": "2025-08-05",
            },
        ],
    }
