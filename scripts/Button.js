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
        this.canBeClicked = this.canBeClicked.bind(this);
    }
    
    handleSubmit(event){
        event.preventDefault();
    
        // this is a local variable so we don't need to initialize in the constructor
        // let random = Math.floor(Math.random() * 100);
        // console.log('Generated a random number: ', random);
        // let m_text = this.state.user_message;
        
        //  *** user-message and user_name is sent from client to server ***
        Socket.emit('new message', {
            'user_name': this.state.user_name,
            'user_message': this.state.user_message
        });
        // In order to clear the input field after sending the message.
        this.setState({user_message: ''});
        
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
    
    canBeClicked() {
    // In order the disable the submit button when there no no input
    const {user_name, user_message} = this.state;
    return user_name.length > 0 && user_message.length > 0;
    }
    
    render() {
        let isEnabled = this.canBeClicked();
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
                        <button disabled = {!isEnabled}>Send</button>
                    </div>
                </form>
            </div>
        );
    }
}