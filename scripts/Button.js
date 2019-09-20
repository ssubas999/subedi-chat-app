import * as React from 'react';

import { Socket } from './Socket';

export class Button extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user_name: '',
            user_message: ''
        };
        this.handleChangeName = this.handleChangeName.bind(this);
        this.handleChangeMessage = this.handleChangeMessage.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    
    handleSubmit(event){
        event.preventDefault();
    
        // this is a local variable so we don't need to initialize in the constructor
        // let random = Math.floor(Math.random() * 100);
        // console.log('Generated a random number: ', random);
        // let m_text = this.state.user_message;
        Socket.emit('new message', {
            'user_name': this.state.user_name,
            'user_message': this.state.user_message
        });
        console.log('Sent a message to server!',this);
        console.log('User Name:', this.state.user_name);
        console.log('User Message:', this.state.user_message);
    }
    
    handleChangeMessage(event) {
        this.setState({user_message: event.target.value});
        console.log('user_message', event.target.value);
    }
    handleChangeName(event) {
        this.setState({user_name: event.target.value});
        console.log('user_name', event.target.value);
    }

    render() {
        return (
            <div>
                <form className = "enter-chat" onSubmit = {this.handleSubmit}>
                    <div className = "enter-chat-input">
                        <input type="text" placeholder="Enter your name" name="name" value = {this.state.user_name} onChange = {this.handleChangeName}></input>
                    </div>
                    <div className = "connected-users">
                        <h5>Connected users: 5</h5>
                    </div>
                </form>
                
                <form className = "reply-area" onSubmit = {this.handleSubmit}>
                    <div>
                        <textarea className="type-box" cols="50" rows="3" placeholder = "Type a message..." value = {this.state.user_message} onChange = {this.handleChangeMessage}></textarea>
                    </div>
                    <div>
                        <button ><i className="fas fa-arrow-circle-up fa-3x"></i> </button>
                    </div>
                </form>
            </div>
        );
    }
}