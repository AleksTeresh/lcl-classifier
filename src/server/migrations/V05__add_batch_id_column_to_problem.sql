ALTER TABLE problems
ADD COLUMN batch_id INTEGER DEFAULT NULL REFERENCES sources ON DELETE CASCADE;
