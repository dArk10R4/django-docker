from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



options = webdriver.ChromeOptions()


caps = webdriver.DesiredCapabilities.CHROME.copy()
caps["networkConnectionEnabled"] = True

options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
command_executor = 'http://localhost:4444/wd/hub'
# driver = webdriver.Remote(command_executor=command_executor,options=options,desired_capabilities=caps)
driver = webdriver.Chrome()
profile_url = f"https://www.instagram.com/nihad_gylrv/"
driver.get(profile_url)
WebDriverWait(driver,10).until(
EC.presence_of_element_located((By.CLASS_NAME, "_ac2a"))
)
my_elements = driver.find_elements(By.CLASS_NAME,'_ac2a')[1:]

for x in range(2):
    my_elements[x] = my_elements[x].find_element(By.TAG_NAME,'span').text

# scrape the number of followers and following

followers = int(my_elements[0].replace(',',''))
following = int(my_elements[1].replace(',',''))
print(followers,following)