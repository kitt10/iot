import { css } from '@emotion/react'
import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'
import InfoBar from '../components/InfoBar'
import BlindStateAndControlTable from '../components/BlindStateAndControlTable'
import { useContext } from 'react'
import useTask from '../hooks/useTask'
import TaskContext, { TargetI } from '../context/TaskContext'
import useControl from '../hooks/useControl'
import ControlContext from '../context/ControlContext'
import DataContext from '../context/DataContext'
import BlindControlVisualization from '../components/BlindControlVisualization'
import CheckBox from '../components/atomic/CheckBox'

const contentAS = () => css({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center'
  })

const wsStatusS = (connected:boolean) => css({
    marginRight: '30px',
    marginTop: '20px',
    textAlign: 'right',
    fontSize: '18px',
    color: `${connected?"green":"red"}`,
    cursor: 'pointer'
  })

const wsTextState = (wsReadyState:number|null) => {
  switch(wsReadyState){
    case 0: return "Connecting";
    case 1: return "Connected";
    case 2: return "Disconnecting";
    case 3: return "Disonnected";
    default: return "Not a browser";
  }
}

const ControlPage = () => {

    const title: string = 'Smartblinds - Control'
    const description: string = 'Vojtěch Breník - The Smartblinds Project.'

    const {targets} = useContext(TaskContext)
    const { documents } = useContext(DataContext);
    const controlContext = useControl(documents[documents.length-1].targets)
    return (
      <Page title={title} description={description}>
        <Header titleText={title} currentPage='control' />
        <div onClick={controlContext.reconnectWS} css={wsStatusS(controlContext.wsState==1)}>{wsTextState(controlContext.wsState)}</div>
        <Content contentAS={contentAS}>
          <ControlContext.Provider value={controlContext}>
            <BlindStateAndControlTable targets={targets}/>
            <CheckBox labelText='Test Mode' onChange={(e) => controlContext.setTestMode((e.target as HTMLInputElement).checked)} defaultChecked={true}/>
            <BlindControlVisualization targets={targets}/>
          </ControlContext.Provider>
        </Content>
        <InfoBar />
      </Page>
    )
  }
  
export default ControlPage