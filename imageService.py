#!/usr/bin/env python3

"""
TODO:
- return an error if no image exists
    -> possible standard image?
- possible to parse for near matches?
    -> turn "grand canyon" into "grand canyon national park"
- get MAIN image from wikipedia

FIND OUT:
- can I resize the image?
    -> do I need to? may be easier to resize at the user end
- can I get images from another source and not just wikipedia?
"""


# pip install <libraries>
from flask import Flask, request, url_for
import wikipedia
import requests
import shutil
#import validators

service = Flask(__name__)

# headers are necessary because wikipedia likes to be difficult
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}


# get the image from wikipedia
def imageStuff(item):
    # clean up string to make it wiki url friendly
    if " " in item:
        item = item.replace(" ", "_")

    validRes = wikipedia.search(item, results = 1)
    if not validRes:
        filename = "imagenotfound.png"
        return filename

    # get the whole page
    wikipage = wikipedia.page(item, auto_suggest=False)
    # wikipage.images is a list of the images
    #print(f"Number of images on page: {len(wikipage.images)}")
    # the 0th image is not the main image! TODO how to get main image???
    #print(f"main image: {wikipage.images[0]}")
    # wikipage.images[0] returns the url of the 0th image

    # get request 0th image
    r = requests.get(wikipage.images[0], headers = headers, stream = True)
    # give it a new name using input string and suffix from wiki image
    #filename = item + "." + wikipage.images[0].split(".")[-1]
    # 200 is good, any other number is bad
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
        #return("nope")
        #print(r.status_code)


@service.route('/requestImage', methods=['GET'])
def index():
    imageName = request.args.get('name')

    filename = imageStuff(imageName)
    #if filename == "nope":
    #    return {"url": "http://notforlong.net:5007/static/imagenotfound.png"}
    #else:
    return {"url": "http://notforlong.net:5007/static/" + filename}


service.run(host='0.0.0.0', port=5007)
# open ports are 5000 to 5010
