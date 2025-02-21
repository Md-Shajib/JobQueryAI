#source venv/bin/activate

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

df = pd.DataFrame()
lJobTitle = []
lJobLocation = []
lWorkLocation = []
lWorkType = []
ljobDescription = []

email = "shajib2999@gmail.com"
password = "Shajib123@#"

driver = webdriver.Chrome()

driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

driver.find_element(By.XPATH, "//input[@id='username']").send_keys(email)
driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)

submitButton = driver.find_element(By.XPATH, "//button[@type='submit']")
submitButton.click()
time.sleep(3)

jobButton = driver.execute_script('return document.querySelector("li-icon[type=\'job\']")')
jobButton.click()
time.sleep(2)

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4136116005&geoId=106215326&origin=JOBS_HOME_LOCATION_SUGGESTION&refresh=true")
time.sleep(3)

location = "Dhaka, Bangladesh"
selectLocation = driver.find_element(By.XPATH, "//input[@class='basic-input jobs-search-box__text-input jobs-search-box__text-input--with-clear']")
selectLocation.clear()
selectLocation.send_keys(location)
time.sleep(2)

search = driver.find_element(By.CLASS_NAME, "jobs-search-box__submit-button")
search.click()
time.sleep(3)

for i in range(1, 5):
    jobList = driver.find_elements(By.XPATH, "//div[@class='scaffold-layout__list-detail-container']/div[2]/div[1]/div/ul/li")
    
    for job in jobList:
        driver.execute_script("arguments[0].scrollIntoView()", job)
        time.sleep(1)

    for link in jobList:
        link.click()
        time.sleep(2)
        
        jobTitle = driver.find_element(By.XPATH, "(//h1[@class='t-24 t-bold inline'])[1]").text
        jobLocation = driver.find_element(By.XPATH, "//body/div[@class='application-outlet']/div[@class='authentication-outlet']/div[4]/div[1]/div[1]/main[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/span[1]").text
        
        try:
            workLocation = driver.find_element(By.XPATH, "//button[@class='job-details-preferences-and-skills']/div[1]/span/span").text
        except:
            workLocation = "N/A"
        
        try:
            workType = driver.find_element(By.XPATH, "(//div[@role='presentation'])[2]/span").text.split("\n")[0]
        except:
            workType = "N/A"
            
        jobDescription = driver.find_element(By.XPATH, "//div[@id='job-details']/div/p").text

        lJobTitle.append(jobTitle)
        lJobLocation.append(jobLocation)
        lWorkLocation.append(workLocation)
        lWorkType.append(workType)
        ljobDescription.append(jobDescription)
        
    last_button = driver.find_element(By.XPATH, "(//div[@class='jobs-search-pagination jobs-search-results-list__pagination p4']/button)[last()]")
    last_button.click()
    time.sleep(3)


data = {
    'Job Title':lJobTitle,
    'Job Location':lJobLocation,
    'Work Location':lWorkLocation,
    'Work Type':lWorkType,
    'Job Description':ljobDescription
}
df = pd.DataFrame(data)
# df.to_csv("jobs_data.csv", index=False, encoding="utf-8-sig")
df.head()

