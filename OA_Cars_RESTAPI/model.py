# Script for the Classifier Class Object(Preprocessing and Others)
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import pickle
from datetime import date
import pandas as pd
import os, os.path, time
import datetime
from datetime import timedelta


tomorrow = date.today() + timedelta(days=20)

class PriceRangeModel(object):
    def __init__(self):
        self.clf = LinearRegression()
        self.version = 0.0
        self.lastModelTrainDate = None
        self.le = LabelEncoder()

    def label_fit_transform(self, data):
        print(data.head())
        df = pd.get_dummies(data['Fuel_Type'],prefix='FT',drop_first=True)
        data['Seller_Type'] = self.le.fit_transform(data['Seller_Type'])
        data['Transmission'] = self.le.fit_transform(data['Transmission'])
        data = pd.concat([data,df],axis=1)
        data.drop(['Fuel_Type'],axis=1,inplace=True)
        print("here")
        print(data.head())
        print("exit")

        return data

    def train(self, X, y):
        self.clf.fit(X,y)

    def predict(self, X):
        prediction = self.clf.predict(X)
        return prediction

    def currentVersion(self):
        DIR = './lib/models/'
        versionNumber = float(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
        return versionNumber

    def updateVersion(self):
        self.version = self.currentVersion() + 1.0

    def updateTrainDate(self):
        versionNumber = self.currentVersion()
        DIR = './lib/models/LogisticRegression-{}.pkl'.format(versionNumber)
        self.lastModelTrainDate = os.stat(DIR).st_ctime
        self.lastModelTrainDate = datetime.datetime.fromtimestamp(self.lastModelTrainDate).date()
        return self.lastModelTrainDate

    def todayDate(self):
        d = datetime.datetime.today().date()
        return d

    def dateDifference(self):
        return self.todayDate().month - self.updateTrainDate().month

    def pickleClassifier(self):
        """
        Saves/Dumps the trained Classifier to be Loaded for Future Use
        :param path:
        :return:
        """
        self.updateVersion()
        print(self.version)
        path = './lib/models/LogisticRegression-{}.pkl'.format(self.version)

        with open(path,'wb') as f:
            pickle.dump(self.clf, f)
            self.updateTrainDate()
            print("Pickled Classifier at {}".format(path))


        self.updateTrainDate()
        print(self.updateTrainDate())
