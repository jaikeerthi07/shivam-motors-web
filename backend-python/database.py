import mysql.connector
from mysql.connector import pooling
import os

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "jaikeerthi07a",
    "database": "shivmotors"
}

# Create a connection pool
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="shiv_pool",
        pool_size=10,
        **db_config
    )
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")

def get_db_connection():
    return connection_pool.get_connection()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create bikes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bikes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            price VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            badge VARCHAR(255),
            info VARCHAR(255),
            description TEXT,
            image_url VARCHAR(255) NOT NULL,
            status VARCHAR(20) DEFAULT 'unsold',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create valuations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS valuations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            bike_model VARCHAR(255) NOT NULL,
            year VARCHAR(255) NOT NULL,
            kilometers VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
