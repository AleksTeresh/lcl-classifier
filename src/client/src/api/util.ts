import type {
  ProblemRequest,
  Query,
  ProblemCountResponse,
  QueryResponse,
  FindProblemResponse,
} from '../types'

const isArray = function (a: AllowedReturnValues): a is AllowedReturnValues[] {
  return Array.isArray(a)
}

const isObject = function (
  o: AllowedReturnValues
): o is { [key: string]: AllowedReturnValues } {
  return o === Object(o) && !isArray(o) && typeof o !== 'function'
}

const toCamel = (s: string): string => {
  return s.replace(/([-_][a-z])/gi, ($1) => {
    return $1.toUpperCase().replace('-', '').replace('_', '')
  })
}

// adapted from https://stackoverflow.com/questions/30970286/convert-javascript-object-camelcase-keys-to-underscore-case
const toSnake = (key: string): string => {
  return key.replace(/([A-Z])/g, '_$1').toLowerCase()
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

type AllowedReturnValues = unknown
type ReturnType = ProblemCountResponse | QueryResponse | FindProblemResponse
// adapted from https://matthiashager.com/converting-snake-case-to-camel-case-object-keys-with-javascript
export const keysToCamel = function (
  o: AllowedReturnValues
): AllowedReturnValues {
  if (isObject(o)) {
    return Object.keys(o).reduce<ReturnType>((acc: ReturnType, k: string) => {
      return { ...acc, [toCamel(k)]: keysToCamel(o[k]) }
    }, {} as ReturnType)
  } else if (isArray(o)) {
    return o.map((i) => {
      return keysToCamel(i)
    })
  }

  return o
}
