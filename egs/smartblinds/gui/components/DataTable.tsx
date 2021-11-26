import React, { useContext } from 'react'
import { css } from '@emotion/react'
import DataContext, { DocumentI } from '../context/DataContext'
import TaskContext, { FeatureI, TargetI } from '../context/TaskContext'
import DataTableLine from './DataTableLine'

const tableS = () => css({
  flexGrow: 1,
  fontSize: '12px',
  textAlign: 'center',
  'th': {
    border: '1px solid lightgray'
  }
})

const thS = () => css({
})

const DataTable: React.FunctionComponent = () => {

  const { features, targets } = useContext(TaskContext)
  const { documents } = useContext(DataContext)

  return (
    <table css={tableS} cellSpacing='10px'>
      <thead>
        <tr>
          <td>&nbsp;</td>
          <th>{'DateTime'}</th>
          {Object.values(features).map((feature: FeatureI, featureInd: number) => 
            <th key={featureInd} css={thS}>
              {'F'+(featureInd+1)}
            </th>
          )}
          {Object.values(targets).map((target: TargetI, targetInd: number) => 
            <th key={targetInd}  css={thS}>
              {'T'+(targetInd+1)}
            </th>
          )}
        </tr>
      </thead>
      <tbody>
        {documents.map((document: DocumentI, docInd: number) => 
          <DataTableLine key={docInd} document={document} documentInd={docInd} /> 
        )}
      </tbody>
    </table>
  )
}

export default DataTable