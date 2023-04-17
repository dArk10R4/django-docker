from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from celery import shared_task
import os
import sys
import django


# Add the project path to the system path so Django can find the settings module.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
django.setup()
from taskapp.models import InstagramCredentials,InstagramDatas


@shared_task
def scrape_all():

    all_instagram_credentials = InstagramCredentials.objects.all()
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    command_executor = os.environ['WEBDRIVER_URL']
    driver = webdriver.Remote(command_executor=command_executor,options=options)

    for instagram_creds in all_instagram_credentials:
        instagram_username = instagram_creds.instagram_username
        profile_url = f"https://www.instagram.com/{instagram_username}/"
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
        # create or update the InstagramDatas instance for this user
        instagram_data, created = InstagramDatas.objects.get_or_create(instagram=instagram_creds)
        instagram_data.instagram_followers = followers
        instagram_data.instagram_following = following
        instagram_data.save()
    driver.quit()