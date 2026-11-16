SMART INVENTORY AND ORDER MANAGEMENT SYSTEM

OVERVIEW
This is a Django web application for managing products, categories, stock,
customers, orders, and sales reports. Users must sign in to use the management
pages. Staff accounts can be registered from the login page.

FEATURES
- Dashboard with product, customer, order, sales, and low-stock summaries
- Product management with SKU, category, price, quantity, and reorder level
- Category management: add, search, edit, and delete categories
- Customer management
- Stock in and stock out records
- Order creation and stock updates
- Sales and inventory reports
- Django admin at /admin/

PROJECT REQUIREMENTS
- Python 3.10 or newer
- Packages listed in requirements.txt
- SQLite for local development; PostgreSQL can be used by setting DATABASE_URL

RUN LOCALLY ON WINDOWS
1. Open a terminal in this folder.
2. Create and activate a virtual environment:

   py -m venv venv
   venv\Scripts\activate

3. Install the project packages:

   python -m pip install --upgrade pip
   pip install -r requirements.txt

4. Create the database tables and an administrator account:

   python manage.py migrate
   python manage.py createsuperuser

5. Start the development server:

   python manage.py runserver

6. Open http://127.0.0.1:8000/ and sign in.

IMPORTANT PAGES
Dashboard:   /
Products:    /products/
Categories:  /categories/
Customers:   /customers/
Stock:       /inventory/
Orders:      /orders/
Reports:     /reports/
Admin:       /admin/

RENDER DEPLOYMENT
The project uses Gunicorn to serve Django and WhiteNoise for static files.
Typical Render commands are:

Build:
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate

Start:
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

Configure DATABASE_URL, SECRET_KEY, and DEBUG in the Render service environment.
Before using this app publicly, update config/settings.py to read SECRET_KEY
and DEBUG from environment variables. The current settings file has DEBUG=True
and a development-only hard-coded secret key, which are not safe for production.

DATA AND SECURITY NOTES
- Do not commit .env, db.sqlite3, database passwords, or virtual environment
  folders to GitHub.
- The deployed PostgreSQL database is separate from the local SQLite database.
- Create a production administrator account after the database is initialized.
- Deleting a category keeps its products and clears their category assignment.

DEPENDENCY NOTE
python-dotenv is listed in requirements.txt because config/settings.py loads
the optional local .env file with that package.
