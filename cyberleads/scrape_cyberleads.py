import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
from lib.user_agent import get_user_agent
import csv


def start_crawl():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"user-agent:{get_user_agent('random')}")
    wait_time = 10
    timeout = 30
    retry_wait_time = 60

    #https://www.getcyberleads.com/directories/companies/C?page=171
    # for url in ['https://www.getcyberleads.com/directories/companies/A?page=159','https://www.getcyberleads.com/directories/companies/B?page=121']:
    # url = 'https://www.getcyberleads.com/directories/companies/S?page=129'
    url = 'https://www.getcyberleads.com/directories/companies/P?page=81'
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    parse_url(driver, wait_time, timeout, retry_wait_time)

    driver.quit()
    print('finised')
    
    # for letter in range(ord('T'), ord('Z')+1):
    #     driver = webdriver.Chrome(options=options)
    #     start_url = f'https://www.getcyberleads.com/directories/companies/{chr(letter)}'
    #     driver.get(start_url)
    #     parse_url(driver, wait_time, timeout, retry_wait_time)
    #     driver.quit()

def parse_url(driver, wait_time, timeout, retry_wait_time):
    while True:
        elements = driver.find_elements(By.XPATH, '//div[@class="company-post"]/div/ul/li/a')
        urls = [elem.get_attribute("href") for elem in elements]
        for url in urls:
            # time.sleep(wait_time)  # wait for 10 seconds between requests
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--no-sandbox')
                options = webdriver.ChromeOptions()
                options.add_argument('--disable-extensions')
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                # options = Options()
                # options.add_argument('--headless')  # use headless browser mode
                options.add_argument(f"user-agent:{get_user_agent('random')}")
                detail_driver = webdriver.Chrome(options=options)
                detail_driver.get(url)
                print('*'*100, 'scraping started with', url)
                parse_details(detail_driver)
                detail_driver.quit()
            except Exception as e:
                print('Error loading details page:', url, e)

        next_page = driver.find_elements(By.XPATH, '//div[@class="pagination"]/a[@class="next_page"]')
        if next_page:
            next_page_url = next_page[0].get_attribute("href")
            print('#'*20, next_page_url)
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--no-sandbox')
                options = webdriver.ChromeOptions()
                options.add_argument('--disable-extensions')
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                # options = Options()
                # options.add_argument('--headless')  # use headless browser mode
                options.add_argument(f"user-agent:{get_user_agent('random')}")
                next_driver = webdriver.Chrome(options=options)
                next_driver.get(next_page_url)
                driver.quit()
                driver = next_driver
            except:
                print('Error loading next page:', next_page_url)
                break
        else:
            break

    time.sleep(retry_wait_time)  # wait for 10 seconds between requests

    try:
        if "Retry later" in driver.find_element(By.XPATH, '//body/pre').text:
            print("Received 'Retry later' message. Waiting for 30 seconds before retrying.")
            time.sleep(60)
            driver.get(driver.current_url)  # use the current URL instead of next_page_url
            parse_url(driver, wait_time, timeout, retry_wait_time)  # call the same function again to retry
    except NoSuchElementException:
        print("Could not find 'Retry later' message. Continuing with next page.", driver.current_url)


def parse_details(driver):
    # Get website URL
    details = {}
    elements = driver.find_elements(By.XPATH,'//div[@class="column field"]')
    for element in elements:
        
        key = element.find_element(By.XPATH, './/p[@class="data-point-title"]/b').text
        try:
            val = element.find_element(By.XPATH, './/p[@class="data-point-subtitle"]').text
        except NoSuchElementException:
            val = element.find_element(By.XPATH, './/a')
            if val.get_attribute("href"):
                val = val.get_attribute("href")
            else:
                val = val.text

        details[key] = val

    details['url'] = driver.current_url
    faq_dict = {}

    faq_questions = driver.find_elements(By.XPATH,'//a[@class="faq-question"]')
    faq_answers = driver.find_elements(By.XPATH,'//p[@class="faq-accordion-answer"]')
    for question, answer in zip(faq_questions, faq_answers):
        answer_text = answer.get_attribute("innerText").replace("\n", "").replace("\t", "")
        faq_dict[question.text] = answer_text

    details['faq'] = faq_dict

    technologies_url = driver.current_url+'/technologies'
    technologies_stack(technologies_url, details)

def technologies_stack(url, data):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"user-agent:{get_user_agent('random')}")
    technologies_driver = webdriver.Chrome(options=options)
    technologies_driver.get(url)
    stack_text = []
    stacks = technologies_driver.find_elements(By.XPATH,'//div[@class="company-post"]/div[@class="columns data-points-columns"]/div[@class="column field"]/p[@class="data-point-title"]/b')
    for stack in stacks:
        stack_text.append(stack.text)
    data['Tech Stack'] = ' '.join(stack_text)
    ###tech faq
    faq_tech = {}

    faq_questions = technologies_driver.find_elements(By.XPATH,'//a[@class="faq-question"]')
    faq_answers = technologies_driver.find_elements(By.XPATH,'//p[@class="faq-accordion-answer"]')
    for question, answer in zip(faq_questions, faq_answers):
        answer_text = answer.get_attribute("innerText").replace("\n", "").replace("\t", "")
        faq_tech[question.text] = answer_text
    data['faq tech'] = faq_tech
    technologies_driver.quit()

    ##send to get email-fromat data
    url = data['url']
    url = url+'/email-format'
    email_format(url,data)


def email_format(url, data):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"user-agent:{get_user_agent('random')}")
    email_driver = webdriver.Chrome(options=options)
    email_driver.get(url)

    headers = email_driver.find_elements(By.XPATH, '//tr[@id="table-headers"]/th')

    rows = email_driver.find_elements(By.XPATH, '//tbody/tr')
    
    email_data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == len(headers):
            email_row = {}
            for header, cell in zip(headers, cells):
                header_text = header.text.strip()
                value_text = cell.text.strip()
                email_row[header_text] = value_text
            email_data.append(email_row)
    ###email faq data
    data['email_data']  =email_data
    
    faq_email = {}

    faq_questions = email_driver.find_elements(By.XPATH,'//a[@class="faq-question"]')
    faq_answers = email_driver.find_elements(By.XPATH,'//p[@class="faq-accordion-answer"]')
    for question, answer in zip(faq_questions, faq_answers):
        answer_text = answer.get_attribute("innerText").replace("\n", "").replace("\t", "")
        faq_email[question.text] = answer_text
    data['faq email'] = faq_email
    email_driver.quit()

    # Write the updated data to the CSV file
    write_data_to_csv("export.csv", data)

def write_data_to_csv(filename, data):
    col_name = list(data.keys())

    with open(filename, 'a', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=col_name)
        if csvFile.tell() == 0:  # Check if the file is empty
            writer.writeheader()
        writer.writerow(data)
    
if __name__ == '__main__':
    start_crawl()

#break after https://www.getcyberleads.com/directories/companies/P?page=81