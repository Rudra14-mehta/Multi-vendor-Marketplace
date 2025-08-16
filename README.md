# Multi-vendor Marketplace

A Django-based web application for a multi-vendor marketplace, allowing consumers and sellers to interact, manage profiles, and handle product listings.

## Project Structure

```
e-com/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── consumer/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   └── ...
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   └── ...
├── media/
│   ├── consumer/
│   ├── default/
│   ├── products/
│   └── seller/
├── mysite/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── seller/
│   └── ...
```

## Features

- User authentication and profile management
- Seller dashboard for managing products
- Consumer interface for browsing and purchasing products
- Media uploads for profile and product images
- Modular Django apps for scalability

## Setup

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd e-com
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Apply migrations**
   ```sh
   python manage.py migrate
   ```

4. **Run the development server**
   ```sh
   python manage.py runserver
   ```

5. **Access the app**
   - Visit `http://127.0.0.1:8000/` in your browser.

## Development

- Django settings are in [`mysite/settings.py`](mysite/settings.py)
- Consumer app templates: [`consumer/templates/`](consumer/templates/)
- Seller dashboard templates: [`seller/templates/dashboard/`](seller/templates/dashboard/)
- Static and media files: [`media/`](media/)

## Testing

Run unit tests with:
```sh
python manage.py test
```

## License

This project is for educational purposes
