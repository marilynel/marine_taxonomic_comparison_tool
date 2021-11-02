"""
TODO:
- find an image from wikipedia
- download the image and put on my own server
- send the url to the requestor

FIND OUT:
- can I resize the image?
- if the image already has a url, can I send that instead?
- can I get images from another source and not just wikipedia?
"""

import requests
import shutil        # for saving image locally

# set up image URL and filename
#image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Sanc0063_-_Flickr_-_NOAA_Photo_Library.jpg/330px-Sanc0063_-_Flickr_-_NOAA_Photo_Library.jpg"
# --> 403 forbidden???
#image_url = "https://cdn.pixabay.com/photo/2020/02/06/09/39/summer-4823612_960_720.jpg"
# --> 503 scheduled maintenance?
#image_url = "https://i.imgur.com/47yrgsI.png"
# --> works!
#image_url = "https://i.imgur.com/63yq1QZ.jpeg"
# --> works!
#image_url = "https://pyxis.nymag.com/v1/imgs/977/5e1/3f86e3b3daa18265b5a280030235496c43-26-mushroom-lede.2x.rsocial.w600.jpg"
# --> works!
#image_url = "https://upload.wikimedia.org/wikipedia/commons/c/c2/Amanita_muscaria_%28fly_agaric%29.JPG"
# --> works!
#image_url = "https://en.wikipedia.org/wiki/File:ChoerodCauteromaRLS.jpg"
# does not work, but gives 200 status_code??
#image_url = "https://upload.wikimedia.org/wikipedia/commons/e/e4/ChoerodCauteromaRLS.jpg"
# --> 403 forbidden
filename = image_url.split("/")[-1]


# open url image, set stream to true, this will return stream content
r = requests.get(image_url, stream = True)

# check if image was sucessfully retrieved
if r.status_code == 200:
    # set decode_content value to true, otherwise the image file's size will be zero
    r.raw.decode_content = True

    #open a local file with wb (write binary) permission
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    print("got it! filename = ", filename)
else:
    print("nope")
    print(r.status_code)






#photoResponse = requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Sanc0063_-_Flickr_-_NOAA_Photo_Library.jpg/330px-Sanc0063_-_Flickr_-_NOAA_Photo_Library.jpg")
#file = open("kelp2.jpg", "wb")
#file.write(photoResponse.content)
#file.close()
