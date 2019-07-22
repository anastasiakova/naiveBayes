import os
import tkMessageBox
from dataPreperation import *
from classifierbuilder import *

allAtributesNames = []
category = {}

def buildTheModel(directoryPath,binsNumber):
    if validateBins(binsNumber) is not None:
        buildStructure(directoryPath)
        train = readTrain(directoryPath)
        dataPre = dataPreperation(train, allAtributesNames, category)
        dataPre.handeleNans()
        dataPre.discretization(int(binsNumber.get()))
        classifier = classifierBuilder(dataPre.data, category, allAtributesNames, int(binsNumber.get()), dataPre.categoryBins)
        tkMessageBox.showinfo("Naive Bayes Classifier", "Building classifier using train-set is done!")
        return classifier
    else:
        #TODO DISABLE BUTTON!
        tkMessageBox.showerror("Naive Bayes Classifier", "you must enter valid bins Number -> positive number greater than 1!")

# validate bins
def validateBins(binsNum):
    if binsNum.get().isdigit() and int(binsNum.get()) > 1:
        return int(binsNum.get())
    return None

# try Structure.txt
# understand Structure
def buildStructure(directoryPath):
    structurePath = directoryPath.get() + '/Structure.txt'

    if os.path.exists(structurePath) and os.path.getsize(structurePath) > 0:
        with open(structurePath, "r") as structure:
            for x in structure:
                if x.startswith('@ATTRIBUTE'):
                    x = x.replace('\n', '')
                    splitedRow = x.split(" ")
                    if splitedRow.__len__() >= 3:
                        allAtributesNames.append(splitedRow[1])
                        if splitedRow[2].startswith('{'):

                            start = x.rindex('{') + 1
                            end = x.rindex('}', start)
                            categories = x[start:end].split(',')
                            category[splitedRow[1]] = categories
                        elif splitedRow[2] != 'NUMERIC':
                            tkMessageBox.showerror("Naive Bayes Classifier", "structure file must have numeric or categorical attributes")
                else:
                    tkMessageBox.showerror("Naive Bayes Classifier", "structure file must have attributes")
    else:
        tkMessageBox.showerror("Naive Bayes Classifier", "you must have not empty Structure.txt file in the directory")

# try train.csv
def readTrain(directoryPath):
    trainPath = directoryPath.get() + '/train.csv'
    if os.path.exists(trainPath) and os.path.getsize(trainPath) > 0:
        train_df = pd.read_csv(trainPath)
        return train_df
    else:
        tkMessageBox.showerror("Naive Bayes Classifier", "you must have not empty train.csv file in the directory")

# fix empty data

# build model

# open dialog on success
