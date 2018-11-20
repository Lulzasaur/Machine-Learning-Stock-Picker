import React, { Component } from 'react';
import './App.css';
import { Route, Switch } from 'react-router-dom';
import DisplayContainer from '../DisplayContainer/DisplayContainer';
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem
} from 'reactstrap';

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
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      isOpen: false
    };
  }
  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
  render() {
    return (
      <div className="App">
        {/* Nav */}
        <div>
          <Navbar color="light" light expand="md">
            <NavbarBrand href="/">Project Silas</NavbarBrand>
            <NavbarToggler onClick={this.toggle} />
            <Collapse isOpen={this.state.isOpen} navbar>
              <Nav className="ml-auto" navbar>
                {/* <NavItem>
                  <NavLink href="/components/">Components</NavLink>
                </NavItem>
                <NavItem>
                  <NavLink href="https://github.com/reactstrap/reactstrap">
                    GitHub
                  </NavLink>
                </NavItem> */}
                <UncontrolledDropdown nav inNavbar>
                  <DropdownToggle nav caret>
                    Tickers
                  </DropdownToggle>
                  <DropdownMenu right>
                    <DropdownItem href="https://apple.com">Apple</DropdownItem>
                    <DropdownItem href="https://microsoft.com">
                      Microsoft
                    </DropdownItem>
                    <DropdownItem divider />
                    <DropdownItem>Reset</DropdownItem>
                  </DropdownMenu>
                </UncontrolledDropdown>
              </Nav>
            </Collapse>
          </Navbar>
        </div>
        {/* Router */}
        <Switch>
          <Route eact path="/" render={() => <DisplayContainer />} />
        </Switch>
      </div>
    );
  }
}

export default App;
