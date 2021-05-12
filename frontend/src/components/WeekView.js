import CompWinPanel from "./CompWinPanel";
import NomineePanel from "./NomineePanel";
import EvictedPanel from './EvictedPanel';
import AppButton from './AppButton';


export default function WeekView(props) {

    const { week, handleClick } = props;

    console.log(week)

    return(
        <div className="week-view">
            <CompWinPanel name={week.hoh} type="HOH" />
            <NomineePanel nominees={week.inoms} />
            <CompWinPanel name={week.pov} type="POV" />
            <NomineePanel nominees={week.fnoms} />
            <EvictedPanel name={week.evicted} />
            <AppButton text="Continue" clickAction={handleClick}/>
        </div>
    )

}
