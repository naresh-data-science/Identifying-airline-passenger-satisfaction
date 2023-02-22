from flask import Flask, render_template, url_for, request, jsonify
import numpy as np
import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "EBzgaFUmCs9XHX5l1aVYKBp9QuJWAEvsOo56KVTgWMFE"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/input')
def input():
    return render_template('prediction.html')


@app.route('/pred', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":

        Gender = request.form["Gender"]
        if Gender == "Female":
            Gender = 0
        if Gender == "Male":
            Gender = 1
        Age = request.form['Age']
        Type_of_Travel = request.form['Type of Travel']
        if Type_of_Travel == 'Business travel':
            Type_of_Travel = 0
        if Type_of_Travel == "Personal Travel":
            Type_of_Travel = 1
        Class = request.form['Class']
        if Class == "Business":
            Class = 0
        if Class == "Eco":
            Class = 1
        if Class == "Eco Plus":
            Class = 2

        Flight_Distance = request.form['Flight Distance']
        Inflight_wifi_service = request.form['Inflight wifi service']
        Departure_Arrival_time_convenient = request.form['Departure/Arrival time convenient']
        Ease_of_Online_booking = request.form['Ease of Online booking']
        Gate_location = request.form['Gate location']
        Food_and_drink = request.form['Food and drink']
        Online_boarding = request.form['Online boarding']
        Seat_comfort = request.form["Seat comfort"]
        Inflight_entertainment = request.form['Inflight entertainment']
        On_board_service = request.form['On-board service']
        Leg_room_service = request.form['Leg room service']
        Baggage_handling = request.form['Baggage handling']
        Checkin_service = request.form['Checkin service']
        Inflight_service = request.form['Inflight service']
        Cleanliness = request.form['Cleanliness']
        Departure_Delay_in_Minutes = request.form['Departure Delay in Minutes']
        Arrival_Delay_in_Minutes = request.form['Arrival Delay in Minutes']

        total = [[Gender, Age, Type_of_Travel, Class, Flight_Distance, Inflight_wifi_service, Departure_Arrival_time_convenient, Ease_of_Online_booking, Gate_location, Food_and_drink, Online_boarding,
            Seat_comfort, Inflight_entertainment, On_board_service, Leg_room_service, Baggage_handling, Checkin_service, Inflight_service, Cleanliness, Departure_Delay_in_Minutes, Arrival_Delay_in_Minutes]]
        print(total)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"field": ["Gender", "Age", "Type_of_Travel", "Class", "Flight_Distance", "Inflight_wifi_service", "Departure_Arrival_time_convenient", "Ease_of_Online_booking", "Gate_location", "Food_and_drink", "Online_boarding",
            "Seat_comfort", "Inflight_entertainment", "On_board_service", "Leg_room_service", "Baggage_handling", "Checkin_service", "Inflight_service", "Cleanliness", "Departure_Delay_in_Minutes", "Arrival_Delay_in_Minutes"], "values": total}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/379b119c-6b51-48ab-bc09-4935fdcd25bf/predictions?version=2023-02-21', json=payload_scoring,
            headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        prediction = response_scoring.json()
        print(prediction)
        pred = prediction["predictions"][0]['values'][0][0]
        print(pred)

        if int(pred) == 0:
            pred = "Passengers have satisfies the Airline Service"
        else:
            pred = "Passengers have neutral or dissatisfied the Airline Service"

        print("hello",pred)
        
    return render_template('prediction.html', prediction_text=pred)
    
      


if __name__=='__main__':
    app.run(debug=True)