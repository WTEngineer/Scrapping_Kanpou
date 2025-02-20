from driver import Driver
from bs4 import BeautifulSoup
import csv, time
from rich import print
import random
import datetime
import time
import os

category = "Radio"
country = "Italy"

WAIT_TIME_LIMIT = 100

class Scraper:
    def __init__(self):
        self.DriversPool = []
        # in case of one-time mode
        self.DriversSize = 1
        self.DriversPool = [Driver() for _ in range(self.DriversSize)]

    def loginProcess(self, random_id):
        while True:
            try:
                for driver in self.DriversPool:
                    if driver.is_available() and not driver.has_response():
                        driver.do_login()
                        break
                else:
                    time.sleep(2)
                    print(f'[{random_id}] Waiting for a driver to be available...')
                    continue
                break
            except Exception as err:
                print(err)

        wait_time = 0
        while True:
            try:
                if driver.has_response():
                    break
                time.sleep(2)
                print(f'[{random_id}] Waiting for a response...')
                wait_time += 1
                if wait_time == WAIT_TIME_LIMIT: 
                    driver.release()
                    return
            except Exception as err:
                print(err)
                return False
            
        driver.release()
            
        return True

    def getArticleResult(self, start_date, end_date, search_word, random_id):

        while True:
            try:
                for driver in self.DriversPool:
                    if driver.is_available() and not driver.has_response():
                        driver.get_article_page(start_date, end_date, search_word)
                        break
                else:
                    time.sleep(1)
                    print(f'[{random_id}] Waiting for a driver to be available...')
                    continue
                break
            except Exception as err:
                print(err)

        wait_time = 0
        while True:
            try:
                if driver.has_response():
                    break
                time.sleep(1)
                print(f'[{random_id}] Waiting for a response...')
                wait_time += 1
                if wait_time == WAIT_TIME_LIMIT: 
                    driver.release()
                    return
            except Exception as err:
                print(err)
                return None
            
        soup = BeautifulSoup(driver.get_response(), 'html.parser')

        # form_search = soup.find('form', {'name': 'formSearch'})

        article_table = soup.select_one("form[name='formSearch'] #articleResultTable")

        result = []

        if article_table is not None:

            rows = article_table.select('tbody tr')

            # Select only odd-indexed rows (0-based index: 1, 3, 5, ...)
            odd_rows = [row for i, row in enumerate(rows) if i % 2 == 0]

            # Print extracted row texts
            for row in odd_rows:
                cells = row.find_all('td')
                index = row.find('th').text.strip()
                date = cells[0].text.strip()
                type = cells[1].text.strip()
                size = cells[2].text.strip()
                listing_item = cells[3].text.strip()
                result.append({
                    'index': index,
                    'date': date,
                    'type': type,
                    'size': size,
                    'listing_item': listing_item,
                })

        driver.release()
            
        return result

    def writeArticleResult(self, start_date, end_date, search_word):

        result = self.getArticleResult(start_date, end_date, search_word, random.randint(10000, 99999))

        if len(result) == 0:
            print("Whoops! no data for the chart you are looking for")
            return
        
        if not os.path.exists('output'):
            os.makedirs('output')

        output_file = open(f'output/output_{start_date}_{end_date}_{search_word}.csv', 'w+', newline='', encoding='utf-8-sig')
        writer = csv.writer(output_file)

        writer.writerow(["No.", "発行日", "種別", "号数", "掲載項目", "本文を表示する"])
        output_file.flush()

        for row in result:
            if (row is None):
                continue
            writer.writerow([row['index'], row['date'], row['type'], row['size'], row['listing_item']])
            output_file.flush()
            print(row)

    def closeDrivers(self):
        for driver in self.DriversPool:
            driver.close()

    def startProc(self, start_date, end_date, search_word):
        print("======== Starting the App ==========")
        self.loginProcess(random.randint(10000, 99999))
        self.writeArticleResult(start_date, end_date, search_word)
        time.sleep(2)
        self.closeDrivers()


if __name__ == '__main__':

    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H-%M-%S")

    scraper = Scraper()

    scraper.startProc('1947-05-03','1947-05-03', '破産')
