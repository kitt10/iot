import { TargetsTunerI } from "./BlindStateAndControlTable";
import React, { useContext } from "react";
import { css } from "@emotion/react";
import ControlContext from "../context/ControlContext";
import { createMap } from "../fcn/_tools";

const BlindControlVisualization: React.FunctionComponent<TargetsTunerI> = (targets) => {
    const controlContext = useContext(ControlContext)
    const slatsN = 11;
    const slatsSpacing = 25;

    const pospercent = createMap(0, 250, 100, 0);
    const percentpos = createMap(100, 0, 0, 250);
    const angle2tilt = createMap(0, 87, 100, 0);
    const tilt2angle = createMap(100, 0, 0, 87);

    const slatS = (N:number) => {
        let output = css``
        let targets = controlContext.preview?controlContext.targetNew:controlContext.targetVector
        let pos = percentpos(targets['position']);
        let tlt = tilt2angle(targets['tilt']);
        for(let i=1;i<=N;i++){
            output = css`${output}
            .slat:nth-of-type(${i}){
                transform-origin: 20px 2px;
                transform: translate(5px, ${((pos-250)+((i-1)*slatsSpacing))}px) rotate(${tlt}deg);
            }`
        }
        return output;
    }

    const svgS = css({
        border: '1px solid black'
    });

    const blindS = css`
    padding: 5% 0 3% 0;
    background-color: #a8a8a8;
    text-align: center;
    border: 2px solid #8a8a8a;
    position: relative;
    flex-grow: 1;
    text-align: center;
    min-width: 35%;
    max-height: 290px;
    margin: 2% 0 0 0;
    #loading, #preview {
        position: absolute;
        top: 3%;
    }
    
    #loading {
        right: 2%;
        visibility: ${controlContext.loading?"visible":"hidden"};
    }
    
    #preview {
        right: 2%;
        visibility: ${controlContext.preview?"visible":"hidden"};
    }
    ${slatS(slatsN)}
    `
    return(
        <div css={blindS} id="blind">
            <svg css={svgS} className="blind" width="50" height="275" xmlns="http://www.w3.org/2000/svg">
                <rect className="slat" width="40" height="4" />
                <rect className="slat" width="40" height="4" />
                <rect className="slat" width="40" height="4" />
                <rect className="slat" width="40" height="4" />
                <rect className="slat" width="40" height="4" />
                <rect className="slat" width="40" height="4"/>
                <rect className="slat" width="40" height="4" />
                <rect className="slat" width="40" height="4" />
                <rect className="slat" width="40" height="4" />
                <rect className="slat" width="40" height="4" />
                <rect className="slat last" width="40" height="4" />
            </svg>
            <div id="preview">Preview<br/><button onClick={() => controlContext.setPreview(false)}>Reset</button></div>
            <svg id="loading" viewBox="0 0 20 20" height="20" width="20">
                <circle cx="10" cy="10" r="8" fillOpacity="0" strokeDasharray="40, 10.4" stroke="black" strokeWidth="2px">
                <animateTransform attributeName="transform" attributeType="XML" type="rotate" dur="1s"  from="0 10 10" to="360 10 10" repeatCount="indefinite"/>
                </circle>
            </svg>
        </div>
    )
}

export default BlindControlVisualization