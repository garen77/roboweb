import React, { Component } from "react";
import { render } from "react-dom";
//import Iframe from './iframe';

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
    const mystyle = {
        width: "200px",
        height: "200px",
        position: "fixed",
        left: "50%",
        marginLeft: "-100px"
    };
    //<!Iframe source={"http://192.168.1.3:8082/?action=stream"} />
    return (
          <div className="justify-content-center">
              <div id="joystickDiv" style={mystyle}></div>
          </div>
      
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);