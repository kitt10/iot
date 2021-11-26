import { useEffect, useContext } from 'react'
import { GetServerSideProps } from 'next'
import { css } from '@emotion/react'
import TaskContext, { TaskI } from '../context/TaskContext'
import DataContext from '../context/DataContext'
import { useState } from 'react'
import { loadTask, loadData } from '../fcn/serverSide'
import Page from '../components/core/Page'
import { useRouter } from 'next/router'
import Header from '../components/Header'
import Content from '../components/Content'

export const getServerSideProps: GetServerSideProps = async (context) => {
  const task: TaskI = await loadTask()
  const data: Object[] = await loadData()

  return { props: {task: task, data: data} }
}

const contentAS = () => css({
  display: 'flex',
  flexDirection: 'column'
})

const blindsS = (countDown: number, animationTime: number) => css({
  width: '100%',
  flex: countDown/animationTime * 10,
  margin: '0 auto',
  backgroundColor: 'darkgray',
  borderBottom: '1px solid black'
})

const IndexPage = (props: {task: TaskI, data: Object[]}) => {

  const title: string = 'Smartblinds'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  const taskContext = useContext(TaskContext)
  const dataContext = useContext(DataContext)

  const animationTime: number = 1000    // [ms]
  const step: number = 10              // [ms]

  const router = useRouter()
  const [countDown, setCountDown] = useState(animationTime)

  const redirect = () => {
    router.push('/live')
  }

  useEffect(() => {
    /** Make the animation and then redirect to the /live page in 2 secs after load. */
    if (countDown > 0) {
      setTimeout(() => {setCountDown(countDown-step)}, step)
    } else {
      redirect()
    }
  }, [countDown])

  useEffect(() => {
    /** Fill in server-side loaded props. */
    taskContext.setTask(props.task.features, props.task.targets)
    dataContext.parseData(props.data)
  }, [])

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='index' />
      <Content contentAS={contentAS}>
        <div css={blindsS(countDown, animationTime)}>
          &nbsp;
        </div>
        <div css={{'flex': (10 - countDown/animationTime * 10)}}>
          &nbsp;
        </div>
      </Content>
    </Page>
  )
}

export default IndexPage
