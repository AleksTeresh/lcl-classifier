# LCL classifier

## Usage instructions

The page contains two forms.
* One for classifying individual LCL problems,
* Another for querying multiple problems

### Problem classification form

The tool uses problem representation similar to [Round Eliminator](https://github.com/olidennis/round-eliminator) e.g.

Active configurations:
```
M U U U
P P P P
```

Passive configurations:
```
M UP UP UP
U U U U
```

If a problem assumes that the underlying graph is directed (for cycles and paths) or rooted (for trees), the directedness is indicated as follows:

Active configurations:
```
M : U U U
P : P P P
```

Passive configurations:
```
M : UP UP UP
U : U U U
```

Here, the label before the `:` sign is an output label on the incoming edge.

So in the example below, we have a rooted tree, in which an active node
can output `M` on its incoming edge (and then `U` label on all its outgoing edges), or it can output `P` on its incoming edge (and then `P` label on all its outgoing edges).

By default irregular nodes (i.e. nodes of degree 1 on paths, leaves and root nodes on trees) are allowed to produce any output. If such nodes
also need to be constrained, those constraints can be specified under the
`Leaf/Root constraints` dropdown. e.g.

Leaf constraints (optional):
```
A
B
```

The above means that a leaf can only output label `A` or label `B` on its
edge.

### Query form

The form allows querying our database, which contains pre-classified problems. Alongside the problems satisfying the query, some statistics about the problems will be returned as well.

First, one will need to choose a problem class: specify degrees of 
active and passive nodes as well as allowed number of labels, a
type of the underlying graph (path, cycle, tree), and whether the graph
is directed.

Under the `Complexity` dropdown, one might restrict returned problems to
only those of a specific complexity range. E.g. only those that
have randomized complexity between _log* n_ and _log n_. Moreover,
one can ask to return only unclassified (or partially classified) problems.

Finally, under the `Configs restrictions` dropdown, one can further
filter out returned problems by their configurations. For example, one can
ask only for problems whose "Passive configs are all the same" (which
means configs of the type `A A` or `B B B`, etc.). Or one can ask
to return only one "smallest" or "largest" problem out of those
satisfying other filtering criteria. Finally, one can ask
to exclude some problems if they contain some/all of the specified
configurations. Alternatively, one can ask to include **only** those
problems that contain some/all of the specified
configurations.

## Acknowledgements

The authors wish to acknowledge [CSC – IT Center for Science, Finland](https://www.csc.fi/en), for computational resources.
