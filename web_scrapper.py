import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
import logging
# from datetime import datetime

# # Setup logging
# logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_jobs():
    try:
                 # Fetch webpage content
         url = "https://vacancymail.co.zw/jobs/"
         response = requests.get(url)
         response.raise_for_status()  # Raise HTTPError for bad status codes
         logging.info("Successfully fetched webpage content.")

#         # Parse HTML content
         soup = BeautifulSoup(response.text, 'html.parser')
         job_cards = soup.find_all('div', class_='job-listing-description')[:10]  # Updated class name

#         # Extract relevant data
         jobs = []
         for card in job_cards:
             job_title_tag = card.find('h3', class_='job-listing-title')
             company_tag = card.find('h4', class_='job-listing-company')
             description_tag = card.find('p', class_='job-listing-text')

             job_title = job_title_tag.text.strip() if job_title_tag else "N/A"
             company = company_tag.text.strip() if company_tag else "N/A"
             job_description = description_tag.text.strip() if description_tag else "N/A"

             jobs.append({
                 "Job Title": job_title,
                 "Company": company,
                 "Job Description": job_description
             })

         # Save to CSV 
         df = pd.DataFrame(jobs)
         df.drop_duplicates(inplace=True)  # Data cleaning
         df.to_csv('scraped_data.csv', index=False)
         logging.info("Data successfully written to 'scraped_data.csv'.")

    except requests.exceptions.RequestException as e:
         logging.error(f"Request failed: {e}")
    except Exception as e:
         logging.error(f"An error occurred: {e}")

 # Scheduling function
def schedule_scraping():
     schedule.every().day.at("10:00").do(scrape_jobs)  # Adjust timing as needed
     logging.info("Scheduled scraping task initiated.")
     while True:
         schedule.run_pending()
         time.sleep(1)

if __name__ == "__main__":
     print("Starting scraper...")
     scrape_jobs() 
     schedule_scraping()

