# 🎫 Event Finder Application

A **full-stack event discovery platform** built with **FastAPI** and **Streamlit**, integrated with the **Ticketmaster Discovery API** to enable users to find, explore, and save upcoming concerts, sports matches, and live events across the globe.

> 🚀 Deployed Backend: [https://eventfinderbackend.onrender.com](https://eventfinderbackend.onrender.com)

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Unique Features](#unique-features)
- [Database Design](#database-design)
- [Security Best Practices](#security-best-practices)
- [Deployment & DevOps](#deployment--devops)
- [API Endpoints](#api-endpoints)
- [Performance Optimizations](#performance-optimizations)
- [Getting Started](#getting-started)
- [License](#license)

---

## 🌍 Project Overview

**Event Finder** is a user-focused event discovery tool that allows registered users to:

- 🔍 Search events by **location**, **date**, or **category**
- ❤️ Save their favorite events
- 👥 Register and log in securely with JWT-based authentication

It pulls live event data from Ticketmaster’s Discovery API, offering access to 230,000+ events worldwide. The app is modular, scalable, and cloud-deployed—ideal for production use and extensibility.

---

## 🛠️ Tech Stack

### 🧠 Backend – FastAPI
- Python-based high-performance REST API
- Authentication using **OAuth2 & JWT**
- ORM: **SQLAlchemy** with MySQL
- Secure password hashing via **PassLib (bcrypt)**

### 🖥️ Frontend – Streamlit
- Pure Python web UI with interactive components
- Token-based session state handling
- Dynamic pages for search, login, registration, and favorites

### 🌐 External APIs
- **Ticketmaster Discovery API** for event data
- JSON-based country-to-code mapping for internationalization

### ☁️ Deployment
- **Render.com** for hosting backend
- **FreeSQLDatabase** for MySQL hosting
- `.env` or environment variables for secret management

---

## ⚙️ Backend Architecture

### 📊 Models
- **User**
  - Unique email/username
  - Hashed password
  - `created_at` timestamp (UTC)
- **FavoriteEvent**
  - Foreign key: User → Event
  - Stores name, URL, image, and date for each favorited event

### 🔒 Authentication & Security
- Stateless JWT-based auth system
- Tokens valid for **30 minutes**
- Middleware validates tokens on protected routes
- CORS policies enabled for secure cross-origin access

### 🧩 Modular Design
- `auth.py`, `events.py`, `database.py`, `schemas.py`, etc.
- Clean separation of concerns using FastAPI routers
- Pydantic models for input/output validation

---

## 🎨 Frontend Architecture

### 📄 Multi-Page Layouts (Streamlit)
- **Login Page** – Secure token capture and session storage
- **Register Page** – User account creation
- **Search Events** – Real-time API integration and display
- **Favorites** – Personalized view of bookmarked events

### ⚡ Real-Time Features
- Rich event media display (name, image, venue, ticket URL)
- Country and date-based filtering with formatted ISO 8601 inputs
- Responsive layout using Streamlit columns and containers

### 🧠 Smart Session Management
- `st.session_state` for token and login persistence
- Conditional rendering based on authentication
- Optimized caching for favorites (1-minute TTL)

---

## 🚀 Unique Features

| Feature | Description |
|--------|-------------|
| 🔐 **Secure JWT Auth** | FastAPI OAuth2PasswordBearer flow with token expiry |
| 🌎 **Global Search** | Country, city, and keyword-based discovery using Ticketmaster API |
| 💾 **Favorites System** | User-specific favorites mapped with foreign keys |
| 🧰 **Modular Backend** | Follows FastAPI best practices with separated routers |
| 🧠 **Smart UI** | Dynamic content rendering, session-based visibility |
| 🧼 **Error Handling** | Clean feedback via FastAPI exceptions and `st.error()` UI alerts |

---

## 🧮 Database Design

- **Normalized schema**: User → FavoriteEvent (1-to-many)
- **Data integrity**: Unique indexes and foreign keys
- **UTC timezones** for consistency across regions
- **Cascading deletes** for clean user data removal

---

## 🔐 Security Best Practices

- **bcrypt hashing** with automatic salting (no plain text passwords)
- **JWT tokens** with expiration to prevent hijacking
- **OAuth2 Bearer scheme** for stateless authentication
- **ORM queries** to prevent SQL injection
- **Input validation** with strict Pydantic schemas

---

## ⚙️ Deployment & DevOps

- ✅ **FastAPI backend** hosted on [Render](https://render.com)
- ✅ **MySQL DB** hosted via FreeSQLDatabase
- ✅ `.env` file or Render Dashboard for storing secrets like:
  - `TICKETMASTER_API_KEY`
  - `SECRET_KEY`
- ✅ Deployed with `uvicorn main:app` as entry point
- ✅ Streamlit frontend runs locally or can be deployed via Streamlit Community Cloud

---

## 🔌 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/register` | Create a new user |
| `POST` | `/login` | Authenticate and receive JWT |
| `POST` | `/mark_favorite` | Save an event to favorites |
| `GET` | `/favorites` | Retrieve logged-in user’s saved events |

---

## 🚦 Performance Optimizations

- ✅ Indexed queries for faster DB performance
- ✅ Streamlit caching with TTL to reduce Ticketmaster API calls
- ✅ Stateless backend for horizontal scaling
- ✅ Efficient session handling with `session_state`

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/event-finder.git
cd event-finder
