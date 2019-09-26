# Project 2 Checkpoint 1

### A public online Chat-Application

This program is a simple public online chat application where multiple people can send and reply to each other's messages (very similar to group chat feature in modern chat apps).



### Built With:
- React- Fronted end
- Python- Serverside
-	Flask- Microframework
- PostgreSQL- Database
- WebSocket (Socket.io)- For full duplex communication channel
- Additional libraries- flask_socketio, flask_sqlalchemy, psycopg2



1. This is a complete web application written in cloud ( with AWS-cloud9 IDE).
2. I used React and Vanilla JavaScript as the fronted-end programming language and Python as the server-side programming language. The client (a browser) communicates with server via Websocket (Socket.io in this case) and stores the data sent from client to server on database (PostgreSQL).

### Encountered Issues:
- As I was using react for the first time, it was quite confusing at the begining just to understand how it works.
- Creating a component on react was quite frustrating in some cases. However, I created multiple components sucessfully for this project.
- Took a time to understand the tree to components.
- Websocket was the first technology that I have worked with that can have two-way communication over single TCP. Took long time to understand how does it exactly works.
- I think PostgreSQL is quite problematic on iteself and used psycopg2 library for ease. However, psycopg2 created more complexity than expected. Which is still an issue.


### Known Problems:
Even though I don't have any known problems while running on AWS, this application doesn't work as expected after deploying on heroku. I Tried to deploy on heroku more than 5 times with different configuration but didn't solve the issue. I think it is the problem with certain version of psycopg2 library that I used to acces PostgreSQL. 
