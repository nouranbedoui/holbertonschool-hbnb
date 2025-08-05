# HBnB API

A Flask-based REST API for an Airbnb-like application (HBnB) with user management, property listings, reviews, and amenities.

## Features

- **User Management**: Registration, authentication, and role-based access control
- **Property Listings**: Create, read, update, and delete places
- **Review System**: Users can review places they've stayed at
- **Amenities**: Property features and amenities management
- **JWT Authentication**: Secure token-based authentication
- **Admin Panel**: Administrative functions for user and content management

## Technology Stack

- **Backend**: Flask, Flask-RESTX, SQLAlchemy
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

1. Create a MySQL database
2. Run the schema file:
```bash
mysql -u root -p < hbnb_schema.sql
```

### 3. Configuration

Update `config.py` with your database credentials:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/database_name'
```

### 4. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/reset_password` - Password reset (requires JWT)

### Users (Admin Only)
- `POST /api/v1/users/setup` - Create first admin user
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/<user_id>` - Get specific user
- `PUT /api/v1/users/<user_id>` - Update user
- `DELETE /api/v1/users/<user_id>` - Delete user

### Places
- `GET /api/v1/places/` - Get all places
- `POST /api/v1/places/` - Create place (requires JWT)
- `GET /api/v1/places/<place_id>` - Get specific place
- `PUT /api/v1/places/<place_id>` - Update place (owner or admin)
- `DELETE /api/v1/places/<place_id>` - Delete place (owner or admin)

### Reviews
- `GET /api/v1/reviews/` - Get all reviews
- `POST /api/v1/reviews/` - Create review (requires JWT)
- `GET /api/v1/reviews/<review_id>` - Get specific review
- `PUT /api/v1/reviews/<review_id>` - Update review (author or admin)
- `DELETE /api/v1/reviews/<review_id>` - Delete review (author or admin)

### Amenities (Admin Only)
- `POST /api/v1/amenities/` - Create amenity
- `PUT /api/v1/amenities/<amenity_id>` - Update amenity
- `DELETE /api/v1/amenities/<amenity_id>` - Delete amenity

## Testing with Postman

### 1. Create First Admin User
```http
POST http://localhost:5000/api/v1/users/setup
Content-Type: application/json

{
  "first_name": "Admin",
  "last_name": "User",
  "email": "admin@hbnb.io",
  "password": "admin123"
}
```

### 2. Login to Get JWT Token
```http
POST http://localhost:5000/api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@hbnb.io",
  "password": "admin123"
}
```

### 3. Use JWT Token for Protected Endpoints
Add the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## API Documentation

Interactive API documentation is available at:
`http://localhost:5000/api/v1/docs`

## Project Structure

```
hbnb/
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── api/v1/          # REST API endpoints
│   ├── services/        # Business logic
│   ├── persistence/     # Data access layer
│   └── utils/           # Utility functions
├── requirements.txt     # Python dependencies
├── config.py           # Configuration settings
├── run.py              # Application entry point
└── hbnb_schema.sql     # Database schema
```

## Security Features

- Password hashing with bcrypt
- JWT-based authentication
- Role-based access control
- Input validation and sanitization
- SQL injection protection via ORM

## Business Rules

- Users cannot review their own places
- Users can only have one review per place
- Admin users have elevated privileges
- Place ownership validation for modifications
