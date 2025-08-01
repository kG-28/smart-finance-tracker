CATEGORIES = {
    "coffee": "Food & Drink",
    "uber": "Transport",
    "zomato": "Food & Drink",
    "petrol": "Transport",
    "grocery": "Groceries",
    "electricity": "Utilities",
    "netflix": "Entertainment",
    "amazon": "Shopping",
    "medical": "Health",
    "gym": "Fitness",
    "rent": "Housing",
    "bus": "Transport",
    "train": "Transport",
    "phone": "Utilities",
    "clothes": "Shopping",
}

def categorize(description):
    for keyword, cat in CATEGORIES.items():
        if keyword in description.lower():
            return cat
    return "Uncategorized"
