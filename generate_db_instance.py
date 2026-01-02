import sqlite3

# Path to SQL File
sql_file_path = 'project.sql'

# Connect to the SQLite database
conn = sqlite3.connect('project.db')
cursor = conn.cursor()

# Enable Foreign Key Constraint
conn.setconfig(sqlite3.SQLITE_DBCONFIG_ENABLE_FKEY,True)

# Open and read the SQL file if database is new
res = cursor.execute("SELECT name FROM sqlite_master")
if(len(res.fetchall()) == 0):
  with open(sql_file_path, 'r') as sql_file:
    sql_script = sql_file.read()

  # Execute the SQL script if database is new
  cursor.executescript(sql_script)

  # Commit the changes and close the connection if database is new
  conn.commit()

# Close Cursor and Connection
cursor.close()
conn.close()