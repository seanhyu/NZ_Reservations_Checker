import Controllers.web_nav
import Controllers.query_database
import Models.query

# Create instance of database
db = Controllers.query_database.Query_Database()

# Ask if user wants to enter a new query
add_data = input("Would you like to enter a new query? Enter 1 for yes, enter any other key for no: ")
if add_data == "1":
# Creat new instance of a query
    current_query = Models.query.Query()

    # Prompt user for all required fields
    # If user supplies all fields, run the web automation
    if current_query.set_all_fields():
        response = db.add_to_database(current_query)
    # otherwise delete the object
    else:    
        del current_query

# Checks all queries in the database for availability and sends emails to those with availabilities found
all_queries = db.send_emails_if_available()

