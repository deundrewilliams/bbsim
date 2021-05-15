import '../css/ContestantPanel.css';

export default function ContestantPanel(props) {

    const { name, clickAction } = props;

    return(
        <div className="contestant-panel" onClick={clickAction}>
            {name}
        </div>
    )

}
