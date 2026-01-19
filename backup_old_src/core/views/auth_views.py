"""
Authentication views.

Uses Django's built-in auth views - no custom logic needed.
Configuration handled in urls.py.
"""

# No code needed here - Django's built-in views handle everything
# LoginView expects: username + password POST to /login/
# LogoutView: GET to /logout/ clears session and redirects

# For custom logic post-MVP, override these views here
