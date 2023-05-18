# Online Store on Django

It is an online store web application developed on Django that provides functionality for selling products and provides convenient management of products and orders.

# Basic functionality

- User registration and authorization
- Product page with images, description, other
- Adding products to the cart and placing an order
- Ability to view and edit orders by buyers and sellers
- Product search with the ability to sort and filter results
- Chat between buyer and client

# Deployment

1. Clone the repository: git clone https://github.com/chamois1/Online-Store-Django.git

2. Go to the "my_shop_users" project directory: cd my_shop_users

3. Install dependencies: pip install -r requirements.txt

4. Python manage.py migrate

5. Python manage.py runserver

# Warning

## Dependencies

This project has dependencies on Redis and Daphne. Please note that these dependencies are not supported for Windows operating systems. However, they can be supported on WSL (Windows Subsystem for Linux), Linux, and macOS. If you are using Windows and these dependencies are not supported, I advise you to remove the following packages from the `INSTALLED_APPS` list in the settings:

- `channels`
- `daphne`

By removing these packages, you can ensure that your project will run without any compatibility issues in your Windows environment, however chat will not work