"""
This script extracts all the financial data from marketwatch for a given stock.

Selenium Demo.
https://www.youtube.com/watch?v=GJjMjB3rkJM

https://selenium-python.readthedocs.io/locating-elements.html#locating-elements

"""


from selenium import webdriver

class finExtract:

    def finExtractor(self,stockName):
        
        #open textfile
        fileName = stockName + ".txt"
        myFile = open(fileName,"w")

        URL = 'https://www.marketwatch.com/investing/stock/%s' %stockName

        #instantiate browser with chrome driver
        browser = webdriver.Chrome('C:\\Users\\Alan\Documents\\StockApp\\chromedriver')
        browser.get(URL)

        #access 'financials' tab from the sourcecode
        elem = browser.find_element_by_xpath('//div[@class="element element--subnav"]/ul/li[4]/a')

        #click financials tab sends "enter" for links and buttons
        elem.send_keys("\n")
        
        #gather Income statement text
        i1 = browser.find_element_by_xpath('//table[@class="crDataTable"][1]')
        i2 = browser.find_element_by_xpath('//table[@class="crDataTable"][2]')
        
        myFile.write(i1.text)
        myFile.write(i2.text)
        myFile.write("-------------------")

        browser.implicitly_wait(5)

        #access balance sheet button/ link
        elem2 = browser.find_element_by_xpath('//div[@class="financials"]/div[@class="subnavigation"]/span[2]')

        elem2.click()
        
        #access balance sheet text
        b1 = browser.find_element_by_xpath('//table[@class="crDataTable"][1]')
        b2 = browser.find_element_by_xpath('//table[@class="crDataTable"][2]')
        b3 = browser.find_element_by_xpath('//table[@class="crDataTable"][3]')


        myFile.write(b1.text)
        myFile.write(b2.text)
        myFile.write(b3.text)
        myFile.write("-------------------")

        browser.implicitly_wait(5)

        #access cash flow statement button/ link
        elem3 = browser.find_element_by_xpath('//div[@class="financials"]/div[@class="subnavigation"]/span[3]')

        elem3.click()
        
        #access cash flow sheet text
        cf1 = browser.find_element_by_xpath('//table[@class="crDataTable"][1]')
        cf2 = browser.find_element_by_xpath('//table[@class="crDataTable"][2]')
        cf3 = browser.find_element_by_xpath('//table[@class="crDataTable"][3]')

        myFile.write(cf1.text)
        myFile.write(cf2.text)
        myFile.write(cf3.text)

        browser.implicitly_wait(5)

        myFile.close()

        #quit after scraping all financial data
        browser.quit()