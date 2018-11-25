import React, { Component } from 'react';
import TickerForm from '../TickerForm/TickerForm';

class TickerFormContainer extends Component {
  render() {
    return (
      <React.Fragment>
        <TickerForm />
        {/* TODO: Add more components once we know what else there is
            to display */}
      </React.Fragment>
    );
  }
}

export default TickerFormContainer;
