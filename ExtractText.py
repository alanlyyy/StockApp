import pandas as pd

import datetime

#to use regular expressions to split each line to text + numbers
import re


class ExtractText:
    """This script processes the financial data extracted from marketwatch.

    """
    
    def __init__(self,stockName):
        
        self.fileName = stockName + ".txt"

        #read file
        self.file = open(self.fileName)

    def generateTable(self):
        #split text doc into list of lines
        
        current_year_full = datetime.datetime.today().year
        year_delta = (current_year_full - 5)
        
        
        #with statement closes the file after reading everything
        with self.file as f:
            data = f.read().split('\n')
        
        listWords = []
        

        for line in data:
            
            if len(re.split('(\D+[^-])\s', line)) < 4:
                
                split_words = []
                
                #split the string and iterate over contents
                for value in re.split('(\D+[^-])\s', line):
                    
                    if value != '':
                    
                        split_words.append(value)
            
                listWords.append(split_words)
                
                
        df = pd.DataFrame(listWords, columns=['Metric', 'Years'])
                           
        df = df.join(df.pop('Years').str.split(expand=True))


        df.columns = ['Metric'] + list(range(current_year_full, year_delta, -1))

        df = df.set_index('Metric')
        
        return df

    def testStrings(self):
        #Test list of strings    
        myText = ["Cost of Goods Sold (COGS) incl. D&A 142.26B 131.51B 141.7B 163.83B 162.26B",
        "Depreciation & Amortization Expense 10.5B 9.8B 9.4B 9.3B 11.3B","Other SG&A 14.33B 14.19B 15.26B 16.71B 18.25B"]

        #Test list of strings that break the code
        breakStrings = ["Other Operating Expense - - - - -", "Unusual Expense - (548M) - - -","Fiscal year is October-September. All values USD millions. 2015 2016 2017 2018 2019 5-year trend"]
        #params = ExtractParams(file)

        print(re.split('(\D+[^-])\s', breakStrings[0]))
        print(re.split('(\D+[^-])\s', breakStrings[-1]))
        print(re.split('(\D+[^-])\s', myText[0]))
        print(re.split('(\D+[^-])\s', myText[1]))

