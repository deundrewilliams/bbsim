import '../css/EvictedPanel.css';

export default function EvictedPanel(props) {

    const { name } = props;

    return(
        <div className="evicted-panel">
            {name}
        </div>
    )

}
