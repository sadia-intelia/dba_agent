import sqlite3
from typing import Dict, Any

def check_database_lock()-> Dict[str, Any]:

# Connection 1: Lock database
    conn1 = sqlite3.connect('./mydatabase.db')
    conn1.execute("BEGIN EXCLUSIVE")
    print("Table locked. ")   

    # Connection 2: Try to access
    conn2 = sqlite3.connect('./mydatabase.db')
    msg = "Unlocked"
    try:
        conn2.execute("SELECT * FROM employees")
    except Exception as e:
        print(f"Error: {e}")
        msg = "Locked"

    finally:
        print("Unlocking the connection")
        conn1.commit()
        conn1.close()
        return {"status": "error", "message": str(msg)}
