"""
Personal Finance & Expense Manager
------------------------------------
A command-line application to track income and expenses, categorise
spending, and generate simple financial reports — built using only
core Python and the standard library (no external frameworks).

Author: Kamalishri J
"""

import json
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = "transactions.json"


class Transaction:
    """Represents a single financial transaction (income or expense)."""

    def __init__(self, txn_id, txn_type, category, amount, note, date=None):
        self.txn_id = txn_id
        self.txn_type = txn_type        # "income" or "expense"
        self.category = category
        self.amount = amount
        self.note = note
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        """Convert the transaction object into a dictionary for JSON storage."""
        return {
            "txn_id": self.txn_id,
            "type": self.txn_type,
            "category": self.category,
            "amount": self.amount,
            "note": self.note,
            "date": self.date,
        }

    @staticmethod
    def from_dict(data):
        """Recreate a Transaction object from a stored dictionary."""
        return Transaction(
            txn_id=data["txn_id"],
            txn_type=data["type"],
            category=data["category"],
            amount=data["amount"],
            note=data["note"],
            date=data["date"],
        )

    def __str__(self):
        sign = "+" if self.txn_type == "income" else "-"
        return (f"[{self.txn_id:>4}] {self.date}  "
                f"{self.txn_type.upper():<8} {self.category:<15} "
                f"{sign}₹{self.amount:>10,.2f}   {self.note}")


class ExpenseManager:
    """Core engine: handles storage, business logic, and reporting."""

    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.transactions = []
        self.next_id = 1
        self._load()

    # ---------- Persistence ----------

    def _load(self):
        """Load transactions from the JSON file if it exists."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    raw_data = json.load(f)
                self.transactions = [Transaction.from_dict(t) for t in raw_data]
                if self.transactions:
                    self.next_id = max(t.txn_id for t in self.transactions) + 1
            except (json.JSONDecodeError, KeyError):
                print("⚠️  Warning: data file was corrupted. Starting with a fresh ledger.")
                self.transactions = []

    def _save(self):
        """Persist all current transactions to the JSON file."""
        with open(self.data_file, "w") as f:
            json.dump([t.to_dict() for t in self.transactions], f, indent=2)

    # ---------- Core operations ----------

    def add_transaction(self, txn_type, category, amount, note):
        """Validate input and add a new transaction to the ledger."""
        if txn_type not in ("income", "expense"):
            raise ValueError("Transaction type must be 'income' or 'expense'.")
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")
        if not category.strip():
            raise ValueError("Category cannot be empty.")

        txn = Transaction(self.next_id, txn_type, category.strip().title(), amount, note.strip())
        self.transactions.append(txn)
        self.next_id += 1
        self._save()
        return txn

    def delete_transaction(self, txn_id):
        """Remove a transaction by its ID. Returns True if deleted."""
        original_len = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.txn_id != txn_id]
        deleted = len(self.transactions) < original_len
        if deleted:
            self._save()
        return deleted

    def get_all(self):
        """Return all transactions sorted by date (most recent first)."""
        return sorted(self.transactions, key=lambda t: (t.date, t.txn_id), reverse=True)

    def filter_by_type(self, txn_type):
        return [t for t in self.transactions if t.txn_type == txn_type]

    def filter_by_category(self, category):
        return [t for t in self.transactions if t.category.lower() == category.lower()]

    # ---------- Reporting ----------

    def total_income(self):
        return sum(t.amount for t in self.transactions if t.txn_type == "income")

    def total_expense(self):
        return sum(t.amount for t in self.transactions if t.txn_type == "expense")

    def balance(self):
        return self.total_income() - self.total_expense()

    def category_breakdown(self):
        """Returns a dict of {category: total_spent} for expenses only."""
        breakdown = defaultdict(float)
        for t in self.transactions:
            if t.txn_type == "expense":
                breakdown[t.category] += t.amount
        return dict(sorted(breakdown.items(), key=lambda x: x[1], reverse=True))

    def monthly_summary(self):
        """Returns a dict of {month: {'income': x, 'expense': y}}."""
        summary = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        for t in self.transactions:
            month = t.date[:7]  # YYYY-MM
            summary[month][t.txn_type] += t.amount
        return dict(sorted(summary.items()))

    def top_expense_category(self):
        """Returns the (category, total) with the highest spending, or None."""
        breakdown = self.category_breakdown()
        if not breakdown:
            return None
        top_cat = next(iter(breakdown))
        return top_cat, breakdown[top_cat]


# ============================================================
#  COMMAND-LINE INTERFACE
# ============================================================

def print_header(title):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)


def print_menu():
    print_header("PERSONAL FINANCE & EXPENSE MANAGER")
    print("""
  1. Add Income
  2. Add Expense
  3. View All Transactions
  4. View Transactions by Category
  5. Delete a Transaction
  6. View Summary Report
  7. View Category-wise Spending
  8. View Monthly Report
  9. Exit
""")


def get_positive_float(prompt):
    """Keep asking until the user enters a valid positive number."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= 0:
                print("  ❌ Amount must be greater than zero. Try again.")
                continue
            return value
        except ValueError:
            print("  ❌ Please enter a valid number (e.g. 1500 or 250.50).")


def handle_add(manager, txn_type):
    print_header(f"ADD {txn_type.upper()}")
    category = input("  Category (e.g. Food, Rent, Salary, Travel): ").strip()
    amount = get_positive_float("  Amount (₹): ")
    note = input("  Note (optional): ").strip()

    try:
        txn = manager.add_transaction(txn_type, category, amount, note)
        print(f"\n  ✅ Added successfully:\n  {txn}")
    except ValueError as e:
        print(f"\n  ❌ Error: {e}")


def handle_view_all(manager):
    print_header("ALL TRANSACTIONS")
    txns = manager.get_all()
    if not txns:
        print("  No transactions recorded yet.")
        return
    for t in txns:
        print(f"  {t}")
    print(f"\n  Total records: {len(txns)}")


def handle_view_by_category(manager):
    print_header("VIEW BY CATEGORY")
    category = input("  Enter category name: ").strip()
    results = manager.filter_by_category(category)
    if not results:
        print(f"  No transactions found for category '{category}'.")
        return
    for t in sorted(results, key=lambda x: x.date, reverse=True):
        print(f"  {t}")
    total = sum(t.amount for t in results)
    print(f"\n  Total for '{category.title()}': ₹{total:,.2f}")


def handle_delete(manager):
    print_header("DELETE TRANSACTION")
    handle_view_all(manager)
    raw_id = input("\n  Enter Transaction ID to delete (or 0 to cancel): ").strip()
    try:
        txn_id = int(raw_id)
        if txn_id == 0:
            print("  Cancelled.")
            return
        if manager.delete_transaction(txn_id):
            print(f"  ✅ Transaction #{txn_id} deleted.")
        else:
            print(f"  ❌ No transaction found with ID {txn_id}.")
    except ValueError:
        print("  ❌ Please enter a valid numeric ID.")


def handle_summary(manager):
    print_header("SUMMARY REPORT")
    income = manager.total_income()
    expense = manager.total_expense()
    balance = manager.balance()

    print(f"  Total Income   : ₹{income:,.2f}")
    print(f"  Total Expense  : ₹{expense:,.2f}")
    print(f"  {'-'*40}")
    status = "Surplus" if balance >= 0 else "Deficit"
    print(f"  Net Balance    : ₹{balance:,.2f}  ({status})")

    top = manager.top_expense_category()
    if top:
        print(f"\n  💡 Highest spending category: {top[0]} (₹{top[1]:,.2f})")


def handle_category_breakdown(manager):
    print_header("CATEGORY-WISE SPENDING")
    breakdown = manager.category_breakdown()
    if not breakdown:
        print("  No expense data available yet.")
        return

    total = sum(breakdown.values())
    for category, amount in breakdown.items():
        pct = (amount / total) * 100 if total else 0
        bar = "█" * int(pct // 4)
        print(f"  {category:<15} ₹{amount:>10,.2f}  ({pct:5.1f}%)  {bar}")
    print(f"\n  Total Expenses: ₹{total:,.2f}")


def handle_monthly_report(manager):
    print_header("MONTHLY REPORT")
    summary = manager.monthly_summary()
    if not summary:
        print("  No transactions recorded yet.")
        return

    print(f"  {'Month':<10}{'Income':>16}{'Expense':>16}{'Net':>16}")
    print(f"  {'-'*58}")
    for month, data in summary.items():
        net = data["income"] - data["expense"]
        income_str = f"₹{data['income']:,.2f}"
        expense_str = f"₹{data['expense']:,.2f}"
        net_str = f"₹{net:,.2f}"
        print(f"  {month:<10}{income_str:>16}{expense_str:>16}{net_str:>16}")


def main():
    manager = ExpenseManager()

    print("\n👋 Welcome to your Personal Finance Manager!")
    print(f"   Loaded {len(manager.transactions)} existing transaction(s) from disk.\n")

    while True:
        print_menu()
        choice = input("  Enter your choice (1-9): ").strip()

        if choice == "1":
            handle_add(manager, "income")
        elif choice == "2":
            handle_add(manager, "expense")
        elif choice == "3":
            handle_view_all(manager)
        elif choice == "4":
            handle_view_by_category(manager)
        elif choice == "5":
            handle_delete(manager)
        elif choice == "6":
            handle_summary(manager)
        elif choice == "7":
            handle_category_breakdown(manager)
        elif choice == "8":
            handle_monthly_report(manager)
        elif choice == "9":
            print("\n  👋 Thank you for using Personal Finance Manager. Goodbye!\n")
            break
        else:
            print("  ❌ Invalid choice. Please enter a number between 1 and 9.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()
