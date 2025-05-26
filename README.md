FastAPI URL Shortener
Overview
This project is a URL shortener web application built using FastAPI. It allows users to generate short codes for long URLs, enabling easier sharing and management of links. The backend API handles URL shortening, redirection, and basic management of shortened URLs.

Features
Generate shortened URLs from long URLs.

Redirect short URLs to their corresponding original URLs.

Store URL mappings in a SQLite database.

Simple and clean REST API endpoints for interaction.

Designed for easy extension and integration with other services.

Technologies Used
Python 3.x

FastAPI — Web framework for building APIs

Uvicorn — ASGI server to run FastAPI app

SQLite — Database to store URL mappings

SQLAlchemy or equivalent ORM (if used)

Pydantic — Data validation and serialization

Installation and Setup
Prerequisites
Python 3.7 or higher installed on your system.

Git installed for cloning the repository.

Steps
Clone the repository:

bash
Copy
Edit
git clone https://github.com/dilshodazamjonov/Short_code_generator.git
cd Short_code_generator
Create a virtual environment and activate it:

bash
Copy
Edit
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
Install the required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the application:

bash
Copy
Edit
uvicorn app.main:app --reload
The API will be accessible at http://127.0.0.1:8000.

Usage
To shorten a URL, send a POST request to /shorten with the original URL in the request body.

Use the returned short code to access the original URL via redirection.

Access API documentation and test endpoints via Swagger UI at /docs.

Project Structure
bash
Copy
Edit
.
├── app
│   ├── main.py            # Application entry point
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas for request/response validation
│   ├── crud.py            # Database operations
│   ├── database.py        # Database connection setup
│   └── routers            # API routes
├── shortener.db           # SQLite database file
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
Contributing
Contributions and improvements are welcome. Please fork the repository, create a new branch for your changes, and open a pull request for review.

