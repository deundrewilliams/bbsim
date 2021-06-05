import CompWinPanel from "./CompWinPanel";
import EvictedPanel from "./EvictedPanel";
import FinaleVote from "./FinaleVote";
import AppButton from './AppButton';
import GameSummary from './GameSummary';
import { useState } from 'react';
import { Link } from 'react-router-dom'

import '../css/FinaleView.css';

export default function FinaleView(props) {

    const { info } = props;
    const [winnerReveal, setWinnerReveal] = useState(false);

    console.log(winnerReveal + " <- winner reveal")


    function handleContinue() {
        setWinnerReveal(true)
    }


    if (winnerReveal === false) {

        return(
            <div className="finale-view">
                <CompWinPanel name={info.final_hoh.name} type="HOH" />
                <EvictedPanel name={info.final_juror.name} />
                <div className="jury-votes">
                    {
                        Object.keys(info.votes).map((voter, index) => {
                            return(
                                <FinaleVote key={index} juror={voter} votee={info.votes[voter]} />
                            )
                        })
                    }
                </div>
                <AppButton text="Continue" clickAction={handleContinue}/>
            </div>
        )

    }

    else {
        return(
            <div className="finale-view">
                <div className="winner-panel">
                    The winner is {info.winner.name}
                    <GameSummary weeks={props.weeks} finale={info}/>
                    <Link to="/">
                        <AppButton text="Finish" />
                    </Link>
                </div>
            </div>
        )

    }




}
