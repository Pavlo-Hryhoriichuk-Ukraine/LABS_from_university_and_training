import sqlite3

print("1. Dialing the database...")
# This creates a file named 'guardian_test.db' in your current folder.
conn = sqlite3.connect('guardian_test.db')

print("2. Creating the cursor...")
cursor = conn.cursor()

print("3. Creating the table...")
# We use triple quotes (''') in Python to write multi-line strings.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS backups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        status TEXT
    )
''')

print("4. Inserting a fake backup record...")
# Notice we only provide filename and status. The 'id' is AUTOINCREMENT, so the DB handles it!
cursor.execute("INSERT INTO backups (filename, status) VALUES ('system_files.zip', 'success')")

print("5. Committing the changes (saving to disk)...")
conn.commit()

print("6. Reading the data back...")
cursor.execute("SELECT * FROM backups")
# fetchall() grabs all the rows the cursor just found and puts them in a Python list.
records = cursor.fetchall()

print("Here is what is inside the database:")
for row in records:
    print(row)

print("7. Closing the connection...")
conn.close()