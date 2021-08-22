import React from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import SiteBanner from '../components/SiteBanner';
import '../css/AppButton.css';

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


const AppButton = (props) => {

    const { text, class_name } = props;

    return(
        <div className={class_name}>
            <p>{text}</p>
        </div>
    )
}

const GameTable = ({ games, deleteGame, continueGame }) => {

    return (
        <div className="game-table">
            {games.map((item, index) => {
                return(
                    <div key={index}>Game: {item.id} {item.current_step} </div>
                )
            })}
        </div>
    )

}

class HomePage extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            username: '',
            games: [],
        }

        this.getHome = this.getHome.bind(this);
    }

    async getHome() {

        const response = await axios.get('/api/home', options)
        .then(res => res.data)
        .catch(err => err.response.data);

        if (response.username) {
            this.setState({
                username: response.username,
                games: response.games,
            });
        } else {
            console.log(response);
        }

    }

    continueGame(game_id) {
        console.log("Continuing game", game_id);
    }

    deleteGame(game_id) {
        console.log("Deleting game", game_id);
    }

    componentDidMount() {

        this.getHome();

    }

    render() {

        return(
            <div className="home-page">
                <SiteBanner />
                <div className="container">
                    <h2 id="greeting">Hello, {this.state.username}</h2>
                    <h2 id="in-progress-header">GAMES IN PROGRESS</h2>
                    <GameTable games={this.state.games} deleteGame={this.deleteGame} continueGame={this.continueGame} />
                    <AppButton text="Create New Game" class_name="app-button newgame-btn" />
                </div>
                {/* <Link to="/create-game" style={{ textDecoration: 'none', color: 'black' }}>
                    <AppButton text="New Game" class_name="app-button newgame-btn" />
                </Link>
                <AppButton text="Player Bank" class_name="app-button playerbank-btn" /> */}
            </div>
        )

    }


}

export default HomePage;
