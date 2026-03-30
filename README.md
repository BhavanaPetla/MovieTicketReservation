# Movie Ticket Reservation System

CineTick is a professional full-stack web application developed for the Python Full Stack (4AI3) coursework. It provides a platform for users to browse movies across multiple film industries, manage accounts, and book tickets in real-time.

## Project Overview

The system is built using the Flask web framework and follows the Model-View-Controller (MVC) architectural pattern. It features a complete user authentication system, dynamic industry filtering, and a persistent SQLite database to manage movie catalogs and user reservations.

## Key Features

- User Authentication: Secure Registration and Login system with encrypted password hashing using the Werkzeug library.
- Multi-Industry Catalog: Support for Hollywood, Bollywood, Tollywood, Kollywood, Mollywood, Sandalwood, and Anime categories.
- Dynamic Filtering: An interactive horizontal category bar that allows users to filter movies by industry instantly.
- Seat Reservation: Logged-in users can select the number of seats and book tickets, with automatic price calculation in the backend.
- Personal Dashboard: A private area for users to view their confirmed bookings, movie titles, and total expenditure.
- Responsive Interface: A high-end dark-themed UI built with Tailwind CSS, optimized for mobile, tablet, and desktop devices.
- Data Persistence: Uses SQLAlchemy ORM and an SQLite database to store all user profiles and transaction records.

## Technical Stack

- Backend: Python 3.x, Flask
- Database: SQLite, SQLAlchemy (ORM)
- Frontend: HTML5, Jinja2 Templating, Tailwind CSS
- Security: PBKDF2 Password Hashing

## Project Structure

```text
Movieticket/
|
├── app.py              # Main application logic and database models
├── cinema.db           # SQLite database file (auto-generated)
├── README.md           # Project documentation
└── templates/          # Directory for HTML templates
    ├── base.html       # Shared layout and navigation bar
    ├── index.html      # Movie gallery and category filters
    ├── login.html      # User sign-in page
    ├── register.html   # User account creation page
    └── dashboard.html  # User booking history
