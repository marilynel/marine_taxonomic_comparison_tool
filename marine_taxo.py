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

# return a list of taxo names?
def make_taxo_list(name):
    safe_string = urllib.parse.quote_plus(name)
    url = 'https://www.marinespecies.org/rest/AphiaRecordsByName/{}?like=true&marine_only=true&offset=1'
    url = url.format(safe_string)
    taxo = []
    response = requests.get(url)
    if response:
        orgData = response.json()
        for i in orgData[0]:
            if i == 'kingdom':
                taxo.append(orgData[0][i])
            if i == 'phylum':
                taxo.append(orgData[0][i])
            if i == 'class':
                taxo.append(orgData[0][i])
            if i == 'order':
                taxo.append(orgData[0][i])
            if i == 'family':
                taxo.append(orgData[0][i])
            if i == 'genus':
                taxo.append(orgData[0][i])
            if i == 'species':
                taxo.append(orgData[0][i])
    return taxo

def go_thru_list(listname):
    foo = ""
    for i in listname:
        foo += f"{i}\n"
    return foo

#callback function for clicking the search button
def on_click():
    # for printing text to gui later
    global outputText
    global outputText2

    # make the species name from the inputs
    # TODO: do I want to do this as one text box?
    name = genus.get() + " " + spp.get()
    taxo1 = make_taxo_list(name)
    outputText = go_thru_list(taxo1)
    textLabel.config(text = outputText)


    name2 = genus2.get() + " " + spp2.get()
    taxo2 = make_taxo_list(name2)
    outputText2 = go_thru_list(taxo2)
    textLabel2.config(text = outputText2)

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
#textLabel = Text(main_window)
textLabel.grid(row = 3, column = 1)
#textLabel.config(foreground="red")

textLabel2 = Label(main_window, text = "")
#textLabel2 = Text(main_window)
textLabel2.grid(row = 3, column = 3)
#textLabel2.config(foreground="red")

main_window.mainloop()
