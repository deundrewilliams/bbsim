import React from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import SiteBanner from '../components/SiteBanner';
import '../css/AppButton.css';

axios.defaults.xsrfCookieName ='csrftoken';
axios.defaults.xsrfHeaderName ='X-CSRFToken';

// function getCookie(cname) {
//     var name = cname + "=";
//     var ca = document.cookie.split(';');
//     for(var i=0; i<ca.length; i++) {
//        var c = ca[i];
//        while (c.charAt(0) ===' ') c = c.substring(1);
//        if(c.indexOf(name) === 0)
//           return c.substring(name.length,c.length);
//     }
//     return "";
// }

// const options = {
//     headers: {"X-CSRFToken": getCookie('csrftoken')}
// }

// const mock_contestants = [
//     { id: 14, name: "Julie" },
//     { id: 13, name: "Josh" },
//     { id: 12, name: "Latoya" },
//     { id: 11, name: "Kyle" },
//     { id: 10, name: "Austin" },
//     { id: 9, name: "Victoria"},
//     { id: 8, name: "Rohan"},
//     { id: 7, name: "Tina"},
//     { id: 6, name: "Jedson"},
//     { id: 5, name: "Beth"},
//     { id: 4, name: "Kiefer"},
//     { id: 3, name: "Tera"},
//     { id: 2, name: "Breydon"},
//     { id: 1, name: "Tychon"},
// ]

const AppButton = (props) => {

    const { text, class_name } = props;

    return(
        <div className={class_name}>
            <p>{text}</p>
        </div>
    )
}

class HomePage extends React.Component {

    render() {

        return(
            <div className="home-page">
                <SiteBanner />
                <Link to="/create-game" style={{ textDecoration: 'none', color: 'black' }}>
                    <AppButton text="New Game" class_name="app-button newgame-btn" />
                </Link>
                <AppButton text="Player Bank" class_name="app-button playerbank-btn" />
            </div>
        )

    }


}

export default HomePage;
