CREATE TABLE batch_classifications (
  id SERIAL PRIMARY KEY,
  active_degree SMALLINT NOT NULL CHECK (active_degree >= 1),
  passive_degree SMALLINT NOT NULL CHECK (passive_degree >= 1),
  label_count SMALLINT NOT NULL CHECK (label_count >= 1),
  actives_all_same BOOLEAN NOT NULL DEFAULT FALSE,
  passives_all_same BOOLEAN NOT NULL DEFAULT FALSE,

  is_tree BOOLEAN NOT NULL DEFAULT FALSE,
  is_cycle BOOLEAN NOT NULL DEFAULT FALSE,
  is_path BOOLEAN NOT NULL DEFAULT FALSE,
  is_directed_or_rooted BOOLEAN NOT NULL DEFAULT FALSE,
  is_regular BOOLEAN NOT NULL DEFAULT FALSE,
  
  count BIGINT NOT NULL
);
