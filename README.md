# 🏡 HBnB Project - Business Logic & API Implementation

This phase of the HBnB project focuses on building the core structure of the application. You'll develop the **Presentation** and **Business Logic** layers using **Python** and **Flask**, and implement **RESTful API endpoints** using `flask-restx` to manage CRUD operations.

> ⚠️ Authentication and access control will be added in later phases.

---

## 📦 Installation

> _To be added: instructions for setting up virtualenv, installing dependencies from `requirements.txt`, and running the app._

---

## 📁 Project Structure

```plaintext
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
