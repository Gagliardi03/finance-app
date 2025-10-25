# 💰 Personal Finance Manager

Modern financial tracking application with **Fluent Design System**, built with **Python** and **Streamlit**.

## ✨ Features

- 💸 **Expense Tracking**: Add, view, and manage all your expenses
- 🎓 **English Classes Management**: Track classes and revenue per student
- 📊 **Analytics Dashboard**: Visualize spending patterns and revenue trends
- 📈 **Interactive Charts**: Pie charts, bar charts, and trend lines
- 💾 **Data Export**: Export to CSV and Excel formats
- 🎨 **Modern UI**: Clean and professional Fluent Design System

## 🏗️ Architecture

The application follows a **clean architecture** pattern with clear separation between:

```
finance-app/
│
├── backend/                  # Business Logic Layer
│   ├── database.py          # Database manager (SQLite)
│   ├── services/            # Service layer
│   │   ├── expense_service.py
│   │   └── class_service.py
│   └── models/              # Data models
│       └── schemas.py
│
├── frontend/                 # Presentation Layer
│   ├── pages/               # Page components
│   │   ├── home.py
│   │   ├── expenses.py
│   │   ├── classes.py
│   │   └── analytics.py
│   ├── components/          # Reusable UI components
│   │   ├── cards.py
│   │   ├── forms.py
│   │   ├── tables.py
│   │   └── charts.py
│   └── styles/              # Design system
│       └── fluent_theme.py
│
├── app.py                   # Main application entry point
└── requirements.txt         # Project dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run app.py
```

4. **Open your browser** at `http://localhost:8501`

## 📖 Usage Guide

### Managing Expenses

1. Navigate to **Expenses** page
2. Fill in the form with:
   - Category (e.g., "Pharmacy", "Food")
   - Location (e.g., "DROGARIA PAULISTA")
   - Price
   - Payment method
   - Installments (for credit card)
3. Click **Save Expense**

### Managing Classes

1. Navigate to **Classes** page
2. Fill in the form with:
   - Student name
   - Class value (per class)
   - Number of classes
3. Click **Save Classes**

### Viewing Analytics

1. Navigate to **Analytics** page
2. Choose from three tabs:
   - **Expense Analytics**: View spending by category, payment method, and trends
   - **Revenue Analytics**: View revenue by student and trends
   - **Combined View**: Compare expenses vs revenue

## 🎨 Design System

The application uses a **Fluent Design System** inspired by Microsoft's design language:

- **Colors**: Professional blue palette (#0078d4)
- **Typography**: Segoe UI font family
- **Components**: Cards with acrylic effect and subtle shadows
- **Animations**: Smooth transitions and hover effects
- **Responsive**: Adapts to different screen sizes

## 🛠️ Technology Stack

- **Backend**: Python, SQLite
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Excel Export**: OpenPyXL

## 📊 Database Schema

### Expenses Table
- `id`: Primary key
- `date`: Transaction date
- `category`: Expense category
- `location`: Where expense occurred
- `price`: Amount in BRL
- `payment_method`: Payment type
- `installments`: Number of installments

### Classes Table
- `id`: Primary key
- `date`: Registration date
- `student_name`: Student name
- `class_value`: Value per class
- `quantity`: Number of classes
- `total`: Total amount

## 🔒 Security & Best Practices

- ✅ Input validation on all forms
- ✅ Type safety with dataclasses
- ✅ Parameterized SQL queries (no SQL injection)
- ✅ Error handling with try-except blocks
- ✅ Service layer for business logic
- ✅ Clean separation of concerns

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📝 License

This project is for personal use.

## 👤 Author

Created with ❤️ for financial management and English teaching tracking.

---

**Enjoy managing your finances! 💰📊**
