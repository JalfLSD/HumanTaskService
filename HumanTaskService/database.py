import mysql.connector

# Return the database connection
def get_connection():
    try:
        cnx = mysql.connector.connect(user='root', password='hard99',
                                host='localhost',
                                database='humantaskservice');
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            abort (203)        
        else:
            abort(500)

    return cnx;


#Load an application
def load_application(guid):
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
        application = {
            'id':rows[0][0],
            'ownerUserId':rows[0][1],
            'name':rows[0][2],
            'description':rows[0][3],
            'taskCopies':rows[0][4],
            'taskScheduler':rows[0][5],
            'magicNumber':rows[0][6]
        }
        return application

    #fail
    return None

#Load an application
def load_application_id(id):
     #get the database connection
    cnx = get_connection()

    #Get Data
    cursor = cnx.cursor()
    query = ("SELECT * from `HumanTaskService`.`Applications` WHERE id='" + str(id) + "'")
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    cnx.close()

    #Build result
    if (len(rows) > 0):
        application = {
            'id':rows[0][0],
            'ownerUserId':rows[0][1],
            'name':rows[0][2],
            'description':rows[0][3],
            'taskCopies':rows[0][4],
            'taskScheduler':rows[0][5],
            'magicNumber':rows[0][6]
        }
        return application

    #fail
    return None