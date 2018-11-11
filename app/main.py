#! /usr/bin/env python3 

from flask import Flask, request, make_response, jsonify

import os
import json
import pandas as pd

def load_df(path):
    return pd.read_csv(path)

def make_fulliment(data):
    if type(data) != str:
        data = str(data)

    return jsonify({
        "fulfillmentText": data
    })

def set_to_string(s):
    if type(s) == set:
        s = list(s)

    if type(s) != list:
        s = list(s)

    return ", ".join(sorted(s))

def query_cities(city=None):
    column = "CITY"
    avaliable = set(df_data[column].values)

    if city is None or city == "":
        template = "Here is all the cities avaliable: {}"
        return template.format(set_to_string(avaliable))

    city = city[0].upper() + city.lower()[1:]
    if city not in avaliable:
        template = "Information for {} is not avaliable! Here is all the cities avaliable: {}"

        return template.format(city, set_to_string(avaliable))

    return df_data.loc[df_data[column] == city]

def query_range_in_city(price_min, price_max, city):
    df_city = query_cities(city)

    df_result = df_city[df_city["PRICE"].between(price_min, price_max)]

    return df_result

def present_price(df):
    template = "Good! I have found {} house(s) avalible here! What's the range of price you are looking for? The total price ranges from {} to {}"
    
    num_houses = df.shape[0]

    price_min = df["PRICE"].min(axis=0)
    price_max = df["PRICE"].max(axis=0)

    return template.format(num_houses, price_min, price_max)

def present_single_house(df):
    template = "{} with {} square feet, costs ${}, built in {}"
    return template.format(df["ADDRESS"], df["SQUARE FEET"], df["PRICE"], int(df["YEAR BUILT"]))

def show_all():
    """
    List all houses info
    1. number of avaliable houses
    2. List attributes
    """
    avaliable_columns = set(['CITY', 'PRICE', 'SQUARE FEET', 'YEAR BUILT'])

    # template for response
    template_response = "Hello! There are currently {} houses on list. Their avaliable attributes are: {}. Which city are you interested in?"

    # convert columns into string
    str_columns = set_to_string(avaliable_columns)

    # numbe of houses listed
    total_num = df_data.shape[0]

    return template_response.format(total_num, str_columns)

def show_city(parameters):
    city = parameters["geo-city"]
    result = query_cities(city)

    if type(result) == str:
        return result

    result = present_price(result)

    template = "{}"
    return template.format(result)

def show_within_price(parameters, context):
    city = context["parameters"]["geo-city"]
    numbers = parameters["number"]

    price_min, price_max = numbers[0], numbers[1]

    df_result = query_range_in_city(price_min, price_max, city)
    n = df_result.shape[0]

    if n == 0:
        return "There is no match within price range {} to {} in {}. Please try another prices".format(price_min, price_max, city)

    template = "I have found {} houses within price range {} to {} in {}. Do you want to see them or check another price range?"

    return template.format(df_result.shape[0], price_min, price_max, city)

def list_house(parameters, context):
    prices = context["parameters"]["number"]
    city = context["parameters"]["geo-city"]

    df_result = query_range_in_city(prices[0], prices[1], city)

    result = []
    for index, row in df_result.iterrows():
        result.append(present_single_house(row))

    template = "They are:\n{}\nDo you want to save them?"

    tmp_str = ""
    for i, each in enumerate(result):
        tmp_str += "#{}. {}\n".format(i, each)

    return template.format(tmp_str)

def dispatch(intent):
    table = {
        "welcome - yes": show_all,
        "show_all": show_all,
        "show_all - city": show_city,
        "show_all - city - price": show_within_price,
        "list_house": list_house
    }

    return table[intent]


# Create app
app = Flask(__name__)

# Load data
path_data = "./houses.csv"
path_data = os.path.abspath(path_data)
df_data = load_df(path_data)

@app.route("/", methods=["POST", "GET"])
def main_entry():
    if request.method == "GET":
        return jsonify({'fulfillmentText': "use POST instead!"})

    request_body = request.data
    if len(request_body) == 0:
        return make_fulliment("Some thing went wrong! Emtpy request received!")

    request_body = json.loads(request_body)

    # get intent name
    intent = request_body["queryResult"]["intent"]["displayName"]

    # get the function to handle this intent
    handler = dispatch(intent)
    # execute the intent
    parameters = request_body["queryResult"]["parameters"]
    context = None

    if "outputContexts" in request_body["queryResult"]:
        context = request_body["queryResult"]["outputContexts"][0]

    result = handler(parameters, context)

    return make_fulliment(result)

   
if __name__ == "__main__":
    app.run()

