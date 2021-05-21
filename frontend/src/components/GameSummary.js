
function WeekSummary(props) {


    const { week } = props;

    let votestring = '';

    if (week.vote_count.length > 1)
        {
            votestring = "(" + week.vote_count[0] + " - " + week.vote_count[1] + ")"

            if (week.tied) {
                votestring += "*";
            }
        }

        else
        {
            votestring = "(" + week.vote_count[0] + " - 0)";
        }

    return(
        <div className="week-summary">
            <br></br>
            <br></br>
            Week {week.week_num}:<br></br>
            HOH: {week.hoh}<br></br>
            Nominees: {week.inoms.toString()}<br></br>
            POV: {week.pov}<br></br>
            Final Nominees: {week.fnoms.toString()}<br></br>
            Evicted: {week.evicted} {votestring}<br></br>

        </div>
    )

}

function FinaleSummary(props) {

    const { data } = props;

    return(
        <div className="finale-summary">
            <br></br>
            Finale
            <br></br>
            Final HOH: {data.final_hoh.name}<br></br>
            Final Juror: {data.final_juror.name}<br></br>
            Winner: {data.winner.name}<br></br>
            <br></br>
            <br></br>
        </div>
    )

}

export default function GameSummary(props) {

    const { weeks, finale } = props;

    return(
        <div className="game-summary">
            Summary

            {weeks.map((item, index) => {
                return(
                    <WeekSummary key={index} week={item} />
                )
            })}

            <FinaleSummary data={finale} />
        </div>
    )

}
