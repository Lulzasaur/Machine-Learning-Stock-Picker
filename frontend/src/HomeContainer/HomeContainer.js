import React, { Component } from 'react';
import TickerForm from '../TickerForm/TickerForm';
import { Jumbotron } from 'reactstrap';

class HomeContainer extends Component {
  render() {
    return (
      <div className="home-container">
        <Jumbotron>
          <h1 className="display-3">Invest with confidence</h1>
          <p className="lead">
            Silas is a simple tool. Select the stock you want to invest with.
            Use our prediction model to find out its worth for the next five
            days.
          </p>
          <hr className="my-2" />
          <p>Select one of our stock options below</p>
          <TickerForm {...this.props} />
        </Jumbotron>
      </div>
    );
  }
}

export default HomeContainer;
