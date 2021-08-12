import React from 'react'
import axios from 'axios';

import SiteBanner from '../components/SiteBanner';

import '../css/GamePage.css';
import MemoryWall from '../components/MemoryWall';
import HOHCompetition from '../components/HOHCompetition';
import NomCeremony from '../components/NomCeremony';
import POVCompetition from '../components/POVCompetition';
import POVCeremony from '../components/POVCeremony';
import EvictionCeremony from '../components/EvictionCeremony';
import Finale from '../components/Finale';

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

// const mock_data = [
//     {
//         "current_step": "Memory Wall",
//         "players": [
//             {"id": 1, "name": "Tiffany", "evicted": false },
//             {"id": 2, "name": "Derek X", "evicted": false },
//             {"id": 3, "name": "Brent", "evicted": true },
//             {"id": 4, "name": "Derek F", "evicted": false },
//             {"id": 5, "name": "Frenchie", "evicted": false },
//         ]
//     },
//     {
//         "current_step": "HOH Competition",
//         "hoh": {"id": 2, "name": "Derek X", "evicted": false },
//     },
//     {
//         "current_step": "Nomination Ceremony",
//         "nominees": [
//             {"id": 3, "name": "Brent", "evicted": true },
//             {"id": 5, "name": "Frenchie", "evicted": false }
//         ]
//     },
//     {
//         "current_step": "POV Competition",
//         "pov": {"id": 1, "name": "Tiffany", "evicted": false }
//     },
//     {
//         "current_step": "POV Ceremony",
//         "results": {
//             "decision": {"Using": true, "On": {"id": 3, "name": "Brent", "evicted": true } },
//             "final_nominees": [
//                 {"id": 4, "name": "Derek F", "evicted": false },
//                 {"id": 5, "name": "Frenchie", "evicted": false }
//             ]
//         }
//     },
//     {
//         "current_step": "Eviction",
//         "results": {
//             "evicted": {"id": 5, "name": "Frenchie", "evicted": true },
//             "votes": [1],
//             "nominees": [
//                 {"id": 4, "name": "Derek F", "evicted": false },
//                 {"id": 5, "name": "Frenchie", "evicted": false }
//             ],
//             "tied": false,
//         }
//     },
//     {
//         "current_step": "Finale",
//         "results": {
//             "part_one": {"id": 1, "name": "Tiffany", "evicted": false },
//             "part_two": {"id": 2, "name": "Derek X", "evicted": false },
//             "final_hoh": {"id": 2, "name": "Derek X", "evicted": false },
//             "final_juror": {"id": 4, "name": "Derek F", "evicted": false },
//             "jury": [
//                 {"id": 3, "name": "Brent", "evicted": true },
//                 {"id": 4, "name": "Derek F", "evicted": false },
//                 {"id": 5, "name": "Frenchie", "evicted": false },
//             ],
//             "winner": {"id": 1, "name": "Tiffany", "evicted": false },
//             "finalists": [
//                 {"id": 1, "name": "Tiffany", "evicted": false },
//                 {"id": 2, "name": "Derek X", "evicted": false },
//             ],
//             "votes": {"Brent": "Derek X", "Derek F": "Tiffany", "Frenchie": "Tiffany"}
//         }
//     }
// ]


const Picker = (props) => {

    const { step, info, advance, history } = props;

    switch (step) {
        case "Memory Wall":
            return (<MemoryWall players={info.players} advance={advance}/>)
        case "HOH Competition":
            return (<HOHCompetition hoh={info.hoh} advance={advance} />)
        case "Nomination Ceremony":
            return (<NomCeremony nominees={info.nominees} advance={advance} />)
        case "POV Competition":
            return (<POVCompetition pov={info.pov} advance={advance} />)
        case "POV Ceremony":
            return (<POVCeremony results={info.results} advance={advance} />)
        case "Eviction":
            return (<EvictionCeremony results={info.results} advance={advance} />)
        case "Finale":
            return (<Finale results={info.results} advance={() => history.push('/')} />)
        default:
            return null
    }

}
class GamePage extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            game_step: this.props.location.state.game_info.current_step,
            game_id: this.props.location.state.game_info.id
            // mock_index: 0,
        }

        this.advanceSimulation = this.advanceSimulation.bind(this);
        this.mockAdvance = this.mockAdvance.bind(this);

    }

    async componentDidMount() {

        this.setState({ game_step: this.props.location.state.game_info.current_step })
        this.setState({ game_id: this.props.location.state.game_info.id })



        console.log("Advancing...")
        await this.advanceSimulation();

        // this.setState({ game_step: "Memory Wall"})
        // this.setState({ game_id: 999, mock_index: 0 })

        // this.mockAdvance();

    }

    // mockAdvance() {

    //     let num = this.state.mock_index + 1;

    //     console.log(this.state.mock_index);

    //     this.setState({
    //         mock_index: num,
    //         game_info: mock_data[num],
    //         game_step: mock_data[num].current_step
    //     })

    // }

    async advanceSimulation() {

        let results = await axios.post('/api/simulate', {"id": this.state.game_id}, options)
        .then(res => res.data)
        .catch(err => err.response.data)

        if (results.current_step) {

            this.setState({
                game_info: results,
                game_step: results.current_step
            })
        }

    }

    render() {

        if (this.state.game_info) {
            return (
                <div className="game-page">
                    <SiteBanner />
                    <Picker
                        step={this.state.game_step}
                        info={this.state.game_info}
                        advance={this.advanceSimulation}
                        history={this.props.history}
                    />
                </div>
            )
        }
        else {
            return(
                <div className="game-page">
                    <SiteBanner />
                </div>
            )
        }


    }

}

export default GamePage;
