from flask import Flask, render_template, request, redirect, url_for, flash, session
import database as db
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24) # For session and flashing

@app.route('/')
def index():
    # Fetch a few popular products for the homepage
    products = db.get_all_products()
    popular_products = products[:4] if products else []
    categories = db.get_all_categories()
    return render_template('index.html', products=popular_products, categories=categories)

@app.route('/catalog')
def catalog():
    category_id = request.args.get('category_id')
    if category_id:
        products = db.get_all_products(category_id)
    else:
        products = db.get_all_products()
    categories = db.get_all_categories()
    return render_template('catalog.html', products=products, categories=categories, active_category=category_id)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = db.get_product_by_id(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for('catalog'))
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    # Placeholder for actual cart logic. For now, we will use session
    cart_items = session.get('cart', {})
    
    # Hydrate cart items with actual product details
    detailed_cart = []
    total = 0
    for pid, qty in cart_items.items():
        p = db.get_product_by_id(pid)
        if p:
            subtotal = float(p['price']) * qty
            total += subtotal
            detailed_cart.append({
                'product': p,
                'quantity': qty,
                'subtotal': subtotal
            })
            
    return render_template('cart.html', cart_items=detailed_cart, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    # Initialize cart in session if not exists
    if 'cart' not in session:
        session['cart'] = {}
        
    cart = session['cart']
    
    # Add or update quantity
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
        
    session.modified = True
    flash("Product added to cart!", "success")
    return redirect(url_for('cart'))

# --- Admin Routes & Logic ---

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Please log in as admin to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Basic hardcoded admin credentials for milestone
        if username == 'admin' and password == 'admin123':
            session['is_admin'] = True
            flash('Successfully logged in to admin panel.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials.', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Logged out from admin panel.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    stats = db.get_dashboard_stats()
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/products')
@admin_required
def admin_products():
    products = db.get_all_products()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    categories = db.get_all_categories()
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock_quantity = int(request.form.get('stock_quantity'))
        category_id = int(request.form.get('category_id'))
        image_url = request.form.get('image_url')
        
        if db.add_product(name, description, price, stock_quantity, category_id, image_url):
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash('Error adding product.', 'error')
            
    return render_template('admin/product_form.html', categories=categories, product=None)

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    product = db.get_product_by_id(product_id)
    categories = db.get_all_categories()
    
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('admin_products'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock_quantity = int(request.form.get('stock_quantity'))
        category_id = int(request.form.get('category_id'))
        image_url = request.form.get('image_url')
        
        if db.update_product(product_id, name, description, price, stock_quantity, category_id, image_url):
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash('Error updating product.', 'error')
            
    return render_template('admin/product_form.html', categories=categories, product=product)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    if db.delete_product(product_id):
        flash('Product deleted successfully.', 'success')
    else:
        flash('Error deleting product.', 'error')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders = db.get_all_orders()
    return render_template('admin/orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
