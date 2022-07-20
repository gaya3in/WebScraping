Approach to solve problem:

1. Used Selenium, webdriver frameworks to send url request to the browser.
2. Initialized all the driver objects for Chrome Browser.
3. Read the CSV file row by row.  
    For Each row:
       If URL NOT FOUND, print the URL in the console.
       Use string object manipulations to format the url to add country and ASIN.
       Pass the formatted URL to the driver.get function.
       Locate the HTML elements for Product Title, Product Image, Price and details 
       using Selenium find_element functions.
       Manipulate the retrieved string data to fit into a dictionary. 
       Return the dctionary that has the data scraped from the URL to the calling function.
       Catch exceptions and write the URLs in a csv file
4. Append the dictonary to a list. 
5. Repeat steps 3 and 4 until eof.
6. Once eof is reached, dump the list to a jsonfile.

    
   
