
export const get = async (url: string) => {
    const res = await fetch(url, {method: 'GET'})
    return await res.json()
}
  
export const post = async (url: string, signal:null|AbortSignal, params: any) => {
    let fetchParams:any = signal?{body: JSON.stringify(params), method: 'POST', signal: signal}:{body: JSON.stringify(params), method: 'POST'}
    const res = await fetch(url, fetchParams)
    return await res.json()
}