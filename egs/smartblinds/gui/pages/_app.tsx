import type { AppProps } from 'next/app'
import { Global } from '@emotion/react'
import PageContext, { PageContextI } from '../context/PageContext'
import TaskContext, { TaskContextI } from '../context/TaskContext'
import DataContext, { DataContextI } from '../context/DataContext'
import { usePage } from '../hooks/usePage'
import { useTask } from '../hooks/useTask'
import { useData } from '../hooks/useData'


const MainApp = ({ Component, pageProps }: AppProps) => {

  const pageContext: PageContextI = usePage()
  const taskContext: TaskContextI = useTask()
  const dataContext: DataContextI = useData()

  return (
    <PageContext.Provider value={pageContext}>
      <TaskContext.Provider value={taskContext}>
        <DataContext.Provider value={dataContext}>
          <Global styles={pageContext.style.globalStyle} />
          <Component {...pageProps} />
        </DataContext.Provider>
      </TaskContext.Provider>
    </PageContext.Provider>
  )
}

export default MainApp
