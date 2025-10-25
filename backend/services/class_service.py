import pandas as pd
from typing import List, Dict, Optional
from backend.database import FinanceDB
from backend.models.schemas import Class, ClassStats


class ClassService:
    """
    Service layer for English class operations.
    Handles all business logic related to classes.
    """

    def __init__(self, db: FinanceDB):
        """
        Initialize class service.

        Args:
            db: Database instance
        """
        self.db = db

    def create_class(
        self, student_name: str, class_value: float, quantity: int
    ) -> bool:
        """
        Create a new class record.

        Args:
            student_name: Name of the student
            class_value: Value per class in BRL
            quantity: Number of classes

        Returns:
            True if successful

        Raises:
            ValueError: If validation fails
            Exception: If database operation fails
        """
        try:
            # Validate required fields
            if not student_name or not student_name.strip():
                raise ValueError("Student name cannot be empty")

            if class_value <= 0:
                raise ValueError("Class value must be positive")

            if quantity < 1:
                raise ValueError("Quantity must be at least 1")

            # Add class to database
            return self.db.add_class(
                student_name=student_name.strip(),
                class_value=class_value,
                quantity=quantity,
            )

        except Exception as e:
            raise Exception(f"Error creating class: {e}")

    def delete_class(self, class_id: int) -> bool:
        """
        Delete a class record by ID.

        Args:
            class_id: ID of class to delete

        Returns:
            True if successful

        Raises:
            ValueError: If class_id is invalid
            Exception: If database operation fails
        """
        try:
            return self.db.delete_class(class_id)

        except Exception as e:
            raise Exception(f"Error deleting class: {e}")

    def get_all_classes(self) -> pd.DataFrame:
        """
        Retrieve all class records.

        Returns:
            DataFrame with all classes

        Raises:
            Exception: If database operation fails
        """
        try:
            return self.db.get_all_classes()

        except Exception as e:
            raise Exception(f"Error retrieving classes: {e}")

    def get_classes_by_student(self) -> pd.DataFrame:
        """
        Get classes grouped by student.

        Returns:
            DataFrame with student summaries

        Raises:
            Exception: If database operation fails
        """
        try:
            return self.db.get_classes_by_student()

        except Exception as e:
            raise Exception(f"Error retrieving student summaries: {e}")

    def get_total_revenue(self) -> float:
        """
        Calculate total revenue from all classes.

        Returns:
            Total revenue in BRL

        Raises:
            Exception: If calculation fails
        """
        try:
            return self.db.get_total_revenue()

        except Exception as e:
            raise Exception(f"Error calculating revenue: {e}")

    def get_class_stats(self) -> ClassStats:
        """
        Calculate class statistics.

        Returns:
            ClassStats object with aggregated data

        Raises:
            Exception: If calculation fails
        """
        try:
            # Get all classes
            df = self.get_all_classes()

            # Calculate statistics
            if df.empty:
                return ClassStats(
                    total_classes=0,
                    total_revenue=0.0,
                    student_count=0,
                    average_per_class=0.0,
                )

            # Calculate metrics
            total_classes = df["quantity"].sum()
            total_revenue = self.get_total_revenue()
            student_count = df["student_name"].nunique()
            average_per_class = df["class_value"].mean()

            return ClassStats(
                total_classes=int(total_classes),
                total_revenue=total_revenue,
                student_count=student_count,
                average_per_class=average_per_class,
            )

        except Exception as e:
            raise Exception(f"Error calculating stats: {e}")

    def get_revenue_by_student(self) -> Dict[str, float]:
        """
        Get total revenue grouped by student.

        Returns:
            Dictionary with student_name as key and revenue as value

        Raises:
            Exception: If calculation fails
        """
        try:
            # Get classes by student
            df = self.get_classes_by_student()

            if df.empty:
                return {}

            # Convert to dictionary
            return dict(zip(df["student_name"], df["total_revenue"]))

        except Exception as e:
            raise Exception(f"Error grouping by student: {e}")

    def get_monthly_revenue(self) -> pd.DataFrame:
        """
        Get revenue grouped by month.

        Returns:
            DataFrame with monthly revenue totals

        Raises:
            Exception: If calculation fails
        """
        try:
            # Get all classes
            df = self.get_all_classes()

            if df.empty:
                return pd.DataFrame()

            # Convert date to datetime
            df["date"] = pd.to_datetime(df["date"])

            # Extract year-month
            df["month"] = df["date"].dt.to_period("M")

            # Group by month
            monthly = df.groupby("month")["total"].sum().reset_index()
            monthly["month"] = monthly["month"].astype(str)

            return monthly

        except Exception as e:
            raise Exception(f"Error calculating monthly revenue: {e}")

    def get_top_students(self, limit: int = 5) -> pd.DataFrame:
        """
        Get top students by revenue.

        Args:
            limit: Number of top students to return

        Returns:
            DataFrame with top students

        Raises:
            Exception: If calculation fails
        """
        try:
            # Get classes by student
            df = self.get_classes_by_student()

            if df.empty:
                return pd.DataFrame()

            # Sort by revenue and get top N
            top = df.nlargest(limit, "total_revenue")

            return top

        except Exception as e:
            raise Exception(f"Error getting top students: {e}")
