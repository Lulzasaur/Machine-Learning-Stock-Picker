import React, { Component } from 'react';
import TickerForm from '../TickerForm/TickerForm';

class HomeContainer extends Component {
  render() {
    return (
      <div className="home-container">
        <div className="ticker-form-container">
          <TickerForm {...this.props} />
        </div>
      </div>
    );
  }
}

export default HomeContainer;
