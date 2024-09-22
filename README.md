<h1 align="center">New Zealand Great Walks Reservation Alerts</h1>
<p align="center">This program allows users to enter itineraries for any of New Zealand's Great Walks, and get notified through email if their itinerary is available for booking.</p>

# Features:
* Allows users to input specific itineraries for any of the New Zealand Great Walks, and for any date in the future, along with an email that they would like to be alerted at
* Stores information from all queries in an AWS Dynamodb database
* Can be run in interactive mode or non-interactive mode: if in interactive mode, then program allows user to add or delete itineraries; in non-interactive mode, the program checks all itineraries in the database for availabilities 
* If there are spots available for the given itinerary, the program uses SendGrid to email the user notifying them that their itinerary can be reserved, and then deletes their query from the database
  
# How to Run:
* Install Selenium, SendGrid, boto3
* Create a file named "Configs.py"
* Create a SendGrid account, set up email-sending capability based on an email of your choice, add the API key to the configs file with the variable name SENDGRID_KEY, add the email address you would like to have your emails sent from to the configs file with the variable name FROM_EMAIL, and add the corresponding files as indicated by SendGrid
* Create an AWS account, set up a Dynamodb table, install the AWS Command Line Interface, and use the command "aws configure" to link your your AWS account to your current workstation. Then add your table name to your configs file.
* To run the program, use the command line to run the main.py file, along with 3 arguments: "-interactive" takes in any non-zero number as interactive mode, "-repetitions" takes in a non-negative integer number of availability checks, and "-interval" takes in a non-negative integer number of minutes between availability checks
* (For example, run python3 main.py "-interactive" 1 "-repetitions" 2 "-interval" 60)
* Configure your computer to run the script upon the computer's start-up in non-interactive mode so that it checks for availabilites in the background
