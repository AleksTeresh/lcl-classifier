export async function handleResponse<T>(
  response: Response
): Promise<T> {
  if (!response.ok) {
    // try to get `error` field from response body.
    // if not, fall back to statusText
    throw new Error((await response.json())?.error ?? response.statusText)
  } else {
    return response.json()
  }
}

// adapted from https://matthiashager.com/converting-snake-case-to-camel-case-object-keys-with-javascript
export const keysToSnake = function (o: any) {
  const n = {}
  Object.keys(o).forEach((k) => {
    n[toSnake(k)] = o[k]
  })

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

function isNil(x: any) {
  return x === undefined || x === null
}

// adapted from https://stackoverflow.com/questions/30970286/convert-javascript-object-camelcase-keys-to-underscore-case
function toSnake(key: string) {
  return key.replace(/([A-Z])/g, '_$1').toLowerCase()
}
