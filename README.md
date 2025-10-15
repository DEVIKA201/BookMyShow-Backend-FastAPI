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

git clone https://github.com/<your-username>/bms-backend-fastapi.git
cd bms-backend-fastapi

###2. Create & Activate Virtual Environment

python -m venv venv
source venv/bin/activate       # Linux/Mac
# or
venv\Scripts\activate          # Windows

###3. Install Dependencies

pip install -r requirements.txt

###4. Configure Environment Variables

#Create a .env file in the root directory:

MONGO_DATABASE_URL=mongodb://localhost:port
MONGO_DB=bms
POSTGRES_URL=postgresql://user:password@localhost:port/bms

###5. Run the Application

uvicorn main:app --reload

###🧭 API Endpoints Overview

Route Example	                Method	        Description
/explore/movies-{location}	  GET	            Get all movies by location
/venues	                      GET	            Get list of venues
/shows	                      GET	            Get list of shows
/bookings	                    POST	          Create a booking
/users	                      POST	          Register or get user details

###Example Request:

GET /explore/movies-kochi
Respose:
[

  {
    "_id": "670e5dd9d9eab8b4d7b7e2e0",
    "title": "Jawan",
    "rating": "8.5",
    "language": "Hindi"
  }
  
]  
