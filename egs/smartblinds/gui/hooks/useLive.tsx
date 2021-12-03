import { useState } from 'react'
import { ts2date } from '../fcn/_tools'
import { LiveContextI } from '../context/LiveContext'
import { DocumentI } from '../context/DataContext'
import { FeatureI } from '../context/TaskContext'

export const useLive = () => {

    const [samplesTitle, setSamplesTitle] = useState('')

    const updateSamplesTitle = (doc: DocumentI, feature: FeatureI) => {
        let newText = ts2date(doc.timestamp)+': '+feature.name+' = '+doc.features[feature.name]+' ('
        newText += doc.periodical ? 'periodical' : 'event'
        if (doc.testing) newText += ', testing'
        newText += ')'
        setSamplesTitle(newText)
      }

    const liveContext: LiveContextI = {
        samplesTitle: samplesTitle,
        updateSamplesTitle: updateSamplesTitle,
        setSamplesTitle: setSamplesTitle
    }

    return liveContext
}

export default useLive
