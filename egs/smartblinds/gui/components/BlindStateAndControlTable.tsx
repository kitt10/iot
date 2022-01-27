import React, { useContext } from 'react'
import InputBox from './atomic/InputBox'
import { TargetI } from '../context/TaskContext'
import DataContext, { TargetsValuesI } from '../context/DataContext';
import { css } from '@emotion/react';
import ControlContext from '../context/ControlContext';
import useControl from '../hooks/useControl';

interface TargetTunerI{
    target: TargetI,
    targetInd: number
}

export interface TargetsTunerI{
    targets: TargetI[]
}

const tableS = () => css`
    flex-grow: 1;
    font-size: 12px;
    text-align: center;
    margin: 3% 0 3% 0;
    th {
      border: 1px solid lightgray;
      padding: 7px;
    }
    tbody tr:hover {
        background: darkgrey
    }
  }
  `

const StateAndControlRow: React.FunctionComponent<TargetTunerI> = ({target, targetInd}) => {
    const controlContext = useContext(ControlContext);
    return(
        <tr>
            <th>{target.name}</th>
            <td key={target.name}>{controlContext.targetVector[target.name]}</td>
            <td><input type="number" onChange={(e) => {controlContext.setNewTarget(e.target.name, parseInt(e.target.value)); controlContext.setPreview(true)}} name={target.name} id={"new" + target.name} min={target.min} max={target.max}/></td>
            <td><button onClick={() => controlContext.updateBlindState(target.name)} id={"set"+target.name+"button"}>Set {target.name}</button></td>
        </tr>
    )
}

const tblhead = ['Current state', 'New State', 'Set state'];

const BlindStateAndControlTable: React.FunctionComponent<TargetsTunerI> = (targets) => { 
    //var currentState:TargetsValuesI = {'position': 53, 'tilt': 38};
    const { documents } = useContext(DataContext);
    // const controlContext = useControl(documents[documents.length-1].targets)
    const controlContext = useContext(ControlContext);
    //const controlContext = useControl(currentState);

    return (
        <table css={tableS}>
            <thead>
                <tr>
                    <th ></th>
                    {tblhead.map((value: String) =>
                    <th>{value}</th>
                    )}
                </tr>
            </thead>
            <tbody>
                {Object.values(targets.targets).map((target: TargetI, targetInd: number) => 
                <ControlContext.Provider value={controlContext}>
                <StateAndControlRow target={target} targetInd={targetInd}/>
                </ControlContext.Provider>
                )}
            </tbody>
        </table>
    )
}

export default BlindStateAndControlTable;