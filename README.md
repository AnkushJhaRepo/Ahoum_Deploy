# Event Management System

A comprehensive Flask-based event management system with facilitator dashboard and CRM microservice integration.

## 🚀 Features

### Core Features
- **User Authentication & Authorization**: JWT-based authentication with role-based access control
- **Event Management**: Create, view, and manage events with sessions
- **Session Management**: Facilitators can create and manage sessions within events
- **Booking System**: Users can book sessions with real-time availability checking
- **Facilitator Dashboard**: Dedicated interface for facilitators to manage their sessions
- **CRM Integration**: Microservice for handling booking notifications

### User Roles
- **Regular Users**: Can browse events, book sessions, and manage their bookings
- **Facilitators**: Can create sessions, manage bookings, and cancel sessions
- **Admin**: Full system access (future enhancement)

## 🏗️ Architecture

### Main Application (`main_app/`)
- **Flask Web Application**: Main event management system
- **SQLAlchemy ORM**: Database management with SQLite
- **JWT Authentication**: Secure user authentication
- **RESTful API**: JSON-based API endpoints

### CRM Microservice (`crm_microservice/`)
- **Notification Service**: Handles booking notifications
- **Independent Flask App**: Runs on port 5001
- **JSON Logging**: Stores notification data

## 📁 Project Structure

```
Ahoum_Assignment/
├── main_app/                    # Main Flask application
│   ├── models/                  # Database models
│   │   ├── user.py             # User model with roles
│   │   ├── event.py            # Event model
│   │   ├── session.py          # Session model
│   │   └── booking.py          # Booking model
│   ├── routes/                  # API routes
│   │   ├── auth_routes.py      # Authentication endpoints
│   │   ├── event_routes.py     # Event management
│   │   ├── session_routes.py   # Session management
│   │   ├── booking_routes.py   # Booking system
│   │   └── facilitator_routes.py # Facilitator-specific endpoints
│   ├── services/                # Business logic
│   │   └── notify_crm.py       # CRM notification service
│   ├── app.py                  # Flask application factory
│   └── config.py               # Configuration settings
├── crm_microservice/            # CRM notification microservice
│   ├── crm_app.py              # CRM Flask application
│   ├── config.py               # CRM configuration
│   └── routes/                 # CRM API routes
├── migrations/                  # Database migrations (Alembic)
├── instance/                    # Database files (gitignored)
├── venv/                       # Virtual environment (gitignored)
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Ahoum_Assignment
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   # Create .env file (optional)
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Initialize database**
   ```bash
   flask --app main_app.app db upgrade
   ```

## 🚀 Running the Application

### Start Main Application
```bash
python main.py
```
The main application will run on `http://127.0.0.1:5000`

### Start CRM Microservice (Optional)
```bash
cd crm_microservice
python crm_app.py
```
The CRM microservice will run on `http://127.0.0.1:5001`

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/profile` - Get user profile
- `POST /auth/logout` - User logout

### Event Endpoints
- `GET /api/events` - List all events
- `GET /api/events/<id>` - Get specific event
- `POST /api/events` - Create new event (Admin)
- `PUT /api/events/<id>` - Update event (Admin)
- `DELETE /api/events/<id>` - Delete event (Admin)

### Session Endpoints
- `GET /api/events/<event_id>/sessions` - List sessions for event
- `POST /api/events/<event_id>/sessions` - Create session (Facilitator)
- `PUT /api/sessions/<id>` - Update session (Facilitator)
- `DELETE /api/sessions/<id>` - Delete session (Facilitator)

### Booking Endpoints
- `GET /api/bookings` - List user's bookings
- `POST /api/sessions/<id>/book` - Book a session
- `DELETE /api/bookings/<id>` - Cancel booking

### Facilitator Endpoints
- `GET /api/facilitator/dashboard` - Facilitator dashboard data
- `GET /api/facilitator/my-sessions` - Facilitator's sessions
- `POST /api/facilitator/sessions/<id>/cancel` - Cancel session

### CRM Endpoints
- `POST /notify` - Receive booking notifications

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database connection string
- `JWT_SECRET_KEY` - JWT signing key
- `CRM_NOTIFY_TOKEN` - CRM notification token

### Database Configuration
The application uses SQLite by default. For production, consider using PostgreSQL or MySQL.

## 🧪 Testing

The application includes comprehensive testing capabilities:
- Unit tests for models and services
- Integration tests for API endpoints
- Authentication and authorization tests

Run tests with:
```bash
python -m pytest
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-based Access Control**: Different permissions for users and facilitators
- **Input Validation**: Comprehensive request validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS Configuration**: Proper cross-origin resource sharing setup

## 📊 Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `role` (user/facilitator/admin)
- `created_at`
- `updated_at`

### Events Table
- `id` (Primary Key)
- `title`
- `description`
- `start_date`
- `end_date`
- `created_at`
- `updated_at`

### Sessions Table
- `id` (Primary Key)
- `event_id` (Foreign Key)
- `facilitator_id` (Foreign Key)
- `title`
- `description`
- `start_time`
- `end_time`
- `max_capacity`
- `created_at`
- `updated_at`

### Bookings Table
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `session_id` (Foreign Key)
- `status` (booked/cancelled)
- `created_at`
- `updated_at`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation
- Review the code comments for implementation details

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Added facilitator dashboard
- **v1.2.0** - Integrated CRM microservice
- **v1.3.0** - Enhanced security and bug fixes

---

**Note**: This is a development version. For production deployment, ensure proper security configurations and use a production WSGI server.
