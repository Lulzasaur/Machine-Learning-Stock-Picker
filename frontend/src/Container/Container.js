import React, {Component} from 'react'
import Form from '../Form/Form'
import DisplayContainer from '../DisplayContainer/DisplayContainer'


class Container extends Component {
//TODO: Refactor to expirimental JS (bind via arrow func)
  constructor(props) {
  super(props)
//JAY / HASI: What does the response from the backend look like?
  this.state = {
  }

  //function to pass to Form to grab info and make prediction

  //function for API call



  render() {

    return(
      <React.Fragment>
        <h1>Select a ticker</h1>
      <Form />
      {/* 'prediction' is the response from the backend
          ready to pass to DisplayContainer */}
      <DisplayContainer prediction={this.state}/>
      </React.Fragment>
    )
  }
}

}


export default Container;