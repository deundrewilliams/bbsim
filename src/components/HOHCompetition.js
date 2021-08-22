import HouseguestTile from "./HouseguestTile";
import StepHeader from "./StepHeader";
import ButtonBar from './ButtonBar';
import '../css/HOHCompetition.css';

const HOHCompetition = (props) => {

    return(
        <div className="hoh-competition">
            <StepHeader text="HEAD OF HOUSEHOLD"/>
            <div className="hoh-container">
                <HouseguestTile name={props.hoh.name} borderStyle="green"/>
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

export default HOHCompetition;
