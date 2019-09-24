import os, flask, flask_socketio, flask_sqlalchemy, psycopg2

app = flask.Flask(__name__)
import models

# Variable that keeps track of active user scount
user_count = 0

socketio = flask_socketio.SocketIO(app)

# We are going to move this later
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ssubas999:1Maryland1@localhost/postgres'
# db = flask_sqlalchemy.SQLAlchemy(app)


@app.route('/')
def hello():
    return flask.render_template('index.html')
    
@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    global user_count
    user_count += 1

@socketio.on('disconnect')
def on_disconnect():
    print('Someone disconnected!')
    global user_count
    user_count -= 1
    
# Making bot-responses
def chatBot(name, message):
    if message == "!! about":
        name = "Sam(Chat-Bot)"
        message = "Hi, my name is Sam. I am a chat-bot created by Subas."
        return name, message
    elif message == "!! help":
        name = "Sam(Chat-Bot)"
        message = "To enter the chat, send your first message."
        return name, message
    elif message == "!! say <something>":
        name = "Sam(Chat-Bot)"
        message = "Hi, how are you feeling today?"
        return name, message
    elif message == "!! source":
        name = "Sam(Chat-Bot)"
        message = "To find the source code of this web-app, visit the 'Source Code' tab at the top the page."
        return name, message
    elif message == "!! sam":
        name = "Sam(Chat-Bot)"
        message = "List of commands-'!! about': More about me.'!! help': For help.'!! source': To find the source code of this web-app."
        return name, message
    else:
        name = "Sam(chat-Bot)"
        message = "Sorry! I am unable to answer this question. Type '!! sam' to see the lists of commands."
        return name, message
    
# *** Server received new message event sent by client ***
@socketio.on('new message')
def on_new_message(data):
    # print ("Got an event for new message with data: "+ str(data))
    server_received_name = data['user_name']
    server_received_message = data['user_message']
    
    # Checking response for the bot.
    if server_received_message.startswith("!!"):
        server_received_name = chatBot(server_received_name, server_received_message)[0]
        server_received_message = chatBot(server_received_name, server_received_message)[1]
    
    # ***************************
    # Connect to the postgresql using psycopg2
    con = psycopg2.connect(database="postgres", user="ssubas999", password="1Maryland1", host="127.0.0.1", port="5432")
    print("Database opened successfully")
    
    # Insert data to the database
    cur = con.cursor()
    cur.execute("INSERT INTO Message (user_name, user_message) VALUES (%s, %s)", (server_received_name, server_received_message));
    con.commit()
    print("Record inserted successfully")
    con.close()
    
    # Connect to the database again
    con = psycopg2.connect(database="postgres", user="ssubas999", password="1Maryland1", host="127.0.0.1", port="5432")
    print("Database opened successfully")
    
    # Retrieving the data from database
    cur = con.cursor()
    cur.execute("SELECT user_name, user_message from Message")
    rows = cur.fetchall()
    
    new_list = list(rows)
    # print(new_list)
    for name_message_list in rows:
        name = name_message_list[0]
        message = name_message_list[1]

    print("Active online user: ", user_count)
    
    # *** Active user count sent from server to every client ***
    socketio.emit('user count', {'active_user_count': user_count});
    
    # ***************************
    # *** Lists of username and message sent from server to every client ***
    socketio.emit('message received', {'messages_list': new_list});



if __name__ =='__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )