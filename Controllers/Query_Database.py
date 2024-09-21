import boto3
import Controllers.Web_Nav
import Controllers.Email_Sender 
from Configs import TABLE_NAME

class Query_Database:

    def __init__(self):
        # access AWS DynamoDB
        self.table = boto3.resource('dynamodb').Table(TABLE_NAME) 
    
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
    
    def delete_query(self,id):
        self.table.delete_item(Key={"NZGreatWalksAlerts": id})

    
    def send_emails_if_available(self):
        # get all queries
        queries = self.get_database_queries()

        # initiate a web_browers object with the Great Walks bookings
        web_browser = Controllers.Web_Nav.Web_Nav("https://bookings.doc.govt.nz/Web/Facilities/SearchViewGreatWalk.aspx")
        
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
                # if the itinerary is available, send the email and delete the query
                if web_browser.check_if_available(trail_value,month,day,year,group_size):
                    Controllers.Email_Sender.send_email(email)
                    self.delete_query(id)

            except:
                print("Failed to send emails")
            # reset the search back to the first page to prepare for the next query
            web_browser.reset('https://bookings.doc.govt.nz/Web/Facilities/SearchViewGreatWalk.aspx')