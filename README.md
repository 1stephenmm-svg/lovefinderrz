# Lovefinderrz

**Version:** `v0.1.0` · Early development

#### Video Demo: [URL pending]

#### Description

**Lovefinderrz** is the working title of a software project inspired by the fictional app featured in the *Rick and Morty* series. You can learn more about its origins, history, and appearance in the series on the [Rick and Morty fan wiki](https://rickandmorty.fandom.com/wiki/Lovefinderrz). This *codename* is used during development; the commercial name of the final product has not yet been determined.

The project begins as a Python console application to manage profiles and find potential matches between users. Although I have professional experience developing backend applications with Python and Django, I decided to build this project to reinforce my fundamentals and improve my software engineering practices. For this first version, I’m primarily using the knowledge I gained from **CS50’s Introduction to Programming with Python (CS50P)**. I aim to implement the core logic from the ground up before incorporating additional frameworks.

______________________________________________________________________

## Features and Design

The first version includes profile creation and validation, user filtering based on preferences and geographic location, and data persistence via CSV files. It uses Nominatim from OpenStreetMap to obtain coordinates and incorporates fallback mechanisms in case of certain errors with the external service.

The code is organized into modules to facilitate maintenance and future development:

```text
.
├── data/                  # CSV files for data persistence
├── data.py                # Shared constants and reference data
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
- **Requests:** HTTP requests.
- **CSV:** initial data persistence.
- **Nominatim / OpenStreetMap:** geolocation.
- **Git and GitHub:** version control.

Future development may include a relational database, authentication, likes and matches, location-based features, and meetup scheduling. The project could also evolve into a across-platform mobile application using Flutter, supported by a REST API built with Django REST Framework or FastAPI. LLM Integration could help interpret natural-language preferences and explain matching results, while data analytics capabilities could reveal user preference patterns. Eventually, I plan to explore a cloud architecture that supports the gradual deployment, integration, and scaling of the system’s components.

Lovefinderrz is, therefore, a project focused on applied learning and incremental development: consolidating Python fundamentals, practicing sound design decisions, and building a maintainable foundation that can grow into a more comprehensive software solution.
