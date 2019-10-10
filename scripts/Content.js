import * as React from 'react';
import { Button } from './Button';
import { GoogleSignin } from './GoogleSignin';
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
        Socket.on('message received', (data) => {this.setState({'messages': data['messages_list']})});
        console.log('Lets see:', this.state);
        console.log(this.state.messages)
    }
    
    render() {
        let final_messages = this.state.messages;
        
        return (
            <div>
                <header className="main-nav">
                    <div className="container">
                        <div>
                            <h4><a href="https://github.com/msu-fa19-cosc458/project2-cp1-susub3" target="_blank">About</a></h4>
                        </div>
                        <div>
                            <h4><a href="https://github.com/msu-fa19-cosc458/project2-cp1-susub3" target="_blank">Tech</a></h4>
                        </div>
                        <div>
                            <h4><a href="https://github.com/msu-fa19-cosc458/project2-cp1-susub3" target="_blank">Source Code</a></h4>
                        </div>
                    </div>
                </header>

                <section className="chat-app">
                    <div className="container">
                        <h4 className="welcome-text">Welcome to Subedi's Chat-app!</h4>
                        <div className="message-log">
                            <div className="message-block">
                                <ul>
                                    <li className = "chatbot">
                                        <h5 className="user-name">Bot</h5>
                                        <p className="user-message">Hi, my name is Sam. I am a chat-bot. Type and send anything if you wish to see the prviouse messages.</p>
                                    </li>
                                    { final_messages.map( name_message =>
                                    <li key = {name_message[0].id} className = "message-with-image">
                                        <img src={name_message[2]} alt = "User Image" className = "user-image"></img>
                                        <div>
                                            <h5 className="user-name"> {name_message[0]}</h5>
                                            <p className="user-message"> {name_message[1]} </p>
                                        </div>
                                    </li> )}
                                </ul>
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