export const readyQueries = [
  {
    href: `${window.location.origin}/?query_graphType=path&query_isDirectedOrRooted=true&query_isRegular=true&query_randLowerBound=%281%29&query_randUpperBound=unsolvable&query_detLowerBound=%281%29&query_detUpperBound=unsolvable&query_activeDegree=2&query_passiveDegree=2&query_labelCount=3&query_activesAllSame=false&query_passivesAllSame=false&query_largestProblemOnly=false&query_smallestProblemOnly=false&query_completelyRandUnclassifiedOnly=false&query_partiallyRandUnclassifiedOnly=false&query_completelyDetUnclassifiedOnly=false&query_partiallyDetUnclassifiedOnly=false&query_excludeIfConfigHasAllOf=&query_excludeIfConfigHasSomeOf=&query_includeIfConfigHasAllOf=&query_includeIfConfigHasSomeOf=&query_fetchStatsOnly=false`,
    linkText: 'All 3-label problem on directed paths',
    afterText: ''
  },
  {
    href: `${window.location.origin}/?query_graphType=tree&query_isDirectedOrRooted=false&query_isRegular=true&query_randLowerBound=%281%29&query_randUpperBound=unsolvable&query_detLowerBound=%281%29&query_detUpperBound=unsolvable&query_activeDegree=3&query_passiveDegree=2&query_labelCount=3&query_activesAllSame=false&query_passivesAllSame=false&query_largestProblemOnly=false&query_smallestProblemOnly=false&query_completelyRandUnclassifiedOnly=false&query_partiallyRandUnclassifiedOnly=false&query_completelyDetUnclassifiedOnly=false&query_partiallyDetUnclassifiedOnly=false&query_excludeIfConfigHasAllOf=&query_excludeIfConfigHasSomeOf=&query_includeIfConfigHasAllOf=&query_includeIfConfigHasSomeOf=&query_fetchStatsOnly=false`,
    linkText: 'All 3-label problems on (3, 2)-biregular undirected trees',
    afterText: ''
  },
  {
    href: `${window.location.origin}/?query_graphType=tree&query_isDirectedOrRooted=false&query_isRegular=true&query_randLowerBound=%28log*+n%29&query_randUpperBound=%28log*+n%29&query_detLowerBound=%281%29&query_detUpperBound=unsolvable&query_activeDegree=3&query_passiveDegree=2&query_labelCount=3&query_activesAllSame=false&query_passivesAllSame=false&query_largestProblemOnly=false&query_smallestProblemOnly=false&query_completelyRandUnclassifiedOnly=false&query_partiallyRandUnclassifiedOnly=false&query_completelyDetUnclassifiedOnly=false&query_partiallyDetUnclassifiedOnly=false&query_excludeIfConfigHasAllOf=&query_excludeIfConfigHasSomeOf=&query_includeIfConfigHasAllOf=&query_includeIfConfigHasSomeOf=&query_fetchStatsOnly=false`,
    linkText: '3-label problems on (3, 2)-biregular undirected trees with complexity O(log* n)',
    afterText: ' - just 14 problems'
  },
  {
    href: `${window.location.origin}/?query_graphType=tree&query_isDirectedOrRooted=false&query_isRegular=true&query_randLowerBound=%281%29&query_randUpperBound=unsolvable&query_detLowerBound=%281%29&query_detUpperBound=unsolvable&query_activeDegree=3&query_passiveDegree=2&query_labelCount=3&query_activesAllSame=false&query_passivesAllSame=false&query_largestProblemOnly=false&query_smallestProblemOnly=true&query_completelyRandUnclassifiedOnly=false&query_partiallyRandUnclassifiedOnly=true&query_completelyDetUnclassifiedOnly=false&query_partiallyDetUnclassifiedOnly=false&query_excludeIfConfigHasAllOf=&query_excludeIfConfigHasSomeOf=&query_includeIfConfigHasAllOf=&query_includeIfConfigHasSomeOf=&query_fetchStatsOnly=false`,
    linkText: 'Smallest unclassified problem among 3-label problems on (3, 2)-biregular undirected trees',
    afterText: ''
  },
  {
    href: `${window.location.origin}/?query_graphType=tree&query_isDirectedOrRooted=true&query_isRegular=true&query_randLowerBound=%28log*+n%29&query_randUpperBound=%28log*+n%29&query_detLowerBound=%281%29&query_detUpperBound=unsolvable&query_activeDegree=3&query_passiveDegree=2&query_labelCount=4&query_activesAllSame=true&query_passivesAllSame=false&query_largestProblemOnly=false&query_smallestProblemOnly=false&query_completelyRandUnclassifiedOnly=false&query_partiallyRandUnclassifiedOnly=false&query_completelyDetUnclassifiedOnly=false&query_partiallyDetUnclassifiedOnly=false&query_excludeIfConfigHasAllOf=&query_excludeIfConfigHasSomeOf=&query_includeIfConfigHasAllOf=&query_includeIfConfigHasSomeOf=&query_fetchStatsOnly=false`,
    linkText: 'All Theta(log* n)-solvable among 4-label problems on (3, 2)-biregular trees, where active nodes use "homogeneous configs" only',
    afterText: ' - 111 problems in total'
  },
  {
    href: `${window.location.origin}/?query_graphType=tree&query_isDirectedOrRooted=true&query_isRegular=true&query_randLowerBound=%281%29&query_randUpperBound=unsolvable&query_detLowerBound=%281%29&query_detUpperBound=unsolvable&query_activeDegree=3&query_passiveDegree=2&query_labelCount=4&query_activesAllSame=false&query_passivesAllSame=false&query_largestProblemOnly=false&query_smallestProblemOnly=false&query_completelyRandUnclassifiedOnly=false&query_partiallyRandUnclassifiedOnly=true&query_completelyDetUnclassifiedOnly=false&query_partiallyDetUnclassifiedOnly=false&query_excludeIfConfigHasAllOf=&query_excludeIfConfigHasSomeOf=&query_includeIfConfigHasAllOf=&query_includeIfConfigHasSomeOf=&query_fetchStatsOnly=false`,
    linkText: 'Unclassified 4-label problems on (3, 2)-biregular trees',
    afterText: ' - all of them are Omega(n)'
  },
]
