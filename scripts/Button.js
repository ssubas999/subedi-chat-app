import * as React from 'react';
import { GoogleLogin } from 'react-google-login';
import { GoogleLogout } from 'react-google-login';
import { Socket } from './Socket';

/* global gapi */

let active_user_count = 0;
let signedin = false;
const responseGoogle = (response) => {
    console.log("Hey, I am from Button.js")
    console.log("*************");
    
    let auth = gapi.auth2.getAuthInstance();
    let user = auth.currentUser.get();
    if (user.isSignedIn()) {
        active_user_count = active_user_count + 1
        signedin = true;
        console.log("Is user signed in:",signedin)
        console.log("google token:  " + user.getAuthResponse().id_token);
        Socket.emit('google token', {
            'google_user_token': user.getAuthResponse().id_token
        });
    }
}

const logout = (response) => {
    signedin = false;
    active_user_count = active_user_count-1;
    console.log("User just got logged out.")
}


export class Button extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user_message: ''
        };
        
        this.handleChangeMessage = this.handleChangeMessage.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.canBeClicked = this.canBeClicked.bind(this);
    }
    
    handleSubmit(event){
        event.preventDefault();
        //  *** user-message and user_name is sent from client to server ***
        Socket.emit('new message', {
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
    
    
    canBeClicked() {
    // In order the disable the submit button when there no no input
    const {user_message} = this.state;
    return user_message.length > 0 && signedin;
    }
    
    render() {
        let isEnabled = this.canBeClicked();
        return (
            <div>
                <form className = "enter-chat" onSubmit = {this.handleSubmit}>
                    <div>
                        {signedin == false ? (
                            <GoogleLogin
                                clientId="641650714654-3nvhsfpcnhgiljvfrhj70f7idk3uv0gi.apps.googleusercontent.com"
                                buttonText="Log in with Google"
                                onSuccess={responseGoogle}
                                onFailure={responseGoogle}
                                cookiePolicy={'single_host_origin'}
                                className = "google-login-button"
                            />
                        ) : (
                            <GoogleLogout 
                                clientId="641650714654-3nvhsfpcnhgiljvfrhj70f7idk3uv0gi.apps.googleusercontent.com"
                                buttonText="Logout"
                                onLogoutSuccess={logout}
                            >
                            </GoogleLogout>
                        )}
                    </div>
        
                    <div className = "connected-users">
                        <h5>Active Users: { active_user_count }</h5>
                    </div>
                </form>
                
                <form className = "reply-area" onSubmit = {this.handleSubmit}>
                    <div>
                        <textarea className="type-box" cols="50" rows="2" placeholder = "Type a message..." value = {this.state.user_message} onChange = {this.handleChangeMessage}></textarea>
                    </div>
                    <div>
                        <button disabled = {!isEnabled}>Send</button>
                    </div>
                </form>
            </div>
        );
    }
}