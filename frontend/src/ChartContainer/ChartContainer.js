import React, { Component } from 'react';
import Chart from '../Chart/Chart';

/** TickerContainer Component:
 * TODO: Add what this component does
 *
 */

class ChartContainer extends Component {
  render() {
    return (
      <React.Fragment>
        {/* Pass down functions from Routes */}
        <Chart {...this.props} />
        {/* TODO: Add more components once we know what else there is
            to display */}
      </React.Fragment>
    );
  }
}

export default ChartContainer;
