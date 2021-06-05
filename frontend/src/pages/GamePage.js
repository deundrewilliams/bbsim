import React from 'react'
import FinaleView from '../components/FinaleView'
import WeekView from '../components/WeekView'

import '../css/GamePage.css';

// const mock_weeks = [
//     {week_num: 1, vote_count: [2,1], tied: false, hoh: "Tera", pov: "Jedson", evicted: "Jedson", fnoms: ["Breydon", "Jedson"], inoms: ["Beth", "Jedson"]},
//     {week_num: 2, vote_count: [2,1], tied: true, hoh: "Breydon", pov: "Breydon", evicted: "Beth", fnoms: ["Beth", "Tera"], inoms: ["Beth", "Tera"]},
//     {week_num: 3, vote_count: [1,0], tied: false, hoh: "Tychon", pov: "Tera", evicted: "Kiefer", fnoms: ["Kiefer", "Breydon"], inoms: ["Tera", "Kiefer"]}
// ]

// const mock_prejury = [
//     { id: 1, name: "Julie" },
//     { id: 1, name: "Josh" },
//     { id: 1, name: "Latoya" },
//     { id: 1, name: "Kyle" },
//     { id: 1, name: "Austin" },
// ]

// const mock_jury = [
//     { id: 1, name: "Victoria"},
//     { id: 1, name: "Rohan"},
//     { id: 1, name: "Tina"},
//     { id: 1, name: "Jedson"},
//     { id: 1, name: "Beth"},
//     { id: 1, name: "Kiefer"},
//     { id: 1, name: "Tera"},
// ]

// const mock_finale = {
//     final_hoh: { id: 1, name: "Tychon" },
//     final_juror: { id: 1, name: "Tera" },
//     finalists: [
//         { id: 1, name: "Tychon" },
//         { id: 1, name: "Breydon" }
//     ],
//     jury: mock_jury,
//     votes:
//         {
//             Victoria: "Tychon",
//             Rohan: "Tychon",
//             Tina: "Tychon",
//             Jedson: "Tychon",
//             Beth: "Tychon",
//             Kiefer: "Tychon",
//             Tera: "Breydon",
//         },
//     winner: { id: 1, name: "Tychon" }
// }

// const mock_game = {
//     finale: mock_finale,
//     jury: mock_jury,
//     prejury: mock_prejury,
//     weeks: mock_weeks,
//     winner: { id: 1, name: "Tychon" }
// }

class GamePage extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            current_week: 0,
            in_finale: false,
            game_info:  props.location.state.info,
            complete: false,
        }

        this.advanceSimulation = this.advanceSimulation.bind(this);

    }

    componentDidUpdate() {
        window.scrollTo(0, 0);
    }

    advanceSimulation() {

        // If already at week limit, set finale on
        if (this.state.current_week + 1 === this.state.game_info.weeks.length)
        {
            this.setState({ in_finale: true })
        }

        // Else
        else
        {
            this.setState({ current_week: this.state.current_week + 1})
        }




    }

    render() {

        // console.log(this.state.game_info)

        if (this.state.in_finale) {

            return(
                <div className="game-page">
                    <FinaleView info={this.state.game_info.finale} weeks={this.state.game_info.weeks}/>
                </div>
            )

        }

        return(
            <div className="game-page">
                <WeekView week={this.state.game_info.weeks[this.state.current_week]} handleClick={this.advanceSimulation}/>
            </div>
        )
    }

}

export default GamePage;
