from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Expense:
    """
    Data model for expense records.
    Represents a single expense transaction.
    """

    id: Optional[int]  # ID from database
    date: str  # Transaction date
    category: str  # Expense category (e.g., "Pharmacy")
    location: str  # Where expense occurred
    price: float  # Amount in BRL
    payment_method: str  # Payment type (e.g., "Credit Card")
    installments: int = 1  # Number of installments


@dataclass
class Class:
    """
    Data model for English class records.
    Represents classes given to a student.
    """

    id: Optional[int]  # ID from database
    date: str  # Date of class registration
    student_name: str  # Name of student
    class_value: float  # Value per class in BRL
    quantity: int  # Number of classes
    total: float  # Total amount (class_value * quantity)


@dataclass
class ExpenseStats:
    """
    Statistics for expense analysis.
    Contains aggregated expense data.
    """

    total_expenses: int  # Count of expenses
    total_spent: float  # Total amount spent
    average_expense: float  # Average expense value
    top_category: str  # Category with most spending


@dataclass
class ClassStats:
    """
    Statistics for class revenue analysis.
    Contains aggregated class data.
    """

    total_classes: int  # Total number of classes
    total_revenue: float  # Total revenue generated
    student_count: int  # Number of unique students
    average_per_class: float  # Average revenue per class