
export const r2 = (num: number) => {
    return Math.round(num * 100) / 100
}

export const r4 = (num: number) => {
    return Math.round(num * 10000) / 10000
}

export const formatSecs = (secs: number) => {
    if (secs < 0.000001) {
        return r4(secs*1000000)+' ns'
    } else if (secs < 0.001) {
        return r4(secs*1000)+' ms'
    } else if (secs > 60) {
        return r4(secs/60)+' min'
    } else {
        return r4(secs)+' s'
    }
}

export const ts2date = (ts: number) => {
    return new Date(ts*1000).toLocaleString()
}