from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

# Setting up the Flask app
app = Flask(__name__)

# Configuring the database URI
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing the database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Setting up Flask-Restful API
api = Api(app)

# Home Resource
class Home(Resource):
    def get(self):
        response = {"message": "Welcome to the Code Challenge API"} 
        return make_response(response, 200)

api.add_resource(Home, "/")

# Restaurants Resource
class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        my_restaurant_list = [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            }
            for restaurant in restaurants
        ]
        return jsonify(my_restaurant_list), 200

api.add_resource(Restaurants, "/restaurants")

# RestaurantById Resource
class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return restaurant.to_dict(), 200
        else:
            return {"error": "Restaurant not found"}, 404

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        db.session.delete(restaurant)
        db.session.commit()
        return {"message": "Restaurant successfully deleted"}, 204

api.add_resource(RestaurantById, "/restaurants/<int:id>")

# Pizzas Resource
class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()  
        my_pizza_list = [
            {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }
            for pizza in pizzas
        ]
        return jsonify(my_pizza_list), 200

api.add_resource(Pizzas, "/pizzas")

# RestaurantPizzas Resource
class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_pizza = RestaurantPizza(price=data["price"], pizza_id=data["pizza_id"], restaurant_id=data["restaurant_id"])
            db.session.add(new_pizza)
            db.session.commit()
        except ValueError:
            return {"errors": ["validation errors"]}, 400

        return new_pizza.to_dict(), 201

api.add_resource(RestaurantPizzas, "/restaurant_pizzas")

# Running the Flask app
if __name__ == '__main__':
    app.run(port=5555, debug=True)
