<h1 align="center">FAMILY EXPENSE TRACKER 🏦</h1>
<p align="center">
    <a href="https://github.com/SVijayB/PyHub"><img src="assets/logo-hacktober.svg" alt="Logo" border="0"></a><br>
    <a href="https://github.com/SVijayB/PyHub"><img src="assets/pyLogo.png" alt="Logo" border="0"></a>
</p>

<div align="center">

![https://github.com/sree-hari-s/Expense-Tracker/network/members](https://img.shields.io/github/forks/sree-hari-s/Expense-Tracker?color=green) &nbsp;
![https://github.com/sree-hari-s/Expense-Tracker/graphs/issues](https://img.shields.io/github/issues/sree-hari-s/Expense-Tracker)  &nbsp;
![https://github.com/sree-hari-s/Expense-Tracker/graphs/contributors](https://img.shields.io/github/contributors/sree-hari-s/Expense-Tracker) &nbsp;
![https://github.com/sree-hari-s/Expense-Tracker/stargazers](https://img.shields.io/github/stars/sree-hari-s/Expense-Tracker?color=red) &nbsp;
![https://github.com/sree-hari-s/Expense-Tracker/watchers](https://img.shields.io/github/watchers/sree-hari-s/Expense-Tracker?color=yellow) &nbsp;
![https://github.com/sree-hari-s/Expense-Tracker/license](https://img.shields.io/github/license/sree-hari-s/Expense-Tracker) &nbsp;
[![code style: black](https://img.shields.io/badge/code%20style-black-000.svg)](https://github.com/psf/black) &nbsp;
</div>

<div align="center">
Welcome to the Family Expense Tracker - a simple Python project designed to help you keep track of your family members' earnings and expenses. This tool allows you to effortlessly manage family finances by adding members, recording their earnings, and calculating the remaining balance after deducting expenses.
</div>

## Table of Contents

- 📑[Table of Contents](#table-of-contents)
- 🧾[Introduction](#introduction)
- ✨[Features](#features)
- 🛠️[How to Use](#how-to-use)
- ⚙️[Installation](#installation)
- 🙌[How to Contribute](#how-to-contribute)
- 📝[License](#license)

## Introduction

Managing a family's finances can be challenging, especially when dealing with multiple sources of income and various expenses. The Family Expense Tracker simplifies this task by providing a user-friendly interface to:

- 💼 Add Family Members
- 💵 Record Earnings for Each Family Member
- 📉 Track Expenses
- 💰 Calculate Remaining Balance

With this tool, you can easily monitor and manage your family's financial situation.

## Features

- **Add Family Members:** Start by adding the names of family members whose earnings and expenses you want to track.
- **Record Earnings:** Record the earnings for each family member. The tracker calculates the total earnings for the family.
- **Track Expenses:** Log various expenses, and the tracker deducts these from the total earnings, showing the remaining balance.
- **User-Friendly Interface:**

The Expense Tracker features a simple and easy-to-navigate interface, ensuring a seamless user experience, allowing you to effortlessly manage your family's financial data.

## How to Use

1. **Add Family Members:**
   - Run the [application](https://expense-tracker-alpha.streamlit.app/) and choose the option to add family members.
   - Enter the names of the family members you want to track.

2. **Record Earnings:**
   - Select the option to record earnings.
   - Specify the earnings for each family member.

3. **Track Expenses:**
   - Log expenses for various categories (e.g., groceries, bills).
   - The application automatically calculates the remaining balance after deducting expenses.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sree-hari-s/Expense-Tracker.git
   cd Expense-Tracker
   ```

2. Install the required dependencies

   ```bash
    pip install -r requirements.txt
    ```

3. Run the Application

   Now you can run the Family Expense Tracker application using Streamlit:

    ```bash
    streamlit run app.py
    ```

   ## MongoDB (optional)

   The app can persist data to MongoDB. If MongoDB isn't available it falls back to a local `data.json` file in the project directory.

   To enable MongoDB persistence (PowerShell example):

   ```powershell
   $env:MONGODB_URI = "mongodb://localhost:27017"    # or your MongoDB connection string
   $env:MONGODB_DB = "expense_tracker"               # optional database name
   python -m streamlit run "C:\Users\ramnu\OneDrive\Desktop\c2\Expense-Tracker\app.py"
   ```

   On first connect the app will create a unique index on `members.name` and an index on `expenses.category` if possible.

   Quick verification (shows whether app is using MongoDB or local file):

   ```powershell
   python -c "import importlib.util; p=r'C:\Users\ramnu\OneDrive\Desktop\c2\Expense-Tracker\main.py'; spec=importlib.util.spec_from_file_location('main',p); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); ft=mod.FamilyExpenseTracker(); print('use_db=', ft.use_db); print('data_file=', ft._data_file)"
   ```


## How to Contribute

- If you wish to [contribute](CONTRIBUTING.md) in any way, feel free to get involved. You can suggest improvements or provide support and encouragement by [opening an issue](https://github.com/sree-hari-s/Expense-Tracker/issues).

## Contributors

Thank you all for, your contributions. Your contributions hold immense value for our project, and we are genuinely thankful for your valuable support. Your unwavering commitment and hard work are truly commendable.

<p align="center">
  <a href="https://github.com/sree-hari-s/Expense-Tracker/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=sree-hari-s/Expense-Tracker" alt="Contributors" />
  </a>
</p>


## License

This project is licensed under the terms of the [MIT License](LICENSE).
