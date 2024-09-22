from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import WebDriverException

from datetime import date

# this class runs the web automation process that checks if itineraries are available
class Web_Nav:

    # initiates the web driver
    def __init__(self,url = ""):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach",True)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(2)
        self.driver.get(url)

    # chooses the trail on the site
    def choose_trail(self,trail_value):
        trail_input_element = self.driver.find_element(By.NAME,"ctl00$ctl00$mainContent$homeContent$ddlPlaces")
        trail_input_element.click()
        dropdown = Select(trail_input_element)
        dropdown.select_by_value(trail_value)
    
    # calculates the row and column of the itinerary day on the booking calendar
    def day_calendar_grid_finder(self,month,day,year):
        
        # calculate which day of the week the first is using a farmer's almanac formula
        last_two_digits_of_year = year % 100
        quarter_of_last_two_digits = last_two_digits_of_year // 4
        regular_month_keys = {1:1,6:5,7:0,2:4,8:3,9:6,3:4,10:1,4:0,11:4,5:2,12:6}
        leap_month_keys = {1:0,6:5,7:0,2:3,8:3,9:6,3:4,10:1,4:0,11:4,5:2,12:6}
        if year % 4 == 0:
            month_key = leap_month_keys[month]
        else:
            month_key = regular_month_keys[month]
        if year < 2099:
            month_key -= 1
        first_day_of_the_week = (last_two_digits_of_year + quarter_of_last_two_digits + month_key + 1) % 7
        
        if first_day_of_the_week == 0:
            first_day_of_the_week = 7
        
        # calculate which week of the month the date is
        test_day = 1
        week_number = 1
        
        while day - test_day >= 7:
            week_number += 1
            test_day += 7
        for _ in range(day - test_day):
            first_day_of_the_week += 1
            if first_day_of_the_week == 8:
                week_number += 1
                first_day_of_the_week = 1
        
        # returns the grid row and column for the calendar on the site
        return (str(week_number),str(first_day_of_the_week))

         
    # sets the date on the booking site
    def choose_date(self,month,day,year):

        # checks today's date, and then clicks to the corresponding both based on the difference between today's month and the specified month
        today = date.today()
        if today.year == year:
            month_clicks = month - today.month
        else:
            month_clicks = month + 12 - today.month
        date_input_element = self.driver.find_element(By.NAME,"ctl00$ctl00$mainContent$homeContent$txtArrivalDate")
        date_input_element.click()
        for _ in range(month_clicks):
            month_clicker = self.driver.find_element(By.XPATH,"//span[@class='ui-icon ui-icon-circle-triangle-e']" )
            month_clicker.click()
        calendar_row,calendar_col = self.day_calendar_grid_finder(month,day,year)
        day_xpath = '//*[@id="ui-datepicker-div"]/table/tbody/tr[' + calendar_row + ']/td[' + calendar_col + ']'
        day_clicker = self.driver.find_element(By.XPATH, day_xpath)
        day_clicker.click()
    
    # sets the size of the itinerary on the site
    def choose_size(self,size):
        if size == 1:
            return
        size_input_element = self.driver.find_element(By.NAME,"ctl00$ctl00$mainContent$homeContent$ddlParty")
        size_input_element.click()
        dropdown = Select(size_input_element)
        dropdown.select_by_value(str(size))
        size_input_element.click()
    
    # searches the set itinerary
    def search(self):
        search_button = self.driver.find_element(By.ID,"mainContent_homeContent_btnSearch")
        search_button.click()
    
    # resets the browser back to the specified url
    def reset(self,url):
        self.driver.get(url)

    
    # attempts to check if the itinerary is available and returns True if it is
    def check_if_available(self,trail_value,month,day,year,size) -> bool:
        try:
            self.choose_trail(trail_value)
            self.choose_date(month,day,year)
            self.choose_size(size)
            self.search()
            spot_string = self.driver.find_element(By.ID,"mainContent_homeContent_ugGreatWalkGrid_ctl03").get_attribute("title")
            spots = int(spot_string[-2:])
            return spots >= size        
        except:
            return False
    
    def close_chrome(self):
        try:
            self.driver.quit()
            return True
        except:
            return False