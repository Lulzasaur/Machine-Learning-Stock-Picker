import React, { Component } from 'react';

/** Overall Form component:
 *  - Form that handles ticker selection
 *
 */

//TODO: Refactor to make multi-use
class Form extends Component {
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
    this.props.ticker(this.state.ticker);
    this.setState({ ticker: '' });
  }

  render() {
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
            <option value="AAPL">Apple</option>
          </select>
        </form>
      </React.Fragment>
    );
  }
}

export default Form;
