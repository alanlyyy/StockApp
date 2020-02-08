#alphavantage stock api
#https://www.alphavantage.co/documentation/#

#API KEY: 13Y2FLBPUCBDMQCC 

#How to to Query Timeseries data:
#ex) https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=13Y2FLBPUCBDMQCC
#    https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&outputsize=full&apikey=13Y2FLBPUCBDMQCC

#List of Ticker Symbols:
#https://stackoverflow.com/questions/25338608/download-all-stock-symbol-list-of-a-market

#SEC stock fundamentals
#https://www.reddit.com/r/investing/comments/4qxjr6/ive_processed_1tb_of_secs_data_to_extract/
#API Token: MCP1y3oNy9IwN8RrlQ3ceg
#http://usfundamentals.com/

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime, os, time

class stockData:
    
    def __init__(self,stockSymbol):
        
        self.stockSymbol = stockSymbol
        
    def queryStockData(self):
        """Querys stock data given a stock symbol.
        Obtain an json file and convert contents into a python dictionary.
        """
        URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=13Y2FLBPUCBDMQCC" %(self.stockSymbol)

        r = requests.get(URL)

        soup = BeautifulSoup(r.content,'html.parser') 
        #print(soup.prettify()) 

        #convert soup obejct to python dictionary
        newDictionary= json.loads(str(soup))
        
        
        return newDictionary

    def generateDataFrame(self,dict):
        """Given a dictionary of stock data, extract contents and generate dataFrame.
        
        """
        timeSeriesData = dict["Time Series (Daily)"]
        list_of_close =[]
        list_of_open = []
        list_of_high = []
        list_of_low = []
        list_of_vol = []
        list_of_date =[]

        #loop through each date
        for key in timeSeriesData.keys():
            
            tempKey = key
            
            #append date
            list_of_date.append(key)
            
            #append data label
            list_of_open.append(float((timeSeriesData[key]["1. open"])))
            list_of_high.append(float((timeSeriesData[key]["2. high"])))
            list_of_low.append(float((timeSeriesData[key]["3. low"])))
            list_of_close.append(float((timeSeriesData[key]["4. close"])))
            list_of_vol.append(float((timeSeriesData[key]["6. volume"])))

        #generate dataFrame
        data = {'Date': list_of_date, 'Open': list_of_open, 'High':list_of_high, 'Low': list_of_low,
        'Close':list_of_close, 'Volume': list_of_vol}

        df = pd.DataFrame(data)

        #caste date to DateTime object
        df.index = pd.to_datetime(df['Date'])

        #drop previous date
        df = df.drop(columns='Date')
        
        #save a CSV copy for cache
        fileName = "stock/'" + self.stockSymbol + ".csv"
        df.to_csv(fileName)
        
        return df
        
    def plotChart(self,df,time):
        """Plot chart for given time selection given a dataFrame."""
        
        d = datetime.datetime.today()
        currentDay = d.strftime('%Y-%m-%d')
        
        if time == 1:
            #generate date for 1 day and convert to string
            prevDay = (d - datetime.timedelta(days = 1)).strftime('%Y-%m-%d')

        
        elif time == 2:
            #generate date for past week and convert to string
            prevDay = (d - datetime.timedelta(days = 7)).strftime('%Y-%m-%d')
        
        elif time == 3:
            
            #generate date for previous month and convert to string
            prevDay = (d - datetime.timedelta(days = 31)).strftime('%Y-%m-%d')
            
        elif time == 4:
            
            #generate date for past 6 months and convert to string
            prevDay = (d - datetime.timedelta(days = 186)).strftime('%Y-%m-%d')
        
        elif time == 5:
            
            #generate date for past year and convert to string
            prevDay = (d - datetime.timedelta(days = 365)).strftime('%Y-%m-%d')
            
        elif time == 6:
            
            #generate date for past 5 years and convert to string
            prevDay = (d - datetime.timedelta(days = 1825)).strftime('%Y-%m-%d')
            
        else:
            
            #generate date for all time and convert to string
            prevDay = '1990-01-01'
        
        
        plt.plot(df.index,df['Close'])
        plt.title('Closing Price',fontsize=14)
        plt.xlabel('Date',fontsize=14)
        plt.ylabel('$',fontsize=14)
        plt.xlim(prevDay, currentDay)
        plt.autoscale(enable=True, axis='both',tight=None)
        plt.show()
        
    
    def FiftyTwoWkAvg(self,dataFrame):
        """Calculates 260,100,50,30 day moving averages."""
        
        data = dataFrame['Close'].head(260)  #calculate 52 week avg
        data2 = dataFrame['Close'].head(100) #calculate 100 day avg
        data3 = dataFrame['Close'].head(50) #calculate 50 day avg
        data4 = dataFrame['Close'].head(30) #calculate 30 day avg
        
        AVG1 = data.sum()/len(data)
        AVG2 = data2.sum()/len(data2)
        AVG3 = data3.sum()/len(data3)
        AVG4 = data4.sum()/len(data4)
        
        return AVG1,AVG2,AVG3,AVG4
        
    def checkCache(self,stockName):
        """Check the local directory if symbol was queried in the past day.
        If csv file does not exist or symbol was queried past one day query again.
        else return a pandas dataframe.
        """

        directory = "stock\'"
        file = directory + stockName + ".csv"

        #check if file exists
        if os.path.isfile(file):

            #if stock data is one day old , 86400 = 1 day query the data again
            if (os.path.getmtime(file) - time.time()) > 86400.00:

                return False
            
            else:
                
                return True

        else:
            return False

if __name__ == "__main__":

    symbol = input("Enter Stock Ticker: ")
    
    directory = "stock\'"
    file = directory + symbol + ".csv"
    
    #create stock Data object
    p1 = stockData(symbol)
    
    #query data or generate dataframe
    if p1.checkCache(symbol):
        p1df = pd.read_csv(file)
    else:
        #query stock data
        p1Query = p1.queryStockData()
        p1df = p1.generateDataFrame(p1Query)
    
    #plot the timeseries data
    p1.plotChart(p1df,2)
    
    print(p1.FiftyTwoWkAvg(p1.generateDataFrame(p1.queryStockData())))
    
    