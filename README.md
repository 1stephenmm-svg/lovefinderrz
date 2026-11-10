# Lovefinderrz

**Version:** `v0.1.0` · Early development

## Video Demo: [URL pending]

### Description

**Lovefinderrz** is the working title of a software project inspired by the fictional app featured in the *Rick and Morty* series. You can learn more about its origins, history, and appearance in the series on the [Rick and Morty fan wiki](https://rickandmorty.fandom.com/wiki/Lovefinderrz). This *codename* is used during development; the commercial name of the final product has not yet been determined.

The project begins as a Python console application to manage profiles and find potential matches between users. Although I have professional experience developing backend applications with Python and Django, I decided to build this project to reinforce my fundamentals and improve my software engineering practices. For this first version, I’m primarily using the knowledge I gained from **CS50’s Introduction to Programming with Python (CS50P)**. I aim to implement the core logic from the ground up before incorporating additional frameworks.

______________________________________________________________________

## Features and Design

The application currently includes:

- **User registration and profile validation:** separate registration flows for clients and administrators, with input validation and user creation.
- **Authentication:** login functionality for both clients and administrators, with different authentication mechanisms according to user type.
- **Profile discovery:** filtering of compatible profiles based on user preferences, account status, and geographic location.
- **Geographic distance calculation:** implementation of the Haversine formula to calculate distances between geographic coordinates and sort profiles by proximity.
- **Likes management:** registration and retrieval of likes using client IDs, allowing users to track the profiles they have liked and identify mutual likes.
- **Data persistence:** CSV files are used to store user accounts.
- **Geolocation:** Nominatim from OpenStreetMap provides geographic coordinates, with fallback mechanisms for certain external service errors.

### Authentication

Lovefinderrz implements different authentication mechanisms for clients and administrators:

- **Clients:** The current development version uses their nickname as their password. This is a simplified authentication mechanism intended for the initial prototype.
- **Administrators:** Passwords are hashed using PBKDF2-HMAC-SHA256 with a randomly generated salt before being stored. Password verification is handled by the authentication module.

**Development credentials:**

| Account type  | Password                         |
|---------------|----------------------------------|
| Client        | Same as the registered nickname  |
| Administrator | `admin123`                       |

The administrator password corresponds to the preconfigured administrator account included in the project data.

### Project Structure

The code is organized into modules to facilitate maintenance and future development:

```text
.
├── data
│   ├── admins.csv         # Administrator account data
│   ├── clients.csv        # Client profile data
│   └── likes.csv          # Client likes
├── auth.py                # Password hashing, verification, and authentication
├── data.py                # Shared constants and reference data
├── likes.py               # Like management and match-related operations
├── location.py            # Geographic coordinate handling
├── matching.py            # User compatibility logic
├── menu.py                # Client and admin menus, registration forms, and user interaction
├── project.py             # Application entry point and command-line argument handling
├── storage.py             # Loading and saving user data
├── test_project.py        # Automated tests
├── user.py                # User model
├── user_service.py        # User creation and user-related business logic
├── .gitignore
├── .python-version
├── pyproject.toml         # Project and development tool configuration
├── requirements.txt
└── README.md
```

This separation of responsibilities prevents all the logic from being concentrated in a single file and makes it easier to test the components independently. I am also incorporating object-oriented programming (OOP), data validation, exception handling, version control with Git, and a test-driven development (TDD) approach where appropriate.

The decision to start with CSV and a console interface aligns with the educational purpose of this stage: to understand the application’s logic and responsibilities before introducing a database or a more complex architecture.

______________________________________________________________________

## Technologies

- **Python:** application logic and object-oriented programming.
- **pytest:** automated testing.
- **emoji:** terminal menu presentation.
- **Requests:** HTTP requests.
- **CSV:** initial data persistence.
- **Nominatim / OpenStreetMap:** geolocation.
- **Git and GitHub:** version control.

Future development may include migrating CSV persistence to a relational database, expanding authentication and account management, and implementing meetup scheduling. The project could also evolve into a cross-platform mobile application using Flutter, supported by a REST API built with Django REST Framework or FastAPI.

LLM Integration could help interpret natural-language preferences and explain matching results, while data analytics capabilities could reveal user preference patterns. Eventually, I plan to explore a cloud architecture that supports the gradual deployment, integration, and scaling of the system’s components.

Lovefinderrz is, therefore, a project focused on applied learning and incremental development: consolidating Python fundamentals, practicing sound design decisions, and building a maintainable foundation that can grow into a more comprehensive software solution.
