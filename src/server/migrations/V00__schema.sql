CREATE TYPE complexity AS ENUM (
  '(1)',
  '(log* n)',
  '(loglog n)',
  '(log n)',
  '(n)',
  'unsolvable'
);

CREATE TABLE problems (
  id SERIAL PRIMARY KEY,
  active_degree SMALLINT NOT NULL CHECK (active_degree >= 1),
  passive_degree SMALLINT NOT NULL CHECK (passive_degree >= 1),
  label_count SMALLINT NOT NULL CHECK (label_count >= 1),
  actives_all_same BOOLEAN NOT NULL DEFAULT FALSE,
  passives_all_same BOOLEAN NOT NULL DEFAULT FALSE,

  active_constraints TEXT[] NOT NULL,
  passive_constraints TEXT[] NOT NULL,
  root_constraints TEXT[] NOT NULL DEFAULT '{}',
  leaf_constraints TEXT[] NOT NULL DEFAULT '{}',
  is_tree BOOLEAN NOT NULL DEFAULT FALSE,
  is_cycle BOOLEAN NOT NULL DEFAULT FALSE,
  is_path BOOLEAN NOT NULL DEFAULT FALSE,
  is_directed BOOLEAN NOT NULL DEFAULT FALSE,
  is_rooted BOOLEAN NOT NULL DEFAULT FALSE,
  is_regular BOOLEAN NOT NULL DEFAULT FALSE,
  rand_upper_bound complexity NOT NULL DEFAULT 'unsolvable',
  rand_lower_bound complexity NOT NULL DEFAULT '(1)',
  det_upper_bound complexity NOT NULL DEFAULT 'unsolvable',
  det_lower_bound complexity NOT NULL DEFAULT '(1)',
  solvable_count TEXT,
  unsolvable_count TEXT
);
