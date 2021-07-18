import React from 'react';

import '../css/MemoryWall.css';
import StepHeader from './StepHeader';

const PlayerTile = (props) => {

    let class_name = "player-tile"

    if (props.info.evicted) {
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
        </div>
    )

}

export default MemoryWall;
