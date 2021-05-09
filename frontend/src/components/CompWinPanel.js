import '../css/CompWinPanel.css';

export default function CompWinPanel(props) {

    const { name, type } = props;

    if (type === "HOH")
    {
        return(
            <div className="hoh-panel">
                {name}
            </div>
        )
    }
    else if (type === "POV")
    {
        return(
            <div className="pov-panel">
                {name}
            </div>
        )
    }



}
