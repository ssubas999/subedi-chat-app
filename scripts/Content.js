import * as React from 'react';
import { Socket } from './Socket';

export class Content extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            'user_name' : 'User1',
            'user_message' : 'My new message'
        };
    }
    
    componentDidMount(){
        Socket.on('update', (user_message) => {this.setState(user_message)});
    }
    
    render() {
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
                                <h5 className="user-name"> {this.state.user_name} </h5>
                                <p className="user-message"> {this.state.user_message} </p>
                            </div>
                        </div>
                        <div className = "count-login">
                            <form className = "enter-chat">
                                <div className = "enter-chat-input">
                                    <input type="text" placeholder="Enter name" name="name"></input>
                                </div>
                                <div className = "enter-chat-button">
                                    <button> Enter Chat </button>
                                </div>
                            </form>
                            <div className = "connected-users">
                                <h5>Connected users: 5</h5>
                            </div>
                        </div>

                        <div className="reply-area">
                            <div>
                                <textarea className="type-box" name="" id="" cols="50" rows="3" placeholder = "Type a message..."></textarea>
                            </div>
                            <div>
                                <button ><i className="fas fa-arrow-circle-up fa-3x"></i> </button>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        );
    }
}