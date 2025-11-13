import pandas as pd
from typing import List, Dict, Optional
from backend.database import FinanceDB
from backend.models.schemas import Expense, ExpenseStats

#?Teste para ver como funciona os commits automataticos
class ExpenseService:
    """
    Service layer for expense operations.
    Handles all business logic related to expenses.
    """

    def __init__(self, db: FinanceDB):
        """
        Initialize expense service.

        Args:
            db: Database instance
        """
        self.db = db

    def create_expense(
        self,
        category: str,
        location: str,
        price: float,
        payment_method: str,
        installments: int = 1,
    ) -> bool:
        """
        Create a new expense record.

        Args:
            category: Expense category
            location: Location of expense
            price: Amount spent
            payment_method: Payment type
            installments: Number of installments

        Returns:
            True if successful

        Raises:
            ValueError: If validation fails
            Exception: If database operation fails
        """
        try:
            # Validate required fields
            if not category or not category.strip():
                raise ValueError("Category cannot be empty")

            if not location or not location.strip():
                raise ValueError("Location cannot be empty")

            # Add expense to database
            return self.db.add_expense(
                category=category.strip(),
                location=location.strip(),
                price=price,
                payment_method=payment_method,
                installments=installments,
            )

        except Exception as e:
            raise Exception(f"Error creating expense: {e}")

    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete an expense by ID.

        Args:
            expense_id: ID of expense to delete

        Returns:
            True if successful

        Raises:
            ValueError: If expense_id is invalid
            Exception: If database operation fails
        """
        try:
            return self.db.delete_expense(expense_id)

        except Exception as e:
            raise Exception(f"Error deleting expense: {e}")

    def get_all_expenses(self) -> pd.DataFrame:
        """
        Retrieve all expenses.

        Returns:
            DataFrame with all expenses

        Raises:
            Exception: If database operation fails
        """
        try:
            return self.db.get_all_expenses()

        except Exception as e:
            raise Exception(f"Error retrieving expenses: {e}")

    def get_expenses_by_category(self) -> pd.DataFrame:
        """
        Get expenses grouped by category.

        Returns:
            DataFrame with category totals

        Raises:
            Exception: If database operation fails
        """
        try:
            return self.db.get_total_by_category()

        except Exception as e:
            raise Exception(f"Error retrieving category totals: {e}")

    def get_expense_stats(self) -> ExpenseStats:
        """
        Calculate expense statistics.

        Returns:
            ExpenseStats object with aggregated data

        Raises:
            Exception: If calculation fails
        """
        try:
            # Get all expenses
            df = self.get_all_expenses()

            # Calculate statistics
            if df.empty:
                return ExpenseStats(
                    total_expenses=0,
                    total_spent=0.0,
                    average_expense=0.0,
                    top_category="N/A",
                )

            # Calculate metrics
            total_expenses = len(df)
            total_spent = df["price"].sum()
            average_expense = df["price"].mean()

            # Get top category
            category_totals = self.get_expenses_by_category()
            top_category = (
                category_totals.iloc[0]["category"]
                if not category_totals.empty
                else "N/A"
            )

            return ExpenseStats(
                total_expenses=total_expenses,
                total_spent=total_spent,
                average_expense=average_expense,
                top_category=top_category,
            )

        except Exception as e:
            raise Exception(f"Error calculating stats: {e}")

    def clear_all_expenses(self) -> bool:
        """
        Delete all expenses from database.
        WARNING: This action cannot be undone!

        Returns:
            True if successful

        Raises:
            Exception: If database operation fails
        """
        try:
            return self.db.clear_all_expenses()

        except Exception as e:
            raise Exception(f"Error clearing expenses: {e}")

    def delete_all_expenses(self) -> bool:
        """
        Alias para clear_all_expenses, para compatibilidade com frontend.
        """
        return self.clear_all_expenses()

    def get_expenses_by_payment_method(self) -> Dict[str, float]:
        """
        Get total spending grouped by payment method.

        Returns:
            Dictionary with payment_method as key and total as value

        Raises:
            Exception: If calculation fails
        """
        try:
            # Get all expenses
            df = self.get_all_expenses()

            if df.empty:
                return {}

            # Group by payment method
            grouped = df.groupby("payment_method")["price"].sum()

            return grouped.to_dict()

        except Exception as e:
            raise Exception(f"Error grouping by payment method: {e}")

    def get_monthly_expenses(self) -> pd.DataFrame:
        """
        Get expenses grouped by month.

        Returns:
            DataFrame with monthly expense totals

        Raises:
            Exception: If calculation fails
        """
        try:
            # Get all expenses
            df = self.get_all_expenses()

            if df.empty:
                return pd.DataFrame()

            # Convert date to datetime
            df["date"] = pd.to_datetime(df["date"])

            # Extract year-month
            df["month"] = df["date"].dt.to_period("M")

            # Group by month
            monthly = df.groupby("month")["price"].sum().reset_index()
            monthly["month"] = monthly["month"].astype(str)

            return monthly

        except Exception as e:
            raise Exception(f"Error calculating monthly expenses: {e}")
