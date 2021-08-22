import React from 'react';
import axios from 'axios';

import SiteBanner from '../components/SiteBanner';
import { Link } from 'react-router-dom';

import '../css/AppButton.css';
import '../css/HomePage.css';

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

const mock_players = [
    {"name": "Mitch", "evicted": false},
    {"name": "Claire", "evicted": false},
    {"name": "Cam", "evicted": true},
    {"name": "Gloria", "evicted": false},
    {"name": "Jay", "evicted": false},
    {"name": "Phil", "evicted": true},
    {"name": "Mitch", "evicted": false},
    {"name": "Claire", "evicted": false},
    {"name": "Cam", "evicted": true},
    {"name": "Gloria", "evicted": false},
    {"name": "Jay", "evicted": false},
    {"name": "Phil", "evicted": true},
]

const PlayerTile = (props) => {

    const { name, evicted } = props;

    const class_name = "player-cell-tile" + (evicted ? " evicted" : "");

    return (
        <div className={class_name}>
            <p className="player-tile-name">{name}</p>
        </div>
    )

}

const GameTableCell = (props) => {

    const { id, total_players, players_left, players, full_info } = props.game;

    return(
        <div className="game-table-cell">
            <div className="remaining">
                <p className="remaining-label">PLAYERS LEFT:</p>
                <p className="remaining-value">{players_left}/{total_players}</p>
            </div>
            <div className="player-list">
                {players.map((item, index) => {
                    return(
                        <PlayerTile key={index} name={item.name} evicted={item.evicted}/>
                    )
                })}
            </div>
            <div className="cell-buttons">
                <button className="continue-btn" onClick={() => props.continue(full_info)}>CONTINUE</button>
                <button className="delete-btn" onClick={() => props.delete(id)}>DELETE</button>
            </div>
        </div>
    )
}

const GameTable = ({ games, deleteGame, continueGame }) => {

    if (games.length === 0) {

        return(
            <div className="empty-game-table">
                <p>No games found.</p>
            </div>
        )

    }

    return (
        <div className="game-table">
            {games.map((item, index) => {
                return(
                    <GameTableCell key={index} game={item} delete={deleteGame} continue={continueGame}/>
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
        this.continueGame = this.continueGame.bind(this);
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

    continueGame(game_info) {
        console.log("Continuing game", game_info.id);

        this.props.history.push('/game',
            { "game_info": game_info}
        );
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
                <SiteBanner buttonText="Settings" />
                <div className="container">
                    <h2 id="greeting">Hello, {this.state.username}</h2>
                    <h2 id="in-progress-header">GAMES IN PROGRESS</h2>
                    <GameTable games={this.state.games} deleteGame={this.deleteGame} continueGame={this.continueGame} />
                    <Link to="/create-game" style={{ textDecoration: 'none', color: 'black' }}>
                        <button id="create-game">Create New Game</button>
                    </Link>
                </div>
            </div>
        )

    }


}

export default HomePage;
