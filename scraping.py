

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)




# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)




#Set HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')



#Begin scraping, identify parent element
slide_elem.find('div', class_='content_title')




# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title





# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images




# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)





# Find and click the full image button
#Index[1], indicates to click on the second button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()




# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')



# Find the relative image url
img_url_rel = img_soup.find('img', class_='thumbimg').get('src')
img_url_rel



# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url



#we're creating a new DataFrame from the HTML table.
#read_html() specifically searches for and returns a list of tables found in the HTML
# [0] pull only the first table it encounters, or the first item in the list
df = pd.read_html('https://galaxyfacts-mars.com')[0]

#we assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'Mars', 'Earth']

#By using the .set_index() function, we're turning the Description column into the DataFrame's index. inplace=True means that 
#the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace=True)
df



#convert our DataFrame back into HTML-ready code using the .to_html()
df.to_html()

#end session
browser.quit()






