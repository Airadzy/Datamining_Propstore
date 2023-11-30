from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# give access to type keys etc so we access Enter etc

driver = webdriver.Chrome()

driver.get("https://propstore.com/products/?auction=1&buyNow=1&archive=1")
print(driver.title)

search = driver.find_element("s") #  this is because the search bar is labelled as name "s" in the youtube video
search.send_keys("test") # brings us to search results and types in test. thats why its send_keys, because we type in test
search.send_keys(Keys.RETURN) # to hit enter. importing driver to get Keys and Return is like ENTER

#issue that we could look for things before we landed on website. to fix that we can wait on Selenium for specific page to come up. "Explicit Waits"
# wait tuntil presence on page
try:
    main = webdriv


main = driver.find_element("")

print(driver.page_source) # not that useful. entire sourcecode for the page

# driver.close() / driver.quit() -> to close tab or window
# access id, name, class name. Hierarchy is id first (because unique)