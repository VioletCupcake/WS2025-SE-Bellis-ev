# Release Packaging Guide

## Manual Packaging Steps

From repository root:

```bash
cd /home/violet/repos/WS2025-SE-Bellis-ev

# Create clean copy
mkdir -p /tmp/B-EV-MVP
rsync -av --exclude='.git' \
          --exclude='venv' \
          --exclude='__pycache__' \
          --exclude='.env' \
          --exclude='*.pyc' \
          . /tmp/B-EV-MVP/

# Create zip
cd /tmp
zip -r B-EV-MVP-Submission.zip B-EV-MVP/
```

## What to Include

**Required:**
- Dockerfile (root)
- docker-compose.yml (root)
- entrypoint.sh (root)
- requirements.txt (root)
- INSTALLATION.txt (root)
- README.md (root)
- src/ (entire folder with fixtures/)

**Exclude:**
- .git/
- venv/
- __pycache__/
- .env (has credentials)
- test/
- *.pyc

## Quick Test

```bash
# Extract somewhere
cd /tmp
unzip B-EV-MVP-Submission.zip
cd B-EV-MVP

# Test build
docker compose up --build

# Check login works
# http://localhost:8002/login/
# user_admin / test123
```

## Checklist

- [ ] Fresh build works
- [ ] seed_data.json is included (src/core/fixtures/)
- [ ] .env is NOT included
- [ ] All three test users work
- [ ] INSTALLATION.txt is present
