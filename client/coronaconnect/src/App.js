import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route } from 'react-router-dom';

// component imports
import HomePageComponent from "./components/homepage.component"
// import FloorComponent from "./components/floor.component"
import DataComponent from "./components/dashboard/dashboard.component"
// import CheckInComponent from "./components/input/donationin.component"
import CheckInComponent from "./components/input/form.component"

// import DonationInComponent from "./components/input/donationin.component"



function App() {
  return (
    <Router>
      <div>
        <Route exact path="/" component={HomePageComponent}/>
        {/* <Route exact path="/floor" component={FloorComponent} /> */}
        <Route exact path="/data" component={DataComponent}/>
        <Route exact path="/input" component={CheckInComponent}/>        
        {/* <Route exact path="/donationin" component={DonationInComponent}/> */}

      </div>
    </Router>
  );
}

export default App;
