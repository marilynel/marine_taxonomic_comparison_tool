from tkinter import *
from PIL import ImageTk,Image
import requests
import json
import urllib.parse

main_window = Tk()
#canvas = Canvas(main_window, width = 300, height = 300)
#canvas.grid(row = 4, columnspan = 2)

#photoResponse = requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Sanc0063_-_Flickr_-_NOAA_Photo_Library.jpg/330px-Sanc0063_-_Flickr_-_NOAA_Photo_Library.jpg")
#file = open("kelp.jpg", "wb")
#file.write(response.content)
#file.close()

# example for invoking service
# image = request.get("notforlong.org?name={}&size={}".format("kelp", "400x400"))
# will need to encode and decode base 64 image

#strText = request.get("urlOfTeammateServce.com")

#photo = ImageTk.PhotoImage(Image.open("kelp.jpg"))
#canvas.create_image(100,100, image = photo)

# labels for text bars for searching
Label(main_window, text = "Genus 1:").grid(row = 0, column = 0)
Label(main_window, text = "species 1:").grid(row = 1, column = 0)
Label(main_window, text = "Genus 2:").grid(row = 0, column = 2)
Label(main_window, text = "species 2:").grid(row = 1, column = 2)

# for printing text to gui later; may not be needed?
outputText = ""
outputText2 = ""

# text input for searching
genus = Entry(main_window, width = 50, borderwidth = 5)
genus.grid(row = 0, column = 1)
spp = Entry(main_window, width = 50, borderwidth = 5)
spp.grid(row = 1, column = 1)

genus2 = Entry(main_window, width = 50, borderwidth = 5)
genus2.grid(row = 0, column = 3)
spp2 = Entry(main_window, width = 50, borderwidth = 5)
spp2.grid(row = 1, column = 3)

#callback function for clicking the search button
def on_click():
    # for printing text to gui later
    global outputText
    global outputText2

    # make the species name from the inputs
    # TODO: do I want to do this as one text box?
    name = genus.get() + " " + spp.get()
    name2 = genus2.get() + " " + spp2.get()

    # stick the species name in the url
    safe_string = urllib.parse.quote_plus(name)
    url = 'https://www.marinespecies.org/rest/AphiaRecordsByName/{}?like=true&marine_only=true&offset=1'
    url = url.format(safe_string)

    safe_string2 = urllib.parse.quote_plus(name2)
    url2 = 'https://www.marinespecies.org/rest/AphiaRecordsByName/{}?like=true&marine_only=true&offset=1'
    url2 = url2.format(safe_string2)

    # get the json object for the spp
    response = requests.get(url)
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

    response2 = requests.get(url2)
    if response2:
        orgData2 = response2.json()
        for i in orgData2[0]:
            if i == 'kingdom':
                outputText2 += f"Kingdom: {orgData2[0][i]}"
            if i == 'phylum':
                outputText2 += f"\nPhylum: {orgData2[0][i]}"
            if i == 'class':
                outputText2 += f"\nClass: {orgData2[0][i]}"
            if i == 'order':
                outputText2 += f"\nOrder: {orgData2[0][i]}"
            if i == 'family':
                outputText2 += f"\nFamily: {orgData2[0][i]}"
            # print outputText (taxonomic data)
        textLabel2.config(text = outputText2)
    else:
        textLabel2.config("Organism not found. Please try another.")

###########
# TODO: Error checking is not working!!
# change banner at top to say somthing other than 'tk'
# color comparison
# split on_click into smaller functions, you're no longer in 161
###########



# button widget
Button(main_window, text = "Search", command = on_click ).grid(row = 2, columnspan = 4)

# place for the outputText later
textLabel = Label(main_window, text = "")
textLabel.grid(row = 3, column = 1)

textLabel2 = Label(main_window, text = "")
textLabel2.grid(row = 3, column = 3)

main_window.mainloop()
