import re
import sys
import time
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from models import User


@dataclass
class Youlikehits:
    chrome_driver_location = 'chromedriver'
    REGEX_POINTS = r'(?<=Points: )[0-9/]+'
    REGEX_TIME = r'(?<=Timer: [0-9][/])[0-9/]+'
    points: str = 0

    def __init__(self):
        self.chrome_driver = None

    def connect(self, user: User):
        self.go_to_youlikehits()  # go to link
        self.chrome_driver.find_element(By.NAME, 'username').send_keys(user.username)
        self.chrome_driver.find_element(By.NAME, 'pass').send_keys(user.password)
        self.chrome_driver.find_element(By.CSS_SELECTOR, 'input').submit()

    def go_to_youlikehits(self):
        youlikehits_url = 'https://www.youlikehits.com/login.php'
        self.chrome_driver = webdriver.Chrome(youlikehits_url)
        self.chrome_driver.get(youlikehits_url)

    def go_earn_points(self):
        self.chrome_driver.find_element(By.LINK_TEXT, 'Earn Points').click()

    def go_earn_youtube_views_points(self):
        self.chrome_driver.find_element(By.XPATH, "//div[@data='youtubenew2.php']").click()

    def watch_youtube_video(self):
        self.chrome_driver.find_element(By.XPATH, "//a[@class='followbutton']").click()

    def get_timer_points(self):
        return self.get_time_to_wait, self.get_point_to_earn()

    def get_point_to_earn(self) -> int:
        text = self.chrome_driver.find_element(By.CSS_SELECTOR, "center").text
        return int(re.search(self.REGEX_POINTS, text).group())

    def get_time_to_wait(self) -> int:
        text = self.chrome_driver.find_element(By.CSS_SELECTOR, "center").text
        return int(re.search(self.REGEX_TIME, text).group())

    def get_points(self, user: User, end_time: int = 1800):
        self.connect(user)
        self.go_earn_points()
        self.go_earn_youtube_views_points()
        start_time = time.time()
        while time.time() - start_time < end_time:
            print(f"Start watching new video")
            self.watch_youtube_video()
            time.sleep(1)
            points = self.get_point_to_earn()
            timer = self.get_time_to_wait()
            print(f"Wait... {timer} seconds")
            time.sleep(timer)
            print(f"You just earned {points} points")
            self.points += points

        print(f"Congratulation !!!! You earned {self.points} points")
        self.logout()


    def logout(self):
        self.chrome_driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.exit()
    def exit(self):
        time.sleep(2)
        self.chrome_driver.quit()
        sys.exit(0)
