import ContestantPanel from './ContestantPanel';

export default function ContestantView(props) {

    const { contestants, clickAction } = props;

    return(
        <div className="contestant-view">
            {contestants.map((item, index) => {
            return(
                <ContestantPanel key={index} name={item} clickAction={clickAction} />
            )
        })}

        </div>
    )
}
