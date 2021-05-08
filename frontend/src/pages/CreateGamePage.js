import React from 'react';
import axios from 'axios';

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
    }

    componentDidMount() {
        this.postGame()
    }

    postGame() {

        // console.log(this.props.location.state.houseguests)
        let hgs = this.props.location.state.houseguests.response

        let hg_ids = hgs.map(x => x.id)

        axios.post('/api/create-game', {"houseguests": hg_ids}, options)
        .then((res) => console.log(res))
        .catch((err) => console.log(err))

    }

    render() {
        return(
            <div className="create-game-page">
                Create Game Page
            </div>
        )
    }

}

export default CreateGamePage;
