import os, flask, flask_socketio, flask_sqlalchemy, psycopg2

app = flask.Flask(__name__)
import models

socketio = flask_socketio.SocketIO(app)

# We are going to move this later
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ssubas999:1Maryland1@localhost/postgres'
db = flask_sqlalchemy.SQLAlchemy(app)

@app.route('/')
def hello():
    return flask.render_template('index.html')
    
@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    
@socketio.on('disconnect')
def on_disconnect():
    print('Someone disconnected!')
    
# *** Server received new message event sent by client ***
@socketio.on('new message')
def on_new_message(data):
    print ("Got an event for new message with data: "+ str(data))
    server_received_name = data['user_name']
    server_received_message = data['user_message']
    print(server_received_name, server_received_message)
    # ***************************
    # message = models.Message(server_received_name, server_received_message)
    # models.db.session.add(message)
    # models.db.session.commit()
    
    # messages = models.Message.query.all()
    # print(messages)
    
    # Connect to the database
    con = psycopg2.connect(database="postgres", user="ssubas999", password="1Maryland1", host="127.0.0.1", port="5432")
    print("Database opened successfully")
    
    # Insert data to the database
    cur = con.cursor()
    cur.execute("INSERT INTO Message (user_name, user_message) VALUES (%s, %s)", (server_received_name, server_received_message));
    con.commit()
    print("Record inserted successfully")
    con.close()
    
    # Connect to the database
    con = psycopg2.connect(database="postgres", user="ssubas999", password="1Maryland1", host="127.0.0.1", port="5432")
    print("Database opened successfully")
    
    #Retrieving the data from database
    cur = con.cursor()
    cur.execute("SELECT user_name, user_message from Message")
    rows = cur.fetchall()
    
    for name_message_list in rows:
        # print(name_message_list)
        name = name_message_list[0]
        message = name_message_list[1]
        # print(name)
        # print(message)
        
        
    html = ['<li>' + name + '</li><li>' + message + '</li>' for m in name_message_list]
    messages = '<ul>' + ''.join(html) + '</ul>'
    print(messages)
    # return messages

    # ***************************
    # *** username and message sent from server to every client ***
    socketio.emit('message received', {'user_name': server_received_name, 'user_message': server_received_message});



if __name__ =='__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )