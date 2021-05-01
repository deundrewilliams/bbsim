import './App.css';
import axios from 'axios';
import React from 'react';

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


class App extends React.Component {

    constructor() {
        super()

        this.state = {
            houseguests: [],
        }

        this.fetchHouseguests = this.fetchHouseguests.bind(this);
    }

    setHousegeusts(data) {
        this.setState({ houseguests: data })
    }

    fetchHouseguests() {

        axios.defaults.xsrfCookieName ='csrftoken';
        axios.defaults.xsrfHeaderName ='X-CSRFToken';

        axios.get('http://localhost:8000/api/houseguests/', options)
        .then(function(res) {
            return res
        })
        .then((res) => this.setHousegeusts(res.data.response))
        .catch((err) => console.log(err))

    }


    render() {

        if (this.state.houseguests.length === 0) {
            return (
                <div className="App">
                    <button onClick={this.fetchHouseguests}>Fetch Houseguests!</button>
                </div>
            );
        }

        return(
            this.state.houseguests.map((item, index) => {
                return(
                    <p key={index}>{item.name}</p>
                )
            })
        )


    }

}

export default App;
