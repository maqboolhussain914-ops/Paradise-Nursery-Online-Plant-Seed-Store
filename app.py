from flask import Flask, render_template, request, redirect, url_for, flash, session
import database as db
import os

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
