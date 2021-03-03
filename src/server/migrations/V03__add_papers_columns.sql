CREATE TABLE sources (
  id SERIAL PRIMARY KEY,
  short_name TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  urls TEXT[]
);

INSERT INTO sources (short_name, name, urls)
VALUES (
  'cp',
  'Distributed graph problems through
an automata-theoretic lens',
  '{"https://arxiv.org/abs/2002.07659", "https://github.com/AleksTeresh/cyclepath-classifier"}'
);

INSERT INTO sources (short_name, name, urls)
VALUES (
  'brt',
  'Binary rooted tree classifier (database)',
  '{"https://github.com/AleksTeresh/tree-classifications"}'
);

INSERT INTO sources (short_name, name, urls)
VALUES (
  'rt',
  'Rooted tree classifier',
  '{"https://arxiv.org/abs/2102.09277", "https://github.com/jendas1/rooted-tree-classifier"}'
);

INSERT INTO sources (short_name, name, urls)
VALUES (
  'tlp',
  'TLP Classifier',
  '{"https://github.com/trocher/tlpClassifier", "https://github.com/trocher/tlpDoc"}'
);

INSERT INTO sources (short_name, name, urls)
VALUES (
  're',
  'Round Eliminator',
  '{"https://github.com/olidennis/round-eliminator"}'
);

ALTER TABLE problems
ADD COLUMN rand_upper_bound_source INTEGER REFERENCES sources ON DELETE CASCADE,
ADD COLUMN rand_lower_bound_source INTEGER REFERENCES sources ON DELETE CASCADE,
ADD COLUMN det_upper_bound_source INTEGER REFERENCES sources ON DELETE CASCADE,
ADD COLUMN det_lower_bound_source INTEGER REFERENCES sources ON DELETE CASCADE;
