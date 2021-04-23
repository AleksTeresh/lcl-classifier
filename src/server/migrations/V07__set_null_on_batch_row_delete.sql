ALTER TABLE problems
DROP CONSTRAINT problems_batch_id_fkey,
ADD CONSTRAINT problems_batch_id_fkey
   FOREIGN KEY (batch_id)
   REFERENCES batch_classifications(id)
   ON DELETE SET NULL;
