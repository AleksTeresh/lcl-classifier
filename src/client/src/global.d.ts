interface ObjectConstructor {
  typedKeys<T>(o: T): (keyof T)[]
}
