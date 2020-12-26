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
      imagerecognized: null,
      selfdriving: '0'
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

  selfDriving(ctx,value) {
    ctx.setState({
      selfdriving: '0'
    });
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          var jsonResponse = JSON.parse(this.responseText);
          ctx.setState({
            selfdriving: jsonResponse.selfdriving
          });  
      }
    };
    var parameters="selfdriving="+value;
    xmlHttp.open("POST", "/movemanagement/selfDriving", true);
    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlHttp.overrideMimeType("application/json");
    xmlHttp.send(parameters);
  }  

  render() {
    const selfdrivingValueToSend = this.state.selfdriving == '0' ? '1' : '0';
    return (
        <React.Fragment>
          <div className="justify-content-center">
              <div id="joystickDiv" className="joystick-div"></div>
              <div className="container-recognize"> 
                <button className="button-recognize" onClick={() => this.recognize(this)} >
                  Recognize
                </button>
                {this.state.recognized ? (<div className="min-height">{this.state.recognized}</div>) : null}
                {this.state.imagerecognized ? (
                  <img id="idstream" className="recognized-image" src={this.state.imagerecognized}></img>
                ) : null}
                {this.state.selfdriving ? (<div className="min-height">{this.state.selfdriving}</div>) : null}
                <button className="button-recognize" onClick={() => this.selfDriving(this,selfdrivingValueToSend)} >
                    {this.state.selfdriving == '0' ? "Self Driving Activate" : "Self Driving Deactivate"} 
                </button>
              </div>
          </div>
        </React.Fragment>

    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);