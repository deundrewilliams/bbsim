import React from 'react'
import CompWinPanel from '../components/CompWinPanel'
import NomineePanel from '../components/NomineePanel'
import WeekView from '../components/WeekView'

const mock_weeks = [
    {"Week Number": 1, HOH: "Tera", POV: "Jedson", Evicted: "Jedson", "Final Nominees": ["Breydon", "Jedson"], "Initial Nominees": ["Beth", "Jedson"]},
    {"Week Number": 2, HOH: "Breydon", POV: "Breydon", Evicted: "Beth", "Final Nominees": ["Beth", "Tera"], "Initial Nominees": ["Beth", "Tera"]},
    {"Week Number": 3, HOH: "Tychon", POV: "Tera", Evicted: "Kiefer", "Final Nominees": ["Kiefer", "Breydon"], "Initial Nominees": ["Tera", "Kiefer"]}
]

const mock_prejury = [
    { id: 1, name: "Julie" },
    { id: 1, name: "Josh" },
    { id: 1, name: "Latoya" },
    { id: 1, name: "Kyle" },
    { id: 1, name: "Austin" },
]

const mock_jury = [
    { id: 1, name: "Victoria"},
    { id: 1, name: "Rohan"},
    { id: 1, name: "Tina"},
    { id: 1, name: "Jedson"},
    { id: 1, name: "Beth"},
    { id: 1, name: "Kiefer"},
    { id: 1, name: "Tera"},
]

const mock_finale = {
    "Final HOH": { id: 1, name: "Tychon" },
    "Final Juror": { id: 1, name: "Tera" },
    Finalists: [
        { id: 1, name: "Tychon" },
        { id: 1, name: "Breydon" }
    ],
    Jury: mock_jury,
    Votes: [
        {
            Victoria: "Tychon",
            Rohan: "Tychon",
            Tina: "Tychon",
            Jedson: "Tychon",
            Beth: "Tychon",
            Kiefer: "Tychon",
            Tera: "Breydon",
        }
    ],
    Winner: { id: 1, name: "Tychon" }
}

const mock_game = {
    Finale: mock_finale,
    Jury: mock_jury,
    Prejury: mock_prejury,
    Weeks: mock_weeks,
    Winner: { id: 1, name: "Tychon" }
}

class GamePage extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            current_week: 1,
            game_info:  mock_game // props.location.state.info
        }

    }

    render() {

        let noms = ["Josh", "Julie"]

        return(
            <div className="game-page">
                <WeekView week={mock_weeks[0]} />
            </div>
        )
    }

}

export default GamePage;
