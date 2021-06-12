import '../css/HouseguestTile.css';

export default function HouseguestTile(props) {

    const { name } = props;

    return(
        <div className="hg-tile">
            <p className="hg-name">{name}</p>
        </div>
    )

}
