import boto3
from datetime import date

from configs import TABLE_NAME
import Controllers.web_nav
import Controllers.email_sender 
import Models.query

class QueryDatabase:

    def __init__(self):
        # access AWS DynamoDB
        self.table = boto3.resource('dynamodb').Table(TABLE_NAME) 
    
    def add_query_to_db(self):
        # ask if user wants to add an itinerary, if not then return
        save_to_database = input("Would you like to enter a new itinerary? Enter 1 for yes, enter any other key for no: ")
        if save_to_database != "1":
            return
        
        # initiate a Query object
        current_query = Models.query.Query()

        # prompt user for all required fields, and if user supplies all fields, checks if the itinerary is available
        if current_query.set_all_fields():
            
            web_browser = Controllers.web_nav.WebNav("https://bookings.doc.govt.nz/Web/Facilities/SearchViewGreatWalk.aspx")
            
            try:
                found = web_browser.check_if_available(current_query.trail_value,current_query.month,current_query.day,current_query.year,current_query.group_size)
                web_browser.close_chrome()
                if found:
                    print("Your itinerary was found, we will send an email with the available itinerary.")
                    Controllers.email_sender.send_email(current_query.email,current_query.track,current_query.month,current_query.day,current_query.year,current_query.group_size)
                else:
                    add_to_db = input("Your itinerary was not available. Would you like to save the itinerary for future checking? Enter 1 for yes, enter any other key for no: ")
                    if add_to_db == "1":
                        self.add_to_database(current_query)
            except:
                web_browser.close_chrome()
        
        # otherwise delete the object
        else:    
            del current_query
    
    def delete_query_from_db(self):
        delete_from_database = input("Would you like to remove an itinerary? Enter 1 for yes, enter any other key for no: ")
        if delete_from_database != "1":
            return
        else:
            # initiate a Query object
            current_query = Models.query.Query()

            # prompt user for all required fields, and if user supplies all fields, add it to the database
            if current_query.set_all_fields():
                self.delete_query(current_query.query_id) 
            del current_query
    
    def add_to_database(self,current_query):
        # add current_query to the database
        response = self.table.put_item(
            Item={
                "NZGreatWalksAlerts":current_query.query_id,
                "email":current_query.email,
                "track":current_query.track,
                "trail_value":current_query.trail_value,
                "month":current_query.month,
                "day":current_query.day,
                "year":current_query.year,
                "group_size":current_query.group_size,
            }
        )
    def get_database_queries(self):
        response = self.table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        return data
    
    # removes an itinerary from the database
    def delete_query(self,id):
        try:
            self.table.delete_item(Key={"NZGreatWalksAlerts": id})
        except:
            print("Itinerary not found!")

    
    def send_emails_if_available(self):
        # get all queries
        queries = self.get_database_queries()

        # initiate a web_browers object with the Great Walks bookings
        web_browser = Controllers.web_nav.WebNav("https://bookings.doc.govt.nz/Web/Facilities/SearchViewGreatWalk.aspx")
        
        try:
            # check each query to see if the itinerary is available
            for query in queries:
                id = query["NZGreatWalksAlerts"]
                email = query["email"]
                track = query["track"]
                trail_value = query["trail_value"]
                month = int(query["month"])
                day = int(query["day"])
                year = int(query["year"])
                group_size = int(query["group_size"])
                try:
                    today = date.today()
                    # if itinerary is in the past, delete it
                    if year < today.year or year == today.year and (month < today.month or (month == today.month and day < today.day)):
                        self.delete_query(id)
                    # if the itinerary is available, send the email and delete the query
                    elif web_browser.check_if_available(trail_value,month,day,year,group_size):
                        Controllers.email_sender.send_email(email,track,month,day,year,group_size)
                        self.delete_query(id)

                except:
                    print("Failed to send emails")
                # reset the search back to the first page to prepare for the next query
                web_browser.reset('https://bookings.doc.govt.nz/Web/Facilities/SearchViewGreatWalk.aspx')
        
        # Close Chrome once finished
        finally:
            web_browser.close_chrome()