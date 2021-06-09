import CompWinPanel from "./CompWinPanel";
import NomineePanel from "./NomineePanel";
import EvictedPanel from './EvictedPanel';
import AppButton from './AppButton';

import '../css/WeekView.css';

export default function WeekView(props) {

    const { week, handleClick } = props;

    console.log(week)

    return(
        <div className="week-view">
            <h2 id="week-number">WEEK {week.week_num}</h2>

            <CompWinPanel name={week.hoh} type="HOH" />
            <NomineePanel nominees={week.inoms} />
            <CompWinPanel name={week.pov} type="POV" />
            <NomineePanel nominees={week.fnoms} />
            <EvictedPanel name={week.evicted} vote_count={week.vote_count} tied={week.tied}/>
            <AppButton text="Continue" clickAction={handleClick}/>
        </div>
    )

}
