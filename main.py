import Controllers.query_database

# Create instance of database
db = Controllers.query_database.Query_Database()

# Adds new query if user wants to
db.add_query_to_db()

# Deletes a query if user wants to
db.delete_query_from_db()

# Checks all queries in the database for availability and sends emails to those with availabilities found
all_queries = db.send_emails_if_available()

