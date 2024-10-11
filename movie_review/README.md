Here’s a comprehensive **README** for my **Movie Review API** project. This README covers the project setup, features, API endpoints, and more.

---

# **Movie Review API**

## **Overview**

The Movie Review API allows users to create, read, update, and delete movie entries and reviews. Users can register and log in to manage their movies and reviews, while anonymous users can post reviews without authentication. The API also features a user profile management system for authenticated users. The platform is built using Python,Django and Django REST Framework (DRF), basic authentication for secure access to endpoints.

## **Features**
- **Movie Management**: Users can create, update, delete, and view movies.
- **Review Management**: Users (authenticated or anonymous) can post reviews with star ratings.
- **User Authentication**: I made JWT-based authentication optional but it allows users to securely log in and manage their content.
- **User Profiles**: Authenticated Admin can manage their profiles, including profile pictures and bio.
- **Search and Filtering**: Search functionality is provided for movies and reviews.

---

## **Technologies Used**
- **Backend**: Python, Django, Django REST Framework (DRF)
- **Authentication**: JWT (JSON Web Token) using `djangorestframework-simplejwt`
- **Database**: SQLite (Development)
- **Documentation**: Swagger (using `drf-yasg`)
- **File Handling**: Django `ImageField` for profile pictures
- **Deployment**: pythonanywhere.com

---

## **Getting Started**

### **Prerequisites**

- Python 3.8+
- Django 4.x
- Virtual Environment 

### **Installation**

1. **Clone the Repository**:
   git clone https://github.com/your-username/movie-review-api.git
   cd movie-review-api
   

2. **Create and Activate a Virtual Environment**:
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True  # Set to False for production
   DATABASE_URL=postgres://your-db-url  # For PostgreSQL
   ```

5. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the API**:
   Open your browser and navigate to `http://127.0.0.1:8000/api/`.

---

## **API Endpoints**

### **1. Movie Endpoints**
- **GET** `/api/movies/`: List all movies
- **POST** `/api/movies/`: Create a new movie (Authenticated Users)
- **GET** `/api/movies/{id}/`: Retrieve a specific movie
- **PUT** `/api/movies/{id}/`: Update a specific movie (Owner Only)
- **DELETE** `/api/movies/{id}/`: Delete a specific movie (Owner Only)

### **2. Review Endpoints**
- **GET** `/api/reviews/`: List all reviews
- **POST** `/api/reviews/`: Create a new review (Authenticated or Anonymous)
- **GET** `/api/reviews/{id}/`: Retrieve a specific review
- **PUT** `/api/reviews/{id}/`: Update a specific review (Author Only)
- **DELETE** `/api/reviews/{id}/`: Delete a specific review (Author Only)

### **3. User Endpoints**
- **GET** `/api/users/`: List all users (Admin Only)
- **GET** `/api/users/{id}/`: Retrieve a specific user (Admin Only)

### **4. Profile Endpoints**
- **GET** `/api/profile/`: Retrieve the authenticated user's profile
- **PUT** `/api/profile/`: Update the authenticated user's profile

### **5. Authentication Endpoints**
- **POST** `/api/auth/login/`: Obtain JWT token #This is optional
- **POST** `/api/auth/refresh/`: Refresh JWT token #This is optional
- **POST** `/api/auth/signup/`: Register a new user

### **6. Search and Filtering**
- **GET** `/api/movies/?search={query}`: Search for movies by title, description
- **GET** `/api/reviews/?search={query}`: Search for reviews by content, stars

---

## **Authentication**

The API uses Basic authentication for authentication. But To access protected endpoints, include the JWT token in the `Authorization` header.

Example:

```
Authorization: Bearer <your-token>
```

To obtain a token, use the login endpoint:
```
POST /api/auth/login/
```

To refresh a token, use:
```
POST /api/auth/refresh/
```

---

## **Usage**

### **Create a Movie** (Authenticated)
```bash
POST /api/movies/
Authorization: Bearer <your-token>
Content-Type: application/json

{
    "title": "Inception",
    "description": "A mind-bending thriller by Christopher Nolan."
}
```

### **Create a Review** (Authenticated or Anonymous)
```bash
POST /api/reviews/
Content-Type: application/json

{
    "movie_id": 1,
    "stars": 5,
    "comment": "An amazing movie!"
}
```

---

## **Testing**

To run tests, use the following command:
```bash
python manage.py test
```

---

Deployment

To deployment was done using pythonanywhere.com


Project Structure

movie_review_api/
│
├── accounts/             # CustomUser user models
├── movie_review/         # my main project folder with my settings
├── api/                  # API views and serializers
├── templates/            # HTML templates 
├── review_api/           # My API views, models and serializers
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # Project README documentation



