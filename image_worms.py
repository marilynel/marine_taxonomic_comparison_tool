'''
trying to get the "first" img from wikipedia is driving me crazy
in the meantime, I will implement a separate scraper service that just grabs an image from WORMS
will see what happens
'''
import urllib
from flask import Flask, request, url_for
import requests
from bs4 import BeautifulSoup


service = Flask(__name__)
'''
do i still need this s wikipedia???
# Headers are necessary because wikipedia likes to be difficult
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}
'''

# Get an image from worms
def imageStuff(name):
    #try:
    name = urllib.parse.quote_plus(name)
    wormsUrl = 'https://www.marinespecies.org/rest/AphiaRecordsByName/{}?like=true&marine_only=true&offset=1'
    wormsUrl = wormsUrl.format(name)
    wormsLinkUrl = ""
    response = requests.get(wormsUrl)
    if response.status_code == 200:
        orgData = response.json()
        for i in orgData[0]:
            if i == 'url':
                wormsLinkUrl = orgData[0][i]        # this is the one I want to parse html of
    r = requests.get(wormsLinkUrl)
    soup = BeautifulSoup(r.text)

    # TODO: what is this printing out?
    # need to find first image under "images" tab at the bottom of the page and grab that
    # then, do all the other stuff like i was from wikipedia images? not sure yet
    for item in soup.find_all('img'):
        print(item['src'])

'''
        wikipage = wikipedia.page(item, auto_suggest=False)

        # wikipage.images[0] returns the url of the 0th image
        r = requests.get(wikipage.images[0], headers = headers, stream = True)

        if r.status_code == 200:
            filename = item + "." + wikipage.images[0].split(".")[-1]
            # set decode_content value to true, otherwise the image file size will be zero
            r.raw.decode_content = True
            # save as a local file with write binary permission
            with open("static/" + filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            return filename
        else:
            filename = "imagenotfound.png"
            return filename
    except wikipedia.exceptions.PageError:
        filename = "imagenotfound.png"
        return filename


@service.route('/requestImage', methods=['GET'])
def index():
    imageName = request.args.get('name')
    filename = imageStuff(imageName)
    return {"url": "http://notforlong.net:5007/static/" + filename}


service.run(host='0.0.0.0', port=5007)
'''
def main():
    #name = input()
    imageStuff("hermissenda crassicornis")

main()