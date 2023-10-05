# Yastvo Vegetarian Cafe

https://yastvo.fly.dev/

Welcome to the Yastvo Vegetarian Cafe's code repository. This project is a web application for our vegetarian cafe, built using Django.

## Features

- **Responsive Design**: Our website is designed to be accessible on all devices, ensuring a seamless experience for all visitors.
- **Admin Panel**: Dishes can be easily added, updated, or removed by the admin directly from the site.
- **Delivery & Order Services**: Customers can place orders for their favorite dishes and opt for delivery, all through the website.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DemetrPI/Yastvo.git
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` in your browser to see the application in action.

## Contributing

We welcome contributions to improve the cafe's website. If you have suggestions or bug reports, please open an issue. If you'd like to contribute code, please open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Feel free to customize this template further to suit your needs. Once you're satisfied, you can add this README to your repository.
