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

const mock_contestants = [
    { id: 14, name: "Julie" },
    { id: 13, name: "Josh" },
    { id: 12, name: "Latoya" },
    { id: 11, name: "Kyle" },
    { id: 10, name: "Austin" },
    { id: 9, name: "Victoria"},
    { id: 8, name: "Rohan"},
    { id: 7, name: "Tina"},
    { id: 6, name: "Jedson"},
    { id: 5, name: "Beth"},
    { id: 4, name: "Kiefer"},
    { id: 3, name: "Tera"},
    { id: 2, name: "Breydon"},
    { id: 1, name: "Tychon"},
]


class HomePage extends React.Component {

    constructor() {
        super()

        this.state = {
            contestants: mock_contestants
        }

        this.fetchContestants = this.fetchContestants.bind(this);
    }

    componentDidMount() {
        this.fetchContestants()
    }

    fetchContestants() {

        axios.get('/api/contestants/', options)
        .then((res) => this.setState({ contestants: res.data.response }))
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
