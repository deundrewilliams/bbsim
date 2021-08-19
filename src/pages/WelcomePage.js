import React from 'react';

class WelcomePage extends React.Component {


    constructor(props) {
        super(props);
        this.state = {
            name: '',
            email: '',
            password: '',
            confirmPassword: '',
            error: ''
        };
    }


    render() {
        return (
            <div>
                <h1>Welcome</h1>
                <p>This is the welcome page</p>
            </div>
        );
    }

}

export default WelcomePage;
