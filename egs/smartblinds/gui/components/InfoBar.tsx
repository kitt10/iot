import React, { useContext } from 'react'
import { css } from '@emotion/react'
import TaskContext from '../context/TaskContext'
import { formatSecs, ts2date } from '../fcn/_tools'


const componentS = () => css({
  flexGrow: 0,
  width: 'calc(100% - 50px)',
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-between',
  marginLeft: '25px',
  marginRight: '25px',
  marginTop: '25px',
  paddingTop: '5px',
  paddingBottom: '5px',
  fontSize: '12px',
  color: 'darkgray',
  borderTop: '1px solid #ddd',
  borderBottom: '1px solid #ddd'
})

const infoItemS = () => css({
  
})


const InfoBar: React.FunctionComponent = () => {

  const { taskInfo, classifiers } = useContext(TaskContext)

  return (
    <div css={componentS}>
      <div css={infoItemS}>
        {'Train time | Control time | Last retrained | N samples'}
        {classifiers.map((cl) =>
          cl.trainable && ' :: '+cl.name+': '+formatSecs(cl.trainTime)+' | '+formatSecs(cl.controlTime)+' | '+ts2date(cl.retrained)+' | '+cl.nSamples
        )}
      </div>
      <div css={infoItemS}>
        {'Next training: '+ts2date(taskInfo.nextTraining)}
      </div>
    </div>
  )
}

export default InfoBar