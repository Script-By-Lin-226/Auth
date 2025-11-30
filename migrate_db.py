"""
Migration script to add the role column to the user table if it doesn't exist.
Run this script to update your database schema.
"""
import sqlite3
import os

DB_PATH = "test.db"

def migrate():
    """Add role column to user table if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} does not exist. It will be created when you start the app.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if role column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'role' not in columns:
            print("Adding 'role' column to user table...")
            # Add role column with a default value
            cursor.execute("ALTER TABLE user ADD COLUMN role VARCHAR(50) DEFAULT 'user' NOT NULL")
            conn.commit()
            print("Migration completed successfully! Added 'role' column with default value 'user'.")
        else:
            print("Column 'role' already exists. No migration needed.")
        
        # Check if hashed_password column exists
        if 'hashed_password' not in columns:
            if 'password' in columns:
                print("Warning: Found 'password' column instead of 'hashed_password'.")
                print("You may need to recreate the database.")
            else:
                print("Warning: 'hashed_password' column not found.")
        
    except sqlite3.Error as e:
        print(f"Migration failed: {e}")
        print("\nIf you're in development, you can delete test.db and restart the app to recreate the database.")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
