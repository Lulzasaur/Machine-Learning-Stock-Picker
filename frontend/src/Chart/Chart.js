import React, { Component } from 'react';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';

class Chart extends Component {
  render() {
    const options = {
      title: {
        text: 'My stock chart'
      },
      series: [
        {
          data: [1, 2, 3]
        }
      ]
    };
    return (
      <HighchartsReact
        highcharts={Highcharts}
        constructorType={'stockChart'}
        options={options}
      />
    );
  }
}

export default Chart;
