import React, { Component } from 'react';

/** Overall Form component:
 *  - Form that handles ticker selection
 *
 */

//TODO: Refactor to make multi-use
class TickerForm extends Component {
  constructor(props) {
    super(props);
    //local state for form
    this.state = {
      ticker: ''
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(evt) {
    this.setState({ [evt.target.name]: [evt.target.value] });
  }

  handleSubmit(evt) {
    evt.preventDefault();
    this.props.history.push(`/silas/${this.state.ticker}`);
    this.setState({ ticker: '' });
  }

  render() {
    console.log('tickerform props', this.props);
    return (
      <React.Fragment>
        <form onSubmit={this.handleSubmit}>
          <label htmlFor="">Select Ticker</label>
          <select
            name="ticker"
            id="ticker"
            required="required"
            value={this.state.ticker}
            onChange={this.handleChange}
          >
            <option value="" />
            {/* TODO: Once we have more tickers, make this dynamic or expand */}
            <option value="GOOGL">Alphabet (Google)</option>
            <option value="AMZN">Amazon</option>
            <option value="AAPL">Apple</option>
            <option value="FB">Facebook</option>
            <option value="NFLX">Netflix</option>
            <option value="SPY">S&P 500 ETF</option>
          </select>
          <br />
          <button>Get Predictions</button>
        </form>
      </React.Fragment>
    );
  }
}

export default TickerForm;
