import '../css/StepHeader.css';

const StepHeader = (props) => {
    const { text } = props;

    return(
        <h2 className="step-header">{text}</h2>
    )
}

export default StepHeader
