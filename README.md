# Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit
## Project Description
This project automates the extraction of bus travel data such as  bustype, route, price range, star rating, seat availability using Selenium. It offers a streamlined solution for analyzing and visualizing data, empowering efficient decision-making and enhancing operational strategies in the transportation industry.
## Key Features
- **State and Route Filtering**: Retrieve bus details by selecting a specific state and its associated route name.
- **Price Range Customization**: Filter buses based on a user-defined price range for precise results.
- **Targeted Bus Information**: Displays relevant details for buses matching the selected state, route name and price range criteria.
## Technologies Used in this Project
-  Web Scraping using Selenium
-  Python
-  SQL
-  Streamlit
## Run Locally

Clone the project

```bash
  git clone https://github.com/HarithaSree74/redbus-.git
```

Go to the project directory

```bash
  cd "demo.py"
```

Install dependencies

```bash
  pip install streamlit
  pip install pymysql
  
```

Start the server

```bash
  streamlit run app.py 
```
## Data Collection and Processing
This application uses Selenium to scrape bus details for different states from Redbus. Below is an example code snippet for scraping data from one state. The same logic can be extended to the other states by changing the specific state names.

- Python script for scraping data from one state

```python
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 

#chandigarh
driver=webdriver.Chrome()  

driver.get("https://www.redbus.in/online-booking/chandigarh-transport-undertaking-ctu")

driver.maximize_window()

#RETRIVE BUS LINKS AND ROUTE

wait=WebDriverWait(driver,10)
def Chan_link_route(path):
    LINKS_CHAN=[]    
    ROUTE_CHAN=[]
    #RETRIVE THE ROUTE LINKS
    for i in range(1,4):
        paths=driver.find_elements(By.XPATH,path)

        for links in paths:
            d=links.get_attribute("href")
            LINKS_CHAN.append(d)

        #RETRIVE THE ROUTE
        for route in paths:
            ROUTE_CHAN.append(route.text)

        if i < 3:  # Don't try to click next on the last page
            try:
            # Locate the pagination container
                pagination_container = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div[4]/div[12]')
            ))

            # Locate the next page button within the container
                next_page_button = pagination_container.find_element(
                By.XPATH, f'.//div[contains(@class, "DC_117_pageTabs") and text()="{i + 1}"]'
            )

            # Ensure the next page button is in view
                actions = ActionChains(driver)
                actions.move_to_element(next_page_button).perform()
                time.sleep(1)  # Wait for a bit after scrolling

            # Log the action
                print(f"Clicking on page {i + 1}")

            # Click the next page button
                next_page_button.click()

            # Wait for the page number to update to the next page
                wait.until(EC.text_to_be_present_in_element(
                (By.XPATH, '//div[contains(@class, "DC_117_pageTabs DC_117_pageActive")]'), str(i + 1)))

            # Log the successful page navigation
                print(f"Successfully navigated to page {i + 1}")

            # Wait for a short duration to ensure the next page loads completely
                time.sleep(3)
            except Exception as e:
                print(f"An error occurred while navigating to page {i + 1}: {e}")
                break
    return LINKS_CHAN,ROUTE_CHAN 
LINKS_CHAN,ROUTE_CHAN=Chan_link_route("//a[@class='route']")

#convert to dataframe
df_CH=pd.DataFrame({"Route_name":ROUTE_CHAN,"Route_Links":LINKS_CHAN})
print(df_CH)
df_CH.to_csv("df_CH.csv",index=False)
df_CH

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def find_seats_available(bus):
    seats_xpath_options = [
        './/div[contains(@class, "seat-left")]',
        './/div[@class="seat-left m-top-30"]',
        './/div[contains(text(), "seats")]',
        './/div[contains(@class, "availSeats")]',
        './/div[contains(text(), "Seats Available")]'
    ]
    
    for xpath in seats_xpath_options:
        try:
            # Try to find seats element within the bus element
            seats_element = bus.find_element(By.XPATH, xpath)
            seats = seats_element.text
            return seats
        except (NoSuchElementException, Exception):
            continue
    
    return "Seats Not Found"

# Main scraping code
driver = webdriver.Chrome()
chan_data = []

for index in df_CH.index:
    link = str(df_CH.loc[index, 'Route_Links'])
    routes = str(df_CH.loc[index, 'Route_name'])
    
    driver.get(link)
    driver.maximize_window()
    time.sleep(2)  # Ensure page loads
    
    # Click all buttons if needed
    buttons = driver.find_elements(By.CSS_SELECTOR, "div[class='button']")
    for i in range(len(buttons)-1, -1, -1):
        buttons[i].click()
    
    # Scroll to the bottom of the page
    for t in range(25):
        driver.execute_script("window.scrollBy(0,650);") 
        time.sleep(1)
    
    try:
        # Wait for bus list to load
        bus_list = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="clearfix bus-item"]'))
        )
    except TimeoutException:
        print("Timeout occurred. Trying alternative methods:") 
        
    
    for bus in bus_list:
        try:
            bus_info = {
                'route_name': routes,
                'route_link': link,
                'bus_name': bus.find_element(By.XPATH, './/div[@class="travels lh-24 f-bold d-color"]').text,
                'bus_type': bus.find_element(By.XPATH, './/div[@class="bus-type f-12 m-top-16 l-color evBus"]').text,
                'departing_time': bus.find_element(By.XPATH, './/div[@class="dp-time f-19 d-color f-bold"]').text,
                'duration': bus.find_element(By.XPATH, './/div[@class="dur l-color lh-24"]').text,
                'reaching_time': bus.find_element(By.XPATH, './/div[@class="bp-time f-19 d-color disp-Inline"]').text,
                'star_rating': bus.find_element(By.XPATH, './/div[@class="clearfix row-one"]/div[@class="column-six p-right-10 w-10 fl"]').text,
                'price': bus.find_element(By.XPATH, './/div[@class="fare d-block"]').text,
                # New seats availability extraction
                'seats_availability': find_seats_available(bus)
            }
            chan_data.append(bus_info)
        except Exception as e:
            print(f"Error extracting bus info: {e}")
    
    print(f"Successfully scraped {routes}")

print("Successfully scraped all routes")
driver.quit()

# Convert the list of dictionaries to a DataFrame
df_CH_buses = pd.DataFrame(chan_data)

# Save to CSV
df_CH_buses.to_csv('chandigarh_bus_data.csv', index=False)

# Print the DataFrame to verify
print(df_CH_buses)
df_CH_buses


```
- Python script for SQL database interaction

SQL Connection

```bash
import mysql.connector

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",
)

print(mydb)
mycursor = mydb.cursor(buffered=True)
```

Create a database

```bash
  mycursor.execute("CREATE DATABASE project_one")
```

Create a table for that database

```bash
  mycursor.execute("""CREATE TABLE project_one.bus_routes(
                 ID INT AUTO_INCREMENT PRIMARY KEY,
                 route_name VARCHAR(255),
                 route_link VARCHAR(255),
                 bus_name VARCHAR(255),
                 bus_type VARCHAR(255),
                 departing_time VARCHAR(255),
                 duration VARCHAR(255),
                 reaching_time VARCHAR(255),
                 star_rating FLOAT,
                 price FLOAT,
                 seat_availability VARCHAR(255) 
                 
                 )""")
print("Table created successfully")
  
```

Insert data into the created table

```bash
insert_query = """INSERT INTO project_one.bus_routes (
                route_name,
                route_link,
                bus_name,
                bus_type,
                departing_time,
                duration,
                reaching_time,
                star_rating,
                price,
                seat_availability
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

# Convert DataFrame to list of tuples
data = final_df.values.tolist()
mycursor.executemany(insert_query, data)
mydb.commit()
print("values inserted successfully")
```


  
