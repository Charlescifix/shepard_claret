# Shepard Claret Data Collection

Shepard Claret is a data collection web application designed for educational institutions. It uses FastAPI for the backend, SQLAlchemy for PostgreSQL database interactions, and Jinja2 templates for a clean, responsive frontend. The application is pre-configured for deployment on Railway, with the flexibility to migrate to other cloud providers as needed.

## Features

- **Data Collection:** Capture user details including first name, last name, email, role, and date joined.
- **API Endpoints:** 
  - Create users via `/users/`
  - Query total user count via `/users/count`
- **Frontend:** Uses Jinja2 templates and static files to render a modern UI.
- **Deployment Ready:** Includes a Procfile for Railway deployment and SSL/TLS via environment configurations.


