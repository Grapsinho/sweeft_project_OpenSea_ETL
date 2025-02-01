import psycopg2

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the values like this
db_host__var = os.environ.get('DB_HOST')
db_port__var = os.environ.get('DB_PORT')
db_name__var = os.environ.get('DB_NAME')
db_user__var = os.environ.get('DB_USER')
db_pass__var = os.environ.get('DB_PASS')

class Database:
    def __init__(self, db_name=db_name__var, user=db_user__var, password=db_pass__var, host=db_host__var, port=db_port__var):
        """Initialize connection to PostgreSQL"""
        self.connection = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=()):
        """Execute a query with optional parameters"""
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch(self, query, params=()):
        """Fetch data from the database"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection"""
        self.cursor.close()
        self.connection.close()
