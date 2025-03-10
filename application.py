import uuid
import boto3
import os
from flask import Flask, url_for, session, redirect, request

application = Flask(__name__)
application.secret_key = 'your-secret-key'  # Replace with your own secret key

# S3 bucket configuration (update with your bucket name)
S3_BUCKET = "my-tf-test-bucket20250205092730828700000001"
# "elasticbeanstalk-us-east-1-277707133519"


# Product catalog (update images as required)
products = {
    "sneaker1": {
        "name": "Sneaker 1",
        "price": 99.99,
        "image": f"https://{S3_BUCKET}.s3.amazonaws.com/sneaker1.jpg"
    },
    "sneaker2": {
        "name": "Sneaker 2",
        "price": 129.99,
        "image": f"https://{S3_BUCKET}.s3.amazonaws.com/sneaker2.jpg"
    },
    "sneaker3": {
        "name": "Sneaker 3",
        "price": 149.99,
        "image": f"https://{S3_BUCKET}.s3.amazonaws.com/sneaker3.jpg"
    }
}

# --------------------------
# Base HTML Templates
# --------------------------
base_header = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sneaker Store</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #333;
        padding-top: 70px;
      }
      /* Navigation adjustments */
      .navbar {
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      }
      /* Hero Section */
      .hero-section {
        position: relative;
        overflow: hidden;
      }
      .hero-section img {
        width: 100%;
        height: auto;
        display: block;
      }
      /* Product Cards */
      .product-image {
        width: 100%;
        height: 220px;
        object-fit: cover;
      }
      .card {
        margin-bottom: 30px;
      }
      /* Testimonials */
      .testimonial {
        padding: 20px;
        font-style: italic;
      }
      .testimonial-author {
        margin-top: 10px;
        font-weight: bold;
      }
      /* Subscription Section */
      .subscribe-section {
        background-color: #f8f9fa;
        padding: 40px 20px;
        margin: 40px 0;
        text-align: center;
      }
      footer {
        background-color: #343a40;
        color: #ddd;
        padding: 30px 20px;
      }
      footer a {
        color: #ddd;
      }
    </style>
  </head>
  <body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
      <div class="container">
        <a class="navbar-brand" href="/">Sneaker Store</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" 
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
      
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active"><a class="nav-link" href="/">Home</a></li>
            <li class="nav-item"><a class="nav-link" href="/products">Products</a></li>
            <li class="nav-item"><a class="nav-link" href="/about">About Us</a></li>
            <li class="nav-item"><a class="nav-link" href="/contact">Contact</a></li>
            <li class="nav-item"><a class="nav-link" href="/customer_care">Customer Care</a></li>
            <li class="nav-item"><a class="nav-link" href="/faq">FAQ</a></li>
            <li class="nav-item"><a class="nav-link" href="/custom_order">Custom Order</a></li>
            <li class="nav-item"><a class="nav-link" href="/my_uploads">My Orders</a></li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item"><a class="nav-link" href="/login">Login</a></li>
            <li class="nav-item"><a class="nav-link" href="/signup">Sign Up</a></li>
            <li class="nav-item">
              <a class="nav-link btn btn-primary text-white" href="/cart">View Cart</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container-fluid p-0">
"""
 
base_footer = """
    </div> <!-- end container-fluid -->
    <footer class="text-center">
      <div class="container">
        <p>&copy; 2025 Sneaker Store. All rights reserved.</p>
        <p>
          <strong>About Sneaker Store:</strong> Your one-stop shop for the latest sneakers. 
          Experience the perfect blend of style, comfort, and quality.
        </p>
        <p>
          <a href="/customer_care">Customer Care</a> | <a href="/contact">Contact Us</a>
        </p>
      </div>
    </footer>
    <!-- Bootstrap JS, Popper.js, and jQuery -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""
 
def render_page(content):
    return base_header + content + base_footer

# --------------------------
# Main Routes
# --------------------------

@application.route('/')
def index():
    """Enhanced Home Page with Hero, Featured Collections, Testimonials & Subscription."""
    # Hero Section with a full-width image from Unsplash (no text/button)
    hero_section = """
        <section class="hero-section" style="
        position: relative;
        background: url('https://images.unsplash.com/photo-1519744346367-dfba0ef3c9e6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80') no-repeat center center;
        background-size: cover;
        height: 600px;
    ">
      <!-- Dark Overlay -->
      <div style="
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(0, 0, 0, 0.5);
      "></div>
      
      <!-- Hero Content -->
      <div class="hero-content container" style="
          position: relative;
          z-index: 2;
          text-align: center;
          top: 50%;
          transform: translateY(-50%);
      ">
        <h1 class="display-3 text-white" style="
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        ">
          Elevate Your Sneaker Experience
        </h1>
        <p class="lead text-white" style="
            font-size: 1.5rem;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
        ">
          Discover the perfect blend of style, comfort, and innovation.
        </p>
      </div>
    </section>

    """
    # Featured Collections Section (using product cards)
    product_cards = ""
    for pid, product in products.items():
        product_cards += f"""
        <div class="col-md-4">
          <div class="card shadow-sm">
            <img src="{product['image']}" class="card-img-top product-image" alt="{product['name']}">
            <div class="card-body text-center">
              <h5 class="card-title">{product['name']}</h5>
              <p class="card-text">Price: ${product['price']}</p>
              <a href="/add_to_cart/{pid}" class="btn btn-success">Add to Cart</a>
            </div>
          </div>
        </div>
        """
    featured_section = f"""
    <section class="py-5">
      <div class="container">
        <h2 class="text-center mb-5">Featured Collections</h2>
        <div class="row">
          {product_cards}
        </div>
      </div>
    </section>
    """
    # Testimonials Section
    testimonials_section = """
    <section class="py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-5">What Our Customers Say</h2>
        <div class="row">
          <div class="col-md-4">
            <div class="testimonial text-center">
              <p>"Absolutely love these sneakers! They are stylish and comfortable."</p>
              <p class="testimonial-author">- Alex D.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="testimonial text-center">
              <p>"Fast shipping and excellent customer service. Highly recommended."</p>
              <p class="testimonial-author">- Jamie L.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="testimonial text-center">
              <p>"Great quality and a perfect fit. My go-to sneakers every day!"</p>
              <p class="testimonial-author">- Morgan K.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    """
    # Subscription Section
    subscribe_section = """
    <section class="subscribe-section">
      <div class="container">
        <h2 class="mb-4">Join Our Newsletter</h2>
        <p class="mb-4">Get exclusive offers, news, and updates straight to your inbox.</p>
        <form class="form-inline justify-content-center">
          <div class="form-group mb-2">
            <label for="subscribeEmail" class="sr-only">Email</label>
            <input type="email" class="form-control" id="subscribeEmail" placeholder="Enter your email">
          </div>
          <button type="submit" class="btn btn-primary mb-2 ml-2">Subscribe</button>
        </form>
      </div>
    </section>
    """
    content = hero_section + featured_section + testimonials_section + subscribe_section
    return render_page(content)
 
@application.route('/products')
def products_page():
    """Products page: display all sneakers (reuse Featured Collections layout)."""
    return index()
 
@application.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    """Add product to cart and redirect to cart page."""
    if product_id not in products:
        return "Product not found", 404
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect("/cart")
 
@application.route('/cart')
def cart():
    """Display shopping cart contents."""
    cart = session.get('cart', {})
    content = "<h2 class='mb-4'>Your Cart</h2>"
    if not cart:
        content += "<p>Your cart is empty.</p>"
    else:
        content += """
        <table class="table table-bordered">
          <thead class="thead-dark">
            <tr>
              <th>Product</th>
              <th>Quantity</th>
              <th>Price</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
        """
        grand_total = 0
        for pid, quantity in cart.items():
            product = products.get(pid)
            if product:
                total_price = product['price'] * quantity
                grand_total += total_price
                content += f"""
                <tr>
                  <td>{product['name']}</td>
                  <td>{quantity}</td>
                  <td>${product['price']}</td>
                  <td>${total_price:.2f}</td>
                </tr>
                """
        content += f"""
          <tr>
            <td colspan="3" class="text-right"><strong>Grand Total:</strong></td>
            <td><strong>${grand_total:.2f}</strong></td>
          </tr>
          </tbody>
        </table>
        """
    content += '<a href="/" class="btn btn-primary">Continue Shopping</a>'
    return render_page(content)
 
@application.route('/about')
def about():
    """About Us page."""
    content = """
    <section class="py-5">
      <div class="container">
        <h2 class="mb-4">About Us</h2>
        <p>At Sneaker Store, we are passionate about footwear and fashion. Our mission is to provide you with exclusive designs, superior quality, and an exceptional shopping experience. Join us as we redefine style, comfort, and performance.</p>
      </div>
    </section>
    """
    return render_page(content)
 
@application.route('/contact')
def contact():
    """Contact page."""
    content = """
    <section class="py-5">
      <div class="container">
        <h2 class="mb-4">Contact Us</h2>
        <p>Have questions or need support? Reach out to us:</p>
        <ul>
          <li>Email: <a href="mailto:support@sneakerstore.com">support@sneakerstore.com</a></li>
          <li>Phone: (123) 456-7890</li>
          <li>Address: 123 Sneaker Blvd, Fashion City, USA</li>
        </ul>
      </div>
    </section>
    """
    return render_page(content)
 
@application.route('/customer_care')
def customer_care():
    """Customer Care page."""
    content = """
    <section class="py-5">
      <div class="container">
        <h2 class="mb-4">Customer Care</h2>
        <p>Our dedicated team is here to help you with any inquiries, returns, or issues you might face. Please visit our <a href="/contact">Contact</a> page for further assistance.</p>
      </div>
    </section>
    """
    return render_page(content)
 
@application.route('/faq')
def faq():
    """Frequently Asked Questions page."""
    content = """
    <section class="py-5">
      <div class="container">
        <h2 class="mb-4">Frequently Asked Questions</h2>
        <ul>
          <li><strong>What is your return policy?</strong> Returns are accepted within 30 days of purchase.</li>
          <li><strong>Do you offer international shipping?</strong> Yes, we ship worldwide.</li>
          <li><strong>How can I track my order?</strong> A tracking number will be emailed to you once your order is shipped.</li>
        </ul>
      </div>
    </section>
    """
    return render_page(content)
 
@application.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'POST':
        # Add login authentication logic here
        return redirect("/")
    content = """
    <section class="py-5">
      <div class="container">
        <h2 class="mb-4">Login</h2>
        <form method="post">
          <div class="form-group">
            <label for="username">Username or Email</label>
            <input type="text" class="form-control" id="username" name="username" placeholder="Enter your username or email">
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" placeholder="Password">
          </div>
          <button type="submit" class="btn btn-primary">Login</button>
        </form>
      </div>
    </section>
    """
    return render_page(content)
 
@application.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign Up page."""
    if request.method == 'POST':
        # Add sign up logic here
        return redirect("/")
    content = """
    <section class="py-5">
      <div class="container">
        <h2 class="mb-4">Sign Up</h2>
        <form method="post">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" name="username" placeholder="Choose a username">
          </div>
          <div class="form-group">
            <label for="email">Email address</label>
            <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email">
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" placeholder="Create a password">
          </div>
          <button type="submit" class="btn btn-primary">Sign Up</button>
        </form>
      </div>
    </section>
    """
    return render_page(content)
 
# --------------------------
# Custom Order Routes
# --------------------------

@application.route('/custom_order', methods=['GET', 'POST'])
def custom_order():
    """
    Custom Order page: Users can upload an image showing the design
    or inspiration for the sneakers they wish to order.
    The image is uploaded to S3 and its filename is stored in the session.
    """
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'order_image' not in request.files:
            return render_page("<h3 class='py-5 text-center'>No file part in the request.</h3>")
        file = request.files['order_image']
        if file.filename == '':
            return render_page("<h3 class='py-5 text-center'>No file selected for uploading.</h3>")
        if file:
            # Generate a unique filename (preserving the original filename as part of it)
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            s3 = boto3.client('s3')
            try:
                s3.upload_fileobj(
                    file,
                    S3_BUCKET,
                    filename,
                    ExtraArgs={'ContentType': file.content_type}
                )
            except Exception as e:
                return render_page(f"<h3 class='py-5 text-center'>Error uploading file: {e}</h3>")
            # Save the filename in the session (list of uploaded images)
            uploaded_images = session.get('uploaded_images', [])
            uploaded_images.append(filename)
            session['uploaded_images'] = uploaded_images
            return redirect('/my_uploads')
    # GET request: render the custom order form
    form_html = """
    <section class="py-5">
      <div class="container">
        <h2 class="mb-4">Custom Order - Upload Your Sneaker Design</h2>
        <form method="post" enctype="multipart/form-data">
          <div class="form-group">
            <label for="order_image">Upload an image of your desired sneaker design</label>
            <input type="file" class="form-control-file" id="order_image" name="order_image" accept="image/*" required>
          </div>
          <button type="submit" class="btn btn-primary">Submit Order</button>
        </form>
      </div>
    </section>
    """
    return render_page(form_html)
 
@application.route('/my_uploads')
def my_uploads():
    """
    My Orders page: Displays the images the user has uploaded for custom orders.
    The images are retrieved from S3 using the stored filenames.
    """
    uploaded_images = session.get('uploaded_images', [])
    if not uploaded_images:
        content = "<section class='py-5'><div class='container'><h2 class='mb-4'>My Custom Orders</h2><p>You haven't uploaded any custom orders yet.</p></div></section>"
    else:
        images_html = ""
        for filename in uploaded_images:
            image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
            images_html += f"""
            <div class="col-md-4 mb-4">
              <div class="card">
                <img src="{image_url}" class="card-img-top" alt="Custom Order">
              </div>
            </div>
            """
        content = f"""
        <section class="py-5">
          <div class="container">
            <h2 class="mb-4">My Custom Orders</h2>
            <div class="row">
              {images_html}
            </div>
          </div>
        </section>
        """
    return render_page(content)
 
# --------------------------
# Run the Application
# --------------------------
if __name__ == "__main__":
    application.debug = True  # Disable debug mode in production.
    # application.run()
    application.run(host=os.getenv("PUBLIC_IP"), port=int(os.getenv("PORT")))
