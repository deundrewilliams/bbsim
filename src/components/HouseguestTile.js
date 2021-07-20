import '../css/HouseguestTile.css';

const HouseguestTile = (props) => {

    let class_name = "hg-tile " + props.borderStyle;

    return(
        <div className={class_name}>
            <p>{props.name}</p>
        </div>
    )
}

export default HouseguestTile;
