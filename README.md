# 📝 FastAPI Todo Application

A full-stack Todo application built with **FastAPI**, featuring secure JWT authentication, PostgreSQL database integration, server-side rendering with Jinja2 templates, and complete CRUD functionality.

This project demonstrates backend engineering fundamentals including authentication, database modeling, API design, template rendering, and full-stack integration.

---

# 🚀 Features

## 🔐 Authentication & Authorization

* User Registration
* Secure Login with JWT Authentication
* Password hashing using bcrypt
* Protected routes using dependency injection
* User-specific todo access (data isolation)

## ✅ Todo Management (CRUD)

* Create new todos
* View all user-specific todos
* Update existing todos (PUT requests)
* Delete todos
* Status tracking (Completed / Not Completed)

## 🖥 Frontend Integration

* Jinja2 templating
* HTML forms with proper method handling
* Bootstrap-based UI styling
* Form validation handling

## 🗄 Database

* PostgreSQL integration
* SQLAlchemy ORM models
* Relationship between Users and Todos
* Proper session management

---

# 🛠 Tech Stack

### Backend

* FastAPI
* Python
* SQLAlchemy
* PostgreSQL
* Passlib (bcrypt)
* Python-JOSE (JWT)

### Frontend

* HTML
* CSS
* Bootstrap
* Jinja2 Templates

### Development Tools

* Uvicorn
* Postman (API testing)
* Git & GitHub

---

# 📂 Project Structure

```
project/
│
├── main.py
├── database.py
├── models.py
├── routers/
│   ├── auth.py
│   ├── users.py
│   └── todos.py
├── templates/
│   ├── layout.html
│   ├── register.html
│   ├── login.html
│   ├── todos.html
│   └── edit-todo.html
└── static/
```

---

# 🔄 API Endpoints Overview

This application follows a modular router structure with separate routes for Authentication, User Todos, and Admin operations.

---

## 🔐 Authentication Routes (`/auth`)

| Method | Endpoint              | Description               |
| ------ | --------------------- | ------------------------- |
| GET    | `/auth/login-page`    | Render login page         |
| GET    | `/auth/register-page` | Render registration page  |
| POST   | `/auth/create_user`   | Create new user           |
| POST   | `/auth/token`         | Generate JWT access token |

---

## ✅ User Todo Routes (`/todos`)

### 📄 Page Rendering Routes

| Method | Endpoint                          | Description                |
| ------ | --------------------------------- | -------------------------- |
| GET    | `/todos/todo-page`                | Render main todo dashboard |
| GET    | `/todos/add-todo-page`            | Render add todo page       |
| GET    | `/todos/edit-todo-page/{todo_id}` | Render edit todo page      |

### 📦 CRUD API Routes

| Method | Endpoint                       | Description                   |
| ------ | ------------------------------ | ----------------------------- |
| GET    | `/todos/`                      | Get all todos (user-specific) |
| GET    | `/todos/todo/{todo_id}`        | Get single todo               |
| POST   | `/todos/create_todo`           | Create new todo               |
| PUT    | `/todos/update_todo/{todo_id}` | Update existing todo          |
| DELETE | `/todos/delete_todo/{todo_id}` | Delete todo                   |

### 👤 User Profile Management

| Method | Endpoint                     | Description              |
| ------ | ---------------------------- | ------------------------ |
| PUT    | `/todos/change_password`     | Change user password     |
| PUT    | `/todos/change_phone_number` | Change user phone number |

All `/todos` routes are protected and require valid JWT authentication.

---

## 🛡 Admin Routes (`/admin`)

These routes are restricted to users with admin privileges.

| Method | Endpoint                       | Description               |
| ------ | ------------------------------ | ------------------------- |
| GET    | `/admin/todo`                  | Get all todos (all users) |
| DELETE | `/admin/delete_todo/{todo_id}` | Delete any user’s todo    |
| GET    | `/admin/get_user`              | Get all registered users  |

---

## 🌐 Default Route

| Method | Endpoint | Description                  |
| ------ | -------- | ---------------------------- |
| GET    | `/`      | Health check / test endpoint |

---

# 🏗 Architecture Highlights

* Modular router structure (`auth`, `todos`, `admin`)
* Dependency injection for authentication (`get_current_user`)
* Role-based authorization (admin vs normal user)
* ORM-based database interaction using SQLAlchemy
* Server-side rendering with Jinja2 templates
* RESTful API design with proper HTTP methods

---

# ⚙️ How to Run the Project Locally

## 1️⃣ Clone the Repository

```
git clone <your-repo-url>
cd <project-folder>
```

## 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

## 3️⃣ Install Required Dependencies

```
pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib[bcrypt] python-jose python-multipart jinja2
```

(Optional but recommended)

```
pip install python-dotenv
```

## 4️⃣ Setup PostgreSQL Database

* Create a new PostgreSQL database.
* Update the database connection string inside `database.py` with your username, password, host, and database name.

Example:

```
DATABASE_URL = "postgresql://username:password@localhost:5432/your_database_name"
```

## 5️⃣ Run the Application

```
uvicorn main:app --reload
```

Open in your browser:

```
http://127.0.0.1:8000
```

------

# 🔐 Security Implementations

- Password hashing using bcrypt
- JWT-based authentication
- Token validation dependency for protected routes
- User-level data protection (users can only access their own todos)

---

# 📌 Key Learning Outcomes

This project demonstrates:

- REST API design principles
- Dependency injection in FastAPI
- Authentication & Authorization implementation
- Database relationships using SQLAlchemy
- Form handling & template rendering
- Debugging real-world backend issues (405 errors, CORS, template errors)
- Full-stack integration between backend and frontend

---

# 📈 Future Improvements

- Role-based authorization
- Docker containerization
- Deployment (Render / Railway / AWS)
- Frontend migration to React
- Unit and integration testing

---

# 👩‍💻 Author

Ishika Gadhwal  
Aspiring Software Engineer  

---

# 🌟 Why This Project Matters

This project reflects practical backend development skills required in real-world software engineering roles. It showcases authentication systems, database design, REST API development, debugging capability, and full-stack integration — all essential for professional backend development.

