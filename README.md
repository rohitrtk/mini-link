# Mini Link

Mini Link is a small URL-shortening service built with FastAPI and PostgreSQL. It provides a browser interface for creating short links and redirects each short link to its original destination.

This project was created after reading Alex Xu's *System Design Interview: An Insider's Guide* and exploring the URL-shortener design discussed in the book.

## Stack

- FastAPI and Jinja2
- SQLAlchemy with asyncpg
- PostgreSQL and Alembic
- Vanilla JavaScript and Pico CSS
- uv and Docker Compose

## How shortening works

1. The client sends a long URL to `POST /shorten`.
2. Mini Link generates a cryptographically secure random number from a space of `62^12` possible values.
3. The number is encoded as a fixed-length, 12-character Base62 string using `0-9`, `a-z`, and `A-Z`.
4. PostgreSQL stores the short code and its target URL. A unique index prevents duplicate short codes.
5. If a generated code collides with an existing code, the service generates another one and retries.
6. If the target URL already exists, Mini Link returns its existing short code, increments `number_of_creations`, and updates `last_created_at`.
7. A request to `GET /{short_code}` looks up the target URL and returns a temporary redirect.

The database `id` is used only as the row's internal primary key; it is not used to generate the public short code.

## Running locally

Create a `.env` file:

```env
POSTGRES_USER=mini_link
POSTGRES_PASSWORD=change_me
POSTGRES_DB=mini_link
POSTGRES_PORT=5432
```

Start PostgreSQL, apply the migrations, and start the application:

```powershell
docker compose up -d db
docker compose run --rm app uv run alembic upgrade head
docker compose up
```

Open `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

## Tests

```powershell
uv run pytest
```
