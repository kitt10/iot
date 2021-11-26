import type { AppProps } from 'next/app'
import { Global } from '@emotion/react'
import PageContext, { PageContextI } from '../context/PageContext'
import TaskContext, { TaskContextI } from '../context/TaskContext'
import { usePage } from '../hooks/usePage'
import { useTask } from '../hooks/useTask'


const MainApp = ({ Component, pageProps }: AppProps) => {

  const pageContext: PageContextI = usePage()
  const taskContext: TaskContextI = useTask()

  return (
    <PageContext.Provider value={pageContext}>
      <TaskContext.Provider value={taskContext}>
        <Global styles={pageContext.style.globalStyle} />
        <Component {...pageProps} />
      </TaskContext.Provider>
    </PageContext.Provider>
  )
}

export default MainApp
