# FastAPI URL Shortener

A simple URL shortener built with FastAPI. This project allows you to create shortened URLs that redirect to the original long URLs.

## Features

- Create short URLs from long URLs via API
- Redirect short URLs to original URLs
- Persistent storage using SQLite database
- FastAPI-powered RESTful API with automatic interactive docs

## Getting Started

### Prerequisites

- Python 3.7 or newer
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dilshodazamjonov/Short_code_generator.git
   cd Short_code_generator
   
2. Create virtual enviornment

  ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload
```

3. Project Structure look like this
  
  ```terminal
  .
  ├── app
  │   ├── main.py          # FastAPI application entry point
  │   ├── models.py        # Database models
  │   ├── schemas.py       # Request and response data validation schemas
  │   ├── crud.py          # Database operations
  │   ├── database.py      # Database connection configuration
  │   └── routers          # API route definitions
  ├── shortener.db         # SQLite database file
  ├── requirements.txt     # Project dependencies
  └── README.md            # Project documentation
```

## Contributing

Contributions are welcome. Feel free to fork the repository and submit pull requests.
