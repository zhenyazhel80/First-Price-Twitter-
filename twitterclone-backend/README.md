# 🐦 TwitterClone Backend

This is the backend for the **TwitterClone** project built with **FastAPI**, **JavaScript**, and a relational database. The app allows users to create accounts, log in, post tweets, edit or delete them, and search by tweet content or hashtags.

---

## 📚 Subject Information

**Course Name:** Cloud Technologies  
**Course Code:** IDG2001  
**Institution:** NTNU (Norwegian University of Science and Technology)  
**Study Year:** 2024/2025 (Spring Semester)  
**Location:** NTNU Gjøvik  
**Student:** Zhenya Ivanova Zhelyazkova  
**Program:** Web Development (BWU)  
**Language of Instruction:** English  

---

## ⚙️ Technologies Used

- **FastAPI** – modern Python web framework for building APIs
- **JavaScript** – frontend interaction with DOM + API
- **HTML/CSS** – static frontend layout and styling
- **PostgreSQL** – production-ready cloud database  
- **SQLite** – optional local testing setup
- **SQLAlchemy** – ORM for database models and queries
- **Uvicorn** – ASGI server
- **Render.com** – PostgreSQL hosting

---

## 🔐 Features

- ✅ Create an account (username, email, password)
- ✅ Login via form (with password check)
- ✅ Post tweets (linked to user ID)
- ✅ Edit & delete your tweets
- ✅ Hashtag highlighting and search (`#example`)
- ✅ Search tweets by keyword or hashtag
- ✅ View all users
- ✅ RESTful API with Swagger docs (`/docs`)

---

## 🔌 API Endpoints

| Method | Endpoint                  | Description                     |
|--------|---------------------------|---------------------------------|
| POST   | `/users/`                 | Create a new user               |
| GET    | `/users/`                 | Get all users                   |
| GET    | `/users/search/`          | Search users by username        |
| POST   | `/login/`                 | Login with username & password  |
| POST   | `/tweets/`                | Create a new tweet              |
| GET    | `/tweets/`                | Get all tweets                  |
| PUT    | `/tweets/{tweet_id}`      | Update a tweet by ID            |
| DELETE | `/tweets/{tweet_id}`      | Delete a tweet by ID            |
| GET    | `/tweets/search/?q=term`  | Search tweets by keyword        |
| GET    | `/hashtags/search/?tag=xyz` | Search tweets with hashtag     |

---

## 🗃️ Database Models

### User
```python
id: int
username: str
email: str
password: str
