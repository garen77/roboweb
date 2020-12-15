import React from 'react';
import "../styles/iframe.scss"

const Iframe = ({ source }) => {

    if (!source) {
        return <div>Loading...</div>;
    }

    const src = source;     
    return (
        // basic bootstrap classes. you can change with yours.
        <div className="col-md-12">
            <div className="container-camera-view" >
                <iframe className="camera-view" src={src}></iframe>
            </div>
        </div>
    );
};

export default Iframe;