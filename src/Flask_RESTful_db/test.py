import sqlite3  # allow to connect with a sqlite database, and run sql queries

connection = sqlite3.connect("data.db")

cursor = connection.cursor()
# for executing the query and store the result

create_table = "CREATE TABLE users (id int, username text, password text)"
# columns: id, username, password

cursor.execute(create_table)

user = (1, "jose", "asdf")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)  # don't need to specify the ?

users = [(2, "rolf", "asdf"), (3, "anne", "xyz")]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
