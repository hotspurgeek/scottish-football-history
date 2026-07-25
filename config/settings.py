# Add these to your Django settings.py file

# ============================================
# INSTALLED APPS
# ============================================
# Add to INSTALLED_APPS:
INSTALLED_APPS = [
    # ... existing apps ...
    'rest_framework',
    'django_filters',
    'corsheaders',
    'football',  # Your app
]

# ============================================
# MIDDLEWARE
# ============================================
# Add corsheaders middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... rest of middleware ...
]

# ============================================
# DATABASE CONFIGURATION
# ============================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'scottish_football',
        'USER': 'mundar',
        'PASSWORD': 'your_password_here',  # Replace with actual password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ============================================
# REST FRAMEWORK CONFIGURATION
# ============================================
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'football.views.StandardPagination',
    'DEFAULT_PAGE_SIZE': 50,
}

# ============================================
# CORS CONFIGURATION
# ============================================
# Allow requests from frontend (adjust as needed for production)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # React development
    "http://localhost:8000",      # Local Django
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# ============================================
# OPTIONAL: API DOCUMENTATION
# ============================================
# To add Swagger/OpenAPI documentation, install:
# pip install drf-spectacular
# Then add to INSTALLED_APPS:
# 'drf_spectacular',
# 
# And add to REST_FRAMEWORK settings:
# 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
