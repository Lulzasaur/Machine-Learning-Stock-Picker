import React, { Component } from 'react';
import './App.css';
import Router from '../Router/Router';
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
 * TODO: NEED TO UPDATE THIS
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
        {/*  */}
        {/*  */}
        {/* Nav */}
        {/*  */}
        {/*  */}
        <div>
          <Navbar light expand="md">
            <NavbarBrand href="/">Project Silas</NavbarBrand>
            <NavbarToggler onClick={this.toggle} />
            <Collapse isOpen={this.state.isOpen} navbar>
              <Nav className="ml-auto" navbar>
                {/* <NavItem>
                  <NavLink href="/components/">Components</NavLink>
                </NavItem> */}
                <NavItem>
                  <NavLink href="/">Home</NavLink>
                </NavItem>
                <UncontrolledDropdown nav inNavbar>
                  <DropdownToggle nav caret>
                    Tickers
                  </DropdownToggle>
                  <DropdownMenu right>
                    <DropdownItem href="/silas/GOOGL">
                      Alphabet (Google)
                    </DropdownItem>
                    <DropdownItem href="/silas/AMZN">Amazon</DropdownItem>
                    <DropdownItem href="/silas/AAPL">Apple</DropdownItem>
                    <DropdownItem href="/silas/FB">Facebook</DropdownItem>
                    <DropdownItem href="/silas/NFLX">Netflix</DropdownItem>
                    <DropdownItem href="/silas/SPY">S&P 500 ETF</DropdownItem>
                    {/* <DropdownItem href="/silas/">Microsoft</DropdownItem> */}
                    <DropdownItem divider />
                    <DropdownItem href="/">Home</DropdownItem>
                  </DropdownMenu>
                </UncontrolledDropdown>
              </Nav>
            </Collapse>
          </Navbar>
        </div>
        {/*  */}
        {/*  */}
        {/* Router */}
        <Router />
      </div>
    );
  }
}

export default App;
