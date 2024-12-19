
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

def is_match(scraped_name, input_name, threshold=45):
    # Check if similarity is above the threshold
    return fuzz.partial_ratio(scraped_name, input_name) > threshold



def scrape_lyrics(artist_name,track_name):
   try:
        print('===Opening the Browser====')
        browser = webdriver.Chrome()
        browser.maximize_window()
        print('===Navigating to Music X Match===')
        browser.get('https://www.musixmatch.com/search')
   except WebDriverException as wd:
        return messagebox.showerror(title='Error occured', message=wd)

   wait = WebDriverWait(browser,10)
   browser.implicitly_wait(5)
   try:
        input_el = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/div/div/input')))
        input_el.send_keys(f'{artist_name} {track_name}')
   except NoSuchElementException:
           return print('Search bar not found!')
   sleep(10)
   try:
        print('===Clicking on the "See all button" to display all tracks===')
        see_all_btn = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[2]/div/div/div[3]/div')))
        see_all_btn.click()
   except NoSuchElementException:
        print('See all button not found')
   except TimeoutException:
       print('Timedout to click on the see all button')
   sleep(10)
   try:
     print('===Fiding Track cards===')
     parent_cards = browser.find_element(By.CSS_SELECTOR,value='.r-1wtj0ep')
     all_cards = parent_cards.find_elements(By.CSS_SELECTOR,value='.r-1f720gc')
   except NoSuchElementException:
      return messagebox.showerror(title='Element not found',message="Track cards not found !")
   print('===Looping throught all cards===')
   for card in all_cards:
        track_el = card.find_element(By.CSS_SELECTOR,value='.r-1wbh5a2').text.strip().lower()
        artist_el = card.find_element(By.CSS_SELECTOR,value='.r-a023e6').text.strip().lower()
               
        if is_match(track_el, track_name.lower().strip()) and is_match(artist_el, artist_name.lower().strip()):
         link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
         print('===Track card Found !===')
         browser.get(link)
         break  # Stop once the correct track is found
        else:
         return messagebox.showinfo(title='Lyrics not found',message=f"Couldn't found lyrics for the track: {track_name}\n Check the track spelling and the artist name and try again.")
   try:
        print('===Loading lyrics===')
        parent_verse = browser.find_element(By.XPATH,value='/html/body/div[1]/div/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div[2]/div')
        lyrics = {
            'artist': artist_name,
            'track' : track_name,
            'lyrics': parent_verse.text
            }
        browser.quit()
        print('===Showing lyrics===')
        return display_lyrics(lyrics)
       
   except NoSuchElementException:
        return messagebox.showerror('Error',message=f'Failed to display lyrics for: {track_name} by {artist_name}')
    
