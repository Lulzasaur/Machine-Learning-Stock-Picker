import React, {Component} from 'react'
import Form from '../Form/Form'
import DisplayContainer from '../DisplayContainer/DisplayContainer'

/** Overall Container Component:
 * 
 *  - Has local state
 *  - Shows form and prediction
 *  - Has function that is passed down to Form
 *  - Has data/response/prediction that is passed down to DisplayContainer
 * 
 * 
 */

class Container extends Component {
//TODO: Refactor to expirimental JS (bind via arrow func)
  constructor(props) {
  super(props)
//JAY / HASI: What does the response from the backend look like?
  this.state = {
  }

  //function to pass to Form to grab info and make prediction
  sendTicker(ticker) {
    //TODO: Wait until we know what backend looks like
    //Axios call should be in here?
    /* ...code goes here... */

    // this.setState at the end? 
  }

  render() {

    return(
      <React.Fragment>
        <h1>Select a ticker</h1>
      <Form ticker={this.sendTicker}/>
      {/* 'prediction' is the response from the backend
          ready to pass to DisplayContainer */}
      <DisplayContainer prediction={this.state}/>
      </React.Fragment>
    )
  }
}

}


export default Container;