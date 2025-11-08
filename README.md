# BookMyShow-Backend-FastAPI
A FastAPI backend for a BookMyShow-style movie ticket booking platform with PostgreSQL and MongoDB integration. Includes APIs for movies, venues, shows, artists, users, and bookings.


# 🎟️ BMS Backend (FastAPI)

A backend service inspired by **BookMyShow**, built using **FastAPI**, **PostgreSQL**, and **MongoDB**.  
This project provides RESTful APIs for managing movies, shows, venues, artists, users, and bookings.

---

## 🚀 Features

- 🧭 Modular API structure using FastAPI routers  
- 🗄️ Dual database integration — PostgreSQL & MongoDB  
- 🎬 Movie, Venue & Show management endpoints  
- 🧑 User and Artist routes  
- 🧾 Booking endpoints  
- 🧹 Clean, production-friendly project structure  

---

## 🏗️ Tech Stack

- **Framework:** FastAPI  
- **Database:** PostgreSQL, MongoDB  
- **ORM:** SQLAlchemy  
- **Async Driver:** Motor (for MongoDB)  
- **Environment Management:** python-dotenv  

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

git clone https://github.com/DEVIKA201/BookMyShow-Backend-FastAPI.git<br>
cd bms-backend-fastapi<br>

### 2. Create & Activate Virtual Environment

python -m venv venv<br>
source venv/bin/activate       # Linux/Mac
##or<br>
venv\Scripts\activate          # Windows

### 3. Install Dependencies

pip install -r requirements.txt<br>

### 4. Configure Environment Variables

#Create a .env file in the root directory:

MONGO_DATABASE_URL=mongodb://localhost:port/book_my_show_db?<br>
MONGO_DB=book_my_show_db<br>
POSTGRES_URL=postgresql://user:password@localhost:port/book_my_show_db<br>

### 5. Run the Application

uvicorn main:app --reload<br>

