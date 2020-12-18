import React, { Component } from "react";
import { render } from "react-dom";
import Iframe from './iframe';
import "../styles/App.scss"

class App extends Component {


  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
 
  }
  
  render() {
 
    return (
        <React.Fragment>
          <div className="justify-content-center">
              <div id="joystickDiv" className="joystick-div"></div>
          </div>
          <Iframe source={"http://192.168.1.3:8082?action=stream"} />
        </React.Fragment>

      
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);