import os, flask, flask_socketio, flask_sqlalchemy, models
# ********
# Importing library for parsing and validation of URIs (RFC 3986)
from rfc3987 import parse

from google.oauth2 import id_token
from google.auth.transport import requests
# ********

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
    
    
# Function to check in the input is an url.
def isURL(string):
    try:
        parse(string, rule='URI')
        print("Got an URL:", parse(string, rule='URI'))
        message = "Got an URL"
    except:
        print("Not an URL.")
        message = "Not an url"
    return message
print(isURL('Subas Subedi'))



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

# Initializing a varible to store imageurl inside function below
server_received_imageurl = ""

# *** Server received the google 'id_token' sent from client (GoogleSignin.js)
@socketio.on('google token')
def on_google_token_id(token):
    print ("Got an event for GOOGLE TOKEN ID: "+ str(token))
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        # To validate an ID token in Python, using the verify_oauth2_token function
        CLIENT_ID = '641650714654-3nvhsfpcnhgiljvfrhj70f7idk3uv0gi.apps.googleusercontent.com'
        idinfo = id_token.verify_oauth2_token(token['google_user_token'], requests.Request(), CLIENT_ID)
    
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
    
        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        
        # In order to insert on database and send it to client later + making global variable
        global server_received_imageurl
        server_received_imageurl = idinfo['picture']
        
        print(idinfo)
        print("************")
        print("Name: "+ idinfo['name'])
        print("Imageurl: "+ idinfo['picture'])
        print("Email: "+ idinfo['email'])
        print("************")
    
    except ValueError:
        # Invalid token
        print("Invalid token")

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
    print("Server received imageurl:", server_received_imageurl)
    
    message = models.Message(server_received_name, server_received_message, server_received_imageurl)
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
        image = s.user_image
        
        chat_list = [name, message, image]
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