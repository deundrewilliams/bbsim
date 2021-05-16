import '../css/ContestantPanel.css';

export default function ContestantPanel(props) {

    const { name, id, clickAction } = props;

    function passIdClick() {
        clickAction(id);
    }

    const c_id = id + "-contestant-panel"

    return(
        <div className="contestant-panel" onClick={passIdClick} id={c_id}>
            {name}
        </div>
    )

}
