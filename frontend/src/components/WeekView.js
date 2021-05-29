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
            Week {week.week_num}:
            <CompWinPanel name={week.hoh} type="HOH" />
            <NomineePanel nominees={week.inoms} />
            <CompWinPanel name={week.pov} type="POV" />
            <NomineePanel nominees={week.fnoms} />
            <EvictedPanel name={week.evicted} votecount={week.vote_count} tied={week.tied}/>
            <AppButton text="Continue" clickAction={handleClick}/>
        </div>
    )

}
