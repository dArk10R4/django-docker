from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import login, logout
from .forms import InstagramCredentialsForm
from .models import InstagramCredentials
from .models import InstagramDatas
# Create your views here.
from django.http import HttpResponse
import time 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os 
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context = {
        'title': 'My Page',
        'content': 'Welcome to my page!',
    }
    return render(request, 'taskapp/index.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/signin')
    else:
        form = UserCreationForm()
    return render(request, 'taskapp/signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'taskapp/signin.html', {'form': form})

@login_required
def save_instagram_credentials(request):
    if request.method == 'POST':
        form = InstagramCredentialsForm(request.POST)
        if form.is_valid():
            instagram_username = form.cleaned_data['instagram_username']
            instagram_password = form.cleaned_data['instagram_password']
            instagram_credentials,created = InstagramCredentials.objects.get_or_create(user=request.user)
            instagram_credentials.instagram_username=instagram_username
            instagram_credentials.instagram_password=instagram_password
            instagram_credentials.save()
            return redirect('/')
    else:
        form = InstagramCredentialsForm()
    return render(request, 'taskapp/save_instagram_credentials.html', {'form': form})

@login_required
def instagram_data(request):
    instagram_creds = None
    try:
        instagram_creds = InstagramCredentials.objects.get(user=request.user)
        instagram_data = InstagramDatas.objects.get(instagram=instagram_creds)
        print(instagram_data)
        # create a new instance of Chrome driver
        return render(request, 'taskapp/home.html', {'instagram_datas': instagram_data})
    except InstagramCredentials.DoesNotExist:
        return redirect('save_instagram_credentials')
    except InstagramDatas.DoesNotExist:
        instagram_username = instagram_creds.instagram_username
        instagram_password = instagram_creds.instagram_password
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        command_executor = os.environ['WEBDRIVER_URL']
        driver = webdriver.Remote(command_executor=command_executor,options=options)

        # navigate to Instagram's login page
        driver.get('https://www.instagram.com/accounts/login/')

        # enter username and password and login
        WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(instagram_username)
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(instagram_password)

        driver.find_element(By.CSS_SELECTOR,'._acan._acap._acas._aj1-').click()

        time.sleep(2)

        # navigate to the user's profile page
        profile_url = f"https://www.instagram.com/{instagram_username}/"
        driver.get(profile_url)
        WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_ac2a"))
        )
        my_elements = driver.find_elements(By.CLASS_NAME,'_ac2a')[1:]

        for x in range(2):
            my_elements[x] = my_elements[x].find_element(By.TAG_NAME,'span').text

        # scrape the number of followers and following
        
        followers = int(my_elements[0])
        following = int(my_elements[1])
        print(followers,following)
        # create or update the InstagramDatas instance for this user
        instagram_data, created = InstagramDatas.objects.get_or_create(instagram=instagram_creds)
        instagram_data.instagram_followers = followers
        instagram_data.instagram_following = following
        instagram_data.save()

        driver.quit()
        print(instagram_data.instagram_followers)
        return render(request, 'taskapp/home.html', {'instagram_datas': instagram_data})

    except TimeoutException:
        messages.error(request, f"Instagram username {instagram_username} does not exist.")
        return redirect('save_instagram_credentials')
