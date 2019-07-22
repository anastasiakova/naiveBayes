import os
import tkMessageBox

import pandas as pd


class classifierBuilder:

    def __init__(self, data, categories, allAttributes, binsNumber, allBinsByAttribute):
        self.data = data
        self.categories = categories
        self.allAttributes = allAttributes
        self.classNumberOfClassifiers = categories.get(allAttributes[len(allAttributes) - 1]) if allAttributes[len(allAttributes) - 1] in categories.keys() else binsNumber
        self.classiferCategories = data[allAttributes[len(allAttributes) - 1]].unique().tolist()
        self.allBinsByAttribute = allBinsByAttribute
        attributes = allAttributes[:-1]
        # column + attribute + class : [nc, p]
        self.ncDic = {}
        self.m = 2
        self.calcNForEachClass(allAttributes[len(allAttributes) - 1])
        for attribute in attributes:
            grouped = data.groupby([attribute, allAttributes[len(allAttributes) - 1]])
            for g in grouped:
                M = len(categories.get(attribute)) - 1 if attribute in categories.keys() else binsNumber
                self.ncDic[(attribute,g[0][0],g[0][1])] = [len(g[1]), float(1/float(M))]

    def calcNForEachClass(self, classAtrr):
        self.n = {}
        grouped = self.data.groupby([classAtrr])
        for g in grouped:
            self.n[g[0]] = len(g[1])

    def classify(self, path):
        self.getTest(path)
        self.calc(path)

    def getTest(self,path):
        testPath = path.get() + '/test.csv'
        if os.path.exists(testPath) and os.path.getsize(testPath) > 0:
            self.test = pd.read_csv(testPath)

            for attribute in self.allAttributes:
                if attribute in self.categories.keys():
                    # categorial
                    self.test[attribute].fillna((self.test[attribute]).mode()[0], inplace=True)
                else:
                    # numeric
                    self.test[attribute].fillna(self.test[attribute].mean(), inplace=True)

            self.testClass = self.test[self.test.columns[len(self.test.columns) - 1]]
            self.test.drop(self.test.columns[len(self.test.columns) - 1], axis=1, inplace=True)

            columns = list(self.test)

            for col in columns:
                if col in self.allBinsByAttribute.keys():
                    for i in range(self.test.shape[0]):
                        changed = False
                        for b in range(1,len(self.allBinsByAttribute[col]) - 1):
                            if self.test[col][i] <= self.allBinsByAttribute[col][b]:
                                self.test[col][i] = b - 1
                                changed = True
                                break
                            if not changed:
                                self.test[col][i] = len(self.allBinsByAttribute[col]) - 2
        else:
            tkMessageBox.showerror("Naive Bayes Classifier", "you must have not empty test.csv file in the directory")

    def calc(self, path):
        for index, row in self.test.iterrows():
            classifier = self.NaiveBaseForRow(row)
            self.printRes(path, index + 1, classifier)

    def NaiveBaseForRow(self, row):
        maxP = 0
        classifier = ''
        for classCategory in self.classiferCategories:
            tmp = 1
            P = float(self.n[classCategory]) / float(self.data.shape[0])
            counter = 0
            for i in row:
                # nc + m*p
                up = self.ncDic[(self.data.columns[counter], i, classCategory)][0] + (self.m * self.ncDic[(self.data.columns[counter], i, classCategory)][1])
                # n + m
                down = self.n[classCategory] + self.m
                tmp = tmp * (up/down)
                counter = counter + 1
            if (tmp * P) > maxP:
                maxP = tmp * P
                classifier = classCategory

        return classifier

    def printRes(self, path, number, classifier):
        outputPath = path.get() + '/output.txt'
        f = open(outputPath, 'a+')
        f.write(str(number) + ' ' + str(classifier) + '\n')
        f.close()
