For image getting service:

Visit url: 
  http://notforlong.net:5007/requestImage?name={}
Place the thing you want an image of within the brackets. For example, if you want a picture of a cat, you will do:
  http://notforlong.net:5007/requestImage?name=cat
Terms with multiple words can be given with spaces.

There are currently some limitations to this service:
  1. This is a Wikipedia specific service. It can only retrieve images from corresponding wikipedia articles
  2. This does not return the "main" image on the wikipedia page.
        --> TODO 11/9/2021
  4. Error handling is still in progress and the service is not yet ready to return the correct output if there is no page or no images on the page available
        --> TODO 11/9/2021

Please let me know if you have any other concerns or issues with the service. Thank you!



------------------------------------------------------------------------------------------------------------------------------------------------------------------------

For local use:

This is a python service that utilizes a number of additional libraries that will need to be installed (listed below). If you would like to run the code locally, you can 
install libaries from the command line:
  pip install <library>
You will need:
  1. flask
  2. wikipedia
  3. requests
  4. shutil
  
To use the service, run the python code with the command 
  python imageService.py
Then, from a browser window, enter
  http://localhost:81/requestImage?name={name of image}
with {name of image} being the images you would like to use for your program. This is a string that can be taken with spaces. For example, entering:
  http://localhost:81/requestImage?name=grand canyon national park
will yield
  http://localhost:81/requestImage?name=grand%20canyon%20national%20park

The return object is a JSON object containing a url to the image you requested. As with the above example:
  {"url":"http://localhost:81//static/grand_canyon_national_park.jpg"}
