import React, { Component } from 'react';
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

/** HIGHCHARTS*/
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';

class Chart extends Component {
  render() {
    const options = {
      // title: {
      //   text: 'My stock chart'
      // },
      // series: [
      //   {
      //     data: [1, 2, 3]
      //   }
      // ]
      rangeSelector: {
        selected: 1
      },

      title: {
        text: 'AAPL Stock Price'
      },

      series: [
        {
          name: 'AAPL',
          data: [
            //Highcharts uses JS Date Numbers which is why we're using Date.UTC
            //Source: https://stackoverflow.com/questions/9548326/what-format-does-the-highcharts-js-library-accept-for-dates
            // How it should be structured for each array within the main array:
            // [Date.UTC(YYYY, MM - 1, DD, TT), VAL]
            [Date.UTC(2012, 3, 6, 10), 5],
            [Date.UTC(2012, 3, 6, 11), 6],
            [Date.UTC(2012, 3, 6, 12), 4]
          ],
          tooltip: {
            valueDecimals: 2
          }
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
