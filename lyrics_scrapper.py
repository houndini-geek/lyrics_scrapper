
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import  NoSuchElementException, WebDriverException, TimeoutException
from fuzzywuzzy import fuzz

from tkinter import messagebox

from time  import sleep

from lyrics_windows import display_lyrics

def is_match(scraped_name, input_name, threshold=80):
    # Check if similarity is above the threshold
    return fuzz.partial_ratio(scraped_name, input_name) > threshold

def scrape_lyrics(artist_name, track_name):
    browser = None
    try:
        print("=== Opening the Browser ===")
        browser = webdriver.Chrome()
        browser.maximize_window()
        print("=== Navigating to Musixmatch ===")
        browser.get("https://www.musixmatch.com/search")
    except WebDriverException as wd:
        messagebox.showerror(title="Error occurred", message=str(wd))
        return

    wait = WebDriverWait(browser, 10)
    browser.implicitly_wait(5)

    try:
        input_el = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/div/div/input')))
        input_el.send_keys(f"{artist_name} {track_name}")
    except TimeoutException:
        messagebox.showerror(title="Error", message="Search bar not found or took too long to load!")
        return

    sleep(5)
    try:
        print("=== Clicking on the 'See All' button ===")
        see_all_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[2]/div/div/div[3]/div')))
        see_all_btn.click()
    except TimeoutException:
        print("Timed out while trying to click 'See All' button.")
    except NoSuchElementException:
        print("'See All' button not found.")

    sleep(5)
    try:
        print("=== Finding Track Cards ===")
        parent_cards = browser.find_element(By.CSS_SELECTOR, value=".r-1wtj0ep")
        all_cards = parent_cards.find_elements(By.CSS_SELECTOR, value=".r-1f720gc")
    except NoSuchElementException:
        messagebox.showerror(title="Element not found", message="Track cards not found!")
        return

    print("=== Looping through all cards ===")
    track_found = False
    for card in all_cards:
        try:
            track_el = card.find_element(By.CSS_SELECTOR, value=".r-1wbh5a2").text.strip().lower()
            artist_el = card.find_element(By.CSS_SELECTOR, value=".r-a023e6").text.strip().lower()

            if is_match(track_el, track_name.lower().strip()) and is_match(artist_el, artist_name.lower().strip()):
                link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                print("=== Track Found! Navigating to lyrics page ===")
                browser.get(link)
                track_found = True
                break
        except NoSuchElementException:
            print("Track or artist element not found within a card. Skipping...")

    if not track_found:
        messagebox.showinfo(
            title="Lyrics not found",
            message=f"Couldn't find lyrics for the track: {track_name}\nCheck the spelling and try again."
        )
        return

    try:
        print("=== Loading Lyrics ===")
        parent_verse = browser.find_element(By.XPATH, value='/html/body/div[1]/div/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div[2]/div')
        lyrics = {
            "artist": artist_name,
            "track": track_name,
            "lyrics": parent_verse.text
        }
        print("=== Lyrics Retrieved Successfully ===")
        display_lyrics(lyrics)
    except NoSuchElementException:
        messagebox.showerror(
            title="Error",
            message=f"Failed to retrieve lyrics for: {track_name} by {artist_name}"
        )
    finally:
        if browser:
            print("=== Closing Browser ===")
            browser.quit()
