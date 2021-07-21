import StepHeader from "./StepHeader";
import HouseguestTile from "./HouseguestTile";
import ButtonBar from "./ButtonBar";
import FinaleVote from "./FinaleVote";
import { useState } from "react";

import '../css/Finale.css';

const Finale = (props) => {

    const [finaleStep, setFinaleStep] = useState('Final HOH');
    const { part_one, part_two, final_hoh, final_juror, winner, finalists, votes } = props.results;


    if (finaleStep === 'Final HOH') {

        return (
            <div className="finale">
                <StepHeader text="FINAL HOH COMPETITION"/>
                <div className="winners">
                    <div className="hoh-winner">
                        <h2>PART 1 WINNER</h2>
                        <HouseguestTile name={part_one.name} borderStyle="green"/>
                    </div>
                    <div className="hoh-winner">
                        <h2>PART 2 WINNER</h2>
                        <HouseguestTile name={part_two.name} borderStyle="green"/>
                    </div>
                    <div className="hoh-winner">
                        <h2>PART 3 WINNER</h2>
                        <HouseguestTile name={final_hoh.name} borderStyle="green"/>
                    </div>
                </div>
                <ButtonBar
                    option_1="Quit"
                    option_2="Continue"
                    clickAction_2={() => setFinaleStep('Final Eviction')}
                />
            </div>
        )
    }

    else if (finaleStep === "Final Eviction") {
        return(
            <div className="finale">
                <StepHeader text="FINAL EVICTION"/>
                <div className="final-evictee">
                    <h2 id="evicted-bar">{final_hoh.name.toUpperCase()} HAS EVICTED...</h2>
                    <HouseguestTile name={final_juror.name} borderStyle="black"/>
                </div>
                <ButtonBar
                    option_1="Quit"
                    option_2="Continue"
                    clickAction_2={() => setFinaleStep('Jury Vote')}
                />
            </div>
        )
    }

    else if (finaleStep === "Jury Vote") {
        return(
            <div className="finale">
                <StepHeader text="JURY VOTING"/>
                <div className="finalists">
                    {finalists.map((item, index) => {
                        return(
                            <HouseguestTile key={index} name={item.name} borderStyle="green" />
                        )
                    })}
                </div>
                <div className="votes">
                    {Object.keys(votes).map((voter, index) => {
                        return(
                            <FinaleVote key={index} juror={voter} votee={votes[voter]} />
                        )
                    })}
                </div>
                <ButtonBar
                    option_1="Quit"
                    option_2="Continue"
                    clickAction_2={() => setFinaleStep('Winner Reveal')}
                />
            </div>
        )
    } else if (finaleStep === "Winner Reveal") {
        return(
            <div className="finale">
                <StepHeader text="WINNER"/>
                <div className="single-tile">
                    <HouseguestTile name={winner.name} borderStyle="gold"/>
                </div>
                <ButtonBar
                    option_1="Quit"
                    option_2="Continue"
                    clickAction_2={props.advance}
                />
            </div>
        )
    }

}

export default Finale;
