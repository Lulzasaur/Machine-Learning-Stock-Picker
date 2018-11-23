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
      let historicData = await axios.get(
        'http://127.0.0.1:5000/silas/aapl/historics'
      );
      console.log('whats the historic data', historicData);

      let data = await historicData.data.reverse().map(d => {
        let startingDate = d.date.split('-');
        return [
          Date.UTC(startingDate[0], startingDate[1], startingDate[2]),
          d.close
        ];
      });
      console.log(data);

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
    } catch (err) {
      console.log('nice error, brochach');
    }
    // let predictiveData = await axios.get('http://127.0.0.1:5000/silas/aapl');
    // let predictiveData = [
    //   { 0: 41, 1: 58, date: '2018-09-25' },
    //   { 0: 49, 1: 50, date: '2018-09-24' },
    //   { 0: 32, 1: 67, date: '2018-09-21' },
    //   { 0: 46, 1: 53, date: '2018-09-20' },
    //   { 0: 36, 1: 63, date: '2018-09-19' }
    // ];
    // const pointStartArray = predictiveData[
    //   predictiveData.length - 1
    // ].date.split('-');
    // // console.log('what does the pSA look like', pointStartArray);
    // this.setState({
    //   predictiveOptions: {
    //     rangeSelector: {
    //       selected: 1
    //     },

    //     title: {
    //       text: 'AAPL Stock Price'
    //     },

    //     series: [
    //       {
    //         name: 'AAPL',
    //         pointStart: Date.UTC(
    //           +pointStartArray[0],
    //           +pointStartArray[1] - 1,
    //           +pointStartArray[2]
    //         ),
    //         pointInterval: 1000 * 60 * 60 * 24,
    // data: [1, 1, 1, 0, 1],
    // tooltip: {
    //   valueDecimals: 2
    // }
    //       }
    //     ]
    //   }
    // });
    // } catch (err) {
    //   console.log('nice error, brochach');
    // }
  }
  render() {
    return (
      <React.Fragment>
        {this.state.historicOptions.series.length === 0 ? (
          <h1 className="HistoricLoadingBar">Loading Historic Data</h1>
        ) : (
          <HighchartsReact
            highcharts={Highcharts}
            constructorType={'stockChart'}
            options={this.state.historicOptions}
          />
        )}
        {this.state.predictiveOptions.series.length === 0 ? (
          <h1 className="Loading Bar">Loading Predictions</h1>
        ) : (
          <HighchartsReact
            highcharts={Highcharts}
            constructorType={'stockChart'}
            options={this.state.predictiveOptions}
          />
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
