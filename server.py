from flask import Flask
from user_blueprint import user
from dish_blueprint import dish
from restaurant_blueprint import restaurant
from booking_blueprint import booking

app = Flask(__name__)
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(dish, url_prefix="/dish")
app.register_blueprint(restaurant, url_prefix="/restaurant")
app.register_blueprint(booking, url_prefix="/booking")


@app.route('/')
def home():
    return "Welcome to the homepage"
