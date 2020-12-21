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
      placeholder: "Loading",
      recognized: null,
      imagerecognized: null
    };
  }

  componentDidMount() {
 
  }
  /* <Iframe source={"http://192.168.1.3:8082?action=stream"} /> */

  recognize(ctx) {
    ctx.setState({
      recognized: null,
      imagerecognized: null
    });
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          var jsonResponse = JSON.parse(this.responseText);
          ctx.setState({
            recognized: jsonResponse.recognized,
            imagerecognized: "data:image/jpeg;base64,"+jsonResponse.imagerecognized
          });  
      }
    };
    xmlHttp.open("GET", "/movemanagement/recognize", true);
    xmlHttp.setRequestHeader("Content-type", "application/json");
    xmlHttp.send(null);

  }   

  render() {
 
    return (
        <React.Fragment>
          <div className="justify-content-center">
              <div id="joystickDiv" className="joystick-div"></div>
              <div className="container-recognize"> 
                <button className="button-recognize" value="Recognize" onClick={() => this.recognize(this)} >
                  Recognize
                </button>
                {this.state.recognized ? (<div className="min-height">{this.state.recognized}</div>) : null}
                {this.state.imagerecognized ? (
                  <img id="idstream" className="recognized-image" src={this.state.imagerecognized}></img>
                ) : null}
              </div>
          </div>
        </React.Fragment>

    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);