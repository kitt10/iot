import { useContext } from 'react'
import { css } from '@emotion/react'
import TaskContext, { ClassifierI, FeatureI } from '../context/TaskContext'
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
  border: '1px solid green'
})

const classificationFrameS = () => css({
  flexGrow: 1,
  display: 'flex',
  flexDirection: 'column',
  marginLeft: '50px',
  border: '1px solid blue'
})

const SimulatorPage = () => {

  const title: string = 'Smartblinds - Simulator'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  const { features, classifiers } = useContext(TaskContext)

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='simulator' />
      <Content contentAS={contentAS}>
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
      </Content>
    </Page>
  )
}

export default SimulatorPage
