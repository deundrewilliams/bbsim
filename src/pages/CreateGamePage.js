import React from 'react';
import axios from 'axios';

import SiteBanner from '../components/SiteBanner';
import ButtonBar from '../components/ButtonBar';

import '../css/CreateGamePage.css';

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

const ContestantTile = (props) => {

    const { object, clickAction, removable } = props;

    let class_name = "contestant-tile";

    if (removable) {
        class_name += " removable";
    }

    return(
        <div className={class_name} onClick={() => clickAction(object)}>
            <p>{object.name}</p>
        </div>
    )

}

class CreateGamePage extends React.Component {

    constructor() {
        super();

        this.state = {
            playersChosen: false,
            currentSearch: '',
            chosenPlayers: new Set(),
        }

        this.handleSubmitPlayers = this.handleSubmitPlayers.bind(this);
        this.deleteChosenPlayer = this.deleteChosenPlayer.bind(this);
        this.handleConfirmDetails = this.handleConfirmDetails.bind(this);
    }

    handleSubmitPlayers()  {

        this.setState({ playersChosen: true });

    }

    async handleConfirmDetails() {

        let arr_players = Array.from(this.state.chosenPlayers);

        let arr_ids = arr_players.map(obj => obj.id);

        let results = await axios.post(`/api/create-game`, { "contestants": arr_ids }, options)
        .then(res => res.data)
        .catch(err => err.response.data);

        console.log(results);

        this.props.history.push('/game',
            { "game_info": results }
        );

    }

    async searchPlayer(e) {

        e.preventDefault();

        console.log("Searching for", this.state.currentSearch);

        let results = await axios.get(`/api/contestant/${this.state.currentSearch}`, options)
        .then(res => res.data)
        .catch(err => err.response.data);

        let _set = this.state.chosenPlayers;

        if (results.name) {
            _set.add(results);
        }

        console.log(this.state.chosenPlayers);
        this.setState({ chosenPlayers: _set })

    }

    deleteChosenPlayer(player_info) {

        console.log("Will remove id ", player_info);

        let _set = this.state.chosenPlayers;

        if (_set.has(player_info)) {
            _set.delete(player_info);
        }

        this.setState({ chosenPlayers: _set });

        console.log(_set);

    }

    // console.log(currentSearch);

    render() {

        if (this.state.playersChosen) {
            return(
                <div className="create-game">
                    <SiteBanner />
                    <h2>GAME DETAILS</h2>
                    <div className="chosen-players">
                        <h2 className="chosen-heading">PLAYERS</h2>
                        {this.state.chosenPlayers.size === 0 ? (<p>None chosen</p>) :
                         Array.from(this.state.chosenPlayers).map((item, index) => {
                            return(
                                <ContestantTile key={index} object={item} clickAction={() => {}} />
                            )
                        })}
                    </div>
                    <ButtonBar
                        option_1="Back"
                        option_2="Create Game"
                        clickAction_1={() => this.setState({ playersChosen: false })}
                        clickAction_2={() => this.handleConfirmDetails()}
                    />
                </div>
            )
        }

        else {
            return(
                <div className="create-game">
                    <SiteBanner buttonText="Settings"/>
                    <div className="player-search">
                        <h2 className="search-heading">Search for Players</h2>
                        <form>
                            <label>
                                <input id="name-field" type="text" name="name" onChange={(e) => this.setState({ currentSearch: e.target.value })}/>
                            </label>
                            <input id="add-btn" type="submit" value="Add" onClick={(e) => this.searchPlayer(e)}/>
                        </form>
                    </div>
                    <div className="chosen-players">
                        <h2 className="chosen-heading">SELECTED PLAYERS</h2>
                        {this.state.chosenPlayers.size === 0 ? (<p>None chosen</p>) :
                         Array.from(this.state.chosenPlayers).map((item, index) => {
                            return(
                                <ContestantTile key={index} object={item} clickAction={this.deleteChosenPlayer} removable/>
                            )
                        })}
                    </div>
                    <ButtonBar
                        option_1="Back"
                        option_2="Continue"
                        clickAction_2={this.handleSubmitPlayers}
                    />
                </div>
            )
        }

    }


}

export default CreateGamePage;
