import os, flask, flask_socketio, flask_sqlalchemy

app = flask.Flask(__name__)
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
    # *** username and message sent from server to every client ***
    socketio.emit('message received', {'server_sent_name': server_received_name,'server_sent_message': server_received_message});

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)