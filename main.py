import Controllers.query_database

def main(interactive_mode=True, duration=12, interval=1):

    '''
    interactive refers to whether the program should take input from user
    duration refers to how long the program will run for in the background in hours
    interval refers to how often the program will run the reservation availability check
    '''
    # creates instance of Query_Database 
    db = Controllers.query_database.Query_Database()

    # runs only if the program is interactive
    if interactive_mode:
        # adds new query if user wants to
        db.add_query_to_db()

        # deletes a query if user wants to
        db.delete_query_from_db()
    
    
    # checks all queries in the database for availability and sends emails to those with availabilities found
    db.send_emails_if_available()


if __name__ == '__main__':
    main()

