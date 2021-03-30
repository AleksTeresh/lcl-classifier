import type {
  Query,
  QueryResponse,
  ProblemCountResponse,
  FindProblemResponse,
  ProblemRequest,
} from '../types'
import {
  FindProblemResponseCodec,
  QueryResponseCodec,
  ProblemCountResponseCodec,
} from '../types'
import { urlWithParams, fetchJson } from './apiHelpers'
import { keysToSnake } from './util'

// PRODUCTION variable needs to be in .svelte file
// that's the reason why isProd is passed as a param here
export async function getProblem(
  problem: ProblemRequest,
  isProd: boolean
): Promise<FindProblemResponse | undefined> {
  const url = urlWithParams(
    `${isProd ? '' : 'http://localhost:5000'}/api/classifier/problem`,
    Object.entries(keysToSnake(problem))
  )
  return fetchJson(url, FindProblemResponseCodec)
}

// PRODUCTION variable needs to be in .svelte file
// that's the reason why isProd is passed as a param here
export async function getQueryResult(
  query: Query,
  isProd: boolean
): Promise<QueryResponse | undefined> {
  const url = urlWithParams(
    `${isProd ? '' : 'http://localhost:5000'}/api/classifier/query`,
    Object.entries(keysToSnake(query))
  )
  return fetchJson(url, QueryResponseCodec)
}

// PRODUCTION variable needs to be in .svelte file
// that's the reason why isProd is passed as a param here
export async function getTotalProblemCount(
  isProd: boolean
): Promise<ProblemCountResponse | undefined> {
  const url = `${isProd ? '' : 'http://localhost:5000'}/api/problem_count`
  return fetchJson(url, ProblemCountResponseCodec)
}
