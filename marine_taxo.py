from tkinter import *
from PIL import ImageTk, Image
import requests
import json
import urllib.parse
from difflib import SequenceMatcher

main_window = Tk()
main_window.resizable(width = True, height = True)


# labels for text bars for searching
Label(main_window, text = "Genus 1:").grid(row = 0, column = 0)
Label(main_window, text = "species 1:").grid(row = 1, column = 0)
Label(main_window, text = "Genus 2:").grid(row = 0, column = 2)
Label(main_window, text = "species 2:").grid(row = 1, column = 2)

# for printing text to gui later; may not be needed?
outputText = ""
outputText2 = ""
labels = ""
strText1 = ""
strText2 = ""

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
    taxo = ""
    response = requests.get(url)
    if response.status_code == 200:
        orgData = response.json()
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

def clear_values():
    genus.delete(0, END)
    genus2.delete(0, END)
    spp.delete(0, END)
    spp2.delete(0, END)

def post_image(colNum, name):
    safe_string = urllib.parse.quote_plus(name)
    url = "http://notforlong.net:5007/requestImage?name={}"
    url = url.format(safe_string)
    imgResponse = requests.get(url)
    if imgResponse.status_code == 200:
        print("Marilyn's image service for " + name)
        res = imgResponse.json()
        # url of image is at: res['url']
        photoResponse = requests.get(res['url'])
        filename = name + "." + res['url'].split(".")[-1]
        file = open(filename, "wb")
        file.write(photoResponse.content)
        image = Image.open(filename)
        image = image.resize((200,150), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = Label(main_window, image = photo)
        label.image = photo
        label.grid(row=4, column = colNum)


def post_wiki_data(colNum, name):
    safe_string = urllib.parse.quote_plus(name)
    url = "http://flip2.engr.oregonstate.edu:4203/?page={}"
    url = url.format(safe_string)
    response = requests.get(url)
    refStr = ""
    refDict = {}
    if response.status_code == 200:
        print("Arek's wiki service for " + name)
        res = response.json()
        for i in res:
            if i == "Description":
                for j in res[i]:
                    refStr = res[i][j]
        label = Label(main_window, text=refStr)
        label.grid(row=6, column=colNum)

#######
# TODO:
# - format output string
# - take out [] and ref numbers
#######


#callback function for clicking the search button
def on_click():
    # for printing text to gui later
    global outputText, outputText2
    global strText1, strText2

    # make the species name from the inputs
    # TODO: do I want to do this as one text box?
    name = genus.get() + " " + spp.get()
    #taxo1 = make_taxo_list(name)
    #outputText = go_thru_list(taxo1)
    outputText = make_taxo_list(name)

    name2 = genus2.get() + " " + spp2.get()
    #taxo2 = make_taxo_list(name2)
    #outputText2 = go_thru_list(taxo2)
    outputText2 = make_taxo_list(name2)


    # compare strings
    match = SequenceMatcher(None, outputText, outputText2).find_longest_match(0, len(outputText), 0, len(outputText2))

    equalSubStr = outputText[match.a: match.a + match.size]
    # THIS DID NOT WORK , FIND ANOTHER METHOD
    #textLabel.tag_add("diff", "2.4")
    #textLabel2.tag_add("diff", "5.7")


    textLabel.config(text = outputText)
    textLabel2.config(text = outputText2)

    textLabelsTaxNames.config(text = "Kingdom:\nPhylum:\nClass:\nOrder:\nFamily:\nGenus:\nSpecies:")
    clear_values()

    #strText1 = request.get()
    #strText1 = strText1.text()
    #strText1 = f"Text from teammate's service about {name} will go here."
    blurb1.config(text = strText1)

    #strText2 = request.get()
    #strText2 = strText2.text()
    #strText2 = f"Text from teammate's service about {name2} will go here."
    blurb2.config(text = strText2)
    post_image(1, name)
    post_image(3, name2)
    post_wiki_data(1, name)
    post_wiki_data(3, name2)


###########
# TODO:
# change banner at top to say somthing other than 'tk'
# color comparison
# change button to say "new search" after first search is done?
###########



# button widget
Button(main_window, text = "Compare", command = on_click ).grid(row = 2, columnspan = 4)

textLabelsTaxNames = Label(main_window, text = "")
textLabelsTaxNames.grid(row = 3, column = 0)

# place for the outputText
textLabel = Label(main_window, text = "")
#textLabel = Text(main_window)
textLabel.grid(row = 3, column = 1)
#textLabel.config(foreground="red")

textLabel2 = Label(main_window, text = "")
#textLabel2 = Text(main_window)
textLabel2.grid(row = 3, column = 3)
#textLabel2.config(foreground="red")

blurb1 = Label(main_window, text = "")
blurb1.grid(row = 5, column = 1)

blurb2 = Label(main_window, text = "")
blurb2.grid(row = 5, column = 3)

main_window.mainloop()
