# GITHUB WORKFLOW FOR B-EV PROJECT

## What is GitHub?
- Cloud-based Git repository hosting
- Collaboration platform for code
- Version control system

## Core Concepts

### Repository (Repo)
- Container for project files and history
- B-EV repo: https://github.com/VioletCupcake/WS2025-SE-Bellis-ev/

### Branches
- Parallel versions of code
- main: Production-ready code
- cleanup: Current working branch
- Feature branches: Individual work streams

Visualization:
main      ──●────●────●────●──
              ╲
cleanup        ●──●──●──●
                    ╲
feature/auth         ●──●

### Commits
- Snapshots of changes
- Each has unique ID and message
- Best practice: Small, focused commits

## Essential Git Commands

### Clone Repository (First Time)
git clone https://github.com/VioletCupcake/WS2025-SE-Bellis-ev.git
cd WS2025-SE-Bellis-ev

### Check Current Branch
git branch
# * indicates active branch

### Switch to cleanup Branch
git checkout cleanup

### Pull Latest Changes (Before Starting Work)
git pull origin cleanup

### Create New Feature Branch
git checkout -b feature/your-feature-name

### Check Status
git status
# Shows modified, added, deleted files

### Stage Changes
git add .                    # Stage all changes
git add Core/models.py       # Stage specific file

### Commit Changes
git commit -m "Add Case model with alias field"

### Push to GitHub
git push origin feature/your-feature-name

## Pull Request (PR) Workflow

1. Create feature branch locally
2. Make changes and commit
3. Push branch to GitHub
4. On GitHub: Click "New Pull Request"
5. Select base: cleanup, compare: feature/your-feature-name
6. Add description explaining changes
7. Request review from team
8. Address feedback
9. Merge when approved

## Common Workflow Pattern

# Day 1: Start work
git checkout cleanup
git pull origin cleanup
git checkout -b feature/add-beratung-model

# Make changes to files

git add .
git commit -m "Add Beratung model with ForeignKey to Case"
git push origin feature/add-beratung-model

# Create PR on GitHub

# Day 2: Continue after feedback
git checkout feature/add-beratung-model
git pull origin feature/add-beratung-model

# Make requested changes

git add .
git commit -m "Update Beratung model: add validation"
git push origin feature/add-beratung-model

# PR gets merged

git checkout cleanup
git pull origin cleanup
git branch -d feature/add-beratung-model  # Delete local branch

## VSCode Git Integration

- Source Control panel (Ctrl+Shift+G)
- Visual diff viewer
- Built-in merge conflict resolution
- GitLens extension recommended

## Best Practices for B-EV Team

1. Always pull before starting work
2. Create feature branches for each task
3. Commit messages: Start with verb (Add, Fix, Update, Remove)
4. Push frequently (at least daily)
5. Keep PRs focused (one feature/fix per PR)
6. Review each other's code
7. Never commit to main directly
