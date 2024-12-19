from tkinter import Tk, ttk, Menu, Text, Frame, Toplevel, Label, Entry, Button, filedialog
from lyrics_scrapper import scrape_lyrics
from threading import Thread
import time

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

            scrape_lyrics(artist_name=artist, track_name=track)
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
window.config(padx=10, pady=10)

# App Title
app_name = Label(
    text='🎵 Lyrics Scraper 🎵',
    justify='center',
    font=('Arial Baltic', 15, 'bold')
)
app_name.pack(anchor='center', pady=5)

# Artist Name Input
artist_name_label = Label(window, text='Type the artist name *:', justify='left')
artist_name_label.pack(anchor='w')
artist_name = Entry(window, width=40)
artist_name.pack(pady=5, padx=10, ipady=5)

# Track Name Input
track_name_label = Label(window, text='Type the track name *:', justify='left')
track_name_label.pack(anchor='w')
tracks_name = Entry(window, width=40)
tracks_name.pack(pady=5, padx=10, ipady=5)

# Feedback Label
feedback_label = Label(window, text='', font=("Arial", 10))
feedback_label.pack(pady=5)

# Submit Button
submit_btn = Button(
    window,
    text='Search for Lyrics',
    width=25,
    height=2,
    background='#353535',
    foreground='#ffffff',
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

window.mainloop()
