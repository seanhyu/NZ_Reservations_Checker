from datetime import date
import re
import os


# This class create instances of user itinerary queries
class Query:
    def __init__(self,valid = False):
        self.valid = valid
        self.email = ""
        self.trail_value = ""
        self.track = ""
        self.month = 0
        self.year = 0
        self.day = 0
        self.group_size = 0
        self.query_id = ""
    
    # setter method for setting the great walk track
    def set_track(self) -> bool:
        
        try_again = "1"
        trail_value_lib = {"Milford Track":"873","Abel Tasman Coast Track":"875","Heaphy Track":"876","Kepler Track":"872",
                           "Lake Waikaremoana Track": "878","Paparoa Track":"880","Rakiura Track":"877","Routeburn Track":"874",
                           "Tongariro Northern Circuit":"879","Whanganui Journey":"881"}
        # continuously prompts users for the track unless the user quits
        while try_again == "1":
            # attempt to set trail_value
            track = input("What trail do you want to add/remove? ")
            if track not in trail_value_lib:
                try_again = input("Invalid track. Enter 1 if you want to try again, otherwise enter 0. ")
            else:
                self.track = track
                self.trail_value = trail_value_lib[track]
                return True
        return False
    
    # setter method for setting the date of the itinerary
    def set_date(self) -> bool:
        month_days = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        try_again = "1"
        # continuously prompts users for the date unless the user quits
        while try_again == "1":
            # attempt to get date
            try:
                self.month,self.day,self.year = map(int,input("Enter the date you want to check in the format MM-DD-YYYY ").split("-"))
            except:
                try_again = input("Invalid date format. Enter 1 if you want to try again, enter any other key to stop. ")
                continue
            today = date.today()
            if self.month in month_days and 0 <= self.year - today.year <= 1 and self.day > 0:
                # check if the date is in the future
                if self.year > today.year or self.month > today.month or (self.month == today.month and self.day >= today.day):
                    if self.year % 4 == 0 and self.month == 2:
                        if self.day <= 29:
                            return True
                    else:
                        if self.day <= month_days[self.month]:
                            return True
            # if function hasn't exited, then invalid input
            try_again = input("Invalid date. Enter 1 if you want to try again, enter any other key to stop. ")
            self.month = self.day = self.year = 0
        return False
    
    # setter method for setting the group size of the itinerary
    def set_group_size(self) -> bool:
        try_again = "1"
        # continuously prompts users for the group size unless the user quits
        while try_again == "1":
            try:
                self.group_size = int(input("Enter the size of your group: "))
                if 0 < self.group_size <= 25:
                    return True
                else:
                    try_again = input("Invalid size. Enter 1 if you want to try again, enter any other key to stop. ")
            except:
                try_again = input("Invalid size. Enter 1 if you want to try again, enter any other key to stop. ")
        return False
    

    # checks if emails are valid
    def is_valid_email(self) -> bool:

        """Check if the email is a valid format."""
        # regular expression for validating an Email
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

        # if the string matches the regex, it is a valid email
        if re.match(regex, self.email):
            return True
        else:
            return False
    
    # setter method for setting the email to send alerts to. Returns true if successful, false otherwise  
    def set_email(self) -> bool: 
        try_again = "1"
        # continuously prompts users for the email unless the user quits
        while try_again == "1":
            self.email = input("Enter the email: ")  
            if self.is_valid_email():
                return True
            else: 
                try_again = input("Invalid email. Enter 1 if you want to try again, enter any other key to stop. ")
        return False
    
    # attempts to set all fields and returns if it was successful
    def set_all_fields(self) -> bool:
        if self.set_track() and self.set_date() and self.set_group_size() and self.set_email():
            self.valid = True
            self.query_id = self.email + self.track + str(self.month) + str(self.day) + str(self.year) + str(self.group_size)
            return True
        return False