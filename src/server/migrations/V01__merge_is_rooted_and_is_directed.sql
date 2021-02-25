ALTER TABLE problems
ADD COLUMN is_directed_or_rooted BOOLEAN NOT NULL DEFAULT FALSE;

UPDATE problems
SET is_directed_or_rooted = (is_directed OR is_rooted);

ALTER TABLE problems
DROP COLUMN is_directed,
DROP COLUMN is_rooted;
