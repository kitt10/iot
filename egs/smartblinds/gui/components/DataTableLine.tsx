import React, { useContext } from 'react'
import { css } from '@emotion/react'
import { ts2date } from '../fcn/_tools'
import { DocumentI } from '../context/DataContext'
import TaskContext, { FeatureI, TargetI } from '../context/TaskContext'
import Icon from './atomic/Icon'

const lineS = (isTesting: boolean) => css({
  color: isTesting ? 'darkgray' : 'inherit'
})

interface DataTableLineI {
  document: DocumentI
  documentInd: number
}

const DataTableLine: React.FunctionComponent<DataTableLineI> = ({ document }) => {

  const { features, targets } = useContext(TaskContext)

  return (
    <tr css={lineS(document.testing)}>
      <td>
        <Icon fontSize='20px'>{document.periodical ? 'event_repeat' : 'sports_esports'}</Icon>
      </td>
      <td>
        {ts2date(document.timestamp)}
      </td>

      {features.map((feature: FeatureI, featureInd: number) => 
        <td key={'feature_'+featureInd}>
          {document.features[feature.name].toString()}
        </td> 
      )}

      {targets.map((target: TargetI, targetInd: number) => 
        <th key={'feature_'+targetInd}>
          {document.targets[target.name]}
        </th> 
      )}
    </tr>
  )
}

export default DataTableLine