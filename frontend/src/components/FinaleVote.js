export default function FinaleVote(props) {

    const { juror, votee } = props;

    return(
        <div className="finale-vote">
            {juror} voted for {votee}
        </div>
    )

}
