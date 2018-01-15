# Parker — The Parking Helper #

#### Pre-run Checklist ####
- `pip install -r requirements.txt` (assuming pwd is root of this project)
- `SECRET_KEY` environment variable (large random string)
- `DEBUG` environment variable (set to 'true' to enable debug mode)
- `ALLOWED_HOSTS` environment variable (comma-separated strings)
- PostGIS (`brew install postgis`) or using instructions at https://postgis.net/install/
- PostgreSQL instance with environments variables: (required by PostGIS)
  - `DATABASE_NAME`
  - `DATABASE_USER`
  - `DATABASE_PASSWORD`
  - `DATABASE_HOST` (if ommitted, uses Unix domain sockets)
  - `DATABASE_PORT` (if ommitted, uses PostgreSQL default port)
- Activate PostGIS plugin
