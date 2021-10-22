from tkinter import *
import requests
import json
import urllib.parse

main_window = Tk()


Label(main_window, text = "Genus:").grid(row = 0, column = 0)
Label(main_window, text = "species:").grid(row = 1, column = 0)

# text input
genus = Entry(main_window, width = 50, borderwidth = 5)
genus.grid(row = 0, column = 1)
spp = Entry(main_window, width = 50, borderwidth = 5)
spp.grid(row = 1, column = 1)

#callback function
def on_click():
    name = genus.get() + " " + spp.get()
    #print(f"my name is {genus.get()} and my age is {spp.get()}")
    safe_string = urllib.parse.quote_plus(name)
    url = 'https://www.marinespecies.org/rest/AphiaRecordsByName/{}?like=true&marine_only=true&offset=1'
    url = url.format(safe_string)
    response = requests.get(url)
    if response:
        print(response.json())


# button widget
Button(main_window, text = "Click Me", command = on_click ).grid(row = 2, column = 1)


main_window.mainloop()
