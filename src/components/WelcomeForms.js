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

const LoginForm = ({ setShowLogin, completeLogin }) => {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const doLogin = async () => {
        console.log("Logging in ", username, password);

        const results = await axios.post('/api/login', {"username": username, "password": password}, options)
        .then(res => res.data)
        .catch(err => err.response.data);

        if (results.success) {
            completeLogin();
        }

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

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [email, setEmail] = useState('');

    const doSignUp = async () => {

        if (password !== confirmPassword) {
            alert("Passwords don't match");
            return;
        }

        const data = {
            "username": username,
            "password": password,
            "email": email
        }

        const results = await axios.post('/api/signup', data, options)
        .then(res => res.data)
        .catch(err => err.response.data);

        console.log(results);
    }

    return (
        <div className="signup-form">
            <h1>Welcome</h1>
            <InputBox type="text" placeholder="Email" updateField={setEmail}/>
            <InputBox type="text" placeholder="Username" updateField={setUsername}/>
            <InputBox type="text" placeholder="Password" updateField={setPassword}/>
            <InputBox type="text" placeholder="Confirm Password" updateField={setConfirmPassword}/>
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
                <LoginForm setShowLogin={setShowLogin} completeLogin={props.handleLoginSuccess}/>
            ) : (
                <SignUpForm setShowLogin={setShowLogin}/>
            )}
        </div>

    )

}

export default WelcomeForms;
