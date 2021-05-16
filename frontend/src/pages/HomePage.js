import React from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import AppButton from '../components/AppButton';

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


class HomePage extends React.Component {

    constructor() {
        super()

        this.state = {
            contestants: []
        }

        this.fetchContestants = this.fetchContestants.bind(this);
    }

    componentDidMount() {
        this.fetchContestants()
    }

    fetchContestants() {

        axios.get('/api/contestants/', options)
        .then((res) => this.setState({ contestants: res.data }))
        .catch((err) => console.log("Error: " + err))

    }

    render() {
        return(
            <div className="home-page">
                <Link to={{
                    pathname: '/create-game',
                    state: {
                        contestants: this.state.contestants
                    }
                }}>
                    <AppButton text="New Game"/>
                </Link>
        </div>
        )

    }


}

export default HomePage;
