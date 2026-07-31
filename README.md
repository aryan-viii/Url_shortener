# URL Shortening Service

A RESTful URL Shortening API built using **Django** and **Django REST Framework**.

This project was created as part of the [roadmap.sh URL Shortening Service](https://roadmap.sh/projects/url-shortening-service) backend project.

The API allows users to create shortened URLs, retrieve and update them, delete them, and view access statistics.

## Features

- Create a short URL from a long URL
- Generate unique random short codes
- Retrieve a URL using its short code
- Update an existing shortened URL
- Delete a shortened URL
- Track the number of times a shortened URL is accessed
- Retrieve statistics for a shortened URL
- URL validation using Django's `URLField`

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- Git & GitHub

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/shorten/` | Create a new short URL |
| GET | `/shorten/<short_code>/` | Retrieve a shortened URL |
| PUT | `/shorten/<short_code>/` | Update an existing URL |
| DELETE | `/shorten/<short_code>/` | Delete a shortened URL |
| GET | `/shorten/<short_code>/stats/` | Get URL access statistics |

## Example

### Create a Short URL

**Request**

```http
POST /shorten/
```

```json
{
    "url": "https://www.example.com/some/long/url"
}
```

**Response**

```json
{
    "id": 1,
    "url": "https://www.example.com/some/long/url",
    "short_code": "abc123",
    "access_count": 0,
    "created_at": "2026-07-30T10:30:00Z",
    "updated_at": "2026-07-30T10:30:00Z"
}
```

## Project Setup

### 1. Clone the Repository

```bash
git clone <https://github.com/aryan-viii/Url_shortener.git>
```

Move into the project directory:

```bash
cd Url_shortener
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

## Short Code Generation

Each shortened URL receives a randomly generated short code.

The short code:

- Contains letters and numbers
- Is generated automatically
- Is checked for uniqueness before being stored
- Cannot be modified directly through the API

Example:

```text
abc123
```

## Access Statistics

Each shortened URL maintains an `access_count`.

The count represents how many times the shortened URL has been accessed.

Statistics can be retrieved using:

```http
GET /shorten/<short_code>/stats/
```

Example response:

```json
{
    "id": 1,
    "url": "https://www.example.com/some/long/url",
    "short_code": "abc123",
    "access_count": 10,
    "created_at": "2026-07-30T10:30:00Z",
    "updated_at": "2026-07-30T10:30:00Z"
}
```

## Project Structure

```text
Url_shortener/
│
├── shortener/
│   ├── migrations/
│   ├── api/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── url_shortener/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## What I Learned

While building this project, I practiced:

- Designing RESTful APIs
- Django models and ORM
- Django REST Framework serializers
- DRF generic views
- URL routing
- HTTP methods and status codes
- Request validation
- Generating unique short codes
- Tracking URL access statistics
- Git and GitHub workflow

## Project Reference

Project challenge:

[roadmap.sh - URL Shortening Service](https://roadmap.sh/projects/url-shortening-service)