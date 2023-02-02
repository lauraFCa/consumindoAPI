# Using Linkedin's API with Python

API requests made with _requests_ package  
Interface made using *PyQt6*

## References

### LinkedIn

[API Documentation](https://learn.microsoft.com/pt-br/linkedin/)

Must have a _company page_ on LinkedIn to request API usage.

### Requests

Made with _requests_ pakage  
[Documentation](https://pypi.org/project/requests/)  
[Usage - Python’s Requests Library (Guide)](https://realpython.com/python-requests/#the-response)  
[Usage - GET and POST requests using Python](https://www.geeksforgeeks.org/get-post-requests-using-python/)

Working with JSON:  
[Python Create JSON](https://pythonexamples.org/python-create-json/)  
[Working with JSON in Python](https://datagy.io/python-requests-json/)  
[Parse a JSON response using Python requests library](https://pynative.com/parse-json-response-using-python-requests-library/)

### Interface

PyQt6: Package to build graphic interfaces with Python

`pip install pyqt6`

**References:**  
[Creating your first app with PyQt6](https://www.pythonguis.com/tutorials/pyqt6-creating-your-first-window/)  
[Python and PyQt: Building a GUI Desktop Calculator](https://realpython.com/python-pyqt-gui-calculator/)

### Pacotes

| Package            | Version   |
| ------------------ | --------- |
| pip                | 22.3      |
| PyQt6              | 6.4.0     |
| PyQt6-Qt6          | 6.4.0     |
| PyQt6-sip          | 13.4.0    |
| requests           | 2.28.1    |

## Application

To use the application is necessary to have an authentication token to the LinkedIn API.  
It is also needed to have installed both libraries, *requests* and *pyqt6*.

**To run simply execute the file *Janelas.py***

The available API actions are the ones allowed by Linkedin's API.  
<!-- ![LinkedIn API](imgs/linkedinProducts.png) -->

Scopes are: Get the data from the autheticated user and Create a new publication (post) of three available types (simple, with a link or with an image).  
<!--
**Simple Post**  
![Simple](imgs/pubSimples.png)


**Image Post**  
![Image](imgs/imgPub.png)


**Post with a Link**  
![Link](imgs/linkPub.png)
-->

Application Prints:  
![Sistema desenvolvido](data/integracaoSft.png)

<!-- 
Command to create the executable file:  
```
pyinstaller --noconsole Janelas.py --icon='data/linkApi.ico' --add-data 'data/linkApi.ico;data' --add-data 'data/integracaoSft.png;data'
``` -->
