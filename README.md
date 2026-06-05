# High Performance Django Blog API

This project demonstrates the N+1 query problem in Django and how to eliminate it with `select_related`, `annotate`, and a database-side aggregation for author totals.

## Endpoints

- `GET /api/posts/naive` - intentionally triggers an N+1 pattern
- `GET /api/posts/optimized` - uses `select_related` and `annotate(Count(...))`
- `GET /api/posts/advanced` - adds an author-wide total views annotation via a subquery
- `GET /healthz` - container health probe

## Local development

1. Create a virtual environment and install dependencies from `requirements.txt`.
2. Run migrations: `python manage.py migrate`
3. Seed the database: `python manage.py seed_db`
4. Start the server: `python manage.py runserver 0.0.0.0:8000`

## Docker

Run the whole stack with:

```bash
docker-compose up --build
```

The `web` service runs migrations and seeds the database on startup before launching Gunicorn.

## Benchmarking

Use `benchmark.py` to measure response latency and query counts for any endpoint:

```bash
python benchmark.py http://localhost:8000/api/posts/naive --requests 50
```

## Notes

- The SQL query count is exposed through the `X-DB-Query-Count` response header when `DEBUG=1`.
- The seeded dataset contains 20 authors, 200 posts, and 2000 comments.
- The measured benchmark on the seeded dataset reduced the naive endpoint from 401 queries to 1 query on both optimized endpoints.
- Sample benchmark timings on the local SQLite-backed dev run were approximately 248.864 ms average for `/api/posts/naive`, 24.718 ms for `/api/posts/optimized`, and 28.288 ms for `/api/posts/advanced`.
