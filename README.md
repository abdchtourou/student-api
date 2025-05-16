# Student Management API

A Django REST Framework API for managing student records with authentication and authorization.

## Features

- User authentication with JWT tokens
- Student record management
- Todo List management
- Email-based authentication
- Secure password hashing with bcrypt
- Comprehensive logging system
- MySQL database integration

## Tech Stack

- Python 3.x
- Django 4.2
- Django REST Framework
- MySQL
- JWT Authentication
- bcrypt for password hashing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abdchtourou/student-api.git
cd student-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MySQL database:
```sql
CREATE DATABASE student CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. Update database settings in `config/settings.py` if needed:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'student',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/signup/` - Register new user
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe",
    "major": "Computer Science"
  }
  ```

- `POST /api/login/` - Login user
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

### User Data

- `GET /api/user/` - Get authenticated user data (requires authentication)

### Todo List

- `GET /api/todos/` - List all todos
- `POST /api/todos/` - Create a new todo
  ```json
  {
    "title": "Task title",
    "description": "Task description",
    "completed": false
  }
  ```
- `GET /api/todos/{id}/` - Retrieve a specific todo
- `PUT /api/todos/{id}/` - Update a todo
- `DELETE /api/todos/{id}/` - Delete a todo

## Project Structure

```
student-api/
├── account/                 # Authentication app
│   ├── models.py           # Custom user model
│   ├── serializers.py      # API serializers
│   └── views.py            # API views
├── student/                # Student management app
│   ├── models.py           # Student model
│   └── views.py            # Student views
├── todoList/               # Todo List app
│   ├── models.py           # Todo model
│   ├── serializers.py      # Todo serializers
│   ├── urls.py            # Todo URLs
│   └── views.py            # Todo views
├── config/                 # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
└── manage.py              # Django management script
```

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Email uniqueness validation
- Input validation and sanitization
- Comprehensive error handling
- Secure password requirements

## Logging

The project includes a comprehensive logging system that tracks:
- User signup attempts
- Login attempts
- Data validation errors
- System errors
- User actions

Logs are stored in both console output and a `debug.log` file.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 