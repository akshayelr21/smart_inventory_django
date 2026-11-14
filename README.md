# Smart Inventory & Order Management System (Django Web App)

A beginner-friendly Django web application with authentication, Admin/Staff roles,
product management, stock tracking, customers, orders, and reports.

## Requirements
- Python 3.10+
- pip
- Windows 10/11 (instructions below)

## Windows setup
1. Extract this ZIP.
2. Open the extracted `smart_inventory_django` folder in VS Code.
3. Open Terminal and run:

```bat
py -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

4. Visit http://127.0.0.1:8000/
5. Sign in with the superuser account you created.

## Create staff accounts
Use the Register link on the login page. Public registration always creates Staff users.
Only a Django superuser can access Django admin at `/admin/` and manage users.

## Main pages
- `/accounts/login/` - Login
- `/accounts/register/` - Staff registration
- `/` - Dashboard
- `/products/` - Product CRUD
- `/customers/` - Customer CRUD
- `/orders/` - Orders and order creation
- `/inventory/` - Stock adjustments and low-stock list
- `/reports/` - Sales and stock summary
- `/admin/` - Django administration

## Notes
- SQLite is configured by default; the database file is created after migrations.
- Currency is displayed as ₹ for presentation. Add your own tax/payment rules as required.
- This is a web-only implementation. If your internship assessment requires an Android app,
  a web app alone will not meet that separate requirement.
