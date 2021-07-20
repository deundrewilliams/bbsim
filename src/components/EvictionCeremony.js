import { useState } from 'react';
import StepHeader from "./StepHeader";
import HouseguestTile from "./HouseguestTile";
import ButtonBar from './ButtonBar';
import '../css/EvictionCeremony.css';

const EvictionCeremony = (props) => {

    const [showEvicted, setShowEvicted] = useState(false);

    const { evicted, votes, nominees, tied } = props.results;

    let votestring = ""

    if (votes) {

        if (votes.length > 1)
        {
            votestring = votes[0] + (tied ? "*": "") + " TO " + votes[1];
        }

        else
        {
            votestring = votes[0] + " TO 0"
        }

    }



    if (showEvicted) {
        return(
            <div className="eviction-ceremony">
                <StepHeader text="VOTE & EVICTION" />
                <h3>{evicted.name} is EVICTED</h3>
                <div className="evicted-container">
                    <HouseguestTile name={evicted.name} borderStyle="black" />
                </div>
                <ButtonBar
                    option_1="Quit"
                    option_2="Continue"
                    clickAction_2={props.advance}
                />
            </div>
        )
    }

    else {
        return(
            <div className="eviction-ceremony">
                <StepHeader text="VOTE & EVICTION" />
                <h3>BY A VOTE OF {votestring}... </h3>
                <div className="nom-tiles">
                    {nominees.map((item, index) => {
                        return(
                            <HouseguestTile key={index} name={item.name} borderStyle="red"/>
                        )
                    })}
                </div>
                <ButtonBar
                    option_1="Quit"
                    option_2="Continue"
                    clickAction_2={() => setShowEvicted(true)}
                />
            </div>
        )
    }


}

export default EvictionCeremony;
