import os, flask, flask_socketio, flask_sqlalchemy, models

app = flask.Flask(__name__)

# Variable that keeps track of active user count
user_count = 0

socketio = flask_socketio.SocketIO(app)

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
    print ("Got an event for new message with data: "+ str(data))
    server_received_name = data['user_name']
    server_received_message = data['user_message']
    
    # Checking response for the bot.
    if server_received_message.startswith("!!"):
        server_received_name = chatBot(server_received_name, server_received_message)[0]
        server_received_message = chatBot(server_received_name, server_received_message)[1]
    
    # Insert data to the database
    print("Server received name: ", server_received_name);
    print("Server received message: ", server_received_message);
    
    message = models.Message(server_received_name, server_received_message)
    models.db.session.add(message)
    models.db.session.commit()
    print("Record inserted successfully")
    
    # Retrieving the data from database
    stored_messages = models.Message.query.all()
    new_list = []
    print("Stored Messages:", stored_messages)
    
    for s in stored_messages:
        name = s.user_name
        message = s.user_message
        
        chat_list = [name, message]
        new_list.append(chat_list)
        
    print("New List: ", new_list)
    print("Active online user: ", user_count)
    
    # *** Active user count sent from server to every client ***
    socketio.emit('user count', {'active_user_count': user_count});

    # *** Lists of username and message sent from server to every client ***
    socketio.emit('message received', {'messages_list': new_list});



if __name__ =='__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )