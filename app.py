import os, flask, flask_socketio, flask_sqlalchemy, random
from requests import *
import models
# ********
# Importing library for parsing and validation of URIs (RFC 3986)
from rfc3987 import parse

from google.oauth2 import id_token
from google.auth.transport import requests
# ********

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)

@app.route('/')
def hello():
    return flask.render_template('index.html')
    
@socketio.on('connect')
def on_connect():
    print('Someone connected!')


@socketio.on('disconnect')
def on_disconnect():
    print('Someone disconnected!')
    
    
# Function to check in the input is an url.
def isURL(string):
    url_message = ""
    nonurl_message = ""
    try:
        parsed_message = parse(string, rule='URI')
        # checked_message = "<a href=" + string + "></a>"
        url_message = string
        print("Got an URL:", url_message)
    except:
        nonurl_message = string
        print("Not an URL: ", nonurl_message)
    return url_message, nonurl_message

print("************")
print("Function print: ", isURL("https://www.subassubedi.com/"))
print("************")


# For Pokemon api
def getJson(url):
    # Requesting information using 'requests'
    response = get(url)
    json_body = response.json()
    return json_body

# Making bot-responses
def chatBot(name, message):
    poke_url = "https://pokeapi.co/api/v2/pokemon/ditto/"
    json_response = getJson(poke_url)
    # print(json_response)
    abilities = json_response["abilities"]
    abilities_list = []
    for i in range(len(abilities)):
        abilities_list.append(abilities[i]["ability"]["name"])
    # print(abilities_list)
    random_ability = random.choice(abilities_list)
    # print(random_ability)
    
    base_experience = json_response["base_experience"]
    # print(base_experience)
    
    poke_height = json_response["height"]
    # print(poke_height)
    
    poke_id = json_response["id"]
    # print(poke_id)
    
    name = "Sam(Chat-Bot)"
    if message[:8] == "!! ditto":
        if message == "!! ditto ability":
            message = "Ditto's one of the ability is " + random_ability + "."
        elif message == "!! ditto base experience":
            message = "Ditto's base experience is " + str(base_experience) + "."
        elif message == "!! ditto height":
            message = "Ditto's height is " + str(poke_height) + "."
        elif message == "!! ditto id":
            message = "Ditto's id is " + str(poke_id) + "."
        else:
            message = "Umm! Looks like you know more about ditto than I do. Sorry, this is out of my knowledge."
    elif message == "!! about":
        message = "Hi, my name is Sam. I am a chat-bot created by Subas."
    elif message == "!! help":
        message = "Commands: '!! about','!! say something','!! source','!! developer','!! ditto ability','!! ditto id','!! ditto height'."
    elif message == "!! say something":
        message = "Hi, how are you feeling today?"
    elif message == "!! source":
        message = "To find the source code of this web-app, visit the 'Source Code' tab at the top the page."
    elif message == "!! developer":
        message = "This app is created by Subas Subedi. Want to know more about him? Visit www.subassubedi.com."
    else:
        message = "Sorry! I am unable to answer this question. Type '!! sam' to see the lists of commands."
    return name, message

# Initializing a varible to store imageurl inside function below
server_received_imageurl = ""
server_received_name = ""

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
        
        global server_received_name
        server_received_name = idinfo['name']
        
        
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
    # server_received_name = data['user_name']
    server_received_message = data['user_message']
    
    # Checking response for the bot.
    if server_received_message[:2] == "!!":
        global server_received_name
        server_received_name = chatBot(server_received_name, server_received_message)[0]
        server_received_message = chatBot(server_received_name, server_received_message)[1]
        # server_received_imageurl = "/static/images/chatbot.png"
        
    
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
        
        # ********
        url = isURL(message)[0]
        non_url = isURL(message)[1]
        # ********
        
        # chat_list = [name, message, image]
        chat_list = [name, url, non_url, image]
        new_list.append(chat_list)
        
    print("New List: ", new_list)

    # *** Lists of username and message sent from server to every client ***
    socketio.emit('message received', {'messages_list': new_list});



if __name__ =='__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )