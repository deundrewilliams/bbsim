import HouseguestTile from "./HouseguestTile";
import StepHeader from "./StepHeader";
import ButtonBar from "./ButtonBar";
import '../css/NomCeremony.css';

const NomCeremony = (props) => {

    return(
        <div className="nom-ceremony">
            <StepHeader text="NOMINATION CEREMONY"/>
            <div className="nom-container">
                {props.nominees.map((item, index) => {
                    return(
                        <HouseguestTile key={index} name={item.name} borderStyle="red" />
                    )
                    })}
            </div>
            <ButtonBar
                option_1="Quit"
                option_2="Continue"
                clickAction_2={props.advance}
            />
        </div>
    )

}

export default NomCeremony;
