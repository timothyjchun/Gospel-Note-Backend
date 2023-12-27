import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import pprint

driver = webdriver.Firefox()
url = "https://www.youtube.com/@user-jg1rl7zp6b/videos"
driver.get(url)


def driver_wait_till_element_found(class_name="", xpath="", id_="", time=1):
    if class_name:
        WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
    elif id_:
        WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, id_)))
    elif xpath:
        WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )


SCROLL_PAUSE_TIME = 0.5

last_height = driver.execute_script("return document.documentElement.scrollHeight")
print(last_height)

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


soup = BeautifulSoup(driver.page_source, "html.parser")

GospelNotes = []


video_link_tag = soup.find_all("a", id="video-title-link")
video_link_tag = video_link_tag[:-2]
for video_link in video_link_tag[:]:
    # print()
    v_url = video_link.attrs.get("href").split("=")[1]
    # print(f"v_url:{v_url}")
    # print(video_link.attrs.get("aria-label"))
    full_title = video_link.attrs.get("title")

    if "천세종" not in full_title:
        title_index = full_title.find("일") + 1
    else:
        title_index = full_title.find("복음노트") + 4
    general_title = full_title[:title_index]
    specific_title = full_title[title_index:]
    if len(specific_title) > 2:
        # maybe recursion?
        passage_index = specific_title.find(
            "장", 3
        )  # Cuz '시편'이 있으면 1까지는 걸러야 하고, 공백 생각하면 2까지 걸러야함.
        if specific_title[passage_index - 1].isnumeric():
            # ok
            passage = specific_title[: passage_index + 1]
            specific_title = specific_title[passage_index + 1 :]
        else:
            # ok
            passage_index = specific_title.find("편", 3)
            if specific_title[passage_index - 1].isnumeric():
                passage = specific_title[: passage_index + 1]
                specific_title = specific_title[passage_index + 1 :]
            else:
                # nothing
                passage = ""
                pass
    # print(f"general_title:{general_title}")
    # print(f"passage:{passage}")
    # print(f"specific_title:{specific_title}")

    indi_note = {
        "url": v_url,
        "general_title": general_title,
        "passage": passage if passage else "",
        "specific_title": specific_title,
    }

    GospelNotes.append(indi_note)
    passage = ""

GospelNotes = GospelNotes[::-1]
pprint.pprint(GospelNotes)
print(len(video_link_tag))
driver.close()

import json

f = open("gospel_notes.txt", "w", encoding="UTF-8")
GospelNotes_string = json.dumps(GospelNotes)
f.write(GospelNotes_string)
f.close()
