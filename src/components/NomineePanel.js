import HouseguestTile from './HouseguestTile';

import '../css/NomineePanel.css';

export default function NomineePanel(props) {

    const { nominees } = props;

    return(
        <div className="nominee-panel">
            <h3 className="nom-label">Nominees</h3>
            <div className="nom-tiles">
                {nominees.map((item, index) => {
                    return(
                        <HouseguestTile key={index} name={item} />
                    )
                })}
            </div>
        </div>
    )

}
