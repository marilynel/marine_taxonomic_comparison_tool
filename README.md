For image getting service:

This is a python service that utilizes a number of additional libraries that will need to be installed (listed below). You can install libaries from the command line:
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
