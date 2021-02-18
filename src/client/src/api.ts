import type { Problem } from "./types"

async function handleResponse(response: Response) {
  if (!response.ok) {
    // try to get `error` field from response body.
    // if not, fall back to statusText
    throw new Error((await response.json())?.error ?? response.statusText)
  } else {
    return response.json()
  }
}

function isNil(x: any) {
  return x === undefined || x === null
}

type UrlParam = [string, string[] | string | number | boolean | undefined | null]
function urlWithParams(url: string, params: readonly UrlParam[]): string {
  const paramString = new URLSearchParams(
    params
      .filter(([, value]) => !isNil(value))
      .filter(([, value]) => value !== '')
      .flatMap(([key, value]) => Array.isArray(value)
        ? value.map(v => [key, `${v}`])
        : [[key, `${value}`]])
  ).toString()

  const hasParams = paramString.length > 0
  return `${url}${hasParams ? '?' : ''}${paramString}`
}

export async function getProblem(problem: Problem) {
  const url = urlWithParams(
    'http://localhost:5000/api/classifier/problem',
    [
      ['is_tree', problem.isTree],
      ['is_cycle', problem.isCycle],
      ['is_path', problem.isPath],
      ['is_directed', problem.isDirected],
      ['is_rooted', problem.isRooted],
      ['is_regular', problem.isRegular],
      ['active_constraints', problem.activeConstraints],
      ['passive_constraints', problem.passiveConstraints],
      ['leaf_constraints', problem.leafConstraints],
      ['root_constraints', problem.rootConstraints],
    ]
  )
  const response = await fetch(url)
  return handleResponse(response)
}
