import mysql.connector
import uuid
import datetime
from flask import Flask,make_response, render_template,jsonify, Blueprint, abort, request
from database import get_connection, load_application,load_application_id

taskResultAPI = Blueprint('results', __name__)

@taskResultAPI.route('/<taskId>')
def get_results(taskId):
    #get the database connection
    cnx = get_connection()

    #Get Data
    cursor = cnx.cursor()
    query = ("SELECT * from `HumanTaskService`.`TaskResults` where TaskId="+str(taskId))
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    #Build result
    tasks = []
    if (len(rows) > 0):
        #get application
        application = load_application_id(rows[0][4])
        if application == None:
            return make_response(jsonify( { 'error': 'Application not found' } ), 404)

        #build result
        for task in rows:
            taskResult = {
                "id":task[0],
                "userId": task[1],
                "result": task[2],
                "finishDate": task[3],
                "applicationNumber": application['magicNumber'],
                "taskId":taskId
            }
            tasks.append(taskResult)

    return jsonify(TaskResults=tasks),200

# resolve an task
@taskResultAPI.route('/',methods=['POST'])
def resolve_task():
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
        command = ("INSERT INTO `HumanTaskService`.`TaskResults` (`UserId`, `Result`, `FinishDate`, `ApplicationId`, `TaskId`) VALUES (%s, %s, %s, %s, %s)")
        #TODO Get the number of copies from application, if not avaliable in object
        data_command = (request.json['userId'],request.json['result'],datetime.datetime.now(),application['id'],request.json['taskId'])
        cursor.execute(command,data_command)
        cnx.commit()
    except mysql.connector.Error as err:
        abort(400) #invalid parameters
    
    #return the new object
    task_id = cursor.lastrowid

    #TODO: Check datetime format
    return jsonify(id= task_id,
        applicationNumber= request.json['applicationNumber'],
        userId= request.json['userId'],
        taskId= request.json['taskId'],
        result= request.json['result'],
        finishDate= datetime.datetime.now()), 201