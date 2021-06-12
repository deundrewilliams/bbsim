import '../css/AppButton.css';

export default function AppButton(props) {

    const { text, clickAction, disabled } = props;

    return(
        <button className="app-button" onClick={clickAction || undefined} disabled={disabled || false}>
            {text}
        </button>
    )

}
