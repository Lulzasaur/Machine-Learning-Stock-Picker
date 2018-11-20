import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Route, NavLink, Switch } from 'react-router-dom';
import DisplayContainer from '../DisplayContainer/DisplayContainer';

/** Overall Project Silas application:
 *
 * - shows header, nav links, and contains routes to:
 *   - Chart page
 *
 * COMPONENT HIERARCHY:
 * https://docs.google.com/drawings/d/1YpgTfRmAHL9connFeR6cSBvD4-hMTtZACfN0oWHIxFQ/edit?usp=sharing
 *
 */

class App extends Component {
  render() {
    return (
      <div className="App">
        {/* Nav */}
        <nav>
          <NavLink exact to="/">
            Project Silas
          </NavLink>
        </nav>
        {/* Router */}
        <Switch>
          <Route eact path="/" render={() => <DisplayContainer />} />
        </Switch>
      </div>
    );
  }
}

export default App;
