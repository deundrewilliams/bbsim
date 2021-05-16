import ContestantPanel from './ContestantPanel';

import '../css/ContestantView.css';

export default function ContestantView(props) {

    const { contestants, clickAction } = props;

    return(
        <div className="contestant-view">
            {contestants.map((item, index) => {
            return(
                <ContestantPanel key={index} name={item.name} id={item.id} clickAction={clickAction} />
            )
        })}

        </div>
    )
}
