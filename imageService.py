#!/usr/bin/env python3

"""
TODO:
- get MAIN image from wikipedia (from infobox)
"""

from flask import Flask, request, url_for
import wikipedia
import requests
import shutil

service = Flask(__name__)

# Headers are necessary because wikipedia likes to be difficult
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}


# Get an image from wikipedia
def imageStuff(item):
    try:
        if " " in item:
            item = item.replace(" ", "_")
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
