 #Library Imports
from flask import Flask, jsonify
from flask_restful import Api, reqparse, Resource
import pickle
import pandas as pd
import numpy as np
from model import PriceRangeModel
from build_model import updateListing, BrowseListing


app = Flask(__name__)
api = Api(app)

# Creating Model Object
model = PriceRangeModel()

versionNumber = model.currentVersion()

print(versionNumber)

# Load Trained Classifier
path = './lib/models/LogisticRegression-{}.pkl'.format(versionNumber)

with open(path,'rb') as f:
    model.clf = pickle.load(f)

# Argument Parsing
parser = reqparse.RequestParser()


#Using Parser to get the various queries
parser.add_argument('Car_Name')
parser.add_argument('Year')
parser.add_argument('Selling_Price')
parser.add_argument('Present_Price')
parser.add_argument('Kms_Driven')
parser.add_argument('Fuel_Type')
parser.add_argument('Seller_Type')
parser.add_argument('Transmission')
parser.add_argument('Owner')
parser.add_argument('Month_Number')

# Updating Car Listing with Current Happenings in MarketPlace
class UpdateCarListing(Resource):
    def post(self):

        #Using Parser to find the queries
        args = parser.parse_args()

        Car_Name = args['Car_Name']
        Year = args['Year']
        Selling_Price = args['Selling_Price']
        Present_Price = args['Present_Price']
        Kms_Driven = args['Kms_Driven']
        Fuel_Type = args['Fuel_Type']
        Seller_Type = args['Seller_Type']
        Transmission = args['Transmission']
        No_of_Owners = args['Owner']

        inputVariable = pd.DataFrame([[Car_Name, Year, Selling_Price, Present_Price, Kms_Driven,
       Fuel_Type, Seller_Type, Transmission, No_of_Owners]], columns=['Car_Name', 'Year', 'Selling_Price', 'Present_Price', 'Kms_Driven',
       'Fuel_Type', 'Seller_Type', 'Transmission', 'Owner'])

        updateListing(inputVariable)

        output = "Car Listing Successfully Updated"

        return jsonify(output)

# Predicting the Price Range to Value a Vehicle
class ValueVehicle(Resource):
    def get(self):

        #Using Parser to find the queries
        args = parser.parse_args()

        Car_Name = args['Car_Name']
        Year = int(args['Year'])
        Present_Price = float(args['Present_Price'])
        Kms_Driven = int(args['Kms_Driven'])
        Fuel_Type = args['Fuel_Type']
        Seller_Type = args['Seller_Type']
        Transmission = args['Transmission']
        No_of_Owners = int(args['Owner'])

        monthNumber = int(args['Month_Number'])



        if monthNumber != 0 and (versionNumber - monthNumber) > 0:
            VN = versionNumber - monthNumber
            print(VN)
            path = './lib/models/LogisticRegression-{}.pkl'.format(VN)
            print(path)

            with open(path,'rb') as f:
                model.clf = pickle.load(f)


        if Fuel_Type == "Petrol":
            FT_Diesel = 0
            FT_Petrol = 1
        else:
            FT_Diesel = 1
            FT_Petrol = 0

        if Seller_Type == "Dealer":
            Seller_Type = 0
        else: Seller_Type = 1

        if Transmission == "Manual":
            Transmission = 1
        else: Transmission = 0


        inputVariable = [[Year, Present_Price, Kms_Driven, Seller_Type, Transmission, No_of_Owners, FT_Diesel, FT_Petrol]]
        print(inputVariable)


        #Make the Price Range Prediction of Proposed Car
        prediction = np.array2string(model.predict(inputVariable))
        prediction = prediction.replace('[',"")
        prediction = prediction.replace(']',"")

        pricePrediction = float(prediction) * 10000

        #Create JSON Output
        output = {'prediction': pricePrediction}

        return jsonify(output)

#Browsing through Onlisting
class BrowseOnListing(Resource):

    def get(self):

        #Using Parser to find the queries
        args = parser.parse_args()

        Car_Name = args['Car_Name']
        Fuel_Type = args['Fuel_Type']
        Seller_Type = args['Seller_Type']
        Transmission = args['Transmission']

        output = BrowseListing([Car_Name, Fuel_Type, Seller_Type, Transmission])

        return jsonify(output)





api.add_resource(UpdateCarListing,'/update')
api.add_resource(ValueVehicle,'/valuevehicle')
api.add_resource(BrowseOnListing,'/onlisting')

if __name__ == '__main__':
    app.run(debug=True)