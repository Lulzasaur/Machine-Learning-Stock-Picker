import React, { Component } from 'react';
import axios from 'axios';
/** HIGHCHARTS*/
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';

class Chart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      predictiveOptions: {
        rangeSelector: { selected: 1 },
        title: { text: '' },
        series: []
      },
      historicOptions: {
        rangeSelector: { selected: 1 },
        title: { text: '' },
        series: []
      }
    };
  }
  //JUAN TODO: Make this dumb and move state up higher or move to Redux
  async componentDidMount() {
    try {
      console.log('getting data');
      //Grabbing Historic Stock data for first Chart
      let historicData = await axios.get(
        'http://127.0.0.1:5000/silas/aapl/historics'
      );

      //Since Data comes latest date first, we need to reverse and map
      //In addition, to get it in the right format for the graph,
      //We needed to split the starting date, convert it to Date.UTC (which is what
      //highcharts uses), and place that with the closing price inside of its own
      //array

      let data = await historicData.data.reverse().map(d => {
        let startingDate = d.date.split('-');
        return [
          Date.UTC(startingDate[0], startingDate[1], startingDate[2]),
          d.close
        ];
      });

      //Updating the state so components re-render
      this.setState({
        historicOptions: {
          title: { text: 'AAPL' },
          series: [
            {
              name: 'AAPL',
              data: data,
              tooltip: {
                valueDecimals: 2
              }
            }
          ]
        }
      });

      //Getting prediction data
      let predictiveData = await axios.get('http://127.0.0.1:5000/silas/aapl');
      console.log(predictiveData);

      //Mapping prediction out
      let prediction = await predictiveData.data.reverse().map(dPoint => {
        let startingDate = dPoint.date.split('-');
        let val = dPoint['0'] >= dPoint['1'] ? 0 : 1;
        return [
          Date.UTC(startingDate[0], startingDate[1], startingDate[2]),
          val
        ];
      });
      console.log('what does predict look like', prediction);

      this.setState({
        predictiveOptions: {
          rangeSelector: { selected: 1 },
          title: { text: 'AAPL Prediction' },
          series: [
            {
              name: 'AAPL Prediction',
              data: prediction,
              tooltip: {
                valueDecimals: 2
              }
            }
          ]
        }
      });
    } catch (err) {
      console.log('nice error, brochach');
    }
  }
  render() {
    return (
      <React.Fragment>
        {/* TODO: Why is this is giving me a bug once it tries to render */}
        {/* {this.state.historicOptions.series.length === 0 ? (
          <h1 className="HistoricLoadingBar">Loading Historic Data</h1>
        ) : (
          <React.Fragment> */}
        <h1>Historic Chart</h1>
        <HighchartsReact
          highcharts={Highcharts}
          constructorType={'stockChart'}
          options={this.state.historicOptions}
        />
        {/* </React.Fragment>
        )} */}
        {this.state.predictiveOptions.series.length === 0 ? (
          <h1 className="Loading Bar">Loading Predictions</h1>
        ) : (
          <React.Fragment>
            <h1>Prediction Chart</h1>
            <HighchartsReact
              highcharts={Highcharts}
              constructorType={'stockChart'}
              options={this.state.predictiveOptions}
            />
          </React.Fragment>
        )}
      </React.Fragment>
    );
  }
}

export default Chart;

/** Below are different chartlibraries
 * - Amcharts
 * - Chartify
 * - D3
 */

/** AMCHARTS */
// import * as am4core from '@amcharts/amcharts4/core';
// import * as am4charts from '@amcharts/amcharts4/charts';
// import am4themes_animated from '@amcharts/amcharts4/themes/animated';

// am4core.useTheme(am4themes_animated);

// class Chart extends Component {
//   componentDidMount() {
//     let chart = am4core.create('chartdiv', am4charts.XYChart);

//     chart.paddingRight = 20;

//     let data = [];
//     let visits = 10;
//     for (let i = 1; i < 366; i++) {
//       visits += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);
//       data.push({
//         date: new Date(2018, 0, i),
//         name: 'name' + i,
//         value: visits
//       });
//     }

//     chart.data = data;

//     let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
//     dateAxis.renderer.grid.template.location = 0;

//     let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
//     valueAxis.tooltip.disabled = true;
//     valueAxis.renderer.minWidth = 35;

//     let series = chart.series.push(new am4charts.LineSeries());
//     series.dataFields.dateX = 'date';
//     series.dataFields.valueY = 'value';

//     series.tooltipText = '{valueY.value}';
//     chart.cursor = new am4charts.XYCursor();

//     let scrollbarX = new am4charts.XYChartScrollbar();
//     scrollbarX.series.push(series);
//     chart.scrollbarX = scrollbarX;

//     this.chart = chart;
//   }

//   componentWillUnmount() {
//     if (this.chart) {
//       this.chart.dispose();
//     }
//   }

//   render() {
//     return <div id="chartdiv" style={{ width: '100%', height: '500px' }} />;
//   }
// }
