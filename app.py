import os, flask, flask_socketio, flask_sqlalchemy

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

# We are going to move this later
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://purple:purpleisawesome@localhost/postgres'
db = flask_sqlalchemy.SQLAlchemy(app)


@app.route('/')
def hello():
    return flask.render_template('index.html')
    
@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    flask_socketio.emit('update', {
        'user_message': 'Got your connection!'
    })

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)