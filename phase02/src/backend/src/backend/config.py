import os

# Application settings
APP_NAME = os.getenv("APP_NAME", "Dad Jokes Dashboard Api")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8080"))
