import pandas as pd
import numpy as np
class dataPreperation:

    def __init__(self, data, allAttributes, categories):

        self.data = data
        self.allAttributes = allAttributes
        self.categories = categories

# fix empty data
    def handeleNans(self):
        for attribute in self.allAttributes:
            if attribute in self.categories.keys():
                #categorial
                self.data[attribute].fillna((self.data[attribute]).mode()[0], inplace=True)
            else:
                #numeric
                self.data[attribute].fillna(self.data[attribute].mean(), inplace=True)

    def discretization(self, binsNumber):
        self.categoryBins = {}
        for column in self.allAttributes:
            #numeric columns
            if column not in self.categories.keys() and column != self.allAttributes[len(self.allAttributes) - 1]:
                self.data[column], bins = pd.cut(self.data[column], binsNumber, labels=np.arange(binsNumber), retbins= True)
                self.categoryBins[column] = bins
