import '../css/EvictedPanel.css';

export default function EvictedPanel(props) {

    const { name, votecount, tied } = props;

    let votestring = ""

    if (votecount) {

        if (votecount.length > 1)
        {
            votestring = "(" + votecount[0] + " - " + votecount[1] + ")"

            if (tied) {
                votestring += "*"
            }
        }

        else
        {
            votestring = "(" + votecount[0] + " - 0)"
        }

    }



    return(
        <div className="evicted-panel">
            {name} {votestring}
        </div>
    )

}
