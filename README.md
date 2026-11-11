# IS601 Module 9 — Raw SQL in pgAdmin

Starter project built to match the assignment screenshot: FastAPI + PostgreSQL + pgAdmin via Docker Compose. SQL commands intentionally run **inside pgAdmin** so you can capture authentic results for the assignment.

## Before you begin

- Install / open Docker Desktop (wait until the Docker engine is running).
- Open the project folder in Visual Studio Code.
- Open **Terminal > New Terminal** in VS Code.
- Make sure your terminal is in the folder containing `docker-compose.yml`.

## 1. Start the project

```powershell
docker --version
docker compose version
docker compose up --build -d
docker compose ps
```

You should see the **db**, **app**, and **pgadmin** services Up. First startup downloads Docker images and can be slower. If a service stops, inspect logs with `docker compose logs --tail=70`.

## 2. Open app and pgAdmin

- FastAPI: http://localhost:8000
- FastAPI docs: http://localhost:8000/docs
- Database connection test: http://localhost:8000/health
- pgAdmin: http://localhost:5050

pgAdmin login:
- Email: `admin@example.com`
- Password: `admin123`

A PostgreSQL server named **Module 9 PostgreSQL** may already appear. Click it and enter database password `postgres` when asked.

If the server isn't listed: Servers > Register > Server:
- General / Name: `Module 9 PostgreSQL`
- Connection / Host name/address: `db` (NOT `localhost`)
- Port: `5432`
- Maintenance database: `fastapi_db`
- Username: `postgres`
- Password: `postgres`
- Save.

Find **Servers > Module 9 PostgreSQL > Databases > fastapi_db**.
Right-click `fastapi_db` and click **Query Tool**.

## 3. Run the assignment's SQL in order

The provided scripts are copies of the assignment's SQL. **Run once and in order**:

1. `sql/01_create_tables.sql`: create `users` and `calculations`.
2. `sql/02_insert_records.sql`: insert Alice, Bob, and three calculations.
3. `sql/03_query_data.sql`: execute each SELECT on its own, screenshot result.
4. `sql/04_update_record.sql`: execute UPDATE, then SELECT separately, screenshot both.
5. `sql/05_delete_record.sql`: execute DELETE, then SELECT separately, screenshot both.

**How to execute:** in VS Code open the `.sql` file, copy the SQL, and paste into the pgAdmin Query Tool editor. To show output for one command at a time, select/highlight the exact statement you want, then press Execute (lightning bolt or F5). Capture screenshots with Snipping Tool (Windows: `Win + Shift + S`).

### Expected data after insert

`users`: Alice / Bob. `calculations`: add 2+3=5 (Alice), divide 10/2=5 (Alice), multiply 4×5=20 (Bob).

After the update, the stored result for calculation ID 1 becomes 6 (even though 2 + 3 = 5); this intentionally demonstrates UPDATE and is **not** a corrected arithmetic calculation. After DELETE, calculation ID 2 no longer appears.

If you run an INSERT twice, you'll get duplicate username errors. Do not rerun CREATE or INSERT once they succeeded. If an ID is not 1 or 2, adjust the WHERE clause based on the actual ID in your SELECT results.

## 4. Document evidence and submit

Save screenshots of commands and their pgAdmin results (and `docker compose ps`). Put them in Word or PDF with short captions. Add your reflection and GitHub repository link. See `SCREENSHOT_CHECKLIST.md` and `REFLECTION_TEMPLATE.md`.

## 5. Publish to GitHub

In VS Code terminal (one time, if this isn't already a Git repository):

```powershell
git init
git add .
git commit -m "Complete Module 9 SQL and Docker setup"
```

Create a **new empty repository** on GitHub, then use the repo-specific `git remote add origin ...`, `git branch -M main`, and `git push -u origin main` commands that GitHub displays. Include your real repository URL in your submission.

## Helpful commands

```powershell
docker compose ps
docker compose logs --tail=70
docker compose down
**Important:** `docker compose down` stops services but preserves database volume data. Don't run `docker compose down -v` unless you intentionally want to **erase** database records.

**Security:** The sample usernames and passwords are only for this local coursework demonstration. Never use these credentials for a production or publicly exposed application.

PostgreSQL is published on host port 5433 to reduce conflict with locally installed PostgreSQL; inside Docker, pgAdmin and FastAPI still connect to `db:5432`.

## Module 10: Secure User Model and CI/CD

This module extends the existing FastAPI calculator with secure user creation, PostgreSQL storage, Pydantic input/output validation, Argon2 password hashing, automated tests, a GitHub Actions security scan, and Docker Hub deployment.

### Requirements

- Docker Desktop and Docker Compose
- A `.env` file in the project root containing `POSTGRES_PASSWORD=<your-local-password>` (do not commit your `.env` file)

### Run the application locally

From the project root:

```powershell
docker compose up -d --build
```

Then open `http://localhost:8000/docs` to try the FastAPI endpoints. Use `POST /users` to create a user; the response should not include a password or password hash.

### Run the tests

With the containers running:

```powershell
docker compose exec app python -m pytest -v
```

The Module 10 test suite includes unit tests for password hashing and Pydantic validation plus PostgreSQL integration tests for user creation, uniqueness, and lookup.

### Docker Hub

Docker image: https://hub.docker.com/r/hkasunmu/is601-fastapi-module10

Pull the published image:

```powershell
docker pull hkasunmu/is601-fastapi-module10:latest
```

The running API requires a PostgreSQL database and an appropriate `DATABASE_URL` environment variable; the repository's Docker Compose setup supplies this for local development. Pulling the image alone does not start a configured database.

### CI/CD

The `.github/workflows/module10.yml` workflow runs automated tests against PostgreSQL, builds the Docker image, scans it with Trivy, and pushes the image to Docker Hub after successful checks. Docker Hub credentials are stored in GitHub Actions secrets/variables, not in the repository.
