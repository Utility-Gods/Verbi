class MenuData:
    BREAKFAST_MENU = {
        "name": "Breakfast Menu",
        "categories": {
            "Drinks": [
                {
                    "name": "Diet Coke",
                    "price": 150,
                    "currency": "ZAR",
                    "description": "Crisp, refreshing taste you know and love"
                },
                {
                    "name": "Lemon Soda",
                    "price": 150,
                    "currency": "ZAR",
                    "description": "Carbonated soft drink with lemon juice"
                }
            ],
            "Main Course": [
                {
                    "name": "Cheese Manakish",
                    "price": 200,
                    "currency": "ZAR",
                    "description": "Lebanese pizza with cheese"
                },
                {
                    "name": "Manakish",
                    "price": 300,
                    "currency": "ZAR",
                    "description": "Traditional Levantine dough with za'atar"
                },
                {
                    "name": "Falafel Platter Full",
                    "price": 350,
                    "currency": "ZAR",
                    "description": "Complete platter with falafel, bread, fries and sides"
                }
            ],
            "Salads": [
                {
                    "name": "Fattoush Salad",
                    "price": 300,
                    "description": "Fresh veggies with crispy pita and sumac dressing"
                },
                {
                    "name": "Fatteh",
                    "price": 250,
                    "description": "Layered dish with pita chips and tahini sauce"
                }
            ]
        }
    }

    LUNCH_MENU = {
        "name": "Lunch Menu",
        "categories": {
            "Coolers": [
                {
                    "name": "Mojito Cooler",
                    "price": 12000,
                    "description": "Refreshing summer mojito cooler"
                }
            ]
        }
    }

    @staticmethod
    def get_all_menu_items():
        """Returns a flat list of all menu items for easy searching"""
        all_items = []
        for menu in [MenuData.BREAKFAST_MENU, MenuData.LUNCH_MENU]:
            for category, items in menu["categories"].items():
                all_items.extend(items)
        return all_items

    @staticmethod
    def format_price(price):
        """Formats price in South African Rand"""
        return f"R{price:,.0f}"
