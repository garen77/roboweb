import React, { Component } from "react";
import "../styles/iframe.scss"



class Iframe extends Component {

    constructor(props) {
        super(props);
        this.state = {
          recognized: null
        };
    }

    recognize(ctx) {

        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
              var jsonResponse = JSON.parse(this.responseText);
              ctx.setState({
                recognized: rec
              });  
          }
        };
        xmlHttp.open("GET", "/movemanagement/recognize", true);
        xmlHttp.setRequestHeader("Content-type", "application/json");
        xmlHttp.send(null);

    }      

    render() {
        const src = this.props.source;     
        return (
            // basic bootstrap classes. you can change with yours.
            <React.Fragment>
                {this.state.recognized ? (<div>{this.state.recognized}</div>) : null}
                <div onClick={() => this.recognize(this)} className="col-md-12">
                    <div id="iddiviframe" className="container-camera-view" >
                        <iframe id="idiframe" className="camera-view" src={src}></iframe>
                    </div>
                </div>
            </React.Fragment>
    
        );
    }


}


export default Iframe;