import { useEffect, useContext } from 'react'
import { GetServerSideProps } from 'next'
import { css } from '@emotion/react'
import { useState } from 'react'
import Page from '../components/core/Page'
import { useRouter } from 'next/router'
import Header from '../components/Header'
import Content from '../components/Content'
import TaskContext, { TaskI } from '../context/TaskContext'
import { loadTask } from '../fcn/serverSide'

export const getServerSideProps: GetServerSideProps = async (context) => {
  const task: TaskI = await loadTask()
  return { props: {task: task} }
}

const blindsS = (countDown: number, animationTime: number) => css({
  width: '100%',
  flex: countDown/animationTime * 10,
  margin: '0 auto',
  backgroundColor: 'darkgray',
  borderBottom: '1px solid black'
})

const IndexPage = (props: {task: TaskI}) => {

  const title: string = 'Smartblinds'
  const description: string = 'Vojtěch Breník - The Smartblinds Project.'

  const animationTime: number = 1000    // [ms]
  const step: number = 10              // [ms]

  const router = useRouter()
  const [countDown, setCountDown] = useState(animationTime)
  const taskContext = useContext(TaskContext)

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
    console.log('Loaded props:', props)
    /** Fill in server-side loaded props. */
    taskContext.setTask(props.task.features, props.task.targets)
  }, [])

  return (
    <Page title={title} description={description}>
      <Header titleText={title} currentPage='index' />
      <Content>
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
