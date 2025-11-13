import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

#Estou testando o nova atomação do comits
class FinanceDB:
    """
    Simple database manager for financial transactions and English classes.
    Uses SQLite to store data locally in the project.
    """

    def __init__(self, db_name: str = "finance.db"):
        """
        Initialize database connection.

        Args:
            db_name: Name of the SQLite database file
        """
        self.db_name = db_name
        self.create_tables()

    def create_tables(self) -> None:
        """
        Create all necessary tables if they don't exist.
        - expenses: for financial expenses
        - classes: for English classes tracking
        """
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Create expenses table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    location TEXT NOT NULL,
                    price REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    installments INTEGER DEFAULT 1
                )
            """
            )

            # Create classes table for English lessons
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    student_name TEXT NOT NULL,
                    class_value REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    total REAL NOT NULL
                )
            """
            )

            # Save changes and close connection
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error creating tables: {e}")

    def add_expense(
        self,
        category: str,
        location: str,
        price: float,
        payment_method: str,
        installments: int = 1,
    ) -> bool:
        """
        Add a new expense to the database.

        Args:
            category: Expense category (e.g., "Pharmacy")
            location: Where the expense occurred (e.g., "DROGARIA PAULISTA")
            price: Amount spent in BRL
            payment_method: How it was paid (e.g., "Credit Card", "PIX")
            installments: Number of installments (default: 1)

        Returns:
            True if successfully added, False otherwise
        """
        try:
            # Validate inputs
            if not isinstance(price, (int, float)) or price <= 0:
                raise ValueError("Price must be a positive number")

            if not isinstance(installments, int) or installments < 1:
                raise ValueError("Installments must be at least 1")

            # Get current date
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Connect and insert data
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO expenses (date, category, location, price, payment_method, installments)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (current_date, category, location, price, payment_method, installments),
            )

            conn.commit()
            conn.close()

            return True

        except (sqlite3.Error, ValueError) as e:
            raise Exception(f"Error adding expense: {e}")

    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete a specific expense from database by ID.

        Args:
            expense_id: The ID of the expense to delete

        Returns:
            True if successfully deleted, False otherwise

        Raises:
            ValueError: If expense_id is invalid
            sqlite3.Error: If database operation fails
        """
        try:
            # Validate input
            if not isinstance(expense_id, int) or expense_id <= 0:
                raise ValueError("Expense ID must be a positive integer")

            # Connect to database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Check if expense exists
            cursor.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
            if cursor.fetchone() is None:
                conn.close()
                raise ValueError(f"Expense with ID {expense_id} not found")

            # Delete the expense
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

            conn.commit()
            conn.close()

            return True

        except (sqlite3.Error, ValueError) as e:
            raise Exception(f"Error deleting expense: {e}")

    def get_all_expenses(self) -> pd.DataFrame:
        """
        Retrieve all expenses from database as DataFrame.

        Returns:
            DataFrame with all expenses
        """
        try:
            # Connect and fetch all data
            conn = sqlite3.connect(self.db_name)

            # Read data into pandas DataFrame
            df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)

            conn.close()

            return df

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error retrieving expenses: {e}")

    def get_total_by_category(self) -> pd.DataFrame:
        """
        Get total spending grouped by category.

        Returns:
            DataFrame with category and total spent
        """
        try:
            conn = sqlite3.connect(self.db_name)

            # Query to sum prices by category
            query = """
                SELECT category, SUM(price) as total
                FROM expenses
                GROUP BY category
                ORDER BY total DESC
            """

            df = pd.read_sql_query(query, conn)
            conn.close()

            return df

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error calculating totals: {e}")

    def clear_all_expenses(self) -> bool:
        """
        Delete all expenses from database.
        Use with caution!

        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM expenses")

            conn.commit()
            conn.close()

            return True

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error clearing expenses: {e}")

    # ==================== CLASSES METHODS ====================

    def add_class(self, student_name: str, class_value: float, quantity: int) -> bool:
        """
        Add a new class record to the database.

        Args:
            student_name: Name of the student
            class_value: Value per class in BRL
            quantity: Number of classes

        Returns:
            True if successfully added, False otherwise
        """
        try:
            # Validate inputs
            if not isinstance(class_value, (int, float)) or class_value <= 0:
                raise ValueError("Class value must be a positive number")

            if not isinstance(quantity, int) or quantity < 1:
                raise ValueError("Quantity must be at least 1")

            if not student_name or not student_name.strip():
                raise ValueError("Student name cannot be empty")

            # Calculate total
            total = class_value * quantity

            # Get current date
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Connect and insert data
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO classes (date, student_name, class_value, quantity, total)
                VALUES (?, ?, ?, ?, ?)
            """,
                (current_date, student_name.strip(), class_value, quantity, total),
            )

            conn.commit()
            conn.close()

            return True

        except (sqlite3.Error, ValueError) as e:
            raise Exception(f"Error adding class: {e}")

    def delete_class(self, class_id: int) -> bool:
        """
        Delete a specific class record from database by ID.

        Args:
            class_id: The ID of the class to delete

        Returns:
            True if successfully deleted, False otherwise
        """
        try:
            # Validate input
            if not isinstance(class_id, int) or class_id <= 0:
                raise ValueError("Class ID must be a positive integer")

            # Connect to database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Check if class exists
            cursor.execute("SELECT id FROM classes WHERE id = ?", (class_id,))
            if cursor.fetchone() is None:
                conn.close()
                raise ValueError(f"Class with ID {class_id} not found")

            # Delete the class
            cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))

            conn.commit()
            conn.close()

            return True

        except (sqlite3.Error, ValueError) as e:
            raise Exception(f"Error deleting class: {e}")

    def get_all_classes(self) -> pd.DataFrame:
        """
        Retrieve all class records from database as DataFrame.

        Returns:
            DataFrame with all classes
        """
        try:
            # Connect and fetch all data
            conn = sqlite3.connect(self.db_name)

            # Read data into pandas DataFrame
            df = pd.read_sql_query("SELECT * FROM classes ORDER BY date DESC", conn)

            conn.close()

            return df

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error retrieving classes: {e}")

    def get_classes_by_student(self) -> pd.DataFrame:
        """
        Get summary of classes grouped by student.
        Shows total classes and total revenue per student.

        Returns:
            DataFrame with student_name, total_classes, and total_revenue
        """
        try:
            conn = sqlite3.connect(self.db_name)

            # Query to sum classes and revenue by student
            query = """
                SELECT 
                    student_name,
                    SUM(quantity) as total_classes,
                    SUM(total) as total_revenue
                FROM classes
                GROUP BY student_name
                ORDER BY total_revenue DESC
            """

            df = pd.read_sql_query(query, conn)
            conn.close()

            return df

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error calculating class totals: {e}")

    def get_total_revenue(self) -> float:
        """
        Calculate total revenue from all classes.

        Returns:
            Total revenue in BRL
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT SUM(total) FROM classes")
            result = cursor.fetchone()[0]

            conn.close()

            # Return 0 if no classes registered
            return result if result else 0.0

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error calculating total revenue: {e}")
