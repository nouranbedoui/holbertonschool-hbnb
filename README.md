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
📝 Explanation
app/: Contains all the core application logic and organization.

api/: Houses the RESTful API endpoints using flask-restx, grouped by version (currently v1/).

users.py, places.py, reviews.py, and amenities.py contain the endpoint definitions for each entity.

models/: Contains the core business logic and entity classes:

user.py, place.py, review.py, and amenity.py define attributes and methods for interacting with business data.

services/: Implements the Facade pattern, offering a simplified and unified interface (facade.py) to interact with the business logic and persistence layers.

persistence/: Responsible for storing and retrieving data. Initially implemented with in-memory persistence, it can be swapped for SQLAlchemy or another database in later phases.

run.py: Main Flask entry point to launch the web application.

config.py: Stores configuration values, environment variables, and settings needed to run the app.

requirements.txt: Lists all required Python packages needed to run the application.

README.md: This file—providing detailed documentation of the project structure and logic.

🧠 Business Logic Layer
The Business Logic Layer defines the core entities and their behaviors:

👤 User
Attributes: id, first_name, last_name, email

Methods:

create_user(user_data)

get_user(user_id)

update_user(user_id, user_data)

get_all_users()

🏠 Place
Attributes: id, title, description, price, latitude, longitude, owner, amenities

Methods:

create_place(...)

get_place(place_id)

update_place(place_id, place_data)

get_all_places()

📝 Review
Attributes: id, text, user_id, place_id, rating

Methods:

create_review(...)

get_review(review_id)

update_review(review_id, review_data)

delete_review(review_id)

get_reviews_by_place(place_id)

🛠️ Amenity
Attributes: id, name

Methods:

create_amenity(amenity_data)

get_amenity(amenity_id)

update_amenity(amenity_id, amenity_data)

get_all_amenities()

🔌 Example Usage
Create a User
python
Copier
Modifier
from app.services.facade import HBnBFacade
facade = HBnBFacade()
user = facade.create_user({
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
})
print(user.id)
Create a Place
python
Copier
Modifier
place = facade.create_place(
    "Cozy Cabin", "A relaxing getaway.", 120, 45.67, -123.45, user.id, []
)
print(place.id)
Create a Review
python
Copier
Modifier
review = facade.create_review("Amazing place!", user.id, place.id, 5)
print(review.id)
Create an Amenity
python
Copier
Modifier
amenity = facade.create_amenity({"name": "WiFi"})
print(amenity.id)
