import React from 'react'

class GamePage extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            current_week: 1,
            weeks: props.location.state.info.Weeks,
            finale: props.location.state.info.Finale
        }

    }

    render() {

        console.log(this.props.location.state)
        console.log(this.state.weeks)
        console.log(this.state.finale)

        return(
            <div className="game-page">
                Game Page
            </div>
        )
    }

}

export default GamePage;
