
export const get = async (url: string) => {
    const res = await fetch(url, {method: 'GET'})
    return await res.json()
}
  
export const post = async (url: string, params: any) => {
    const res = await fetch(url, {body: JSON.stringify(params), method: 'POST'})
    return await res.json()
}