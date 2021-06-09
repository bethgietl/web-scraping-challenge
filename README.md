# web-scraping-challenge

I used Pandas, BueautifulSoup, and Splinter to scrape the content and/or images from nasa's webpage. Once the splinter was set-up (executable_path and browser) I was able to visit and convert the browser html to a soup object. 

I used the soup.select_one and .find functions to find the first tag of the news title and save the text of the news title. I did the same thing to retreive the paragraph text. 

I used the .find_by_tag function to find the button associated with the featured picture on the webpage and used the .click function to click the button. Once the button was clicked I parsed the resulting html with soup, used .find to find the image and .get to get the source. I stored the base url and the featured image url in a variable to create an absolute url. 

My favorite part of the assignment was converting the html table to a DataFrame using pd.read_html - it really showed the power of Pandas! 

I used a for loop to scrape all four images from the requested webpage. 

I downloaded my Jupyter Notebook file to a .py file and renamed it scrape_mars. I cleaned up the scrape file and defined the functions. I created a dictionary to hold hold all the results of the functions. 

