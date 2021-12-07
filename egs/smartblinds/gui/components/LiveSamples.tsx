import React, { useContext } from 'react'
import { css } from '@emotion/react'
import TaskContext, { FeatureI } from '../context/TaskContext'
import DataContext, { DocumentI } from '../context/DataContext'
import LiveContext from '../context/LiveContext'
import LiveSampleColumn from './LiveSamplesColumn'


const componentS = () => css({
  flexBasis: '40%',
  maxWidth: '40%',
  display: 'flex',
  flexDirection: 'row'
})

const featureIdsS = () => css({
  display: 'flex',
  flexDirection: 'column'
})

const featureIdS = (lineNb: number) => css({
  flexBasis: '6.6%',
  width: '35px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: lineNb % 2 == 0 ? '#ddd' : '#fff'
})

const samplesS = () => css({
  flexBasis: 'calc(100% - 37px)',
  maxWidth: 'calc(100% - 37px)',
  overflow: 'scroll',
  display: 'flex',
  flexDirection: 'row-reverse',
  borderRight: '1px solid #ddd'
})

const titleBoxS = (titleText: string) => css({
  display: titleText == '' ? 'none' : 'flex',
  position: 'absolute',
  bottom: '30px',
  left: '25px',
  zIndex: 100,
  backgroundColor: 'lime',
  fontSize: '11px',
  padding: '2px',
  border: '1px solid darkgray'
})

const LiveSamples: React.FunctionComponent = () => {

  const { features } = useContext(TaskContext)
  const { documents } = useContext(DataContext)
  const { samplesTitle, setSamplesTitle } = useContext(LiveContext)

  return (
    <div css={componentS} onMouseOut={() => setSamplesTitle('')}>
      <div css={featureIdsS}>
        {Object.values(features).map((feature: FeatureI, featureInd: number) => 
          <div key={featureInd} css={featureIdS(featureInd)}>
            {'F'+(featureInd+1)}
          </div>
        )}
      </div>
      <div css={samplesS}>
        {documents.map((document: DocumentI, docInd: number) => 
          <LiveSampleColumn key={'sampleCol_'+docInd} 
                            doc={document} 
                            docInd={docInd} 
                            nDocs={documents.length} />
        )}
      </div>
      <div css={titleBoxS(samplesTitle)}>
        {samplesTitle}
      </div>
    </div>
  )
}

export default LiveSamples