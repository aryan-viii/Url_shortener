# Shortly — URL Shortener

A simple URL shortening service built with Django and Django REST Framework.

Shortly allows users to create short links, use custom short codes, set expiration dates, track link visits, and generate QR codes through a simple web interface and REST API.

## Preview

![Shortly URL Shortener](docs/shortly-homepage.png)

## Features

- Generate unique short URLs
- Custom short codes
- Optional link expiration
- Redirect short URLs to their original destination
- Track link visits
- Generate QR codes
- Search and order shortened URLs
- Paginated URL listing
- API and public endpoint rate limiting
- QR code caching
- Command to clean up expired links
- Responsive web interface
- Automated tests

## Tech Stack

- Python
- Django 6.0
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- HTML, CSS & JavaScript
- qrcode & Pillow

## Getting Started

The project is fully dockerized — you only need Docker installed, no local Python/Postgres setup required.

Clone the repository:

```bash
git clone https://github.com/aryan-viii/Url_shortener.git
cd Url_shortener
```

Create a `.env` file in the project root (same folder as `docker-compose.yml`) with the following variables:

```env
POSTGRES_DB=url_shortener_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
DJANGO_SECRET_KEY=your_django_secret_key
```

Build and start the containers (Django app + PostgreSQL):

```bash
docker compose up --build -d
```

Apply migrations:

```bash
docker compose exec web python manage.py migrate
```

(Optional) Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

Open:

```text
http://localhost:8000/
```

To stop the containers:

```bash
docker compose down
```

To stop the containers **and** delete the database volume (fresh reset):

```bash
docker compose down -v
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/shorten/` | List shortened URLs |
| `POST` | `/api/shorten/` | Create a short URL |
| `GET` | `/api/shorten/<short_code>/` | Retrieve a short URL |
| `PUT/PATCH` | `/api/shorten/<short_code>/` | Update a short URL |
| `DELETE` | `/api/shorten/<short_code>/` | Delete a short URL |
| `GET` | `/api/shorten/<short_code>/stats/` | View link statistics |
| `GET` | `/api/shorten/<short_code>/qr/` | Generate a QR code |
| `GET` | `/<short_code>/` | Redirect to the original URL |

The list endpoint also supports search, ordering, and pagination:

```text
/api/shorten/?search=youtube
/api/shorten/?ordering=-access_count
/api/shorten/?page=2
```

## Example

Create a short URL:

```bash
curl -X POST http://127.0.0.1:8000/api/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

You can optionally provide a custom short code and expiration date:

```json
{
    "url": "https://example.com",
    "short_code": "example",
    "expires_at": "2026-12-31T23:59:59Z"
}
```

## Running Tests

```bash
docker compose exec web python manage.py test
```

## Cleaning Up Expired Links

Delete expired links:

```bash
docker compose exec web python manage.py purge_expired_links
```

Preview what would be deleted:

```bash
docker compose exec web python manage.py purge_expired_links --dry-run
```

## Development Notes

This project is configured for local development with Docker Compose, using `DEBUG = True` and Django's built-in dev server.

Before deploying publicly: disable debug mode, set proper `ALLOWED_HOSTS`, swap the dev server for a production WSGI server (e.g. Gunicorn), and use a dedicated production database/cache configuration. Never commit the `.env` file — it's excluded via `.gitignore` and should be created fresh (with strong, unique credentials) in each environment.