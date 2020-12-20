import React, { Component } from "react";
import { render } from "react-dom";
import html2canvas from 'html2canvas';
import "../styles/iframe.scss"



class Iframe extends Component {

    constructor(props) {
        super(props);
        this.state = {
          recognized: null
        };
    }

    recognize(ctx,callback) {

	html2canvas(document.getElementById("iddiviframe")).then(
	     function(canvas) {
	          var base64Url = canvas.toDataURL('image/jpeg').replace('image/jpeg','image/octet-stream');
		  var xmlHttp = new XMLHttpRequest();
		  xmlHttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				var jsonResponse = JSON.parse(this.responseText);
				callback(ctx,jsonResponse.recognized);
			}
		  };
		  xmlHttp.open("POST", "/movemanagement/recognize", true);
		  xmlHttp.setRequestHeader("Content-type", "application/json");
		  
		  var parameters="image=" + base64Url;
		  xmlHttp.send(null);
	     }
	);

        /*var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
            var jsonResponse = JSON.parse(this.responseText);
            callback(ctx,jsonResponse.recognized);
            }
        };
        xmlHttp.open("GET", "/movemanagement/recognize", true);
        xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlHttp.overrideMimeType("application/json");

        xmlHttp.send(null);*/
    }      

    recognizeCallback(ctx,rec) {
        ctx.setState({
            recognized: rec
        });    
    }

    render() {
        const src = this.props.source;     
        return (
            // basic bootstrap classes. you can change with yours.
            <React.Fragment>
                {this.state.recognized ? (<div>{this.state.recognized}</div>) : null}
                <div onClick={() => this.recognize(this,this.recognizeCallback)} className="col-md-12">
                    <div id="iddiviframe" className="container-camera-view" >
                        <iframe id="idiframe" className="camera-view" src={src}></iframe>
                    </div>
                </div>
            </React.Fragment>
    
        );
    }


}

/*const Iframe = ({ source }) => {

    var recognized = null;
    var ctx = this;
    function recognize(callback) {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
            var jsonResponse = JSON.parse(this.responseText);
            callback(jsonResponse.recognized);
            }
        };
        xmlHttp.open("GET", "/movemanagement/recognize", true);
        xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlHttp.overrideMimeType("application/json");

        xmlHttp.send(null);
    }                                   

      function recognizeCallback(rec) {
      
          this.recognized = rec;      

      }

    if (!source) {
        return <div>Loading...</div>;
    }

    const src = source;     
    return (
        // basic bootstrap classes. you can change with yours.
        <React.Fragment>
            {recognized ? (<div>{recognized}</div>) : null}
            <div onClick={recognize(recognizeCallback)} className="col-md-12">
                <div className="container-camera-view" >
                    <iframe className="camera-view" src={src}></iframe>
                </div>
            </div>
        </React.Fragment>

    );
};*/

export default Iframe;