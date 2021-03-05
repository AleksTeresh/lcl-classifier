export function persistStateToUrl<T>(
  state: T,
  prefix: string
): void {
  const params = new URLSearchParams(location.search)
  Object.entries(state).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      params.set(`${prefix}_${key}`, value)
    }
  })
  window.location.search = params.toString()
}

export function loadStateFromUrl<T>(
  initState: T,
  prefix: string
): T {
  const newState = {...initState}
  const params = new URLSearchParams(location.search)
  Object.keys(initState)
    .forEach((key) => {
      const valueInUrl = params.get(`${prefix}_${key}`)
      if (valueInUrl !== undefined && valueInUrl !== null) {
        if (valueInUrl === 'false' || valueInUrl === 'true') {
          newState[key] = (valueInUrl === 'true')
        } else {
          newState[key] = valueInUrl
        }
      }
    })
  return newState
}
