from tkinter import *
from PIL import ImageTk, Image
import requests
import json
import urllib.parse
from difflib import SequenceMatcher


###########
# TODO:
# change banner at top to say somthing other than 'tk'
# color comparison for different taxonomies
# recognize error from Arek's service and print appropriate imgResponse
#       EX: Nereocystis luetkeana will have image response but not wikidata response, show image but error message for wikidata
###########



main_window = Tk()
main_window.resizable(width = True, height = True)

# Labels for search bars
Label(main_window, text = "Genus 1:").grid(row = 0, column = 0)
Label(main_window, text = "species 1:").grid(row = 1, column = 0)
Label(main_window, text = "Genus 2:").grid(row = 0, column = 2)
Label(main_window, text = "species 2:").grid(row = 1, column = 2)

# TODO: do I need this??
# for printing text to gui later; may not be needed?
outputText = ""
outputText2 = ""
labels = ""
strText1 = ""
strText2 = ""

# Input/search bars
genus = Entry(main_window, width = 50, borderwidth = 5)
genus.grid(row = 0, column = 1)
spp = Entry(main_window, width = 50, borderwidth = 5)
spp.grid(row = 1, column = 1)

genus2 = Entry(main_window, width = 50, borderwidth = 5)
genus2.grid(row = 0, column = 3)
spp2 = Entry(main_window, width = 50, borderwidth = 5)
spp2.grid(row = 1, column = 3)

# Function: Get taxonomic data of organism
def make_taxo_list(name):
    scientificName = urllib.parse.quote_plus(name)
    wormsUrl = 'https://www.marinespecies.org/rest/AphiaRecordsByName/{}?like=true&marine_only=true&offset=1'
    wormsUrl = wormsUrl.format(scientificName)
    taxo = ""
    response = requests.get(wormsUrl)
    if response.status_code == 200:
        orgData = response.json()
        # Parse returned JSON object for taxonomic data
        # currently catting a string, commented out sections append to a list instead (need to change taxo type)
        for i in orgData[0]:
            if i == 'kingdom':
                taxo+=orgData[0][i] + "\n"
                #taxo.append(orgData[0][i])
            if i == 'phylum':
                taxo+=orgData[0][i] + "\n"
                #taxo.append(orgData[0][i])
            if i == 'class':
                taxo+=orgData[0][i] + "\n"
                #taxo.append(orgData[0][i])
            if i == 'order':
                taxo+=orgData[0][i] + "\n"
                #taxo.append(orgData[0][i])
            if i == 'family':
                taxo+=orgData[0][i] + "\n"
                #taxo.append(orgData[0][i])
            if i == 'genus':
                taxo+=orgData[0][i] + "\n"
                #taxo.append(orgData[0][i])
            if i == 'species':
                taxo+=orgData[0][i]
                #taxo.append(orgData[0][i])
        taxo+=name
        #taxo.append(name)
        return taxo
    else:
        return f"{name} not found in database."

# Function: clear search bars
def clear_values():
    genus.delete(0, END)
    genus2.delete(0, END)
    spp.delete(0, END)
    spp2.delete(0, END)

# Function: get image (my service)
def post_image(colNum, name):
    scientificName = urllib.parse.quote_plus(name)
    imageServiceUrl = "http://notforlong.net:5007/requestImage?name={}"
    imageServiceUrl = imageServiceUrl.format(scientificName)
    imgResponse = requests.get(imageServiceUrl)
    if imgResponse.status_code == 200:
        # could I clean this up?? too scared to touch it
        # gets image from service and sets it up so tkinter can display it
        print("Marilyn's image service for " + name)
        res = imgResponse.json()
        # url of image is at: res['url']
        photoResponse = requests.get(res['url'])
        filename = name + "." + res['url'].split(".")[-1]
        file = open(filename, "wb")
        file.write(photoResponse.content)
        image = Image.open(filename)
        image = image.resize((300,200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = Label(main_window, image = photo)
        label.image = photo
        label.grid(row=4, column = colNum)

# Function: get data (Arek's service)
def post_wiki_data(colNum, name):
    scientificName = urllib.parse.quote_plus(name)
    #wikiServiceUrl = "http://flip2.engr.oregonstate.edu:4203/?page={}"
    # for temporarily running it locally:
    #wikiServiceUrl = "http://localhost:4203/?page={}"
    wikiServiceUrl = "https://areks-wikipedia-scraper.herokuapp.com/?page={}"
    wikiServiceUrl = wikiServiceUrl.format(scientificName)
    response = requests.get(wikiServiceUrl)
    infoStr = ""
    if response.status_code == 200:
        print("Arek's wiki service for " + name)
        res = response.json()
        for i in res:
            if i == "Description":
                for j in res[i]:
                    infoStr = res[i][j]
        infoStr = re.sub('[\[][0-9]{,2}[\]]', '', infoStr)
    else:
        infoStr = f"No information found for {name}."
    label = Label(main_window, text=infoStr, wraplength=400)
    label.grid(row=6, column=colNum)

# Function: callback function for clicking the search button
def on_click():
    global outputText, outputText2
    global strText1, strText2

    name = genus.get() + " " + spp.get()
    outputText = make_taxo_list(name)

    name2 = genus2.get() + " " + spp2.get()
    outputText2 = make_taxo_list(name2)

# TODO: this doesn't work
    # compare strings
    match = SequenceMatcher(None, outputText, outputText2).find_longest_match(0, len(outputText), 0, len(outputText2))
    equalSubStr = outputText[match.a: match.a + match.size]

    textLabel.config(text = outputText)
    textLabel2.config(text = outputText2)

    textLabelsTaxNames.config(text = "Kingdom:\nPhylum:\nClass:\nOrder:\nFamily:\nGenus:\nSpecies:")
    clear_values()

    blurb1.config(text = strText1)
    blurb2.config(text = strText2)
    post_image(1, name)
    post_image(3, name2)
    post_wiki_data(1, name)
    post_wiki_data(3, name2)

# Button widget
Button(main_window, text = "Compare", command = on_click ).grid(row = 2, columnspan = 4)

# for King Philip labels
textLabelsTaxNames = Label(main_window, text = "")
textLabelsTaxNames.grid(row = 3, column = 0)

# place for the outputText
textLabel = Label(main_window, text = "")
textLabel.grid(row = 3, column = 1)
textLabel2 = Label(main_window, text = "")
textLabel2.grid(row = 3, column = 3)

blurb1 = Label(main_window, text = "")
blurb1.grid(row = 5, column = 1)
blurb2 = Label(main_window, text = "")
blurb2.grid(row = 5, column = 3)

# Let's do this
main_window.mainloop()
