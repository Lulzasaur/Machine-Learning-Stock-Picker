import React, { Component } from 'react';
import Chart from '../Chart/Chart';

class DisplayContainer extends Component {
  render() {
    return (
      <React.Fragment>
        <Chart />
        {/* TODO: Add more components once we know what else there is
            to display */}
      </React.Fragment>
    );
  }
}

export default DisplayContainer;
