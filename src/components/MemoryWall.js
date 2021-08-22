import React from 'react';

import '../css/MemoryWall.css';
import StepHeader from './StepHeader';
import ButtonBar from '../components/ButtonBar';

const PlayerTile = (props) => {

    let class_name = "player-tile"

    if (props.info.evicted === "True") {
        class_name += " evicted"
    }

    return(
        <div className={class_name}>
            <p>{props.info.name}</p>
        </div>
    )

}

const MemoryWall = (props) => {

    console.log(props.players);

    return(
        <div className="memory-wall">
            <StepHeader text="MEMORY WALL" />
            <div className="player-names">
                {props.players.map((item, index) => {
                    return(
                        <PlayerTile key={index} info={item} />
                    )
                })}
            </div>
            <ButtonBar
                option_1="Quit"
                option_2="Continue"
                clickAction_1={props.quit}
                clickAction_2={props.advance}
            />
        </div>
    )

}

export default MemoryWall;
