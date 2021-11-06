"""
TODO:
- download the image and put on my own server
- send the url to the requestor
- put online (notforlong.org?)
- return an error if no image exists
- possible to parse for near matches?
    -> turn "grand canyon" into "grand canyon national park"
FIND OUT:
- can I resize the image?
- can I get images from another source and not just wikipedia?
"""



from flask import Flask, request, url_for
import wikipedia
import requests
import shutil

service = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}
def imageStuff(item):
    #item = input("What would you like to get wiki data on? ")
    if " " in item:
        item = item.replace(" ", "_")
    print(item)


    wikipage = wikipedia.page(item)
    #print(f"Page title: {wikipage.title}")
    #print(f"Page URL: {wikipage.url}")
    #print(f"Number of images on page: {len(wikipage.images)}")
    #print(f"main image: {wikipage.images[0]}")
    # wikipage.images[0] returns the url of the first image

    #print(wikipage.images)
    # this is a list of all images on the page

    r = requests.get(wikipage.images[0], headers = headers, stream = True)
    filename = item + "." + wikipage.images[0].split(".")[-1]
    if r.status_code == 200:
        # set decode_content value to true, otherwise the image file's size will be zero
        r.raw.decode_content = True

        #open a local file with wb (write binary) permission
        with open("static/" + filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        return filename
    else:
        return("nope")
        #print(r.status_code)



@service.route('/requestImage', methods=['GET'])
def index():
    imageName = request.args.get('name')
    filename = imageStuff(imageName)
    # size = request.args.get('size')
    return {"url": "http://localhost:81/" + url_for('static', filename=filename)}


service.run(host='0.0.0.0', port=81)

