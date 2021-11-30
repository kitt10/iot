import { useContext, useEffect } from 'react'
import { css } from '@emotion/react'
import TaskContext, { ClassifierI, FeatureI } from '../context/TaskContext'
import SimulatorContext from '../context/SimulatorContext'
import DataContext from '../context/DataContext'
import useSimulator from '../hooks/useSimulator'
import Page from '../components/core/Page'
import Header from '../components/Header'
import Content from '../components/Content'
import FeatureTuner from '../components/FeatureTuner'
import ClassifierBox from '../components/ClassifierBox'

const contentAS = () => css({
  display: 'flex',
  flexDirection: 'row'
})

const featureTunerFrameS = () => css({
  flexGrow: 0,
  flexBasis: 'fit-content',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'space-between'
})

const classificationFrameS = () => css({
  flexGrow: 1,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'flex-start',
  marginLeft: '50px',
  overflow: 'scroll'
})

const SimulatorPage = () => {

  const title: string = 'Smartblinds - Simulator'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  const { features, classifiers } = useContext(TaskContext)
  const { documents } = useContext(DataContext)
  const simulatorContext = useSimulator(documents[documents.length-1])

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='simulator' />
      <Content contentAS={contentAS}>
        <SimulatorContext.Provider value={simulatorContext}>
          <div css={featureTunerFrameS}>
            {Object.values(features).map((feature: FeatureI, featureInd: number) => 
              <FeatureTuner key={'FeatureTuner_'+featureInd} feature={feature} featureInd={featureInd} />
            )}
          </div>
          <div css={classificationFrameS}>
            {Object.values(classifiers).map((classifier: ClassifierI, classifierInd: number) => 
              <ClassifierBox key={'ClassifierBoxSim_'+classifierInd} classifier={classifier} classifierInd={classifierInd} />
            )}
          </div>
        </SimulatorContext.Provider>
      </Content>
    </Page>
  )
}

export default SimulatorPage
