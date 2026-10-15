# GreenBasket AI

GreenBasket AI is a smart grocery platform for Indian urban households seeking dependable, fresh, and personalized buying of fruits, vegetables, and daily essentials. The product combines digital grocery commerce with AI-assisted discovery, reorder support, freshness awareness, and engagement loops that encourage repeat purchasing while reducing shopping friction.

## Project Structure

```
green-basket/
├── backend/           # Python FastAPI backend
│   ├── app/          # Application code
│   │   ├── models/   # SQLAlchemy ORM models
│   │   ├── main.py   # FastAPI application entry point
│   │   ├── config.py # Configuration management
│   │   └── database.py # Database setup
│   ├── alembic/      # Database migrations
│   ├── tests/        # Backend tests
│   ├── Dockerfile    # Backend container image
│   └── pyproject.toml # Python dependencies
├── frontend/         # React + TypeScript + Vite frontend
│   ├── src/          # Frontend source code
│   ├── Dockerfile    # Frontend container image
│   └── package.json  # Node.js dependencies
├── .github/
│   └── workflows/
│       └── ci.yml    # GitHub Actions CI pipeline
├── start.sh          # Cross-platform startup script
├── stop.sh           # Graceful shutdown script
├── start.bat         # Windows wrapper (calls start.sh via Git Bash)
├── stop.bat          # Windows wrapper (calls stop.sh via Git Bash)
├── docker-compose.yml          # Default SQLite deployment
├── docker-compose.postgres.yml # PostgreSQL override
└── README.md         # This file
```

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Database**: SQLite (default), portable to PostgreSQL
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Authentication**: JWT with bcrypt
- **Frontend**: React + TypeScript + Vite
- **CI/CD**: GitHub Actions
- **Containerization**: Docker and Docker Compose

## Quick Start

### Prerequisites

- **Python 3.11+** — [Download Python](https://python.org)
- **Node.js 18+** — [Download Node.js](https://nodejs.org)
- **npm** (included with Node.js)
- **Git Bash** (Windows only) — [Download Git for Windows](https://git-scm.com/download/win)

### One-Command Startup (Recommended)

**macOS / Linux:**
```bash
./start.sh
```

**Windows:**
```batch
start.bat
```

This single script will:
1. ✓ Check prerequisites (Python 3.11+, Node.js 18+, npm)
2. ✓ Create Python virtual environment if missing
3. ✓ Install backend dependencies (`pip install .`)
4. ✓ Install frontend dependencies (`npm ci`)
5. ✓ Run database migrations (`alembic upgrade head`)
6. ✓ Seed database with demo data (if empty)
7. ✓ Detect available ports (default: backend 8000, frontend 5173)
8. ✓ Start backend and frontend concurrently
9. ✓ Print URLs and demo credentials

**Output example:**
```
==============================================
  GreenBasket AI - Running
==============================================

URLs:
  Frontend:  http://localhost:5173
  Backend:   http://localhost:8000
  API Docs:  http://localhost:8000/api/docs

Demo Credentials:
  Ananya (Shopper):
    Phone:    +919876543210
    Password: Demo@123

  Rohan (Operator):
    Phone:    +919876543220
    Password: Demo@123

Press Ctrl+C to stop all services
==============================================
```

### Stopping the Application

**macOS / Linux:**
```bash
./stop.sh
```

**Windows:**
```batch
stop.bat
```

Gracefully stops both backend and frontend services. The script:
- Sends SIGTERM to all services for graceful shutdown
- Waits up to 10 seconds for processes to exit
- Force kills any remaining processes after timeout
- Only stops services started by `start.sh` (uses `.pids` file)

### Setup Instructions

### Quick Start with Docker Compose

The fastest way to run the full application:

```bash
# Build and start all services (SQLite)
docker compose build
docker compose up -d

# View logs
docker compose logs -f

# Access the application
# - Frontend: http://localhost:80
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs

# Stop services
docker compose down
```

For PostgreSQL deployment:

```bash
# Build and start with PostgreSQL
docker compose -f docker-compose.yml -f docker-compose.postgres.yml build
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up -d

# Stop services
docker compose -f docker-compose.yml -f docker-compose.postgres.yml down
```

### Manual Local Development Setup

If you prefer to set up services manually instead of using `start.sh`:

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install .
   ```

4. Copy the development environment file:
   ```bash
   cp dev.env .env
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Seed the database:
   ```bash
   python seed_data.py
   ```

7. Start the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

8. Access the API documentation:
   - Swagger UI: http://localhost:8000/api/docs
   - ReDoc: http://localhost:8000/api/redoc

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   BACKEND_PORT=8000 npm run dev
   ```

4. Access the frontend:
   - Frontend: http://localhost:5173

## Database Schema

The application implements 19 database tables covering:

- **Customer Management**: customers, addresses
- **Catalog**: categories, products, farmers
- **Inventory**: inventory tracking with freshness
- **Shopping**: shopping_lists, shopping_list_items, recommendations
- **Orders**: orders, order_items, order_discounts
- **Fulfillment**: delivery_slots, delivery_agents, payments
- **Engagement**: reviews, notifications, promotions
- **Compliance**: audit_logs

All tables use prefix-based primary keys (cust-, addr-, ord-, prod-, etc.) and ISO 8601 timestamp format for portability between SQLite and PostgreSQL.

## Docker Deployment

### Backend Container

The backend Dockerfile:
- Uses Python 3.11-slim base image
- Installs PostgreSQL system dependencies (libpq-dev) for optional PostgreSQL support
- Runs multi-stage build with dependency installation
- Includes docker-entrypoint.sh that runs `alembic upgrade head` and seeds data before starting uvicorn
- Exposes port 8000
- Supports SQLite by default, PostgreSQL via `PIP_TARGET=".[postgres]"` build arg

### Frontend Container

The frontend Dockerfile:
- Uses Node 22 for build stage, nginx:alpine for serve stage
- Builds production assets with Vite
- Uses nginx.conf template with ${BACKEND_HOST} substitution
- Proxies `/api` requests to backend service at port 8000
- Serves SPA with fallback to index.html
- Exposes port 80
- Includes x-preview-port: 80 annotation for preview environments

### Docker Compose Services

**docker-compose.yml** (default SQLite):
- `backend`: FastAPI service with SQLite database in named volume `/data/app.db`
- `frontend`: Nginx-served React app with API proxy to backend
- Named volume `app-data` for SQLite persistence

**docker-compose.postgres.yml** (PostgreSQL override):
- `database`: PostgreSQL 16 service with health check
- `backend`: Overrides to use PostgreSQL connection string and install psycopg driver
- Named volume `postgres-data` for PostgreSQL persistence

## Environment Variables

See `.env.example` for all configurable environment variables.

Key variables:
- `DATABASE_URL`: Database connection string (default: sqlite:///./app.db)
- `JWT_SECRET`: Secret key for JWT token signing
- `JWT_EXPIRY_SECONDS`: JWT token lifetime in seconds
- `DEBUG`: Enable debug mode (true/false)

## Database Migrations

Create a new migration after model changes:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Check migration status:
```bash
alembic current
alembic history
```

## Seed Data

Populate the database with development data:
```bash
cd backend
python seed_data.py
```

The seed script creates:
- 2 customers (Ananya shopper, Rohan operator)
- 2 addresses for Ananya in Bengaluru (HSR Layout, Indiranagar)
- 6 product categories (Fruits, Vegetables, Dairy, Staples, Snacks, Beverages)
- 20+ products with nutrition data, tags, and farmer info
- Varied inventory stock levels with freshness dates
- 3 delivery slots (Morning, Afternoon, Evening) with 50 capacity each
- 2 promotions (FIRST10, LOYALTY50)
- Sample recommendations for Ananya
- 1 AI-generated shopping list
- Sample order with 3 items in delivered status
- Sample reviews and notifications

The script is idempotent and will skip seeding if data already exists.

### Demo Credentials

**Ananya Sharma (Shopper)**
- Phone: `+919876543210`
- Password: `Demo@123`
- Role: `shopper`
- Loyalty Points: 420
- Dietary Preference: Vegetarian
- Allergies: Peanuts

**Rohan Mehta (Operator)**
- Phone: `+919876543220`
- Password: `Demo@123`
- Role: `operator`

## Testing

### Local Test Commands

**Backend Tests:**
```bash
cd backend
pytest                                           # Run all tests
pytest -v                                        # Verbose output
pytest tests/unit/                               # Run unit tests only
pytest tests/integration/                        # Run integration tests only
pytest --junit-xml=test-results/backend-junit.xml  # Generate JUnit XML report
pytest --cov=app --cov-report=xml --cov-report=term  # Generate coverage report
```

**Frontend Tests:**
```bash
cd frontend
npm test                                         # Run all tests (watch mode)
npm test -- --run                                # Run tests once (CI mode)
CI=true npm test -- --run --reporter=junit --outputFile=test-results/frontend-junit.xml  # Generate JUnit XML report
npm test -- --run --coverage                     # Generate coverage report
```

**Linting:**
```bash
# Backend linting (ruff)
cd backend
ruff check app/ tests/                           # Run ruff linter
ruff check --select ALL app/ tests/              # Run all ruff rules

# Frontend linting (ESLint + TypeScript)
cd frontend
npm run lint                                     # Run ESLint
npx tsc --noEmit                                 # Run TypeScript type check
```

## CI/CD Pipeline

The GitHub Actions CI pipeline runs automatically on pushes to `main` and `develop` branches, and on pull requests targeting those branches.

### Pipeline Jobs

**1. lint-backend**
- Runs ruff linter on Python backend code
- Checks: `--select ALL` with specific exclusions for FastAPI patterns
- Fails on: Lint errors or critical warnings

**2. lint-frontend**
- Runs ESLint on TypeScript frontend code
- Runs TypeScript type checking with `tsc --noEmit`
- Fails on: Lint errors or type errors

**3. test-backend**
- Runs pytest with JUnit XML report generation
- Generates coverage reports (XML and terminal output)
- Writes test results to `test-results/backend-junit.xml`
- Uses SQLite test database
- Uploads test results and coverage as artifacts
- Fails on: Test failures or crashes

**4. test-frontend**
- Runs vitest with JUnit XML report generation using `--run` flag (no watch mode)
- Generates coverage reports using vitest coverage
- Writes test results to `test-results/frontend-junit.xml`
- Uses `CI=true` environment variable for non-interactive mode
- Uploads test results and coverage as artifacts
- Fails on: Test failures or crashes

**5. build-containers**
- Builds backend Docker image
- Builds frontend Docker image
- Tests `docker compose build` for full stack
- Fails on: Build failures or Dockerfile errors

**6. security-scan**
- Runs `pip-audit` for Python dependency vulnerabilities
- Runs `npm audit --audit-level=high` for Node.js dependency vulnerabilities
- Runs Trivy container scans on backend and frontend for CRITICAL and HIGH severity vulnerabilities
- Currently configured with `exit-code: 0` (does not fail the build, only reports)
- Fails on: Critical vulnerabilities (when exit code is set to 1)

### Pipeline Triggers

- **Push to main/develop**: Runs full pipeline
- **Pull request to main/develop**: Runs full pipeline for the PR branch

### Viewing Pipeline Results

1. Navigate to the **Actions** tab in GitHub repository
2. Select the workflow run you want to view
3. Click on individual job names to see logs
4. Download artifacts (test results, coverage reports) from the artifacts section

### Local CI Simulation

To run the same checks locally before pushing:

```bash
# Backend checks
cd backend
ruff check --select ALL --ignore D,ANN,COM,T201,S101,DTZ003,RUF059,BLE001 app/ tests/
pytest --junit-xml=test-results/backend-junit.xml --cov=app --cov-report=xml

# Frontend checks
cd frontend
npm run lint
npx tsc --noEmit
npm test -- --run --reporter=junit --outputFile=test-results/frontend-junit.xml --coverage

# Container checks
docker compose build
```

## Container Verification

Verify backend Dockerfile includes pyproject.toml (not excluded by .dockerignore):
```bash
grep -v "^#" backend/.dockerignore | grep -v "^$" | grep -q "pyproject.toml" && echo "EXCLUDED" || echo "INCLUDED"
```

Verify frontend Dockerfile includes package.json and package-lock.json:
```bash
grep -v "^#" frontend/.dockerignore | grep -v "^$" | grep -q "package.json" && echo "EXCLUDED" || echo "INCLUDED"
grep -v "^#" frontend/.dockerignore | grep -v "^$" | grep -q "package-lock.json" && echo "EXCLUDED" || echo "INCLUDED"
```

Verify backend entrypoint runs alembic upgrade head:
```bash
grep -q "alembic upgrade head" backend/docker-entrypoint.sh && echo "FOUND" || echo "MISSING"
```

Verify frontend nginx.conf proxies /api to backend:8000:
```bash
grep -q "proxy_pass.*backend:8000" frontend/nginx.conf && echo "FOUND" || echo "MISSING"
```

Verify docker-compose.yml uses SQLite:
```bash
grep -q "DATABASE_URL.*sqlite:////data/app.db" docker-compose.yml && echo "FOUND" || echo "MISSING"
```

Verify frontend service has x-preview-port annotation:
```bash
grep -q "x-preview-port: 80" docker-compose.yml && echo "FOUND" || echo "MISSING"
```

## License

Proprietary - GreenBasket AI
