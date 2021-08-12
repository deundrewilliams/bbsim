import HouseguestTile from "./HouseguestTile";
import StepHeader from "./StepHeader";
import ButtonBar from "./ButtonBar";
import '../css/POVCeremony.css';

const POVCeremony = (props) => {

    const { decision, final_nominees } = props.results;

    console.log(decision);

    return(
        <div className="pov-ceremony">
            <StepHeader text="POWER OF VETO MEETING" />
            {decision.Using ?
                (<h3 id="used-pov">POV USED ON {decision.On.name.toUpperCase()}</h3>) :
                (<h3>POV NOT USED</h3>)
            }
            <div className="nom-tiles">
                {final_nominees.map((item, index) => {
                    return(<HouseguestTile key={index} name={item.name} borderStyle="red"/>)
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

export default POVCeremony;
