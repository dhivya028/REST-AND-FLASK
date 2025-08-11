from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

products = [
    {"id": 1, "name": "Mango", "price": 50},
    {"id": 2, "name": "Apple", "price": 30}
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product_json():
    new_product = request.get_json()
    products.append(new_product)
    return jsonify({"message": "Product added successfully!"}), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product_json(product_id):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return jsonify({"message": "Product deleted successfully!"}),204
    return jsonify({"error": "Product not found"}), 404

# 👇 NEW ROUTES for HTML form support

@app.route('/')
def homepage():
    return render_template('products.html', products=products)

@app.route('/add', methods=['POST'])
def add_product_form():
    name = request.form['name']
    price = int(request.form['price'])
    new_id = max([p["id"] for p in products]) + 1 if products else 1
    products.append({"id": new_id, "name": name, "price": price})
    return redirect(url_for('homepage'))

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product_form(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    return redirect(url_for('homepage'))
def find_product(pid):
    return next((p for p in products if p["id"] == pid), None)

# PUT: Replace the entire product
@app.route('/products/<int:product_id>', methods=['PUT'])
def replace_product(product_id):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()

    if "name" not in data or "price" not in data:
        return jsonify({"error": "PUT requires both 'name' and 'price'"}), 400

    prod = find_product(product_id)
    if not prod:
        return jsonify({"error": "Product not found"}), 404

    prod["name"] = data["name"]
    prod["price"] = int(data["price"])
    return jsonify({"message": "Product replaced", "product": prod}), 200

# PATCH: Update only given fields
@app.route('/products/<int:product_id>', methods=['PATCH'])
def update_product_partial(product_id):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()

    prod = find_product(product_id)
    if not prod:
        return jsonify({"error": "Product not found"}), 404

    if "name" in data:
        prod["name"] = data["name"]
    if "price" in data:
        prod["price"] = int(data["price"])

    return jsonify({"message": "Product updated", "product": prod}), 200

# ---------------------- RUN APP ----------------------

if __name__ == '__main__':
    app.run(debug=True)