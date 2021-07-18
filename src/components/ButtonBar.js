import '../css/ButtonBar.css';

const ButtonBar = (props) => {

    const { option_1, option_2, clickAction_1, clickAction_2 } = props;

    return(
        <div className="button-bar">
            <button onClick={clickAction_1} className="bad-option">
                {option_1}
            </button>
            <button onClick={clickAction_2} className="good-option">
                {option_2}
            </button>
        </div>
    )
}

export default ButtonBar;
