import matplotlib.pyplot as plt


def create_expense_chart(categories):

    labels = list(categories.keys())
    values = list(categories.values())

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%')

    path = "charts/expenses.png"

    plt.savefig(path)
    plt.close()

    return path