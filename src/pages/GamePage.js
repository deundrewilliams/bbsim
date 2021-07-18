import React from 'react'
// import axios from 'axios';

import ButtonBar from '../components/ButtonBar';
import SiteBanner from '../components/SiteBanner';

import '../css/GamePage.css';
import MemoryWall from '../components/MemoryWall';

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

const mock_data = [
    {
        "current_step": "Memory Wall",
        "players": [
            {"id": 1, "name": "Tiffany", "evicted": false },
            {"id": 2, "name": "Derek X", "evicted": false },
            {"id": 3, "name": "Brent", "evicted": true },
            {"id": 4, "name": "Derek F", "evicted": false },
            {"id": 5, "name": "Frenchie", "evicted": false },
        ]
    },
    {
        "current_step": "HOH Competition",
        "hoh": {"id": 2, "name": "Derek X", "evicted": false },
    },
    {
        "current_step": "Nomination Ceremony",
        "nominees": [
            {"id": 4, "name": "Derek F", "evicted": false },
            {"id": 5, "name": "Frenchie", "evicted": false }
        ]
    },
    {
        "current_step": "POV Competition",
        "pov": {"id": 1, "name": "Tiffany", "evicted": false }
    },
    {
        "current_step": "POV Ceremony",
        "results": {
            "Decision": {"Using": false, "On": null },
            "Final Nominees": [
                {"id": 4, "name": "Derek F", "evicted": false },
                {"id": 5, "name": "Frenchie", "evicted": false }
            ]
        }
    },
    {
        "current_step": "Eviction",
        "results": {
            "Evicted": {"id": 5, "name": "Frenchie", "evicted": true },
            "Votes": [1],
            "Nominees": [
                {"id": 4, "name": "Derek F", "evicted": false },
                {"id": 5, "name": "Frenchie", "evicted": false }
            ],
            "Tied": false,
        }
    },
    {
        "current_step": "Finale",
        "results": {
            "part_one": {"id": 1, "name": "Tiffany", "evicted": false },
            "part_two": {"id": 2, "name": "Derek X", "evicted": false },
            "final_hoh": {"id": 2, "name": "Derek X", "evicted": false },
            "final_juror": {"id": 4, "name": "Derek F", "evicted": false },
            "jury": [
                {"id": 3, "name": "Brent", "evicted": true },
                {"id": 4, "name": "Derek F", "evicted": false },
                {"id": 5, "name": "Frenchie", "evicted": false },
            ],
            "winner": {"id": 1, "name": "Tiffany", "evicted": false },
            "finalists": [
                {"id": 1, "name": "Tiffany", "evicted": false },
                {"id": 2, "name": "Derek X", "evicted": false },
            ],
            "votes": {"Brent": "Derek X", "Derek F": "Tiffany", "Frenchie": "Tiffany"}
        }
    }
]


const Picker = (props) => {

    const { step, info } = props;

    switch (step) {
        case "Memory Wall":
            return (<MemoryWall players={info.players}/>)
        case "HOH Competition":
            return null
        default:
            return null
    }

}
class GamePage extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            mock_index: -1,
        }

        // this.advanceSimulation = this.advanceSimulation.bind(this);
        this.mockAdvance = this.mockAdvance.bind(this);

    }

    componentDidMount() {

        // this.setState({ game_step: this.props.location.state.game_info.current_step })
        // this.setState({ game_id: this.props.location.state.game_info.id })

        this.setState({ game_step: "Memory Wall"})
        this.setState({ game_id: 999 })

        this.mockAdvance();

    }

    mockAdvance() {

        let num = this.state.mock_index + 1;

        this.setState({
            mock_index: num,
            game_info: mock_data[num],
            game_step: mock_data[num].current_step
        })

    }

    // async advanceSimulation() {

    //     let results = await axios.post('/api/simulate', {"id": this.state.game_id}, options)
    //     .then(res => res.data)
    //     .catch(err => err.response.data)

    //     if (results.current_step) {

    //         this.setState({
    //             game_info: results,
    //             game_step: results.current_step
    //         })
    //     }

    // }

    render() {

        return (
            <div className="game-page">
                <SiteBanner />
                <Picker step={this.state.game_step} info={this.state.game_info}/>
                <ButtonBar
                    option_1="Quit"
                    option_2="Continue"
                    clickAction_2={this.mockAdvance}
                />
            </div>
        )
    }

}

export default GamePage;
