import '../css/NomineePanel.css';

export default function NomineePanel(props) {

    const { nominees } = props;

    return(
        <div className="nominee-panel">
            {nominees.map((item, index) => {
                return(
                    <div key={index}>
                        {item}
                    </div>
                )
            })}
        </div>
    )

}
