import argparse
import sys
import time

import Controllers.query_database

def main(interactive_mode=True, repetitions=12, interval=60):

    '''
    interactive refers to whether the program should take input from user
    repetitions refers to how many times the program will run the checking function
    interval refers to how often the program will run the reservation availability check in minutes
    '''
    # creates instance of Query_Database 
    db = Controllers.query_database.QueryDatabase()

    # runs only if the program is interactive
    if interactive_mode:
        # adds new query if user wants to
        db.add_query_to_db()

        # deletes a query if user wants to
        db.delete_query_from_db()
        
    else:
        # runs the auto-run script
        auto_run(repetitions,interval)

def auto_run(repetitions=12,interval=60):
    '''
    Repetitions refers to number of time the program will run the checking function
    Interval refers to how many minutes in between runs
    '''
    
    for _ in range(repetitions):
        # creates instance of Query_Database 
        db = Controllers.query_database.QueryDatabase()
        
        # checks all queries in the database for availability and sends emails to those with availabilities found
        db.send_emails_if_available()

        # runs this piece of code every "interval" hours until duration is over
        time.sleep(interval*60)

# allows funciton to be run only when the module is run directly, not when it is imported
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Determines whether function is run interactively.")
    parser.add_argument("-interactive",type=int,help="Run interactive? Enter 1 for yes, 0 for no.")
    parser.add_argument("-repetitions",type=int,help="Enter a positive integer number for number of times the program will check availabilities before terminating.")
    parser.add_argument("-interval",type=int,help="Enter a positive integer number for the number of minutes in between subsequent checks for availabilities.")
    if len(sys.argv) == 1:
        main()
    else:
        args = parser.parse_args()
        interactive = args.interactive if args.interactive else True
        repetitions = args.repetitions if args.repetitions else 12
        interval = args.interval if args.interval else 60
        print(f"""The arguments you entered are: interactive: {interactive}, repetitions: {repetitions}x, interval: {interval} minutes""")
        main(interactive,repetitions,interval)




