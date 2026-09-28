import sqlite3

def init_db(db_name="bugs.db"):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS bugs (
            bug_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
  conn.commit()
  conn.close()

def add_bug_to_db(title, priority, status, created_at, db_name= "bugs.db"):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("""INSERT INTO bugs(title, priority, status, created_at)
                 VALUES (?,?,?,?)
                 """, (title, priority, status, created_at))
  conn.commit()
  conn.close()

def get_all_bugs(db_name= "bugs.db"):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM bugs")
  bugs = cursor.fetchall()
  conn.close()
  return bugs

def delete_bug_from_db(bug_id, db_name= "bugs.db"):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM bugs WHERE bug_id = ?", (bug_id,))
  conn.commit()
  conn.close()

def update_bug_status(new_status, bug_id, db_name= "bugs.db"):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("UPDATE bugs SET status = ? WHERE bug_id = ?", (new_status, bug_id))
  conn.commit()
  conn.close()

def update_bug_priority(new_priority, bug_id, db_name= "bugs.db"):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("UPDATE bugs SET priority = ? WHERE bug_id = ?", (new_priority, bug_id))
  conn.commit()
  conn.close()


  



