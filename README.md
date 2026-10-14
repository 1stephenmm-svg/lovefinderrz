# Lovefinderrz

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
├── menu.py
├── project.py             # Main application flow
├── storage.py             # CSV data access
├── test_project.py        # Automated tests
├── user.py                # User model
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

Once the first version is complete, the project could evolve into a cross-platform app with a relational database, a REST API developed using Django REST Framework or FastAPI, and a mobile interface built with Flutter. I’m also considering adding authentication, likes, matches, and features related to location and scheduling meetups.

In the long term, I plan to explore a cloud architecture that allows for the gradual deployment and scaling of the system’s components.

Lovefinderrz is, therefore, a project focused on applied learning and incremental development: consolidating Python fundamentals, practicing sound design decisions, and building a maintainable foundation that can grow into a more comprehensive software solution.
