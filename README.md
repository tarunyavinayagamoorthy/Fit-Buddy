# Fit-Buddy
AI powered personalized fitness plan generator

## 📌 Project Overview

FitBuddy is an AI-powered fitness planning web application that generates personalized 7-day workout plans using Google Gemini models.

The application allows users to enter their personal fitness information, select their fitness goal and workout intensity, and receive an AI-generated workout plan.

Users can also provide feedback about their generated plan. FitBuddy uses the feedback to generate an updated workout plan.

The application also provides a nutrition/recovery tip based on the user's fitness goal.

An administrator can securely log in and view registered users and their stored workout plans through an administrator dashboard.

---

# ✨ Features

- 🤖 AI-generated personalized 7-day workout plans
- 🏋️ Workout plans based on user fitness goals
- 🥗 AI-generated nutrition/recovery tips
- 🔄 Feedback-based workout plan updates
- 💾 Storage of user information
- 💾 Storage of original and updated workout plans
- 🔐 Secure administrator login
- 👨‍💼 Administrator dashboard
- 🚪 Administrator logout
- 🗄️ SQLite database
- ⚡ FastAPI backend
- 🎨 Responsive HTML/CSS interface
- 🔑 Environment variable configuration for sensitive information
- 🧠 Google Gemini AI integration

---
#Project Structure
```text
Fit Buddy/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   ├── admin_auth.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   └── schemas.py
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── feedback.html
│   ├── admin_login.html
│   └── all_users.html
│
├── static/
│   └── images/
│       └── gym_bg_1.jpg
│
├── .env
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── fitbuddy.db

Technologies Used
  .Backend
    .Python
    .FastAPI
    .Uvicorn
    .SQLAlchemy
    .SQLite
    .Jinja2
    .Artificial Intelligence
    .Google Gemini API
    .google-genai
  .Frontend
    .HTML5
    .CSS3
    .Jinja2 Templates
  .Development Tools
    .Visual Studio Code
    .Git
    .GitHub
    .Python Virtual Environment
```
#System Architecture
```text
                    ┌───────────────────┐
                    │       User        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   HTML / CSS UI   │
                    │     Jinja2        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │      FastAPI      │
                    │      Backend      │
                    └───────┬───┬───────┘
                            │   │
                 ┌──────────┘   └──────────┐
                 ▼                         ▼
        ┌─────────────────┐       ┌─────────────────┐
        │ SQLite Database │       │   Gemini API    │
        │   SQLAlchemy    │       │  AI Generation  │
        └─────────────────┘       └─────────────────┘
```

#Main Application Components

main.py

The main FastAPI application.
Responsibilities:

-Creates the FastAPI application
-Configures the application metadata
-Mounts static files
-Configures Jinja2 templates
-Includes application routes
-Provides the health-check endpoint

routes.py

Contains the application's web routes.
Responsibilities include:

-Displaying the home page
-Processing workout generation requests
-Processing feedback
-Updating workout plans
-Handling administrator functionality
-Displaying stored user information

database.py

Handles the SQLite database using SQLAlchemy.
Responsibilities include:

-Creating database tables
-Creating database sessions
-Saving users
-Saving workout plans
-Retrieving users
-Retrieving workout plans
-Updating workout plans
-Retrieving all users and plans for administration

admin_auth.py

Handles administrator authentication.
The administrator credentials are configured through environment variables rather than being hard-coded into the application.

gemini_generator.py

Generates personalized workout plans using Google Gemini.
The generated plan is based on information such as:
-Username
-Age
-Weight
-Fitness goal
-Workout intensity

gemini_flash_generator.py
Generates the nutrition/recovery recommendation based on the user's fitness goal.

updated_plan.py
Generates an updated workout plan based on:
-Original workout plan
-User feedback
-User information
-Fitness goal
-Workout intensity

Database
FitBuddy uses SQLite as its database and SQLAlchemy as the ORM.
The database contains two main tables:
-Users Table
```text
users
│
├── id
├── user_id
├── username
├── age
├── weight
├── goal
└── intensity
Plans Table
plans
│
├── id
├── user_id
├── original_plan
├── updated_plan
├── nutrition_tip
└── feedback
```
The plans table stores the AI-generated workout plan, updated plan, nutrition/recovery tip, and user feedback.
Environment Variables

#Requirements
The project requires Python 3.x and the following Python packages:

-fastapi
-uvicorn
-jinja2
-sqlalchemy
-python-dotenv
-python-multipart
-google-genai

#How to Run
Start the FastAPI application using:

uvicorn app.main:app --reload

The application will normally be available at:

http://127.0.0.1:8000

Open the address in your browser.

#❤️ User Workflow
```text
The normal FitBuddy user workflow is:
Open FitBuddy
      │
      ▼
Enter Personal Information
      │
      ▼
Enter User ID
      │
      ▼
Select Fitness Goal
      │
      ▼
Select Workout Intensity
      │
      ▼
Generate Workout Plan
      │
      ▼
Gemini Generates Plan
      │
      ▼
Display 7-Day Workout Plan
      │
      ▼
Display Nutrition/Recovery Tip
      │
      ▼
User Provides Feedback
      │
      ▼
Gemini Generates Updated Plan
      │
      ▼
Display Updated Plan
```
