# StyleHub Single Vendor E-commerce Website


StyleHub is a simple single-vendor clothing e-commerce website developed using Django, HTML, CSS, JavaScript, Bootstrap, and SQLite.


## Features


- Customer registration, login, and logout
- Products loaded from the Django database
- Product search and category filtering
- Product details page
- Session-based shopping cart
- Increase and decrease cart quantities
- Remove products from the cart
- Automatic total-price calculation
- Checkout form with JavaScript validation
- Orders saved in the database
- Product stock automatically reduced after checkout
- Django Admin product and order management
- Responsive Bootstrap design


## Technologies


- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript
- Bootstrap


## Installation


### 1. Clone the repository


```bash
git clone https://github.com/YOUR-USERNAME/single-vendor-ecommerce.git
cd single-vendor-ecommerce
```


### 2. Create a virtual environment


```bash
python -m venv .venv
```


Activate it on Windows:


```bash
.venv\Scripts\activate
```


### 3. Install the dependencies


```bash
python -m pip install -r requirements.txt
```


### 4. Configure environment variables


Copy `.env.example` to a new file named `.env` and provide a Django secret key:


```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
```


### 5. Apply database migrations


```bash
python manage.py migrate
```


### 6. Load the sample products


```bash
python manage.py loaddata products
```


### 7. Create an administrator


```bash
python manage.py createsuperuser
```


### 8. Start the development server


```bash
python manage.py runserver
```


Open http://127.0.0.1:8000/ in a browser.


The administration panel is available at:


http://127.0.0.1:8000/admin/


## Customer Journey


```text
View Products → View Details → Add to Cart → Manage Cart → Checkout → Place Order
```


## Main Pages


- Home
- Products
- Product Details
- Cart
- Checkout
- Order Success
- Login and Registration
- Django Admin


## Project Type


Academic assignment: Simple Single Vendor E-commerce Website using Django.
