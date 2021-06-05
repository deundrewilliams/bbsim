import HouseguestTile from './HouseguestTile';

import '../css/EvictedPanel.css';

export default function EvictedPanel(props) {

    console.log(props);

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
