import type { Type } from 'io-ts'
import * as Either from 'fp-ts/lib/Either'
import { PathReporter } from 'io-ts/PathReporter'
import type { ProblemRequest, Query } from '../types'

async function handleResponse<T>(
  response: Response,
  codec: Type<T>
): Promise<T> {
  if (!response.ok) {
    // try to get `error` field from response body.
    // if not, fall back to statusText
    throw new Error((await response.json())?.error ?? response.statusText)
  }
  const json = await response.json()
  const result = codec.decode(json)
  if (Either.isRight(result)) {
    return result.right
  } else {
    throw Error(PathReporter.report(result).join('\n'))
  }
}

export async function fetchJson<T>(
  url: string,
  codec: Type<T>
): Promise<T | undefined> {
  let response
  try {
    response = await fetch(url)
  } catch (e) {
    console.error(e)
    return undefined
  }

  try {
    return await handleResponse(response, codec)
  } catch (e) {
    alert(e.message)
    return undefined
  }
}

type AllowedValues = ProblemRequest[keyof ProblemRequest] | Query[keyof Query]
// adapted from https://matthiashager.com/converting-snake-case-to-camel-case-object-keys-with-javascript
export const keysToSnake = function <
  T extends { [key: string]: AllowedValues },
  S extends { [key: string]: AllowedValues }
>(o: T): S {
  const n: S = Object.typedKeys(o).reduce<S>((acc: S, k: keyof T) => {
    return { ...acc, [toSnake(k as string)]: o[k] }
  }, {} as S)
  return n
}

type UrlParam = [
  string,
  string[] | string | number | boolean | undefined | null
]
export function urlWithParams(
  url: string,
  params: readonly UrlParam[]
): string {
  const paramString = new URLSearchParams(
    params
      .filter(([, value]) => !isNil(value))
      .filter(
        ([, value]) =>
          value !== '' &&
          (!Array.isArray(value) || value.length !== 1 || value[0] !== '')
      )
      .flatMap(([key, value]) =>
        Array.isArray(value)
          ? value.map((v) => [key, `${v}`])
          : [[key, `${value}`]]
      )
  ).toString()

  const hasParams = paramString.length > 0
  return `${url}${hasParams ? '?' : ''}${paramString}`
}

type Nil = undefined | null
function isNil<R>(x: R | Nil): x is Nil {
  return x === undefined || x === null
}

// adapted from https://stackoverflow.com/questions/30970286/convert-javascript-object-camelcase-keys-to-underscore-case
function toSnake(key: string): string {
  return key.replace(/([A-Z])/g, '_$1').toLowerCase()
}
