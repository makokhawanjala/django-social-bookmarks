# Django Social Bookmarks

A full-featured social bookmarking and image sharing platform built with Django. Users can bookmark images from any website, follow other users, and see an activity stream of actions performed by the people they follow.

## Features

### User Authentication
- User registration and login
- Django built-in authentication system
- Social authentication with Google OAuth
- Password reset and change functionality
- User profile management with photo upload

### Image Bookmarking
- Bookmark images from any website using JavaScript bookmarklet
- Upload images directly
- Image thumbnails with easy-thumbnails
- Image detail pages with user interactions
- AJAX-based image operations

### Social Features
- Follow/unfollow other users
- Activity stream showing actions from followed users
- User profile pages
- User discovery and listing
- Like/unlike images

### Activity Tracking
- Generic activity stream using Django's contenttypes framework
- Tracks user actions (image likes, follows, bookmarks)
- Intelligent action deduplication
- Signal-based action creation

### Performance & Optimization
- Redis integration for view counting
- Image ranking based on popularity
- Query optimization with select_related and prefetch_related
- Django Debug Toolbar for development

### Technical Features
- RESTful API endpoints
- HTTPS support with SSL certificates
- AWS Lambda integration for external processing
- NewsAPI integration
- Responsive design
- Custom template tags

## Technology Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development), PostgreSQL-ready
- **Cache**: Redis
- **Image Processing**: Pillow, easy-thumbnails
- **Authentication**: django-allauth, social-auth-app-django
- **Frontend**: HTML5, CSS3, JavaScript, jQuery
- **Deployment**: AWS Lambda support

## Installation

### Prerequisites
- Python 3.8+
- Redis server
- pip and virtualenv

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/django-social-bookmarks.git
cd django-social-bookmarks
```

2. Create and activate virtual environment:
```bash
python -m venv my_bookmarks_env
source my_bookmarks_env/bin/activate  # On Windows: my_bookmarks_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
cd bookmarks
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Start Redis server (in separate terminal):
```bash
redis-server
```

8. Run development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Project Structure

```
bookmarks/
├── account/           # User authentication and profiles
├── actions/           # Activity stream and action tracking
├── bookmarks/         # Main project settings
├── images/            # Image bookmarking functionality
├── media/             # User uploaded files
├── static/            # Static files (CSS, JS, images)
├── cert.crt/cert.key  # SSL certificates for HTTPS
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For questions or feedback, please open an issue on GitHub.
