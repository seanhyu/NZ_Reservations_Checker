<h1 align="center">New Zealand Great Walks Reservation Alerts</h1>
<p align="center">This program allows users to enter itineraries for any of New Zealand's Great Walks, and get notified through email if their itinerary is available for booking.</p>

# Features:
* Allows users to input specific itineraries for any of the New Zealand Great Walks, and for any date in the future, along with an email that they would like to be alerted at
* Stores information from all queries in an AWS Dynamodb database
* Upon running, the program goes through all entries in the database and attempts to find availability by using Selenium to open a browser and input the specified itineraries and check the number of spots available for the given itinerary
* If there are enough spots available for the given itinerary, the program uses SendGrid to email the user notifying them that their itinerary can be reserved, and then deletes their query from the database
  
# How to Run:
* Install Selenium, SendGrid, boto3
* Create a file named "Configs.py"
* Create a SendGrid account, set up email-sending capability based on an email of your choice, add the API key to the configs file with the variable name SENDGRID_KEY, and add the corresponding files as indicated by SendGrid
* Create an AWS account, set up a Dynamodb table, install the AWS Command Line Interface, and use the command "aws configure" to link your your AWS account to your current workstation. Then add your table name to your configs file.
* Run the program and enter your itinerary and email address accordingly. The program will either email you if there are enough spots available for your itinerary, or store your query in the database for future checking
* Configure your computer to auto-run the program each time you start up the computer so that it checks everyday.
