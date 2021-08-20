import { useState } from 'react';
import axios from 'axios';


import '../css/Welcome.css';

axios.defaults.xsrfCookieName ='csrftoken';
axios.defaults.xsrfHeaderName ='X-CSRFToken';

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
       var c = ca[i];
       while (c.charAt(0) ===' ') c = c.substring(1);
       if(c.indexOf(name) === 0)
          return c.substring(name.length,c.length);
    }
    return "";
}

const options = {
    headers: {"X-CSRFToken": getCookie('csrftoken')}
}

const SubmitButton = ({ text, action }) => {

    return (
        <button className="submit-button" onClick={action}>{text}</button>
    )
}

const InputBox = ({ placeholder, type, updateField }) => {

    return (
        <input
            className="input-box"
            id={placeholder.toLowerCase()}
            type={type}
            placeholder={placeholder}
            onChange={(e) => updateField(e.target.value)}
        ></input>
    )

}

const LoginForm = ({ setShowLogin }) => {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const doLogin = async () => {
        console.log("Logging in ", username, password);

        const results = await axios.post('/api/login', {"username": username, "password": password}, options)
        .then(res => console.log(res))
        .catch(err => console.log(err));

    }

    return (
        <div className="login-form">
            <h1>Welcome Back</h1>
            <InputBox type="text" placeholder="Username" updateField={setUsername}/>
            <InputBox type="password" placeholder="Password" updateField={setPassword}/>
            <button className="switch-button" onClick={() => setShowLogin(false)}>Don't have an account? Sign Up</button>
            <SubmitButton text="LOG IN" action={doLogin} />
        </div>
    )
}

const SignUpForm = ({ setShowLogin }) => {

    const doSignUp = () => {
        console.log("Signing up");
    }

    return (
        <div className="signup-form">
            <h1>Welcome</h1>
            <InputBox type="text" placeholder="Email" />
            <InputBox type="text" placeholder="Username" />
            <InputBox type="text" placeholder="Password" />
            <InputBox type="text" placeholder="Confirm Password" />
            <button className="switch-button" onClick={() => setShowLogin(true)}>Already have an account? Log In</button>
            <SubmitButton text="SIGN UP" action={doSignUp}/>
        </div>
    )
}

const WelcomeForms = (props) => {

    const [showLogin, setShowLogin] = useState(props.showLogin);


    return (
        <div className="forms">
            {showLogin ? (
                <LoginForm setShowLogin={setShowLogin}/>
            ) : (
                <SignUpForm setShowLogin={setShowLogin}/>
            )}
        </div>

    )

}

export default WelcomeForms;
