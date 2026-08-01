# 📝 FastAPI Blog

A full-stack blog application built with **FastAPI** and **Jinja2**, featuring async SQLite persistence, JWT authentication, image uploads, and a server-rendered frontend.

---

## 📖 Overview

FastAPI Blog is a modern, fully asynchronous web application that serves both a **REST API** (`/api/...`) and **server-rendered HTML pages**. Users can register, log in, create and manage blog posts, upload profile pictures, and browse posts with infinite-scroll pagination.

### Key Features

- **User Management** — Registration, login, profile updates, and account deletion
- **Blog Posts** — Full CRUD with ownership enforcement (only authors can edit/delete)
- **Profile Pictures** — Upload, resize (300×300), and auto-convert to optimised JPEG
- **JWT Authentication** — Stateless Bearer-token auth via OAuth2
- **Pagination** — Cursor-based "load more" for both API and HTML pages
- **Server-Side Rendering** — Jinja2 templates with a shared layout
- **Custom Error Pages** — HTML error pages for browser clients, JSON for API clients
- **Async Everything** — Fully async database operations with SQLAlchemy + aiosqlite

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance async web framework with auto-generated OpenAPI docs |
| **Server** | [Uvicorn](https://www.uvicorn.org/) (via `fastapi[standard]`) | ASGI server for running the application |
| **Language** | Python 3.12+ | Modern Python with type hints |
| **Database** | SQLite | Lightweight relational database (file: `blog.db`) |
| **Async DB Driver** | [aiosqlite](https://github.com/omnilib/aiosqlite) | Async SQLite driver for non-blocking database access |
| **ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (async) | Async ORM with `Mapped` type annotations and `AsyncSession` |
| **Templating** | [Jinja2](https://jinja.palletsprojects.com/) | Server-side HTML template rendering |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev/) | Request/response schema validation and serialization |
| **Configuration** | [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Type-safe settings loaded from `.env` file |
| **Authentication** | [PyJWT](https://pyjwt.readthedocs.io/) | JWT token creation and verification |
| **Password Hashing** | [pwdlib](https://github.com/frankie567/pwdlib) (Argon2) | Secure password hashing using the Argon2 algorithm |
| **Image Processing** | [Pillow](https://pillow.readthedocs.io/) | Profile picture resizing, format conversion, and EXIF handling |
| **Package Manager** | [uv](https://docs.astral.sh/uv/) | Fast Python package manager and project tool |

---

## 🏗 Project Structure

```
fastapi_blog/
├── main.py              # Application entry point, lifespan, page routes, error handlers
├── database.py          # Async engine, session factory, Base class
├── models.py            # SQLAlchemy models (User, Post)
├── schemas.py           # Pydantic request/response schemas
├── auth.py              # JWT creation/verification, password hashing, auth dependencies
├── config.py            # Settings loaded from .env (secret key, algorithm, limits)
├── image_utils.py       # Profile picture processing (resize, convert, save)
├── populate_db.py       # Database seeder with sample data
├── routers/
│   ├── users.py         # User API endpoints (CRUD, auth, profile pictures)
│   └── posts.py         # Post API endpoints (CRUD, pagination)
├── templates/
│   ├── layout.html      # Base template with shared navigation and styles
│   ├── home.html        # Homepage with post listing
│   ├── post.html        # Single post detail page
│   ├── user_posts.html  # Posts filtered by author
│   ├── login.html       # Login form
│   ├── register.html    # Registration form
│   ├── account.html     # Account management page
│   └── error.html       # Custom error page
├── static/              # CSS, JS, icons, default profile picture
├── media/               # Uploaded profile pictures (runtime generated)
├── pyproject.toml       # Project metadata and dependencies
└── .env                 # Environment variables (SECRET_KEY)
```

---

## 🔌 API Reference

All API endpoints are prefixed with `/api` and return JSON. Interactive docs are available at `/docs` (Swagger UI) and `/redoc`.

### Users — `/api/users`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/users` | ✗ | Register a new user |
| `POST` | `/api/users/token` | ✗ | Login and receive a JWT access token |
| `GET` | `/api/users/me` | ✓ | Get the current authenticated user |
| `GET` | `/api/users/{user_id}` | ✗ | Get a user by ID |
| `PATCH` | `/api/users/{user_id}` | ✓ | Update username or email (owner only) |
| `DELETE` | `/api/users/{user_id}` | ✓ | Delete a user account (owner only) |
| `GET` | `/api/users/{user_id}/posts` | ✗ | Get paginated posts by a specific user |
| `PATCH` | `/api/users/{user_id}/picture` | ✓ | Upload a profile picture (owner only) |
| `DELETE` | `/api/users/{user_id}/picture` | ✓ | Remove profile picture (owner only) |

### Posts — `/api/posts`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/posts` | ✗ | Get paginated list of all posts |
| `POST` | `/api/posts` | ✓ | Create a new post |
| `GET` | `/api/posts/{post_id}` | ✗ | Get a single post by ID |
| `PUT` | `/api/posts/{post_id}` | ✓ | Full update of a post (author only) |
| `PATCH` | `/api/posts/{post_id}` | ✓ | Partial update of a post (author only) |
| `DELETE` | `/api/posts/{post_id}` | ✓ | Delete a post (author only) |

### HTML Pages

| Route | Description |
|---|---|
| `/` or `/posts` | Homepage — latest posts with infinite scroll |
| `/posts/{post_id}` | Single post detail view |
| `/users/{user_id}/posts` | Posts by a specific author |
| `/login` | Login page |
| `/register` | Registration page |
| `/account` | Account management page |

---

## ⚙️ Getting Started

### Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd fastapi_blog
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Create a `.env` file** in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   ```

4. **Run the development server**
   ```bash
   source .venv/bin/activate
   fastapi dev main.py
   ```

5. **Open in your browser**
   - App: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Seed the Database (Optional)

Populate the database with sample users and posts:

```bash
python populate_db.py
```

---

## 🔧 Configuration

All settings are managed via environment variables (loaded from `.env`):

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | *required* | Secret key used for JWT signing |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiry duration in minutes |
| `max_upload_size_bytes` | `5242880` (5 MB) | Maximum profile picture upload size |
| `post_per_page` | `5` | Number of posts per page/API response |

---

## 🔐 Authentication Flow

1. **Register** — `POST /api/users` with username, email, and password
2. **Login** — `POST /api/users/token` with email and password → receive a JWT
3. **Access Protected Routes** — Include the token in the `Authorization: Bearer <token>` header
4. Tokens expire after 30 minutes (configurable)
5. Passwords are hashed with **Argon2** (via pwdlib) — never stored in plain text
