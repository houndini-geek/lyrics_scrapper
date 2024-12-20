from tkinter import Tk, ttk, Menu, Text,Frame,filedialog
import os 


# lyrics= {
#     "track": "father of 4",
#     "artist": "offset",
#     "lyrics": "trynna find my soul when i had you"
# }


def display_lyrics(lyrics):
    root = Tk()
    root.title(f'{lyrics['track']}: {lyrics['artist']}')
    root.geometry('550x480')
    root.resizable(width=False, height=False)

    menu_bar = Menu(root)
    option_menu  = Menu(menu_bar, tearoff=0)

    option_menu.add_command(label='Save lyrics',command=lambda:save_lyrics())


    menu_bar.add_cascade(label='Options', menu=option_menu)



    # Scrollbar setup
    frame = Frame(root)
    frame.pack(expand=True, fill='both')

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side='right', fill="y")

    textarea = Text(frame, wrap="word", yscrollcommand=scrollbar.set, autoseparators=True)
    textarea.insert('1.0',lyrics['lyrics'])

    textarea.config(bg="#030c14", foreground='#F1F1F1',
                    font=('Franklin Gothic Medium', 13),
                    insertbackground='#C1C1C1',padx=4,pady=4)
    textarea.pack(expand=True, fill='both',side='top')

    scrollbar.config(command=textarea.yview)
    def save_lyrics():
        path = filedialog.asksaveasfilename(title='Save lyrics',
                                            defaultextension='.txt',
                                            initialfile=f'{lyrics['artist']}_{lyrics['track']}_lyrics')
        if not path:
            return
        with open(path,'w') as file:
            file.write(str(textarea.get('1.0','end')))

    root.config(menu=menu_bar)
    root.mainloop()

