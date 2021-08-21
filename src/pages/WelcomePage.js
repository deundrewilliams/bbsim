import React from 'react';

import WelcomeForms from '../components/WelcomeForms';

import '../css/Welcome.css';
class WelcomePage extends React.Component {


    constructor(props) {
        super(props);
        this.state = {
            landing: true,
            showLogin: false,
        };

        this.handleLoginSuccess = this.handleLoginSuccess.bind(this);
    }

    handleLoginSuccess = () => {

        // navigate to /home
        this.props.history.push('/home');

    }

    render() {

        return(
            <div className="welcome-page">
                <div className="welcome-container">
                    <div className="site-title">
                        <div>
                            BIG<br></br>BROTHER<br></br>SIM
                        </div>
                    </div>
                    {this.state.landing ? (
                        <div className="right-area">
                            <button className="login-button" onClick={() => this.setState({ showLogin: true, landing: false })}>
                                LOGIN
                            </button>
                            <button className="signup-button" onClick={() => this.setState({ showLogin: false, landing: false })}>
                                SIGN UP
                            </button>
                        </div>
                    ) : (
                        <div className="right-area">
                            <WelcomeForms showLogin={this.state.showLogin} handleLoginSuccess={this.handleLoginSuccess}/>
                        </div>
                    )}

                </div>
            </div>
        )

    }


}

export default WelcomePage;
