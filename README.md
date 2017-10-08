# Parker — The Parking Helper #

#### Pre-run Checklist ####
- `pip install -r requirements.txt` (assuming pwd is root of this project)
- `SECRET_KEY` environment variable (large random string)
- PostgreSQL instance with environments variables:
  - `DATABASE_NAME`
  - `DATABASE_USER`
  - `DATABASE_PASSWORD`
  - `DATABASE_HOST` (if ommitted, uses Unix domain sockets)
  - `DATABASE_PORT` (if ommitted, uses PostgreSQL default port)
