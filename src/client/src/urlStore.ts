import type { Type } from 'io-ts'
import * as Either from 'fp-ts/lib/Either'
import { PathReporter } from 'io-ts/PathReporter'
import { isNumeric } from './typeUtil'

export function persistStateToUrl<T>(state: T, prefix: string): void {
  const params = new URLSearchParams(location.search)
  Object.entries(state).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      params.set(`${prefix}_${key}`, value)
    }
  })
  window.location.search = params.toString()
}

type AllowedProperty = boolean | string | number | undefined
export function loadStateFromUrl<T extends { [key: string]: AllowedProperty }>(
  initState: T,
  prefix: string,
  codec: Type<T>
): T | undefined {
  const newState = { ...initState }
  const params = new URLSearchParams(location.search)
  Object.typedKeys(initState).forEach((key: keyof T) => {
    const valueInUrl = params.get(`${prefix}_${key}`)
    if (valueInUrl !== undefined && valueInUrl !== null) {
      if (valueInUrl === 'false' || valueInUrl === 'true') {
        ;(newState[key] as AllowedProperty) = valueInUrl === 'true'
      } else if (isNumeric(valueInUrl)) {
        ;(newState[key] as AllowedProperty) = parseFloat(valueInUrl)
      } else {
        ;(newState[key] as AllowedProperty) = valueInUrl
      }
    }
  })
  const result = codec.decode(newState)
  if (Either.isRight(result)) {
    return result.right
  } else {
    const errorMessage = PathReporter.report(result).join('\n')
    alert(errorMessage)
    return undefined
  }
}
