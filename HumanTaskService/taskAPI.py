import mysql.connector
import uuid
from flask import Flask,make_response, render_template,jsonify, Blueprint, abort, request
from database import get_connection, load_application

taskAPI = Blueprint('tasks', __name__)

@taskAPI.route('/<appNumber>')
def get_tasks(appNumber):
    #get the database connection
    cnx = get_connection()

     #get application
    application = load_application(appNumber)
    if application == None:
        return make_response(jsonify( { 'error': 'Application not found' } ), 404)

    #Get Data
    cursor = cnx.cursor()
    query = ("SELECT * from `HumanTaskService`.`Tasks` where ApplicationId="+str(application['id']))
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    #Build result
    tasks = []
    if (len(rows) > 0):
        for task in rows:
            taskResult = {
                "id":task[0],
                "applicationNumber": appNumber,
                "params":task[2],
                "copies":task[3]
            }
            tasks.append(taskResult)

    return jsonify(Tasks=tasks),200

# add a new task
@taskAPI.route('/',methods=['POST'])
def add_task():
    if not request.json:
        abort(400)

    #get the database connection
    cnx = get_connection()

    #get application
    application = load_application(request.json['applicationNumber'])
    if application == None:
        return make_response(jsonify( { 'error': 'Application not found' } ), 404)

    #Add Data
    #TODO: Check parameters
    try:               
        cursor = cnx.cursor()
        command = ("INSERT INTO `HumanTaskService`.`Tasks` (`ApplicationId`, `Params`, `Copies`) VALUES (%s, %s, %s)")
        #TODO Get the number of copies from application, if not avaliable in object
        data_command = (application['id'],request.json['params'],request.json['copies'])
        cursor.execute(command,data_command)
        cnx.commit()
    except mysql.connector.Error as err:
        abort(400) #invalid parameters
    
    #return the new object
    task_id = cursor.lastrowid

    task = {
        'id': task_id,
        'applicationNumber': request.json['applicationNumber'],
        'params': request.json['params'],
        'copies': request.json['copies']
    }

    return jsonify({ 'task': task }), 201

# delete an task
@taskAPI.route('/<id>',methods=['DELETE'])
def delete_task(id):  
    #get the database connection
    cnx = get_connection()

    #Remove Data
    try:
        cursor = cnx.cursor()
        command = ("DELETE from `HumanTaskService`.`Tasks` WHERE id='" + str(id)+"'")
        cursor.execute(command)
        cnx.commit()
    except mysql.connector.Error as err:
        abort(400) #invalid parameters
    
    if (cursor.rowcount == 0):
        abort(404)  #not found

    #
    #TODO: remove all tasksruns
    #

    return jsonify({ 'result': True }), 200


#return a new task to the user
@taskAPI.route('/newtask/<user>/<appNumber>')
def get_newtask(user,appNumber):
    #get the database connection
    cnx = get_connection()

    #
    #TODO: Get User
    #


     #get application
    application = load_application(appNumber)
    if application == None:
        return make_response(jsonify( { 'error': 'Application not found' } ), 404)

    #Get Data
    cursor = cnx.cursor()
    #
    #TODO Check the scheduler type
    #

    #Sequencial schedule
    query = ("SELECT * FROM HumanTaskService.Tasks WHERE HumanTaskService.Tasks.ApplicationId = " + str(application['id']) + 
             " AND HumanTaskService.Tasks.id NOT IN (select TaskId from HumanTaskService.TaskResults where HumanTaskService.TaskResults.ApplicationId = " + str(application['id']) + 
             " AND HumanTaskService.TaskResults.UserId = " + str(user) + ") LIMIT 1")
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    #Build result
    if (len(rows) > 0):
        return jsonify(
            id=rows[0][0],
            applicationNumber=appNumber,
            params=rows[0][2],
            copies=rows[0][3]
        ), 200

    #
    #TODO: No more tasks..and now?
    #
    return None