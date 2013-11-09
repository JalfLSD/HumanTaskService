import mysql.connector
from flask import Flask,make_response, render_template,jsonify, Blueprint
from applicationAPI import applicationAPI
from taskAPI import taskAPI
from taskResultAPI import taskResultAPI
from database import get_connection

app = Flask(__name__)

#blueprints
app.register_blueprint(taskAPI, url_prefix='/tasks')
app.register_blueprint(taskResultAPI, url_prefix='/results')
app.register_blueprint(applicationAPI, url_prefix='/applications')

# generic 'not found' error
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

# generic 'bad request' error
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Invalid parameters' } ), 400)

# generic 'non-autorized' error
@app.errorhandler(203)
def not_found(error):
    return make_response(jsonify( { 'error': 'User non-autorized' } ), 203)

# generic 'internal error' error
@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify( { 'error': 'Internal server error' } ), 500)


#chek if the database is accessible
@app.route('/checkdbconnection')
def check_connection():
    #get the database connection
    cnx = get_connection();
    #Get Data
    cursor = cnx.cursor();
    query = ("SELECT count(*) FROM users");
    cursor.execute(query);
    rows = cursor.fetchall();

    cursor.close();
    cnx.close();
    return "database ok!"

# Run application
if __name__ == '__main__':
    app.debug = True
    app.run()