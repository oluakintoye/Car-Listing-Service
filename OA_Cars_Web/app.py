from flask import Flask, render_template, request, redirect, url_for
import requests
import json


app = Flask(__name__)

app._static_folder = './static'

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':

        return render_template('index.html')


@app.route("/valuevehicle", methods=['GET', 'POST'])
def valuevehicle():
    if request.method == 'POST':
        Car_Name = request.form["Car_Name"]
        Year = int(request.form["Year"])
        Present_Price = float(request.form["Present_Price"])
        Kms_Driven = int(request.form["Kms_Driven"])
        Fuel_Type = request.form["Fuel_Type"]
        Seller_Type = request.form["Seller_Type"]
        Transmission = request.form["Transmission"]
        Owner = int(request.form["Owner"])
        Month_Number = int(request.form["Month_Number"] )


        print(Car_Name,Year,Present_Price,Kms_Driven,Fuel_Type,Seller_Type,
              Transmission,Owner, Month_Number
              )

        url = 'http://vehicle-sales.herokuapp.com/valuevehicle'

        data = {"Car_Name": Car_Name,
                "Year": Year,
                "Present_Price": Present_Price,
                "Kms_Driven": Kms_Driven,
                "Fuel_Type": Fuel_Type,
                "Seller_Type": Seller_Type,
                "Transmission": Transmission,
                "Owner": Owner,
                "Month_Number": Month_Number}

        j_data = json.dumps(data)
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

        r = requests.get(url, data=j_data, headers = headers)
        print(r, r.json)

        result=r.text[14:-2]
        print(result)

        return render_template('index.html', result = result )


@app.route("/updateListing", methods=['GET', 'POST'])
def updateCarListing():
    if request.method == 'POST':
        Car_Name = request.form["Car_Name"]
        Year = int(request.form["Year"])
        Selling_Price = float(request.form["Selling_Price"])
        Present_Price = float(request.form["Present_Price"])
        Kms_Driven = int(request.form["Kms_Driven"])
        Fuel_Type = request.form["Fuel_Type"]
        Seller_Type = request.form["Seller_Type"]
        Transmission = request.form["Transmission"]
        Owner = int(request.form["Owner"])


        print(Car_Name,Year,Selling_Price,Present_Price,Fuel_Type,Seller_Type,
              Transmission,Owner
              )

        url = 'http://vehicle-sales.herokuapp.com/update'

        data = {"Car_Name":Car_Name,
                "Year":Year,
                "Present_Price":Present_Price,
                "Kms_Driven":Kms_Driven,
                "Fuel_Type":Fuel_Type,
                "Seller_Type":Seller_Type,
                "Transmission":Transmission,
                "Owner":Owner,
                 }

        j_data = json.dumps(data)
        print(j_data)
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

        r = requests.post(url, data=j_data, headers = headers)

        print(r, r.json)

        output = r.text
        print(output)

        return render_template('index.html', output = output )

@app.route("/browseListing", methods=['GET', 'POST'])
def browseCarListing():
    if request.method == 'POST':
        Car_Name = request.form["Car_Name"]
        Fuel_Type = request.form["Fuel_Type"]
        Seller_Type = request.form["Seller_Type"]
        Transmission = request.form["Transmission"]

        print(Car_Name, Fuel_Type, Seller_Type,
              Transmission
              )

        url = 'http://vehicle-sales.herokuapp.com/onlisting'

        # data = [[Car_Name,Fuel_Type, Seller_Type,
        #          Transmission
        #          ]]

        data = {"Car_Name": Car_Name,
                "Fuel_Type": Fuel_Type,
                "Seller_Type": Seller_Type,
                "Transmission": Transmission
                 }

        j_data = json.dumps(data)
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

        r = requests.get(url, data=j_data, headers = headers)

        print(r, r.json())
        print(r.json()[0])
        l = len(r.json())

        output1 = r.json()



        return render_template('index.html', output1 = output1)


if __name__  == "__main__":
    app.run(debug=True)