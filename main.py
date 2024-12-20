from tkinter import Tk, ttk,Label, Entry, Button,Menu,messagebox
from lyrics_scrapper import scrape_lyrics
from threading import Thread
import requests
# import pywhatkit 
import time


def internet_connection():
    try:
        requests.get('https://google.com')
        return True
    except requests.ConnectionError:
            return False

# Initialize Tkinter Window
window = Tk()

# Function to fetch data in a thread
def fetch_data():
    artist = artist_name.get().strip().lower()
    track = tracks_name.get().strip().lower()
   
    if not artist:
        feedback_label.config(text='Artist name is required!', foreground='red')
        return
    if not track:
        feedback_label.config(text='Track name is required!', foreground='red')
        return

    feedback_label.config(text=f'Searching lyrics for: {track} by {artist}', foreground='blue')
    submit_btn.config(state='disabled')

    def search():
        try:
            # Simulate a loading animation
            for i in range(3):
                feedback_label.config(text=f"Searching{'.' * (i + 1)}")
                time.sleep(0.5)
            if internet_connection():
             scrape_lyrics(artist_name=artist, track_name=track)
            else:
               messagebox.showwarning(title='Network error',message='A network connection is required !')
               feedback_label.config(text='No internet connection')
               return
        finally:
            submit_btn.config(state='normal')

    thread = Thread(target=search)
    thread.start()



# Function to reset form
def enable_submit():
    artist_name.delete(0, 'end')
    tracks_name.delete(0, 'end')
    feedback_label.config(text='', foreground='black')
    submit_btn.config(state='normal')

# Window Configuration
window.title('Lyrics Scraper')
window.geometry('320x300')
window.resizable(width=False, height=False)
window.config(padx=10, pady=10, bg='#F8FAFC')


# def play_track_on_yt():
#     print('Hello')
#     if not artist_name or tracks_name:
#      return
#     try:
#      pywhatkit.playonyt(f'{tracks_name} {artist_name}', use_api=True)
#     except Exception as e:
#         print(f"Failed to play on YouTube: {e}")

# App Title
app_name = Label(
    text='🎵 Lyrics Scraper 🎵',
    justify='center',
    bg='#F8FAFC',
    font=('Arial Baltic', 15, 'bold')
)
app_name.pack(anchor='center', pady=5)


menu_bar = Menu(window)
options_menu = Menu(menu_bar,tearoff=0)
options_menu.add_command(label='Play on YouTube',command='play_track_on_yt')

menu_bar.add_cascade(label='Options',menu=options_menu)

# Artist Name Input
artist_name_label = Label(window,
                           text='Type the artist name *:', justify='left', 
                           pady=7,
                           bg='#F8FAFC',
                           font=("Arial", 12))
artist_name_label.pack(anchor='w')
artist_name = Entry(window,
                     width=70,
                     highlightthickness=2,
                     borderwidth=0,
                     highlightbackground = "#A888B5")
artist_name.pack(ipady=9)

# Track Name Input
track_name_label = Label(window, 
                         text='Type the track name *:', 
                         justify='left',
                         pady=7,
                         bg='#F8FAFC',
                         font=("Arial", 12)
                         )
track_name_label.pack(anchor='w')
tracks_name =Entry(window,
                     width=70,
                     highlightthickness=2,
                     borderwidth=0,
                     highlightbackground = "#A888B5")
tracks_name.pack(ipady=9)

# Feedback Label
feedback_label = Label(window, text='', font=("Arial", 10),bg='#F8FAFC')
feedback_label.pack(pady=5)

# Submit Button
submit_btn = Button(
    window,
    text='Search for Lyrics',
    width=25,
    height=2,
    background='#474E93',
    foreground='#ffffff',
    font=("Arial", 13),
    borderwidth=0,
    cursor='spider',
    activebackground='#8174A0',
    command=fetch_data
)
submit_btn.pack(pady=5)

# Enable Submit Button
enable_submit_btn = Button(
    window,
    text='Search Again',
    height=2,
    background='#ffffff',
    foreground='#212121',
    border='0',
    command=enable_submit
)
enable_submit_btn.pack()

window.config(menu=menu_bar)
window.mainloop()
