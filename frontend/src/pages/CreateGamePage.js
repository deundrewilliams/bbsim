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

class CreateGamePage extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            game_id: undefined,
            game_received: false,
        }

        this.postGame = this.postGame.bind(this);
        this.setGame = this.setGame.bind(this);
    }

    componentDidMount() {
        this.postGame()
    }

    setGame(data) {
        console.log(data)
        this.setState({
            game_id: data.id,
            game_info: data
        })
    }

    async postGame() {

        // console.log(this.props.location.state.houseguests)
        let cs = this.props.location.state.contestants.response

        let c_ids = cs.map(x => x.id)

        await axios.post('/api/create-game', {"contestants": c_ids}, options)
        .then((res) => this.setGame(res.data))
        .catch((err) => console.log(err))

        await axios.post('/api/sim-game', {"id": this.state.game_id}, options)
        .then((res) => this.setGame(res.data))
        .catch((err) => console.log(err))

        this.setState({ game_received: true })

    }

    render() {


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

export default CreateGamePage;
