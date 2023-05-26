from typing import List


class Category:
    def __init__(self, name: str):
        self.name = name
        self.ledger: List[dict] = []

    def deposit(self, amount: float, description: str = "") -> None:
        self.ledger.append(dict(amount=amount, description=description))

    def get_balance(self) -> float:
        return sum([x["amount"] for x in self.ledger])

    def check_funds(self, amount: float) -> bool:
        if (self.get_balance() - amount) < 0:
            return False
        return True

    def withdraw(self, amount: float, description: str = "") -> bool:
        if not self.check_funds(amount):
            return False
        self.ledger.append(dict(amount=0 - amount, description=description))
        return True

    def transfer(self, amount: float, to_budget: "Category") -> bool:
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {to_budget.name}")
        to_budget.deposit(amount, f"Transfer from {self.name}")
        return True

    def __str__(self) -> str:
        output = self.name.center(30, "*") + "\n"
        for items in self.ledger:
            amount, desc = items.values()
            amount = "{:.2f}".format(amount)
            output += desc[:23].ljust(30 - len(amount)) + amount + "\n"
        output += f"Total: {self.get_balance()}"
        return output


def truncate(n):
    return int(n + 10) / 10


def create_spend_chart(categories: List[Category]) -> str:
    total = 0
    breakdown = []
    for category in categories:
        total_withdrawal = sum(
            [x["amount"] for x in category.ledger if x["amount"] < 0]
        )
        total += total_withdrawal
        breakdown.append(total_withdrawal)
    rounded = list(map(lambda x: int(x / total * 10) / 10, breakdown))
    output = "Percentage spent by category"
    for number in range(100, -10, -10):
        line = "\n" + f"{number:3}|"
        for items in rounded:
            if items * 100 >= number:
                line += "o".center(3)
            else:
                line += " " * 3
        output += line + " "
    output += "\n    " + (("---" * len(rounded)) + "-")
    names = [x.name for x in categories]
    lengthy = len(max(names, key=len))
    names = [x.ljust(lengthy) for x in names]
    for pos in range(lengthy):
        output += "\n    "
        for name in names:
            output += name[pos].center(3)
        output += " "
    return output
