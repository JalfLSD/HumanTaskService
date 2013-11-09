import mysql.connector
import uuid
from flask import Flask,make_response, render_template,jsonify, Blueprint, abort, request

applicationAPI = Blueprint('applications', __name__)

from database import get_connection

# Get all applications
@applicationAPI.route('/')
def get_applications():
    #get the database connection
    cnx = get_connection()

    #Get Data
    cursor = cnx.cursor()
    query = ("SELECT * from `HumanTaskService`.`Applications` ORDER BY Name")
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    #Build result
    applications = []
    if (len(rows) > 0):
        for application in rows:
            applications.append(application)

    return jsonify(Applications=applications),200


# Get an Application by id
@applicationAPI.route('/<guid>')
def get_application(guid):
    #get the database connection
    cnx = get_connection()

    #Get Data
    cursor = cnx.cursor()
    query = ("SELECT * from `HumanTaskService`.`Applications` WHERE MagicNumber='" + str(guid) + "'")
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    cnx.close()

    #Build result
    if (len(rows) > 0):
        application = rows[0]
        return jsonify(ownerUserId=application[1],
                name=application[2],
                description=application[3],
                taskCopies=application[4],
                taskScheduler=application[5],
                magicNumber=application[6]),200

    abort(404) #not found


# add a new application
@applicationAPI.route('/',methods=['POST'])
def add_application():
    if not request.json:
        abort(400)

    #get the database connection
    cnx = get_connection()

    #Add Data
    #TODO: Check parameters
    try:
        #create the new UUID
        guid = uuid.uuid1()
        cursor = cnx.cursor()
        command = ("INSERT INTO `HumanTaskService`.`Applications` (`OwnerUserId`, `Name`, `Description`, `TaskCopies`, `TaskScheduler`,`MagicNumber` ) VALUES (%s, %s, %s, %s, %s, %s)")
        data_command = (request.json['ownerUserId'],request.json['name'],request.json['description'],request.json['taskCopies'],request.json['taskScheduler'],str(guid))
        cursor.execute(command,data_command)
        cnx.commit()
    except mysql.connector.Error as err:
        abort(400) #invalid parameters
    
    #return the new object
    app_id = cursor.lastrowid

    application = {
        'id': app_id,
        'ownerUserId': request.json['ownerUserId'],
        'name': request.json['name'],
        'description': request.json['description'],
        'taskCopies': request.json['taskCopies'],
        'taskScheduler': request.json['taskScheduler'],
        'magicNumber': str(guid)
    }

    return jsonify({ 'application': application }), 201


# delete an application
@applicationAPI.route('/<guid>',methods=['DELETE'])
def delete_application(guid):  
    #get the database connection
    cnx = get_connection()

    #Remove Data
    try:
        cursor = cnx.cursor()
        command = ("DELETE FROM `HumanTaskService`.`Applications` WHERE MagicNumber='" + str(guid)+"'")
        cursor.execute(command)
        cnx.commit()
    except mysql.connector.Error as err:
        abort(400) #invalid parameters
    
    if (cursor.rowcount == 0):
        abort(404)  #not found

    #
    #TODO: remove all tasks, etc
    #

    return jsonify({ 'result': True }), 200
