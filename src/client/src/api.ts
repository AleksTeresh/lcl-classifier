import type { Problem, Query } from "./types"
import { urlWithParams, keysToSnake, handleResponse } from './apiHelpers'

export async function getProblem(problem: Problem, isProd: boolean) {
  const url = urlWithParams(
    `${isProd ? '' : 'http://localhost:5000'}/api/classifier/problem`,
    Object.entries(keysToSnake(problem))
  )
  const response = await fetch(url)
  return handleResponse(response)
}

export async function getQueryResult(query: Query, isProd: boolean) {
  const url = urlWithParams(
    `${isProd ? '' : 'http://localhost:5000'}/api/classifier/query`,
    Object.entries(keysToSnake(query))
  )
  const response = await fetch(url)
  return handleResponse(response)
}
