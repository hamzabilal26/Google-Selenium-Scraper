import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import openpyxl

options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
options.add_argument('--lang=en_US')

cities = [
    'South Padre Island',
    'Boca Chica Beach',
    'Laguna Vista',
    'Port Isabel',
    'Port Mansfield',
    'Laguna Madre',
    'Riviera Beach',
    'The Packery-Corpus Christi',
    'Ward Island',
    'North Beach - Corpus Christi',
    'Nueces Bay',
    'Big Shell Beach',
    'Little Shell Beach',
    'Malaquite Beach',
    'Padre Island National Seashore',
    'Padre Island/North Padre Island',
    'Whitecap Beach',
    'Mustang Island',
    'Ingleside On The Bay',
    'Port Aransas',
    'Redfish Bay',
    'Aransas Pass',
    'Rockport',
    'Rockport Beach',
    'Fulton',
    'Bayside',
    'Mission Bay',
    'Copano Bay',
    'Holiday Beach',
    'Aransas Bay',
    'San Jose Island',
    'Matagorda Island',
    'Alamo Beach',
    "Port O'Connor",
    'Port Lavaca',
    'Point Comfort',
    'Port Alto',
    'Shell Beach',
    'Palacios Bay Beach',
    'Palacios',
    'Matagorda Bay',
    'Matagorda Beach',
    'Sargent Beach',
    'Bryan Beach',
    'Surfside Beach',
    'San Luis Beach',
    'Pointe San Luis',
    'Half Moon Beach',
    'Terramar Beach',
    'Sea Isle Beach',
    'Indian Beach',
    'Acapulco Beach TX',
    'San Luis Pass',
    'Jamaica Beach TX',
    'Sand Art Beach',
    'Galveston Island State Park',
    'Palms Beach',
    'Pirates Beach',
    'Bermuda Beach',
    'West Beach (Texas)',
    'Beachside Village Beach',
    'Sunny Beach',
    "Babe's Beach",
    'Galveston Beach',
    'Poretto Beach',
    'Palisade Palms Public Beach',
    'Beachtown Beach',
    'East Beach (Texas)',
    'Galveston Island Seawall',
    'Stewart Beach',
    'Bolivar Beach',
    'Bolivar Peninsula',
    'Crystal Beach',
    'Beach Coast',
    'High Island Beach',
    'McFadden Beach',
    'Quintana Beach',
    'Sea Rim State Park',
    'Loyola Beach',
    'Tiki Island',
    'Sabine Pass',
]

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
url = "https://www.google.com/search?q=Ward+Island&oq=s&aqs=chrome.1.69i60j69i59l3j69i60l4.7121j1j7&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwjTsJ2ypdTzAhVTnWoFHbE3DrUQ8eoFKAJ6BAgUEA8&sxsrf=AOaemvIeL69wcCsjf_o3PoZRAV0-ien3pQ:1634571511099#fpstate=tldetail"
driver.get(url)

wb = openpyxl.Workbook()
ws = wb.active

for city in cities:
    input_field = driver.find_element(By.XPATH, "//input[@id='hs-qsb']")
    input_field.clear()

    input_field.send_keys(city)
    input_field.send_keys(Keys.ENTER)

    events_count = 0

    try:
        events = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='treeitem']")))
    except Exception as e:
        print(e)
    else:
        events_count = len(events)
        retry_count = 0
        while True:
            last_event = events[-1]
            driver.execute_script("arguments[0].scrollIntoView();", last_event)
            time.sleep(1)

            events = driver.find_elements(By.XPATH, "//div[@role='treeitem']")
            this_events_count = len(events)
            if this_events_count > events_count:
                retry_count = 0
                events_count = this_events_count
                continue
            else:
                retry_count += 1

            if retry_count > 10:
                break

        events = driver.find_elements(By.XPATH, "//div[@role='treeitem']")
        for event in events:
            driver.execute_script("arguments[0].scrollIntoView();", event)
            event.click()

            title = event.find_element(By.XPATH, ".//div[@class='YOGjf']").text
            print(f'title: {title}')

            date = event.find_element(By.XPATH, ".//div[@class='cEZxRc']").text
            print(f'date: {date}')

            address = event.find_element(By.XPATH, ".//div[@class='cEZxRc zvDXNd']").text
            print(f'address: {address}')

            this_row = [city, title, date, address]
            ws.append(this_row)
            time.sleep(0.2)

    wb.save('Data2.xlsx')
