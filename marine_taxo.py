from tkinter import *
from PIL import ImageTk, Image
import requests
import json
import urllib.parse
import webbrowser
from tkinter import ttk


#Create an instance of Tkinter frame
#win = Tk()
#Set the geometry of Tkinter frame
#win.geometry("750x270")




###########
# TODO:
# Wikipedia link
# additional info?
###########

main_window = Tk()
main_window.title("Marine Organism Taxonomic Comparison Tool")
main_window.resizable(width = True, height = True)

# Labels for search bars
Label(main_window, text = "Genus 1:").grid(row = 0, column = 0)
Label(main_window, text = "species 1:").grid(row = 1, column = 0)
Label(main_window, text = "Genus 2:").grid(row = 0, column = 2)
Label(main_window, text = "species 2:").grid(row = 1, column = 2)

# For printing text to gui later; may not be needed?
kingdomText1 = ""
kingdomText2 = ""
phylumText1 = ""
phylumText2 = ""
classText1 = ""
classText2 = ""
orderText1 = ""
orderText2 = ""
familyText1 = ""
familyText2 = ""
genusText1 = ""
genusText2 = ""
speciesText1 = ""
speciesText2 = ""



###########################
def open_popup():
   top= Toplevel(main_window)
   top.geometry("405x405")
   top.title("Instructions")
   information = "Welcome to the Marine Organism Taxonomic Comparison Tool! Using \
taxonomic data from the World Register of Marine Species (WoRMS) and \
pictures and introductory information from Wikipedia, we can compare any \
two marine organisms you would like to know more about. Red text in \
taxonomic trees indicates where the two species you are comparing diverge \
in their phylogenies. Simply search for your organisms using their genus \
and species names and click compare."
   examples = "Not sure where to start? Try some favorites:"
   herm = "Opalescent Nudibranch: Hermissenda crassicornis"
   oyst = "Olympia Oyster: Ostrea lurida"
   grtwht = "Greate White Shark: Carcharodon carcharias"
   lngns = "Longnose Skate: Raja rhina"
   seaotr = "Sea Otter: Enhydra lutris"
   sealn = "California Sea Lion: Zalophus californianus"
   orca = "Orca: Orcinus orca"
   dlph = "Bottlenose Dolphin: Tursiops aduncus"
   ane = "Green Anemone = Anthopleura xanthogrammica"
   urch = "Purple Sea Urchin: Strongylocentrotus purpuratus"

   Label(top, text= information, wraplength=400).grid(row = 0)
   Label(top, text = examples).grid(row = 1)
   Label(top, text = herm).grid(row = 2)
   Label(top, text = oyst).grid(row = 3)
   Label(top, text = grtwht).grid(row = 4)
   Label(top, text = lngns).grid(row = 5)
   Label(top, text = seaotr).grid(row = 6)
   Label(top, text = sealn).grid(row = 7)
   Label(top, text = orca).grid(row = 8)
   Label(top, text = dlph).grid(row = 9)
   Label(top, text = ane).grid(row = 10)
   Label(top, text = urch).grid(row = 11)

#################################


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
    kingdom = ""
    phylum = ""
    classTaxo = ""
    order = ""
    family = ""
    genus = ""
    species = ""
    wormsLinkUrl = ""
    response = requests.get(wormsUrl)
    if response.status_code == 200:
        orgData = response.json()
        # Parse returned JSON object for taxonomic data
        for i in orgData[0]:
            if i == 'kingdom':
                kingdom = orgData[0][i]
            if i == 'phylum':
                phylum = orgData[0][i]
            if i == 'class':
                classTaxo = orgData[0][i]
            if i == 'order':
                order = orgData[0][i]
            if i == 'family':
                family = orgData[0][i]
            if i == 'genus':
                genus = orgData[0][i]
            if i == 'url':
                wormsLinkUrl = orgData[0][i]
        return kingdom, phylum, classTaxo, order, family, genus, name, wormsLinkUrl
    else:
        return "","","",f"{name} not found in database.","","","", "NA"

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
        # gets image from service and sets it up so tkinter can display it (including saving to local 'static' dir)
        print("Marilyn's image service for " + name)
        res = imgResponse.json()
        # url of image is at: res['url']
        photoResponse = requests.get(res['url'])
        filename = "static/" + name + "." + res['url'].split(".")[-1]
        file = open(filename, "wb")
        file.write(photoResponse.content)
        image = Image.open(filename)
        image = image.resize((300,200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = Label(main_window, image = photo)
        label.image = photo
        label.grid(row=10, column = colNum)

# Function: get data (Arek's service)
def post_wiki_data(colNum, name):
    scientificName = urllib.parse.quote_plus(name)
    wikiServiceUrl = "https://areks-wikipedia-scraper.herokuapp.com/?page={}"
    wikiServiceUrl = wikiServiceUrl.format(scientificName)
    response = requests.get(wikiServiceUrl)
    infoStr = ""
    if response.status_code == 200:
        print("Arek's wiki service for " + name)
        res = response.json()
        for i in res:
            if i == "intro":
                infoStr = res[i].split("\n")[0]
                break
        infoStr = re.sub('[\[][0-9]{,2}[\]]', '', infoStr)
    else:
        infoStr = f"No information found for {name}."
    return infoStr


def callback(url):
    webbrowser.open_new_tab(url)

def wiki_learn_more(name):
    return f"{name} on Wikipedia"

def worms_learn_more(name):
    return f"{name} on WoRMS"

def wiki_url(name):
    return f"https://en.wikipedia.org/wiki/{name}"

# Function: callback function for clicking the search button
def on_click():
    global kingdomText1, kingdomText2, phylumText1, phylumText2, classText1, classText2, orderText1, orderText2, familyText1, familyText2, genusText1, genusText2, speciesText1, speciesText2

    name = genus.get() + " " + spp.get()
    name2 = genus2.get() + " " + spp2.get()

    kingdomText1, phylumText1, classText1, orderText1, familyText1, genusText1, speciesText1, wormsUrl1 = make_taxo_list(name)
    kingdomText2, phylumText2, classText2, orderText2, familyText2, genusText2, speciesText2, wormsUrl2 = make_taxo_list(name2)

    kingdomLabel1.config(text = kingdomText1)
    kingdomLabel2.config(text = kingdomText2)

    if (kingdomText1 != kingdomText2):
        kingdomLabel.config(foreground = "red")
        kingdomLabel1.config(foreground = "red")
        kingdomLabel2.config(foreground = "red")
    else:
        kingdomLabel.config(foreground = "black")
        kingdomLabel1.config(foreground = "black")
        kingdomLabel2.config(foreground = "black")

    if (phylumText1 != phylumText2):
        phylumLabel.config(foreground = "red")
        phylumLabel1.config(foreground = "red")
        phylumLabel2.config(foreground = "red")
    else:
        phylumLabel.config(foreground = "black")
        phylumLabel1.config(foreground = "black")
        phylumLabel2.config(foreground = "black")

    if (classText1 != classText2):
        classLabel.config(foreground = "red")
        classLabel1.config(foreground = "red")
        classLabel2.config(foreground = "red")
    else:
        classLabel.config(foreground = "black")
        classLabel1.config(foreground = "black")
        classLabel2.config(foreground = "black")

    if (orderText1 != orderText2):
        orderLabel.config(foreground = "red")
        orderLabel1.config(foreground = "red")
        orderLabel2.config(foreground = "red")
    else:
        orderLabel.config(foreground = "black")
        orderLabel1.config(foreground = "black")
        orderLabel2.config(foreground = "black")

    if (familyText1 != familyText2):
        familyLabel.config(foreground = "red")
        familyLabel1.config(foreground = "red")
        familyLabel2.config(foreground = "red")
    else:
        familyLabel.config(foreground = "black")
        familyLabel1.config(foreground = "black")
        familyLabel2.config(foreground = "black")

    if (genusText1 != genusText2):
        genusLabel.config(foreground = "red")
        genusLabel1.config(foreground = "red")
        genusLabel2.config(foreground = "red")
    else:
        genusLabel.config(foreground = "black")
        genusLabel1.config(foreground = "black")
        genusLabel2.config(foreground = "black")

    if (speciesText1 != speciesText2):
        speciesLabel.config(foreground = "red")
        speciesLabel1.config(foreground = "red")
        speciesLabel2.config(foreground = "red")
    else:
        speciesLabel.config(foreground = "black")
        speciesLabel1.config(foreground = "black")
        speciesLabel2.config(foreground = "black")

    phylumLabel1.config(text = phylumText1)
    phylumLabel2.config(text = phylumText2)
    classLabel1.config(text = classText1)
    classLabel2.config(text = classText2)
    orderLabel1.config(text = orderText1)
    orderLabel2.config(text = orderText2)
    familyLabel1.config(text = familyText1)
    familyLabel2.config(text = familyText2)
    genusLabel1.config(text = genusText1)
    genusLabel2.config(text = genusText2)
    speciesLabel1.config(text = speciesText1)
    speciesLabel2.config(text = speciesText2)

    kingdomLabel.config(text="Kingdom:")
    phylumLabel.config(text="Phylum:")
    classLabel.config(text="Class:")
    orderLabel.config(text="Order:")
    familyLabel.config(text="Family:")
    genusLabel.config(text="Genus:")
    speciesLabel.config(text="Species:")

    clear_values()

    if (wormsUrl1 != "NA"):
        learnMore1.config(text = worms_learn_more(name), fg="blue", cursor="hand2")
        learnMore1.bind("<Button-1>", lambda e: callback(wormsUrl1))
        wiki_url1 = wiki_url(name)
        if wiki_url != "NA":
            learnMore3.config(text = wiki_learn_more(name), fg="blue", cursor="hand2")
            learnMore3.bind("<Button-1>", lambda e: callback(wiki_url1))
        post_image(1, name)
        blurb1.config(text = post_wiki_data(1, name))
    else:
        post_image(1, "ijiadf")
    if (wormsUrl2 != "NA"):
        learnMore2.config(text = worms_learn_more(name2), fg="blue", cursor="hand2")
        learnMore2.bind("<Button-1>", lambda e: callback(wormsUrl2))
        wiki_url2 = wiki_url(name2)
        if wiki_url2 != "NA":
            learnMore4.config(text = wiki_learn_more(name2), fg="blue", cursor="hand2")
            learnMore4.bind("<Button-1>", lambda e: callback(wiki_url2))
        post_image(3, name2)
        blurb2.config(text = post_wiki_data(3, name2))
    else:
        post_image(3, "ijiadf")

# Button widget
compareButton = Button(main_window, text = "Compare", command = on_click ).grid(row = 2, columnspan = 4)
compareButton = Button(main_window, text = "What's going on?", command = open_popup ).grid(row = 14, columnspan = 4)





# For King Philip labels
kingdomLabel = Label(main_window, text = "")
kingdomLabel.grid(row = 3, column = 0)
phylumLabel = Label(main_window, text = "")
phylumLabel.grid(row = 4, column = 0)
classLabel = Label(main_window, text = "")
classLabel.grid(row = 5, column = 0)
orderLabel = Label(main_window, text = "")
orderLabel.grid(row = 6, column = 0)
familyLabel = Label(main_window, text = "")
familyLabel.grid(row = 7, column = 0)
genusLabel = Label(main_window, text = "")
genusLabel.grid(row = 8, column = 0)
speciesLabel = Label(main_window, text = "")
speciesLabel.grid(row = 9, column = 0)


# Individual text label boxes for each taxonomic level
kingdomLabel1 = Label(main_window, text = "")
kingdomLabel1.grid(row = 3, column = 1)
kingdomLabel2 = Label(main_window, text = "")
kingdomLabel2.grid(row = 3, column = 3)

phylumLabel1 = Label(main_window, text = "")
phylumLabel1.grid(row = 4, column = 1)
phylumLabel2 = Label(main_window, text = "")
phylumLabel2.grid(row = 4, column = 3)

classLabel1 = Label(main_window, text = "")
classLabel1.grid(row = 5, column = 1)
classLabel2 = Label(main_window, text = "")
classLabel2.grid(row = 5, column = 3)

orderLabel1 = Label(main_window, text = "")
orderLabel1.grid(row = 6, column = 1)
orderLabel2 = Label(main_window, text = "")
orderLabel2.grid(row = 6, column = 3)

familyLabel1 = Label(main_window, text = "")
familyLabel1.grid(row = 7, column = 1)
familyLabel2 = Label(main_window, text = "")
familyLabel2.grid(row = 7, column = 3)

genusLabel1 = Label(main_window, text = "")
genusLabel1.grid(row = 8, column = 1)
genusLabel2 = Label(main_window, text = "")
genusLabel2.grid(row = 8, column = 3)

speciesLabel1 = Label(main_window, text = "")
speciesLabel1.grid(row = 9, column = 1)
speciesLabel2 = Label(main_window, text = "")
speciesLabel2.grid(row = 9, column = 3)

# Text box for blurb from Arek's service
blurb1 = Label(main_window, text = "", wraplength=400)
blurb1.grid(row = 11, column = 1)
blurb2 = Label(main_window, text = "", wraplength=400)
blurb2.grid(row = 11, column = 3)

learnMore1 = Label(main_window, text = "")
learnMore1.grid(row = 12, column = 1)

learnMore2 = Label(main_window, text = "")
learnMore2.grid(row = 12, column = 3)

learnMore3 = Label(main_window, text = "")
learnMore3.grid(row = 13, column = 1)

learnMore4 = Label(main_window, text = "")
learnMore4.grid(row = 13, column = 3)


# Let's do this
main_window.mainloop()
