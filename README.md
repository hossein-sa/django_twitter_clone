# 🐦 Django Twitter Clone API

🚀 A simple Twitter-like social media API built using Django REST Framework (DRF). This project supports user authentication, tweets, likes, comments (with replies), follow/unfollow, and a personalized feed.

---

## 📌 Features

✅ **User Authentication (JWT)**  
- Signup, Login, Logout  
- User Profile (View & Edit)  

✅ **Tweet System**  
- Create, Edit, Delete, View tweets  
- Tweet character limit: **280**  

✅ **Like System**  
- Users can **like/unlike** tweets (toggle mechanism)  

✅ **Comment System**  
- Users can add, edit, delete, and view comments  
- Supports **nested replies (threaded comments)**  

✅ **Follow/Unfollow System**  
- Users can **follow/unfollow** others  
- View followers and following lists  

✅ **Personalized Feed**  
- Shows tweets only from followed users  

✅ **Notifications System**  
- Receive notifications when:  
  - Someone likes your tweet  
  - Someone replies to your comment  
  - Someone follows you  

---

## 🛠️ Installation & Setup

1️⃣ **Clone the repository**  
```bash
git clone https://github.com/hossein-sa/django_twitter_clone.git
cd django_twitter_clone
```

2️⃣ **Create a virtual environment**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3️⃣ **Install dependencies**  
```bash
pip install -r requirements.txt
```

4️⃣ **Run database migrations**  
```bash
python manage.py makemigrations
python manage.py migrate
```

5️⃣ **Create a superuser (optional)**  
```bash
python manage.py createsuperuser
```

6️⃣ **Start the development server**  
```bash
python manage.py runserver
```

---

## 🔗 API Endpoints

### 🧑‍💻 Authentication
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/users/signup/` | Register a new user |
| POST | `/users/login/` | Login and receive JWT token |
| POST | `/users/logout/` | Logout (blacklist token) |

### 📝 Tweets
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/tweets/` | Get all tweets |
| POST | `/tweets/` | Create a new tweet |
| GET | `/tweets/{tweet_id}/` | Retrieve a specific tweet |
| PUT | `/tweets/{tweet_id}/` | Edit a tweet |
| DELETE | `/tweets/{tweet_id}/` | Delete a tweet |

### ❤️ Likes
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/tweets/{tweet_id}/like/` | Like/unlike a tweet (toggle) |

### 💬 Comments & Replies
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/tweets/{tweet_id}/comments/` | Get all comments for a tweet |
| POST | `/tweets/{tweet_id}/comments/` | Add a comment or reply |
| PUT | `/comments/{comment_id}/` | Edit a comment |
| DELETE | `/comments/{comment_id}/` | Delete a comment |

### 👥 Follow/Unfollow
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/users/{user_id}/follow/` | Follow a user |
| POST | `/users/{user_id}/unfollow/` | Unfollow a user |
| GET | `/users/{user_id}/followers/` | Get a user's followers |
| GET | `/users/{user_id}/following/` | Get a user's following list |

### 📰 Personalized Feed
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/feed/` | Get tweets from followed users |

### 🔔 Notifications
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/notifications/` | Get user notifications |
| POST | `/notifications/{notification_id}/read/` | Mark notification as read |

---

## 🛡️ Authentication (JWT)
This project uses **JWT (JSON Web Tokens)** for authentication.

- After login, the user receives an `access` and `refresh` token.
- The `access` token is used for making authenticated API requests.
- The `refresh` token is used to generate a new `access` token.

### 📌 Example Login Request:
```bash
POST /users/login/
{
    "username": "testuser",
    "password": "password123"
}
```
**Response:**
```json
{
    "access": "JWT_ACCESS_TOKEN",
    "refresh": "JWT_REFRESH_TOKEN"
}
```
Use the `access` token in API requests:
```http
Authorization: Bearer JWT_ACCESS_TOKEN
```

---

## 📂 Project Structure

```
django_twitter_clone/
│── config/                  # Configuration & settings
│── tweets/                  # Tweets, likes, comments, feed
│── users/                   # User authentication, follow/unfollow
│── .gitignore               # Git ignore file
│── manage.py                # Django management script
│── requirements.txt         # Project dependencies
│── README.md                # Project documentation
```

---

## 🚀 Deployment (Optional)
To deploy the project:

- Use **Docker** or **Heroku** for hosting.
- Set up a **PostgreSQL** database for production.
- Use **Gunicorn** as the production WSGI server.

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork this repository, make improvements, and submit a pull request.

---

## 📄 License
This project is open-source and available under the **MIT License**.

---

💡 **Built with Django, Django REST Framework, and ❤️**  
