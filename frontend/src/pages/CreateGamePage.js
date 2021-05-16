import React from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import AppButton from '../components/AppButton';
import ContestantView from '../components/ContestantView'

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

class CreateGamePage extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            game_id: undefined,
            game_created: false,
            game_received: false,
            picked_contestants: new Set(),
            num_picked: 0
        }

        this.simGame = this.simGame.bind(this);
        this.setGame = this.setGame.bind(this);
        this.createGame = this.createGame.bind(this);
        this.handleContestantClick = this.handleContestantClick.bind(this);
    }

    setGame(data) {
        console.log(data)
        this.setState({
            game_id: data.id,
            game_info: data
        })
    }

    handleContestantClick(contestant_id) {

        const clicked = document.getElementById(contestant_id + "-contestant-panel")

        if (this.state.picked_contestants.has(contestant_id))
        {
            this.state.picked_contestants.delete(contestant_id);

            clicked.style.backgroundColor = "#f5f5f5";
        }
        else
        {
            this.state.picked_contestants.add(contestant_id);
            clicked.style.backgroundColor = "green";
        }

        console.log(this.state.picked_contestants)
        this.setState({ num_picked: this.state.picked_contestants.size})
        // console.log(this.state.picked_contestants.size)

    }

    async createGame() {

        await axios.post('/api/create-game', {"contestants": Array.from(this.state.picked_contestants)}, options)
        .then((res) => this.setGame(res.data))
        .catch((err) => console.log(err))

        this.setState({ game_created: true })

        this.simGame()

    }

    async simGame() {

        await axios.post('/api/sim-game', {"id": this.state.game_id}, options)
        .then((res) => this.setGame(res.data))
        .catch((err) => console.log(err))

        this.setState({ game_received: true })

    }

    render() {

        // this.props.location.state.contestants.response



        if (!this.state.game_created)
        {
            return(
                <div className="create-game-page">
                    <ContestantView
                        contestants={this.props.location.state.contestants.response}
                        clickAction={this.handleContestantClick}
                    />
                    <AppButton
                        text="Create Game"
                        clickAction={this.createGame}
                        disabled={this.state.num_picked < 5 || this.state.num_picked > 16}
                    />
                </div>
            )

        }

        else
        {
            return(
                <div className="create-game-page">
                    <Link to={{
                        pathname: '/game',
                        state: {
                            info: this.state.game_info
                        }
                    }}>
                        <AppButton disabled={!this.state.game_received} text="Simulate Game"/>
                    </Link>

                </div>
            )
        }


    }

}

export default CreateGamePage;
