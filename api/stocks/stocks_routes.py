########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################

from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db


stocks = Blueprint('stocks', __name__)

# Get all the stocks from the database
@stocks.route('/stocks', methods=['GET'])
def get_stocks():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of stocks
    cursor.execute('SELECT id, product_code, product_name, list_price, category FROM stocks')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@stocks.route('/product/<id>', methods=['GET'])
def get_product_detail (id):

    query = 'SELECT id, product_name, description, list_price, category FROM stocks WHERE id = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)
    

# get the top 5 stocks from the database
@stocks.route('/mostExpensive')
def get_most_pop_stocks():
    cursor = db.get_db().cursor()
    query = '''
        SELECT product_code, product_name, list_price, reorder_level
        FROM stocks
        ORDER BY list_price DESC
        LIMIT 5
    '''
    cursor.execute(query)
    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


@stocks.route('/tenMostExpensive', methods=['GET'])
def get_10_most_expensive_stocks():
    
    query = '''
        SELECT product_code, product_name, list_price, reorder_level
        FROM stocks
        ORDER BY list_price DESC
        LIMIT 10
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)

    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    
    return jsonify(json_data)

@stocks.route('/product', methods=['POST'])
def add_new_product():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['product_name']
    description = the_data['product_description']
    price = the_data['product_price']
    category = the_data['product_category']

    # Constructing the query
    query = 'insert into stocks (product_name, description, category, list_price) values ("'
    query += name + '", "'
    query += description + '", "'
    query += category + '", '
    query += str(price) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

### Get all product categories
@stocks.route('/categories', methods = ['GET'])
def get_all_categories():
    query = '''
        SELECT DISTINCT category AS label, category as value
        FROM stocks
        WHERE category IS NOT NULL
        ORDER BY category
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)

    json_data = []
    # fetch all the column headers and then all the data from the cursor
    column_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()
    # zip headers and data together into dictionary and then append to json data dict.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    
    return jsonify(json_data)

@stocks.route('/product', methods = ['PUT'])
def update_product():
    product_info = request.json
    current_app.logger.info(product_info)

    return "Success"