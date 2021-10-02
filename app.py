import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

## Version Page
@app.route('/')
def index():
    return "PlantGraph v0.1 - please submit a request via QR code."

## Graph data from qr code. Import data, and place in a pandas df
@app.route('/graph')
def data():
    device_id = request.args.get('device_id', default = 'Null', type = str)
    device_data = request.args.get('device_data', default = 'Null', type = str)
    sample_freq = request.args.get('sample_freq', default = 'H', type = str)

    ## Invalid data results in an error, need to validate URI data before running.
    if device_data == 'Null':
        return 'Please retry. No data was attached to your request.'

    elif len(device_data) % 5 != 0:
        return 'Data validation error. The data you submitted was incorrectly formatted.'

    else:
        split_data = []
        n = 5
        for index in range(0, len(device_data), n):
            split_data.append(device_data[index : index + n])

        num_points = len(split_data)
        
        temperature = list(map(int, [num[:2] for num in split_data]))
        moisture = list(map(int, [num[2:4] for num in split_data]))
        light = list(map(int, [num[4] for num in split_data]))
    
        #def timeRange(r1, r2):
        #    return list(range(r1, r2+1))

        #r1, r2 = 1, len(split_data)

        #hour = list(map(str, timeRange(r1, r2)))

        days_passed = num_points / 24
        start_date = pd.to_datetime("today") - pd.Timedelta("{}. day".format(days_passed))

        date = list((map(str, pd.date_range(start_date, periods=num_points, freq=sample_freq))))

        graph_data = pd.DataFrame(
        {
        "Temperature": temperature,
        "Moisture": moisture,
        "Light": light,
        "Date": date
        }
        )

        # Some kind of conditional label genarator is needed. Switch to only including date on 00:00
        # if Date == 00:00 then Label = Date
        # else Label = " "

        graph_data["Date"] = graph_data["Date"].str.split(expand=True)

        temp_legend = 'Temperature'
        temp_label = graph_data['Date']
        temp_values = graph_data['Temperature']

        mos_legend = 'Moisture'
        mos_label = graph_data['Date']
        mos_values = graph_data['Moisture']

        light_legend = 'Day/Night'
        light_label = graph_data['Date']
        light_values = graph_data['Light']
    
        return render_template('graph.html',
                           temp_values=temp_values, temp_label=temp_label, temp_legend=temp_legend,
                           mos_values=mos_values, mos_label=mos_label, mos_legend=mos_legend,
                           light_values=light_values, light_label=light_label, light_legend=light_legend,
                           device_id=device_id, sample_freq=sample_freq, num_points=num_points)

if __name__ == '__main__':
    app.run(debug=True)

## Functions for temp, mos, and day/night cycle, summary stats, export data, and share data. 