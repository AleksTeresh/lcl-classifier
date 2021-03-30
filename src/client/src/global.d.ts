/* eslint no-var: "off" */

type KeysFunc = <T>(o: T) => (keyof T)[]
interface ObjectConstructor {
  typedKeys: KeysFunc
}

declare var PRODUCTION: boolean
