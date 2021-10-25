from tkinter import *
from PIL import ImageTk,Image
import requests
import json
import urllib.parse

main_window = Tk()
canvas = Canvas(main_window, width = 300, height = 300)
canvas.grid(row = 4, columnspan = 2)

photoResponse = requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Sanc0063_-_Flickr_-_NOAA_Photo_Library.jpg/330px-Sanc0063_-_Flickr_-_NOAA_Photo_Library.jpg")
file = open("kelp.jpg", "wb")
file.write(response.content)
file.close()



photo = ImageTk.PhotoImage(Image.open("kelp.jpg"))
canvas.create_image(100,100, image = photo)

# labels for text bars for searching
Label(main_window, text = "Genus:").grid(row = 0, column = 0)
Label(main_window, text = "species:").grid(row = 1, column = 0)

# for printing text to gui later; may not be needed?
outputText = ""

# text input for searching
genus = Entry(main_window, width = 50, borderwidth = 5)
genus.grid(row = 0, column = 1)
spp = Entry(main_window, width = 50, borderwidth = 5)
spp.grid(row = 1, column = 1)

#callback function for clicking the search button
def on_click():
    # for printing text to gui later
    global outputText

    # make the species name from the inputs
    # TODO: do I want to do this as one text box?
    name = genus.get() + " " + spp.get()

    # stick the species name in the url
    safe_string = urllib.parse.quote_plus(name)
    url = 'https://www.marinespecies.org/rest/AphiaRecordsByName/{}?like=true&marine_only=true&offset=1'
    url = url.format(safe_string)

    # get the json object for the spp
    response = requests.get(url)
    #orgData = response.json()
    if response:
        orgData = response.json()
        for i in orgData[0]:
            if i == 'kingdom':
                outputText += f"Kingdom: {orgData[0][i]}"
            if i == 'phylum':
                outputText += f"\nPhylum: {orgData[0][i]}"
            if i == 'class':
                outputText += f"\nClass: {orgData[0][i]}"
            if i == 'order':
                outputText += f"\nOrder: {orgData[0][i]}"
            if i == 'family':
                outputText += f"\nFamily: {orgData[0][i]}"
        # print outputText (taxonomic data)
        textLabel.config(text = outputText)
    else:
        textLabel.config("Organism not found. Please try another.")

###########
# TODO: Error checking is not working!!
###########


# button widget
Button(main_window, text = "Search", command = on_click ).grid(row = 2, column = 1)

# place for the outputText later
textLabel = Label(main_window, text = "")
textLabel.grid(row = 3, columnspan = 2)

main_window.mainloop()
