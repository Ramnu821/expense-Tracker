import datetime
import json
from pathlib import Path
from typing import Any

try:
    import db
except Exception:
    db = None


class FamilyMember:
    def __init__(self, name, earning_status=True, earnings=0, _id: Any = None):
        self._id = _id
        self.name = name
        self.earning_status = earning_status
        self.earnings = earnings

    def __str__(self):
        return (
            f"Name: {self.name}, Earning Status: {'Earning' if self.earning_status else 'Not Earning'}, "
            f"Earnings: {self.earnings}"
        )

    def to_dict(self) -> dict:
        d = {"name": self.name, "earning_status": self.earning_status, "earnings": self.earnings}
        # do not include _id when inserting/updating via $set
        return d

    @staticmethod
    def from_dict(d: dict) -> "FamilyMember":
        return FamilyMember(d.get("name", ""), d.get("earning_status", True), d.get("earnings", 0), _id=d.get("_id"))


class Expense:
    def __init__(self, value, category, description, date, _id: Any = None):
        self._id = _id
        self.value = value
        self.category = category
        self.description = description
        # date expected to be a date or string; normalize to ISO string for persistence
        if isinstance(date, (str,)):
            self.date = date
        elif isinstance(date, datetime.date):
            self.date = date.isoformat()
        else:
            # fallback
            self.date = str(date)

    def __str__(self):
        return f"Value: {self.value}, Category: {self.category}, Description: {self.description}, Date: {self.date}"

    def to_dict(self) -> dict:
        return {"value": self.value, "category": self.category, "description": self.description, "date": self.date}

    @staticmethod
    def from_dict(d: dict) -> "Expense":
        return Expense(d.get("value", 0), d.get("category", ""), d.get("description", ""), d.get("date", ""), _id=d.get("_id"))


class FamilyExpenseTracker:
    def __init__(self):
        # In-memory lists for streamlit session
        self.members: list[FamilyMember] = []
        self.expense_list: list[Expense] = []

        # Try to initialize DB collections; if unavailable, continue with in-memory only
        self.use_db = False
        self.members_coll = None
        self.expenses_coll = None
        if db is not None:
            try:
                mongodb = db.init_db()
                self.members_coll = mongodb.get_collection("members")
                self.expenses_coll = mongodb.get_collection("expenses")
                self.use_db = True
            except Exception:
                # if DB connect fails, keep using in-memory/file fallback
                self.use_db = False

        # File fallback path
        self._data_file = Path(__file__).parent / "data.json"

        # Load existing data from DB if available, otherwise from JSON file
        if self.use_db:
            try:
                # load documents; keep _id values
                self.members = [FamilyMember.from_dict(m) for m in self.members_coll.find()]
                self.expense_list = [Expense.from_dict(e) for e in self.expenses_coll.find()]
            except Exception:
                # any issue loading -> fall back to file or empty lists
                self._load_from_file()
        else:
            # load from local file if present
            self._load_from_file()

    def _load_from_file(self):
        try:
            if self._data_file.exists():
                with open(self._data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.members = [FamilyMember.from_dict(m) for m in data.get("members", [])]
                self.expense_list = [Expense.from_dict(e) for e in data.get("expenses", [])]
            else:
                self.members = []
                self.expense_list = []
        except Exception:
            self.members = []
            self.expense_list = []

    def _save_to_file(self):
        try:
            data = {
                "members": [m.to_dict() for m in self.members],
                "expenses": [e.to_dict() for e in self.expense_list],
            }
            with open(self._data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            # ignore file save errors in UI flow
            pass

    def add_family_member(self, name, earning_status=True, earnings=0):
        if not name.strip():
            raise ValueError("Name field cannot be empty")
        member = FamilyMember(name, earning_status, earnings)
        self.members.append(member)
        if self.use_db and self.members_coll is not None:
            try:
                result = self.members_coll.update_one({"name": member.name}, {"$set": member.to_dict()}, upsert=True)
                # if inserted, set _id on object
                if getattr(result, "upserted_id", None):
                    member._id = result.upserted_id
                else:
                    # fetch existing doc's _id
                    doc = self.members_coll.find_one({"name": member.name})
                    if doc:
                        member._id = doc.get("_id")
            except Exception:
                pass
        else:
            # persist to local file
            self._save_to_file()
    
    def delete_family_member(self, member):
        self.members.remove(member)
        if self.use_db and self.members_coll is not None:
            try:
                if getattr(member, "_id", None) is not None:
                    self.members_coll.delete_one({"_id": member._id})
                else:
                    self.members_coll.delete_one({"name": member.name})
            except Exception:
                pass
        else:
            self._save_to_file()

    def update_family_member(self, member, earning_status=True, earnings=0):
        if member:
            member.earning_status = earning_status
            member.earnings = earnings
            if self.use_db and self.members_coll is not None:
                try:
                    if getattr(member, "_id", None) is not None:
                        self.members_coll.update_one({"_id": member._id}, {"$set": member.to_dict()})
                    else:
                        self.members_coll.update_one({"name": member.name}, {"$set": member.to_dict()}, upsert=True)
                except Exception:
                    pass
            else:
                self._save_to_file()

    def calculate_total_earnings(self):
        total_earnings = sum(
            member.earnings for member in self.members if member.earning_status
        )
        return total_earnings

    def add_expense(self, value, category, description, date):
        if value == 0:
            raise ValueError("Value cannot be zero")
        if not category.strip():
            raise ValueError("Please choose a category")
        expense = Expense(value, category, description, date)
        self.expense_list.append(expense)
        if self.use_db and self.expenses_coll is not None:
            try:
                res = self.expenses_coll.insert_one(expense.to_dict())
                expense._id = getattr(res, "inserted_id", None)
            except Exception:
                pass
        else:
            self._save_to_file()

    def delete_expense(self,expense):
        self.expense_list.remove(expense)
        if self.use_db and self.expenses_coll is not None:
            try:
                # delete by _id if available, otherwise match by fields
                if getattr(expense, "_id", None) is not None:
                    self.expenses_coll.delete_one({"_id": expense._id})
                else:
                    self.expenses_coll.delete_one({"value": expense.value, "category": expense.category, "date": expense.date})
            except Exception:
                pass
        else:
            self._save_to_file()


    def merge_similar_category(self, value, category, description, date):
        if value == 0:
            raise ValueError("Value cannot be zero")
        if not category.strip():
            raise ValueError("Please choose a category")
        # If an existing category exists, merge into it; else add new
        existing_expense = None
        for expense in self.expense_list:
            if expense.category == category:
                existing_expense = expense
                break

        if existing_expense:
            existing_expense.value += value
            if description:
                existing_expense.description = description
            # update in DB
            if self.use_db and self.expenses_coll is not None:
                try:
                    self.expenses_coll.update_one({"category": category}, {"$set": existing_expense.to_dict()})
                except Exception:
                    pass
            else:
                # update local file representation
                self._save_to_file()
        else:
            self.add_expense(value, category, description, date)

    def calculate_total_expenditure(self):
        total_expenditure = sum(expense.value for expense in self.expense_list)
        return total_expenditure


if __name__ == "__main__":
    expense_tracker = FamilyExpenseTracker()
