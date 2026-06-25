INCOME_CATEGORIES = [
    "зарплата",
    "фриланс",
    "инвестиции",
    "бизнес",
    "другое"
]

EXPENSE_CATEGORIES = [
    "еда",
    "транспорт",
    "здоровье",
    "развлечения",
    "другое"
]


def validate_amount(amount):

    try:
        amount = float(amount.strip())

    except ValueError:
        return False, "❌ Введите число."

    if amount <= 0:
        return False, "❌ Сумма должна быть больше 0."

    if amount > 1_000_000:
        return False, "❌ Слишком большая сумма."

    return True, amount


def validate_category(category, transaction_type):

    category = category.strip().lower()

    if not category:
        return False, "❌ Категория не может быть пустой."

    categories = (
        INCOME_CATEGORIES
        if transaction_type == "income"
        else EXPENSE_CATEGORIES
    )

    if category not in categories:

        allowed = "\n• " + "\n• ".join(categories)

        return (
            False,
            f"❌ Разрешены только:{allowed}"
        )

    return True, category