from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
import csv
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

STARS = [('⭐(1 Star)', '⭐(1 Star)'), ('⭐⭐(2 Star)', '⭐⭐(2 Star)'), ('⭐⭐⭐(3 Star)',
                                                                    '⭐⭐⭐(3 Star)'), ('⭐⭐⭐⭐(4 Star)', '⭐⭐⭐⭐(4 Star)'), ('⭐⭐⭐⭐⭐(5 Star)', '⭐⭐⭐⭐⭐(5 Star)')]
# create a list of tuples for the select field with antena strength
WIFI_STRENGTH = [('📶(1)', '📶(1)'), ('📶📶(2)', '📶📶(2)'), ('📶📶📶(3)',
                                                        '📶📶📶(3)'), ('📶📶📶📶(4)', '📶📶📶📶(4)'), ('📶📶📶📶📶(5)', '📶📶📶📶📶(5)')]


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField(
        'Cafe Location on Google Maps(URL)', validators=[DataRequired()])
    cafe_open_time = TimeField(
        'Opening Time e.g. 8AM', validators=[DataRequired()])
    cafe_close_time = TimeField(
        'Closing Time e.g. 5:30PM', validators=[DataRequired()])
    cafe_coffee_rating = SelectField(
        u'Coffee Rating', choices=STARS, validators=[DataRequired()])
    cafe_wifi_rating = SelectField(
        'Wifi Strength Rating', choices=WIFI_STRENGTH, validators=[DataRequired()])
    cafe_power_rating = SelectField('Power Socket Availability', choices=[
                                    ('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    submit = SubmitField('Submit')

# all Flask routes below


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        validated_cafe_name = form.cafe_name.data
        validated_cafe_location = form.cafe_location.data
        validated_cafe_open_time = form.cafe_open_time.data.strftime(
            "%I:%M %p")
        validated_cafe_close_time = form.cafe_close_time.data.strftime(
            "%I:%M %p")
        validated_cafe_cooffee_rating = form.cafe_coffee_rating.data
        validated_cafe_wifi_rating = form.cafe_wifi_rating.data
        validated_cafe_power_rating = form.cafe_power_rating.data
        # print(validated_cafe_open_time)
        # Make the form write a new row into cafe-data.csv

        with open('cafe-data.csv', 'a', newline='', encoding="utf8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([validated_cafe_name, validated_cafe_location, validated_cafe_open_time, validated_cafe_close_time,
                                validated_cafe_cooffee_rating, validated_cafe_wifi_rating, validated_cafe_power_rating])
        # with   if form.validate_on_submit()

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
