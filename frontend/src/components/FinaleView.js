import CompWinPanel from "./CompWinPanel";
import EvictedPanel from "./EvictedPanel";
import FinaleVote from "./FinaleVote";
import AppButton from './AppButton';
import { useState } from 'react';
import { Link } from 'react-router-dom'

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
                {
                    Object.keys(info.votes).map((voter, index) => {
                        return(
                            <FinaleVote key={index} juror={voter} votee={info.votes[voter]} />
                        )
                    })
                }
                <AppButton text="Continue" clickAction={handleContinue}/>
            </div>
        )

    }

    else {
        return(
            <div className="finale-view">
                <div className="winner-panel">
                    The winner is {info.winner.name}
                    <Link to="/">
                        <AppButton text="Finish" />
                    </Link>
                </div>
            </div>
        )

    }




}
