import type { Problem, Query } from './types'
import { urlWithParams, keysToSnake, handleResponse } from './apiHelpers'

// PRODUCTION variable needs to be in .svelte file
// that's the reason why isProd is passed as a param here
export async function getProblem(problem: Problem, isProd: boolean) {
  const url = urlWithParams(
    `${isProd ? '' : 'http://localhost:5000'}/api/classifier/problem`,
    Object.entries(keysToSnake(problem))
  )
  const response = await fetch(url)
  return handleResponse(response)
}

// PRODUCTION variable needs to be in .svelte file
// that's the reason why isProd is passed as a param here
export async function getQueryResult(query: Query, isProd: boolean) {
  const url = urlWithParams(
    `${isProd ? '' : 'http://localhost:5000'}/api/classifier/query`,
    Object.entries(keysToSnake(query))
  )
  const response = await fetch(url)
  return handleResponse(response)
}

// PRODUCTION variable needs to be in .svelte file
// that's the reason why isProd is passed as a param here
export async function getTotalProblemCount(isProd: boolean) {
  const url = `${isProd ? '' : 'http://localhost:5000'}/api/problem_count`
  const response = await fetch(url)
  return handleResponse(response)
}

