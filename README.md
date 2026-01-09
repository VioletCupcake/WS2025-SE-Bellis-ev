<div align="center">

  <h1>B-EV Case Management System</h1>
  <p><strong>Bellis e.V. — MVP for SE2025</strong></p>
  
  <p>
    A case management system for documenting and tracking cases of violence against women.
  </p>

</div>

---

## Table of Contents

- [Quick Start (Docker)](#-quick-start-docker)
- [Test Accounts](#-test-accounts)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Local Development](#-local-development)
- [Environment Variables](#-environment-variables)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🐳 Quick Start (Docker)

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine with Compose plugin.

```bash
# 1. Clone the repository
git clone <repository-url>
cd WS2025-SE-Bellis-ev

# 2. Start the application
docker compose up --build

# 3. Open in browser
# http://localhost:8002/login/
```

**That's it.** Docker handles PostgreSQL, migrations, and test data automatically.

### Stopping the Application

```bash
# Stop containers (keeps data)
docker compose down

# Stop and DELETE all data (fresh start)
docker compose down -v
```

---

## 👤 Test Accounts

All accounts use password: **`test123`**

| Username | Role | Permissions |
|----------|------|-------------|
| `user_basis` | BASIS | View & edit cases |
| `user_erweitert` | ERWEITERT | + Delete cases, manage reference data |
| `user_admin` | ADMIN | + Manage users, hard delete, full access |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.12, Django 5.0 |
| **Database** | PostgreSQL 15 |
| **Frontend** | Django Templates, HTML/CSS |
| **Deployment** | Docker, Docker Compose |

---

## ✨ Features

- **Case Management**: Create, view, edit, and delete cases (Fall)
- **Multi-step Forms**: Guided case creation with validation
- **Role-based Access Control**: Three-tier permission system
- **Consultation Tracking**: Document counseling sessions (Beratung)
- **Violence Documentation**: Record incidents with categorization (Gewalttat)
- **German Localization**: Date formats, labels, and UI in German

---

## 💻 Local Development

*For development without Docker (requires local PostgreSQL):*

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 4. Run migrations and seed data
cd src
python manage.py migrate
python manage.py loaddata core/fixtures/seed_data.json

# 5. Start development server
python manage.py runserver 8002
```

---

## 🔑 Environment Variables

See [.env.example](.env.example) for all options.

| Variable | Docker Value | Local Default |
|----------|--------------|---------------|
| `DB_HOST` | `db` (service name) | `localhost` |
| `DB_NAME` | `bev_dev` | `bev_dev` |
| `DB_USER` | `bev_user` | `bev_user` |
| `DB_PASSWORD` | `SE2025.bellis` | *(set in .env)* |
| `DB_PORT` | `5432` | `5432` |
| `DEBUG` | `True` | `True` |

**Note:** When using Docker Compose, environment variables are set in `docker-compose.yml` and override any `.env` file. No separate `.env.docker` is needed.

---

## 🔧 Troubleshooting

### Docker Deployment

| Issue | Cause | Solution |
|-------|-------|----------|
| Port 8002 in use | Another service running | `docker compose down` or change port in `docker-compose.yml` |
| Database connection timeout | PostgreSQL not ready | Container retries automatically; check `docker logs bev-postgres` |
| Permission denied on entrypoint.sh | File not executable | `chmod +x entrypoint.sh` and rebuild |
| "No such container" | Containers not started | Run `docker compose up --build` |
| Data not persisting | Volume deleted | Only use `docker compose down -v` for fresh start |

### Application

| Issue | Cause | Solution |
|-------|-------|----------|
| Login fails | Wrong password | Password is `test123` for all test users |
| 403 Forbidden | CSRF or permission | Clear cookies, re-login |
| "No cases found" | First run | Create a new case via "Neuer Fall" |
| Form validation errors | Required fields | Check German field labels for requirements |
| Date format rejected | Wrong format | Use `DD.MM.YYYY` (German) or `YYYY-MM-DD` |

### Invariants

**Docker Deployment:**
- Container `bev-postgres` must be healthy before `bev-django` starts
- Migrations run on every container start (idempotent)
- Seed data loads only if user count = 0

**Application:**
- All users must have exactly one Role
- Each Role has exactly one PermissionSet
- Cases (Fall) require valid PersonenbezogeneDaten
- Deleted cases are soft-deleted by default (unless hard delete permission)

---

## 📋 Project Structure

```
WS2025-SE-Bellis-ev/
├── docker-compose.yml    # Orchestration
├── Dockerfile            # Django container
├── entrypoint.sh         # Startup script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── src/
│   ├── manage.py
│   ├── B_EV/             # Django project settings
│   └── core/             # Main application
│       ├── models/       # Database models
│       ├── views/        # Request handlers
│       ├── forms/        # Form definitions
│       ├── templates/    # HTML templates
│       └── fixtures/     # Seed data
└── docs/                 # Documentation
```

---

## 📄 License

See [LICENSE](LICENSE) for details.

---

## 👥 Team

SE2025 Project Team — Bellis e.V. Case Management System

