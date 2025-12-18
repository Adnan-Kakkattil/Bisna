import sqlite3
import os

db_path = 'instance/site.db'
if not os.path.exists(db_path):
    print("Database not found.")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Add columns to note table
    cursor.execute("ALTER TABLE note ADD COLUMN file_url VARCHAR(500)")
    cursor.execute("ALTER TABLE note ADD COLUMN material_type VARCHAR(20) DEFAULT 'pdf'")
    
    # Make filename nullable (SQLite is tricky with this, but usually ALTER works if not adding NOT NULL)
    # Actually, in SQLite, columns are nullable by default unless NOT NULL is specified.
    # We can't easily remove NOT NULL from existing column without recreating table.
    # However, for now, we can just allow it to stay as it is if we always provide something,
    # OR we can do the recreation dance.
    
    print("Columns added successfully.")
    conn.commit()
except sqlite3.OperationalError as e:
    print(f"Operational error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
