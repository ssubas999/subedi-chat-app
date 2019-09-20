import * as React from 'react';
import { Button } from './Button';
import { Socket } from './Socket';

export class Content extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            'messages': []
        };
        this.componentDidMount = this.componentDidMount.bind(this);
    }
    
    componentDidMount(){
        Socket.on('message received', (data) => {this.setState({'server_sent_name': data['user_name'], 'server_sent_message': data['user_message']})});
        console.log('Lets see:', this.state);
    }
    
    render() {
        let final_message = this.state.server_sent_message;
        let final_name = this.state.server_sent_name;
        
        return (
            <div>
                <header className="main-nav">
                    <div className="container">
                        <div>
                            <h4><a href="https://www.subassubedi.com/" target="_blank">About</a></h4>
                        </div>
                        <div>
                            <h4><a href="https://www.subassubedi.com/" target="_blank">Tech</a></h4>
                        </div>
                        <div>
                            <h4><a href="https://www.subassubedi.com/" target="_blank">Source Code</a></h4>
                        </div>
                    </div>
                </header>

                <section className="chat-app">
                    <div className="container">
                        <h4 className="welcome-text">Welcome to Subedi's Chat-app!</h4>
                        <div className="message-log">
                            <div className="message-block">
                                <h5 className="user-name">User1</h5>
                                <p className="user-message">Hi everyone, good morning!</p>
                            </div>
                            <div className="message-block">
                                <h5 className="user-name">User2</h5>
                                <p className="user-message">Hello, is anybody having any problem with the project?!</p>
                            </div>
                            <div className="message-block">
                                <h5 className="user-name">User3</h5>
                                <p className="user-message">Better not to talk about it</p>
                            </div>
                            <div className="message-block">
                                <h5 className="user-name">User4</h5>
                                <p className="user-message">Yes, sure!</p>
                            </div>
                            <div className="message-block">
                                <h5 className="user-name">User5</h5>
                                <p className="user-message">You guys are crazy.</p>
                            </div>
                            <div className="message-block">
                                <h5 className="user-name"> {final_name} </h5>
                                <p className="user-message"> {final_message} </p>
                            </div>
                        </div>
                        
                        <div>
                            <Button />
                        </div>
                        
                    </div>
                </section>
            </div>
        );
    }
}