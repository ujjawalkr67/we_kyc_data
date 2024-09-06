import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import requests
import csv

LOGIN_URL = "https://portal.wekyc.io/auth/login"
DISCOVERY_URL = "https://portal.wekyc.io/merchant/completed_kyc_links"
EMAIL = "trade@dollarpe.com"
PASSWORD = "Doll@rPe@10"
ORDER_ID = "22664725443653197824"
#EMAIL = "ujjawal.cool.singh@gmail.com"
# PASSWORD = "ujjawal@123"
# ORDER_ID = "1234"


# Calculate the date one month back from today
one_month_ago = (datetime.now() - timedelta(days=30)).strftime('%d-%m-%Y')
print(one_month_ago)
driver = webdriver.Chrome()


def login_to_we_kyc(driver):
    driver.get(LOGIN_URL)# Open hyperauditor.com
    try:
        email_input = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.NAME, 'email'))
        )  # Wait for email feild to be visible

        email_input.send_keys(EMAIL)  # Populate input field

        password_input = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.NAME, 'password'))
        )  # Wait for password field to be visible

        password_input.send_keys(PASSWORD)  # Populate input field
        password_input.send_keys(Keys.RETURN)  # Press enter
        time.sleep(5)  # Wait for browser to login
        csv_headers = [["Order_Id", "Created_At", "Name", "Mobile_No",
                        "Status", "Adhar_name", "Aadhar_No","Adhar_selfie_url", "Date_Of_Birth",
                        "Country", "State", "District","Sub_District",
                        "Village/City", "Address", "PAN_Document_No",
                        "PAN_Name", "Aadhaar_Kyc_User_Mobile_match_status",
                        "Selfie_Match_Percentage", "Completed_Order",
                        "Finish_Rate_100", "Register_Days",
                        "Completed_Order_Num", "Finish_Rate", "IP",
                        "Browser", "Browser_Version", "OS", "Device",
                        "Document_Link_Status",
                        "selfie_url"]]
        with open('data.csv', 'a+', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(csv_headers)

        driver.get(DISCOVERY_URL)  # Navigate to target url
        time.sleep(5)

    except Exception as e:
        raise e


def set_search_filters(driver, date, order_id):
    try:
        # Wait for the "from date" input field and set the date
        from_date_input = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.NAME, 'from_date'))
        )
        from_date_input.clear()  # Clear the current value
        from_date_input.send_keys(date)  # Set the date one month back
        from_date_input.send_keys(Keys.RETURN)  # Hit Enter to submit the date
        time.sleep(5)
        # Input the order ID in the order ID field
        order_id_input = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.NAME, 'client_txn_id'))
        )
        order_id_input.send_keys(order_id)
        order_id_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for the search results to load

        first_result_link = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tab_block_1"]/div/div/div/div[2]/div/div[1]/table/tbody/tr[1]/td[7]/a'))
        )
        first_result_link.click()
        time.sleep(5)

        scrape_user_data(driver)
    except Exception as e:
        raise e


def scrape_user_data(driver):
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
    try:
        data_list = []
        data_row_list = []
        order_id = '//*[@id="tab_block_1"]/div/div/div[2]/div/div/div/div/div/div[1]/div/h6'
        order = wait.until(EC.presence_of_element_located((By.XPATH, order_id)))
        print(order.text)

        Created_at = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[2]/div/div/div/div/div/div[2]/div/h6')
        data_row_list.append(Created_at.text)
        
        Name = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[2]/div/div/div/div/div/div[3]/div/h6')
        data_row_list.append(Name.text)

        Mobile_No = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[2]/div/div/div/div/div/div[4]/div/h6')
        data_row_list.append(Mobile_No.text)

        Status = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[2]/div/div/div/div/div/div[5]/div/h6/span')
        data_row_list.append(Status.text)

        time.sleep(3)
        open_link = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tab_block_1"]/div/div/div[3]/div/div[3]/div/a'))
        )
        driver.execute_script("arguments[0].click();", open_link)
        time.sleep(3)

        # AADHAR INFORMATION:-
        Adhar_name = driver.find_element(By.XPATH, '//*[@id="name"]')
        data_row_list.append(Adhar_name.text)

        Aadhar_No = driver.find_element(By.XPATH, '//*[@id="aadhar_no"]')
        data_row_list.append(Aadhar_No.text)

        Adhar_selfie_url = driver.find_element(By.XPATH, '//*[@id="view_aadhar_detail"]/div/div/div[2]/div[2]/div/div[2]/img')
        image_url2 = Adhar_selfie_url.get_attribute('src')
        data_row_list.append(image_url2)

        Date_Of_Birth = driver.find_element(By.XPATH, '//*[@id="dob"]')
        data_row_list.append(Date_Of_Birth.text)

        Country = driver.find_element(By.XPATH, '//*[@id="country"]')
        data_row_list.append(Country.text)
        State = driver.find_element(By.XPATH, '//*[@id="state"]')
        data_row_list.append(State.text)
        District = driver.find_element(By.XPATH, '//*[@id="dist"]')
        data_row_list.append(District.text)
        Sub_District = driver.find_element(By.XPATH, '//*[@id="subdist"]')
        data_row_list.append(Sub_District.text)
        Village = driver.find_element(By.XPATH, '//*[@id="vtc"]')
        data_row_list.append(Village.text)
        Address = driver.find_element(By.XPATH, '//*[@id="address"]')
        data_row_list.append(Address.text)
        close_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="view_aadhar_detail"]/div/div/div[3]/button'))
        )
        close_button.click()
        time.sleep(2) 

        #pan information
        PAN_Document_No = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[4]/div/div[2]/div[2]/div[1]/div/h6')
        data_row_list.append(PAN_Document_No.text)
        PAN_Name = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[4]/div/div[2]/div[2]/div[1]/div/h6')
        data_row_list.append(PAN_Name.text)

        Aadhaar_Kyc_User_Mobile_match_status = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[7]/div/div[2]/div[2]/div[2]/div/h6')
        data_row_list.append(Aadhaar_Kyc_User_Mobile_match_status.text)
        Selfie_Match_Percentage = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[8]/div/div[2]/div[2]/div[2]/div/h4')
        data_row_list.append(Selfie_Match_Percentage.text)

        #historial order
        Completed_Order = driver.find_element(By.XPATH, ' //*[@id="tab_block_1"]/div/div/div[9]/div/div[2]/div/div[1]/div/h6')
        data_row_list.append(Completed_Order.text)

        Finish_Rate_100 = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[9]/div/div[2]/div/div[2]/div/h6')
        data_row_list.append(Finish_Rate_100.text)

        Register_Days = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[9]/div/div[2]/div/div[3]/div/h6')
        data_row_list.append(Register_Days.text)

        Completed_Order_Num = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[9]/div/div[2]/div/div[4]/div/h6')
        data_row_list.append(Completed_Order_Num.text)

        Finish_Rate = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[9]/div/div[2]/div/div[5]/div/h6')
        data_row_list.append(Finish_Rate.text)

        #device INfo
        IP = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[10]/div/div[2]/div/div[1]/div/h6/span')
        data_row_list.append(IP.text)
        Browser = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[10]/div/div[2]/div/div[2]/div/h6')
        data_row_list.append(Browser.text)
        Browser_Version = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[10]/div/div[2]/div/div[3]/div/h6')
        data_row_list.append(Browser_Version.text)
        OS = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[10]/div/div[2]/div/div[4]/div/h6')
        data_row_list.append(OS.text)
        Device = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[10]/div/div[2]/div/div[5]/div/h6')
        data_row_list.append(Device.text)
        Document_Link_Status = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[11]/div/div[2]/div[2]/div[2]/div/h6')
        data_row_list.append(Document_Link_Status.text)
        selfie_url = driver.find_element(By.XPATH, '//*[@id="tab_block_1"]/div/div/div[5]/div/div[2]/div/div/img')
        image_url = selfie_url.get_attribute('src')
        data_row_list.append(image_url)

        data_list.append(data_row_list)
        with open('data.csv', 'a+', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(data_list)  # Creates CSV with headers



    except Exception as e:
        raise e

try:
    login_to_we_kyc(driver)
    set_search_filters(driver, one_month_ago, ORDER_ID)
finally:
    driver.quit()
