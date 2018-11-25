import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import HomeContainer from '../HomeContainer/HomeContainer';
import ChartContainer from '../ChartContainer/ChartContainer';

/** Router Component:
 * TODO: Add what this component does
 *
 */

class Router extends Component {
  render() {
    return (
      <Switch>
        {/* Passing down props so we can use the history API
            for the TickerForm */}
        <Route exact path="/" render={props => <HomeContainer {...props} />} />
        <Route
          exact
          path="/silas/:ticker"
          render={props => <ChartContainer {...props} />}
        />
      </Switch>
    );
  }
}

export default Router;
