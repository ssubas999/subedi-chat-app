# Project 2 Checkpoint 2

### A public online Chat-Application + Chat Bot

This program is a simple public online chat application where multiple people can send and reply to each other's messages (very similar to group chat feature in modern chat applications).



### Built With:
- React- Fronted end
- Python- Serverside
- Flask- Microframework
- PostgreSQL- Database
- WebSocket (Socket.io)- For full duplex communication channel
- Additional libraries- flask_socketio, flask_sqlalchemy, psycopg2, requests, rfc3987, google.oauth2



1. This is a complete web application written in cloud ( with AWS-cloud9 IDE).
2. I used React and Vanilla JavaScript as the fronted-end programming language and Python as the server-side programming language. The client (a browser) communicates with server via Websocket (Socket.io in this case) and stores the data sent from client to server on database (PostgreSQL).

3. Encountered Issues:
- It had to spend more than enough time to implement third party authentication (Google Login) because of not having enough experience on react. Finally, I figured it out by placing the callBack function outside of the class.
- I also had a hard time to display the status of login on UI but I fixed if by using conditional rendering.
- One thing that I forgot at begining and tried to fix at last minute was inline rendering but I think I fixed it creatively by adding condition in serverside.
- I think PostgreSQL is quite problematic on iteself and used psycopg2 library for ease. However, psycopg2 created more complexity than expected. I fixed it by completely avoiding use of psycopg2.


### Known Problems:
- One of the issue I am having at this version is that user cannnot send any message of length longer than 120 characters.

If I had would had more time I would have created the entire new database with where I can store messages of any length (I means as allowed by postgresql) so that a current issue would have been fixed.