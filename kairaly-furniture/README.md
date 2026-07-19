# Kairaly Furniture — Sofa Catalog (MVP)

A full-stack catalog system for a furniture business with two branches
(**Choondi** and **Tripunithura**). This MVP covers **sofas only**.

The backend (FastAPI + SQLAlchemy) is the focus of this project — a complete,
production-structured REST API, database, and admin authentication system.
The frontend is intentionally minimal (plain HTML/JS, no build step) since
the UI will be rebuilt separately in Stitch.

---

## 1. Core Business Rule

> A customer standing inside one branch only wants to see what's available at
> the **other** branch (they can already see what's in front of them).

So:
- Customer selects **Choondi** → catalog shows sofas stocked at **Tripunithura**
- Customer selects **Tripunithura** → catalog shows sofas stocked at **Choondi**

This is implemented in `GET /api/v1/products?visiting_branch=Choondi`, which
resolves the visiting branch and excludes it from the results
(`app/crud/product.py::list_products`, `exclude_branch_id` filter).

Stock rule:
- `stock_count > 0` → **"In Stock"**
- `stock_count == 0` → product still shown, labeled **"Made to Order"**
  (the workshop can manufacture it on demand)

This is a computed field (`stock_status`) returned by the API, not a stored
column — so it's always accurate and can't drift out of sync with stock_count.

---

## 2. Project Structure

```
kairaly-furniture/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entrypoint
│   │   ├── config.py            # Environment-based settings
│   │   ├── database.py          # SQLAlchemy engine/session
│   │   ├── seed.py              # Seeds branches + admin user + sample sofas
│   │   ├── models/               # SQLAlchemy ORM models (DB schema)
│   │   │   ├── branch.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   └── product_image.py
│   │   ├── schemas/               # Pydantic request/response models + validation
│   │   │   ├── branch.py
│   │   │   ├── user.py
│   │   │   ├── auth.py
│   │   │   ├── product.py
│   │   │   └── product_image.py
│   │   ├── crud/                  # DB access + business logic layer
│   │   │   ├── branch.py
│   │   │   ├── user.py
│   │   │   └── product.py
│   │   ├── core/
│   │   │   └── security.py       # Password hashing + JWT
│   │   └── api/
│   │       ├── deps.py           # Auth dependency (get_current_admin)
│   │       └── routes/
│   │           ├── auth.py           # POST /auth/login
│   │           ├── branches.py       # GET /branches
│   │           ├── products.py       # Public catalog (browse + detail)
│   │           └── admin_products.py # Admin CRUD, stock, image upload
│   ├── static/uploads/           # Uploaded product images served at /static/uploads/...
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html                # Customer catalog (branch select → browse → detail)
│   ├── admin.html                # Admin login + product management
│   └── config.js                 # Points the frontend at your backend URL
└── README.md
```

### Database schema (normalized)

| Table            | Purpose                                                        |
|-------------------|------------------------------------------------------------------|
| `branches`        | Choondi, Tripunithura                                          |
| `users`           | Admin accounts only (customers never log in)                   |
| `products`        | Sofas — pricing, stock, dimensions, materials, branch (FK)     |
| `product_images`  | One-to-many images per product (FK to `products`)              |

All foreign keys use `ON DELETE CASCADE` where appropriate (deleting a
product removes its images; deleting a branch removes its products).
Price and stock have DB-level `CHECK` constraints (`>= 0`) in addition to
Pydantic-level validation.

---

## 3. Setup & Run

### Requirements
- Python 3.11+
- (Optional) PostgreSQL — SQLite is used automatically if you don't configure one

### Steps

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # then edit .env if needed (see below)

# Creates tables, the two branches, a default admin user, and sample sofas
python -m app.seed

# Start the API
uvicorn app.main:app --reload
```

The API is now live at **http://localhost:8000**
Interactive docs (Swagger UI): **http://localhost:8000/docs**

### Default admin login (from `.env.example`)
```
username: admin
password: change_this_password
```
**Change these in `.env` before deploying anywhere real.**

### Running the frontend
The frontend is static — no build step. Just open the files directly, or serve them:
```bash
cd frontend
python3 -m http.server 5500
# visit http://localhost:5500/index.html  (customer catalog)
# visit http://localhost:5500/admin.html  (admin panel)
```
If your backend runs somewhere other than `localhost:8000`, update
`frontend/config.js`.

### Switching to PostgreSQL
Edit `.env`:
```
DATABASE_URL=postgresql://kairaly_user:kairaly_pass@localhost:5432/kairaly_db
```
Then re-run `python -m app.seed` to create tables against the new database.

---

## 4. Environment Variables (`.env`)

| Variable                     | Description                                      |
|-------------------------------|--------------------------------------------------|
| `DATABASE_URL`                 | SQLAlchemy connection string                    |
| `SECRET_KEY`                   | JWT signing secret — set a long random value in prod |
| `ALGORITHM`                    | JWT algorithm (default `HS256`)                 |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | Admin session length                            |
| `DEFAULT_ADMIN_USERNAME/PASSWORD/EMAIL` | Used only by `app/seed.py`             |
| `UPLOAD_DIR`                   | Where product images are stored on disk         |
| `MAX_IMAGE_SIZE_MB`            | Per-image upload limit                          |
| `CORS_ORIGINS`                 | Comma-separated allowed origins (`*` for dev)   |

---

## 5. API Reference

Base URL: `/api/v1`

### Public (no auth)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/branches` | List branches (for the home page buttons) |
| GET | `/products` | Browse catalog — see query params below |
| GET | `/products/{id}` | Full sofa detail page |

**`GET /products` query params:**
- `visiting_branch` (name) or `visiting_branch_id` — **required for correct branch logic**; returns sofas from the *other* branch
- `search` — search by product name
- `min_price`, `max_price`
- `fabric`, `foam_type`
- `sort` — `newest` | `oldest` | `price_low_to_high` | `price_high_to_low`
- `page`, `page_size`

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/login` | OAuth2 form login (`username`, `password`) → JWT bearer token |

### Admin (JWT bearer token required)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/admin/products` | List ALL products, both branches (management view) |
| POST | `/admin/products` | Create a sofa |
| PUT | `/admin/products/{id}` | Edit a sofa (partial updates supported) |
| PATCH | `/admin/products/{id}/stock` | Update stock count only |
| DELETE | `/admin/products/{id}` | Delete a sofa |
| POST | `/admin/products/{id}/images` | Upload one or more images (multipart) |
| DELETE | `/admin/products/{id}/images/{image_id}` | Delete a single image |

Full request/response schemas, including all sofa spec fields (dimensions,
seating capacity, foam thickness/type, fabric, frame material, warranty,
available colors, etc.), are documented interactively at `/docs`.

---

## 6. Design Notes

- **Why exclude-branch instead of a fixed "other branch" mapping?** The query
  logic (`exclude_branch_id`) generalizes automatically to any number of
  branches later — it isn't hardcoded to "if Choondi then Tripunithura."
- **Stock status is computed, not stored** — avoids a second source of truth
  that could get out of sync with `stock_count`.
- **Images** are stored on disk under `static/uploads/` with UUID filenames
  and served at `/static/uploads/<file>`; `ProductImage` rows track order and
  which image is primary (shown in listings).
- **Customers never authenticate** — by design, there is no customer
  registration/login table or endpoint. Only admins hold accounts.
- **Validation** happens at both the Pydantic layer (type/range checks, e.g.
  price > 0, stock >= 0) and the database layer (`CHECK` constraints), so bad
  data can't get in even via a direct DB script.

## 7. Next Steps (post-MVP ideas)
- Alembic migrations for schema changes in production (Alembic is already in `requirements.txt`)
- Refresh tokens / logout-all for admin sessions
- Additional product categories beyond sofas (the `category` column on `Product` is already there for this)
- Rate limiting on the login endpoint
