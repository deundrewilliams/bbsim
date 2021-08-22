import HouseguestTile from "./HouseguestTile";
import StepHeader from "./StepHeader";
import ButtonBar from "./ButtonBar";
import '../css/POVCompetition.css';

const POVCompetition = (props) => {

    return(
        <div className="pov-competition">
            <StepHeader text="POWER OF VETO HOLDER"/>
            <div className="pov-container">
                <HouseguestTile name={props.pov.name} borderStyle="gold"/>
            </div>
            <ButtonBar
                option_1="Quit"
                option_2="Continue"
                clickAction_1={props.quit}
                clickAction_2={props.advance}
            />
        </div>
    )

}

export default POVCompetition;
