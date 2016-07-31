# Bazaarvoice-API

**Note: this module comfortable with 5.4 Bazaarvoice-API version only**

Bazaarvoice-API is python module that lets you get data from Bazaarvoice in the easy way
the only thing you need to do is to install this module and provide your api key and searched brand

* First, lets install the python module from pip

           pip install git+https://github.com/danieldanieltata/Bazaarvoice-API.git

**Now you can use bazaarvoice_api module**

# How to use this module ?

* First lets import Bazaarvoice-API module

          from bazaarvoice_api import BazaarvoiceAPI

* Now I will show you a small code example that shows how you can use this module and get all the data from the bazaarvoice-api

          bazzarvoice = BazaarvoiceAPI('[API_KEY]', '[SEARCHED_BRAND]')
          data_container = []

          for prod in bazzare.get_product():
              data_container.append(prod)

In this peace of code you can see that I'm holding my data in array, all the reviews of product and data for product stored inside a product object,
so if I will want to get the product Id I will write this easy command

          data_container[0].Id

**Inside the product object we have also the reviews object, the reviews object stores all the reviews**

This module doesn't stores data in variables, so you dont need to worry about memory usage in this module
