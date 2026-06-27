"""
Unit tests for the Personal Finance & Expense Manager.

Run with:
    python -m unittest test_expense_manager.py -v
"""

import unittest
import os
from expense_manager import ExpenseManager, Transaction

TEST_FILE = "test_transactions.json"


class TestTransaction(unittest.TestCase):

    def test_to_dict_and_back(self):
        txn = Transaction(1, "expense", "Food", 250.50, "Lunch", "2026-06-01")
        data = txn.to_dict()
        rebuilt = Transaction.from_dict(data)
        self.assertEqual(rebuilt.txn_id, 1)
        self.assertEqual(rebuilt.category, "Food")
        self.assertEqual(rebuilt.amount, 250.50)

    def test_string_representation(self):
        txn = Transaction(1, "income", "Salary", 50000, "June pay", "2026-06-01")
        text = str(txn)
        self.assertIn("INCOME", text)
        self.assertIn("Salary", text)


class TestExpenseManager(unittest.TestCase):

    def setUp(self):
        """Runs before every test — start with a clean ledger."""
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)
        self.manager = ExpenseManager(data_file=TEST_FILE)

    def tearDown(self):
        """Runs after every test — clean up the test file."""
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_add_income(self):
        txn = self.manager.add_transaction("income", "Salary", 50000, "June pay")
        self.assertEqual(txn.txn_id, 1)
        self.assertEqual(self.manager.total_income(), 50000)

    def test_add_expense(self):
        self.manager.add_transaction("expense", "Food", 1500, "Groceries")
        self.assertEqual(self.manager.total_expense(), 1500)

    def test_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction("expense", "Food", -100, "Invalid")

    def test_rejects_zero_amount(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction("expense", "Food", 0, "Invalid")

    def test_rejects_invalid_type(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction("savings", "Bank", 1000, "Invalid type")

    def test_rejects_empty_category(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction("expense", "   ", 100, "Invalid")

    def test_balance_calculation(self):
        self.manager.add_transaction("income", "Salary", 50000, "")
        self.manager.add_transaction("expense", "Rent", 12000, "")
        self.manager.add_transaction("expense", "Food", 3000, "")
        self.assertEqual(self.manager.balance(), 35000)

    def test_category_breakdown(self):
        self.manager.add_transaction("expense", "Food", 1000, "")
        self.manager.add_transaction("expense", "Food", 500, "")
        self.manager.add_transaction("expense", "Rent", 8000, "")
        breakdown = self.manager.category_breakdown()
        self.assertEqual(breakdown["Food"], 1500)
        self.assertEqual(breakdown["Rent"], 8000)

    def test_top_expense_category(self):
        self.manager.add_transaction("expense", "Food", 1000, "")
        self.manager.add_transaction("expense", "Rent", 8000, "")
        top = self.manager.top_expense_category()
        self.assertEqual(top[0], "Rent")
        self.assertEqual(top[1], 8000)

    def test_delete_transaction(self):
        txn = self.manager.add_transaction("expense", "Food", 500, "")
        deleted = self.manager.delete_transaction(txn.txn_id)
        self.assertTrue(deleted)
        self.assertEqual(len(self.manager.transactions), 0)

    def test_delete_nonexistent_transaction(self):
        deleted = self.manager.delete_transaction(999)
        self.assertFalse(deleted)

    def test_filter_by_category_case_insensitive(self):
        self.manager.add_transaction("expense", "Food", 500, "")
        results = self.manager.filter_by_category("food")
        self.assertEqual(len(results), 1)

    def test_persistence_across_instances(self):
        self.manager.add_transaction("income", "Salary", 30000, "")
        self.manager.add_transaction("expense", "Food", 2000, "")

        # Create a new manager instance pointing to the same file
        reloaded = ExpenseManager(data_file=TEST_FILE)
        self.assertEqual(len(reloaded.transactions), 2)
        self.assertEqual(reloaded.total_income(), 30000)

    def test_next_id_increments_correctly(self):
        t1 = self.manager.add_transaction("income", "Salary", 1000, "")
        t2 = self.manager.add_transaction("income", "Bonus", 500, "")
        self.assertEqual(t1.txn_id, 1)
        self.assertEqual(t2.txn_id, 2)

    def test_monthly_summary_structure(self):
        self.manager.add_transaction("income", "Salary", 50000, "")
        self.manager.add_transaction("expense", "Rent", 10000, "")
        summary = self.manager.monthly_summary()
        self.assertEqual(len(summary), 1)
        month_key = list(summary.keys())[0]
        self.assertIn("income", summary[month_key])
        self.assertIn("expense", summary[month_key])


if __name__ == "__main__":
    unittest.main(verbosity=2)
