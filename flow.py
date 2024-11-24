# user will put his product name , import country name

# will check if product data already exist in db or not
# then will rereive that products export, amazon, import complaince data from amazon , dgft and macmap
# once data is there will structure it save it in db
# but if data is already there then will serve that

from flask import Flask, request, jsonify
from back import process_data
from flask_cors import CORS
 

app = Flask(__name__)
CORS(app)

# Sample storage for products and related data (in-memory for simplicity)
products = {}

@app.route('/submit-product', methods=['POST'])
def submit_product():
    """
    Endpoint to receive and process product name and import country.
    """
    try:
        data = request.get_json()

        # Validate required fields
        product_name = data.get('product_name')
        import_country = data.get('import_country')

        if not product_name or not import_country:
            return jsonify({
                "status": "error",
                "message": "Both 'product_name' and 'import_country' are required."
            }), 400

        # Save the product information
        product_id = len(products) + 1  # Simple ID assignment
        products[product_id] = {
            "product_name": product_name,
            "import_country": import_country
        }
        final_json = process_data(product_name,import_country)

        return jsonify({
            "status": "success",
            "message": "Product information received and processed successfully.",
            "product_id": product_id,
            "data": final_json['product_type'],
            "doc_urls":final_json['urls']
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500



if __name__ == '__main__':
    app.run(debug=True)