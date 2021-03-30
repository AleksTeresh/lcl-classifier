import type { Type } from 'io-ts'
import * as Either from 'fp-ts/lib/Either'
import { PathReporter } from 'io-ts/PathReporter'
import { keysToCamel } from './util'

async function handleResponse(response: Response): Promise<unknown> {
  if (!response.ok) {
    // try to get `error` field from response body.
    // if not, fall back to statusText
    throw new Error((await response.json())?.error ?? response.statusText)
  }
  return await response.json()
}

function validateResponse<T>(json: unknown, codec: Type<T>): T {
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
    const json = await handleResponse(response)
    const camelized = keysToCamel(json)
    return validateResponse(camelized, codec)
  } catch (e) {
    alert(e.message)
    return undefined
  }
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
