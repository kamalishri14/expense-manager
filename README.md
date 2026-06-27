# 💰 Personal Finance & Expense Manager

A command-line application to track income and expenses, categorise spending, and generate financial reports — built using **pure Python** and the standard library only (no external frameworks, no database server required).

---

## 📸 Features

- ➕ **Add income and expenses** with category, amount, and notes
- 🛡️ **Input validation** — rejects negative amounts, empty categories, invalid transaction types
- 👀 **View all transactions** sorted by most recent first
- 🔍 **Filter transactions by category**
- 🗑️ **Delete transactions** by ID
- 📊 **Summary report** — total income, total expense, net balance, top spending category
- 📈 **Category-wise spending breakdown** with visual bar chart (in terminal)
- 📅 **Monthly report** — income vs expense vs net, grouped by month
- 💾 **Persistent storage** — all data saved automatically to a local JSON file
- ✅ **17 unit tests** covering core logic, validation, and persistence

---

## 🛠️ Tech Stack

| Component       | Technology                          |
|------------------|--------------------------------------|
| Language         | Python 3 (no external libraries)     |
| Data Storage     | JSON file (`transactions.json`)      |
| Testing          | Python's built-in `unittest` module  |
| Design Pattern   | Object-Oriented Programming (OOP)    |

---

## 📂 Project Structure

```
expense-manager/
├── expense_manager.py        # Main application (Transaction, ExpenseManager classes, CLI)
├── test_expense_manager.py   # Unit test suite (17 tests)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/expense-manager.git
cd expense-manager
```

### 2. Run the application
No installation needed — uses only Python's standard library.

```bash
python expense_manager.py
```

### 3. Run the test suite
```bash
python -m unittest test_expense_manager.py -v
```

Expected output: `Ran 17 tests ... OK`

---

## 🖥️ Sample Usage

```
============================================
  PERSONAL FINANCE & EXPENSE MANAGER
============================================

  1. Add Income
  2. Add Expense
  3. View All Transactions
  4. View Transactions by Category
  5. Delete a Transaction
  6. View Summary Report
  7. View Category-wise Spending
  8. View Monthly Report
  9. Exit

  Enter your choice (1-9): 6

============================================
  SUMMARY REPORT
============================================
  Total Income   : ₹50,000.00
  Total Expense  : ₹15,500.00
  ----------------------------------------
  Net Balance    : ₹34,500.00  (Surplus)

  💡 Highest spending category: Rent (₹12,000.00)
```

---

## 🎯 Key Concepts Demonstrated

- **Object-Oriented Programming** — `Transaction` and `ExpenseManager` classes with clear separation of concerns
- **File I/O & data persistence** — reading/writing JSON to disk, surviving program restarts
- **Error handling** — custom validation with `try/except` and `ValueError`
- **Data structures** — use of `defaultdict` for category and monthly aggregation
- **Static & instance methods** — `to_dict()` / `from_dict()` for serialization
- **Unit testing** — `unittest` framework with `setUp`/`tearDown` for isolated test runs
- **Clean CLI design** — input validation loops, formatted tabular output, ASCII bar charts
- **List comprehensions & sorting** — filtering and sorting transactions efficiently

---

## 🔮 Possible Future Enhancements

- Export reports to CSV or PDF
- Add a budget-limit warning system per category
- Switch storage from JSON to SQLite for larger datasets
- Add a simple `matplotlib` chart for visual spending trends

---

## 👤 Author

**Kamalishri J**
📧 kamalibassu@gmail.com
🔗 [linkedin.com/in/kamalishri-j](https://linkedin.com/in/kamalishri-j)
🔗 [github.com/kamalishri14](https://github.com/kamalishri14)

---

## 📄 License

This project is open source and available for learning purposes.
