import HouseguestTile from './HouseguestTile';

import '../css/CompWinPanel.css';

export default function CompWinPanel(props) {

    const { name, type } = props;

    if (type === "HOH")
    {
        return(
            <div className="hoh-panel">
                <h3 className="comp-type">Head of Household</h3>
                <HouseguestTile name={name} />
            </div>
        )
    }
    else if (type === "POV")
    {
        return(
            <div className="pov-panel">
                <h3 className="comp-type">POV Holder</h3>
                <HouseguestTile name={name} />
            </div>
        )
    }



}
