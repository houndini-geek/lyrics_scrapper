from tkinter import Tk, ttk, Menu, Text, Frame, filedialog
import os

folder_path = os.path.join(os.path.expanduser('~'), 'documents', 'scrapped_lyrics')

def save_folder_path():
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

# Sample lyrics dictionary
# lyrics = {
#     "track": "Father of 4",
#     "artist": "Offset",
#     "lyrics": "Tryna find my soul when I had you"
# }

def display_lyrics(lyrics):
    root = Tk()
    root.title(f'{lyrics["track"]}: {lyrics["artist"]}')  # Fix string formatting
    root.geometry('550x480')
    root.resizable(width=False, height=False)

    menu_bar = Menu(root)
    option_menu  = Menu(menu_bar, tearoff=0)

    option_menu.add_command(label='Save lyrics', command=lambda: save_lyrics())

    menu_bar.add_cascade(label='Options', menu=option_menu)

    # Scrollbar setup
    frame = Frame(root)
    frame.pack(expand=True, fill='both')

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side='right', fill="y")

    textarea = Text(frame, wrap="word", yscrollcommand=scrollbar.set, autoseparators=True)
    textarea.insert('1.0', lyrics["lyrics"])  # Fix string formatting

    textarea.config(bg="#FFFFFF", foreground='#262626',
                    font=('Franklin Gothic Medium', 13),
                    insertbackground='#C1C1C1', padx=4, pady=4)
    textarea.pack(expand=True, fill='both', side='top')

    scrollbar.config(command=textarea.yview)
    save_folder_path()

    def save_lyrics():
        path = filedialog.asksaveasfilename(title='Save lyrics',
                                            defaultextension='.txt',
                                            initialfile=f'{lyrics["artist"]}_{lyrics["track"]}_lyrics',  # Fix string formatting
                                            initialdir=folder_path)

        if not path:
            return
        with open(path, 'w') as file:
            file.write(str(textarea.get('1.0', 'end')))

    root.config(menu=menu_bar)
    root.mainloop()

# # Example call
# display_lyrics(lyrics)
