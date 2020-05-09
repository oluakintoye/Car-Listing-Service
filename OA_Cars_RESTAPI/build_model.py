import pandas as pd
import numpy as np
from model import PriceRangeModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime

pd.set_option('display.max_columns',10)


path='./lib/data/car data.csv'

with open(path) as f:
    data = pd.read_csv(f)

version = None
# PriceRangeObject
model = PriceRangeModel()

def buildModelWithVersioning():

    # X = data.iloc[:, :-1]
    # y = data.iloc[:, -1]
    X = data.drop(['Car_Name','Selling_Price'], axis = 1)
    y = data['Selling_Price']

    X = model.label_fit_transform(X)



    print('Label Encoding Complete')

    X_train, X_test, y_train, y_test =train_test_split(X, y, test_size=0.25, random_state=10)

    #Train the Model
    model.train(X_train,y_train)
    print("Training...")
    print("Model Training Complete")

    print()

    #Testing the Model
    y_pred = model.predict(X_test)
    print("Testing...")
    print("Model Testing Complete")
    print()


    #Dumping the trained classifier
    model.pickleClassifier()

    # currentVersion = model.currentVersion
    mse = mean_squared_error(y_test,y_pred)
    tmse = mean_squared_error(y_test,y_pred)
    trmse = np.sqrt(mse)
    rmse = np.sqrt(mse)

    print("Performance")
    print('Mean Squared Error of Test Set : {}'.format(mse))
    print('Root Mean Square Error of Test Set : {}'.format(rmse))
    print('Mean Squared Error of Train Set : {}'.format(tmse))
    print('Root Mean Square Error of Train Set : {}'.format(trmse))

    version = model.version


def buildModel():

    # X = data.iloc[:, :-1]
    # y = data.iloc[:, -1]
    X = data.drop(['Car_Name','Selling_Price'], axis = 1)
    y = data['Selling_Price']

    X = model.label_fit_transform(X)



    print('Label Encoding Complete')

    X_train, X_test, y_train, y_test =train_test_split(X, y, test_size=0.25, random_state=10)

    #Train the Model
    model.train(X_train,y_train)
    print("Training...")
    print("Model Training Complete")

    print()

    #Testing the Model
    y_pred = model.predict(X_test)
    print("Testing...")
    print("Model Testing Complete")
    print()

    # currentVersion = model.currentVersion
    mse = mean_squared_error(y_test,y_pred)
    tmse = mean_squared_error(y_test,y_pred)
    trmse = np.sqrt(mse)
    rmse = np.sqrt(mse)

    print("Performance")
    print('Mean Squared Error of Test Set : {}'.format(mse))
    print('Root Mean Square Error of Test Set : {}'.format(rmse))
    print('Mean Squared Error of Train Set : {}'.format(tmse))
    print('Root Mean Square Error of Train Set : {}'.format(trmse))

    version = model.version

# Updating Car Listing
def updateListing(row):

    frames = [data, row]
    dataset = pd.concat(frames, ignore_index=True)
    print(dataset.head())

    dataset.to_csv(path,index = False ,columns = ['Car_Name', 'Year', 'Selling_Price', 'Present_Price', 'Kms_Driven',
                                    'Fuel_Type', 'Seller_Type', 'Transmission', 'Owner'])

    #Retrain
    # buildModel()
    print(model.todayDate(), model.todayDate().month)
    print(model.updateTrainDate(), model.updateTrainDate().month)
    print("Train Date Difference: ", model.dateDifference())

    if model.dateDifference() >= 1:
        print("We are here")
        buildModelWithVersioning()
    else:
        buildModel()

#Browse Car Listing
def BrowseListing(input):

    Listing = []

    for index, row in data.iterrows():
        if data.at[index,'Car_Name'] == input[0] and data.at[index,'Fuel_Type']== input[1] and data.at[index,'Seller_Type'] == input[2] and data.at[index,'Transmission'] == input[3]:
            Listing.append(list(row[data.columns]))

    return Listing




if __name__ == '__main__':
    buildModelWithVersioning()

