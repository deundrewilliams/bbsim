import CompWinPanel from "./CompWinPanel";
import NomineePanel from "./NomineePanel";
import EvictedPanel from './EvictedPanel';


export default function WeekView(props) {

    const { week } = props;

    console.log(week)

    return(
        <div className="week-view">
            <CompWinPanel name={week.HOH} type="HOH" />
            <NomineePanel nominees={week["Initial Nominees"]} />
            <CompWinPanel name={week.POV} type="POV" />
            <NomineePanel nominees={week["Final Nominees"]} />
            <EvictedPanel name={week.Evicted} />
        </div>
    )

}
