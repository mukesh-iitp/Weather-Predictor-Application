from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__, template_folder='templates')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])

def predict():
    # retrieve form data
    TMIN = request.form['TMIN']
    TMAX = request.form['TMAX']
    WIND_MIN = request.form['WIND_MIN(kph)']
    WIND_MAX = request.form['WIND_MAX(kph)']
    PRCP = request.form['PRCP']
    HUMIDITY = request.form["HUMIDITY"]
    

    # create a DataFrame using the input values
    input_df = pd.DataFrame({'PRCP': [float(PRCP)], 
                             'TMAX': [float(TMAX)], 
                             'TMIN': [float(TMIN)], 
                             'WIND_MAX(kph)': [float(WIND_MAX)],
                             'WIND_MIN(kph)': [float(WIND_MIN)], 
                             'HUMIDITY': [float(HUMIDITY)]})
    
    # load the model
    with open('pipe.pkl', 'rb') as f:
        model = pickle.load(f)

    # do model prediction
    prediction = model.predict(input_df)
    # load the model
    

    # convert prediction to weather condition
    if prediction == 0:
        weather = 'Clear'
    elif prediction == 1:
        weather = 'Partially cloudy'
    elif prediction == 2:
        weather = 'Rain, Partially cloudy'
    elif prediction == 3:
        weather = 'Rain, Cloudy'
    elif prediction == 4:
        weather = 'Rain'
    else:
        weather = 'Cloudy'
    
    # display message
    message = f'The predicted weather for the provided inputs is: {weather}. '
    if weather == 'Clear':
        message += ' Sunny Day! Do not go out in the heat of noon.'
    elif weather == 'Partially Cloudy':
        message += ' Awesome! The weather is favorable out there.'
    elif weather == 'Rain, Partially cloudy':
        message += ' Rain expected anytime! Carry Umbrella.'
    elif weather == 'Rain, Cloudy':
        message += ' Its Rainy and Cloudy Weather, Stay indoors and avoid going out if possible.'
    elif weather == 'Rain':
        message += ' Its raining across the areas.'
    else:
        message += 'Cloudy Weather! Carry Umbrella or Stay indoors if possible'


    thanking = "Thank you for using this application. Come again!"   
    return  render_template("index.html", message=message, thanking = thanking) 
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



