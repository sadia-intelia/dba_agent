import sqlite3

def setup_db():
    conn = sqlite3.connect('mydatabase.db')  # this creates the file if it doesn't exist
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        );
    ''')

    # Optional: Insert sample data
    cursor.execute("INSERT INTO employees (name, role) VALUES (?, ?)", ("Alice", "Engineer"))
    cursor.execute("INSERT INTO employees (name, role) VALUES (?, ?)", ("Bob", "Manager"))

    conn.commit()
    conn.close()
    print("✅ Database 'mydatabase.db' and table 'employees' created.")

if __name__ == "__main__":
    setup_db()
