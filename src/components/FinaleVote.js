import HouseguestTile from './HouseguestTile';

import "../css/FinaleVote.css";

export default function FinaleVote(props) {

    const { juror, votee } = props;

    return(
        <div className="finale-vote">
            <HouseguestTile name={juror}/>
            <p className="voted-for">voted for</p>
            <HouseguestTile name={votee} />
        </div>
    )

}
