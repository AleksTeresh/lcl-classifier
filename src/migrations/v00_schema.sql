CREATE TABLE problems (
  id SERIAL PRIMARY KEY,
  active_constraints TEXT NOT NULL,
  passive_constraints TEXT NOT NULL,
  root_constraints TEXT NOT NULL,
  leaf_constraints TEXT NOT NULL,
  is_tree BOOLEAN NOT NULL,
  is_cycle BOOLEAN NOT NULL,
  is_path BOOLEAN NOT NULL,
  is_directed BOOLEAN NOT NULL,
  is_rooted BOOLEAN NOT NULL,
  is_regular BOOLEAN NOT NULL,
  rand_upper_bound SMALLINT NOT NULL,
  rand_lower_bound SMALLINT NOT NULL,
  det_upper_bound SMALLINT NOT NULL,
  det_lower_bound SMALLINT NOT NULL,
  solvable_count TEXT,
  unsolvable_count TEXT
);
