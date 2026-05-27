ALLOWED_CATEGORIES = [
    "еда",
    "транспорт",
    "здоровье",
    "развлечения",
    "зарплата",
    "фриланс",
    "инвестиции"
]


def validate_amount(amount):
    try:
        amount = float(amount)
        return amount > 0
    except:
        return False


def validate_category(category):
    return category.lower() in ALLOWED_CATEGORIES