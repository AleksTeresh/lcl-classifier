ALTER TABLE problems ADD CONSTRAINT unique_problems UNIQUE (
  active_constraints,
  passive_constraints,
  root_constraints,
  leaf_constraints,
  is_tree,
  is_cycle,
  is_path,
  is_directed_or_rooted,
  is_regular
);
