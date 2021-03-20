import type {
  Query,
  QueryResponse,
  ProblemCountResponse,
  FindProblemResponse,
  ProblemRequest
} from './types'
import {
  FindProblemResponseCodec,
  QueryResponseCodec,
  ProblemCountResponseCodec,
} from './types'
import { urlWithParams, keysToSnake, handleResponse } from './apiHelpers'

// PRODUCTION variable needs to be in .svelte file
// that's the reason why isProd is passed as a param here
export async function getProblem(
  problem: ProblemRequest,
  isProd: boolean
): Promise<FindProblemResponse> {
  const url = urlWithParams(
    `${isProd ? '' : 'http://localhost:5000'}/api/classifier/problem`,
    Object.entries(keysToSnake(problem))
  )
  const response = await fetch(url)
  return handleResponse(response, FindProblemResponseCodec)
}

// PRODUCTION variable needs to be in .svelte file
// that's the reason why isProd is passed as a param here
export async function getQueryResult(
  query: Query,
  isProd: boolean
): Promise<QueryResponse> {
  const url = urlWithParams(
    `${isProd ? '' : 'http://localhost:5000'}/api/classifier/query`,
    Object.entries(keysToSnake(query))
  )
  const response = await fetch(url)
  return handleResponse(response, QueryResponseCodec)
}

// PRODUCTION variable needs to be in .svelte file
// that's the reason why isProd is passed as a param here
export async function getTotalProblemCount(
  isProd: boolean
): Promise<ProblemCountResponse> {
  const url = `${isProd ? '' : 'http://localhost:5000'}/api/problem_count`
  const response = await fetch(url)
  return handleResponse(response, ProblemCountResponseCodec)
}
