import HouseguestTile from './HouseguestTile';

import '../css/EvictedPanel.css';

export default function EvictedPanel(props) {

    console.log(props);

    const { name, vote_count, tied } = props;

    let votestring = ""

    if (vote_count) {

        if (vote_count.length > 1)
        {
            votestring = "(" + vote_count[0] + " - " + vote_count[1] + ")"

            if (tied) {
                votestring += "*"
            }
        }

        else
        {
            votestring = "(" + vote_count[0] + " - 0)"
        }

    }

    if (votestring.length > 0)
    {
        return(
            <div className="evicted-panel">
                <h3 id="evicted-header">Evicted</h3>
                <p id="voteline">By a vote of {votestring}...</p>
                <HouseguestTile name={name} />
            </div>
        )
    }
    else
    {
        return(
            <div className="evicted-panel">
                <h3 id="evicted-header">Evicted</h3>
                <HouseguestTile name={name} />
            </div>
        )
    }




}
