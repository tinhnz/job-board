INSERT INTO users (username, password, role)
VALUES
  ('Bob', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'editor'),
  ('Jane', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'viewer');

INSERT INTO jobs (company, salary, title, body, author_id, created_at)
VALUES
  ('DNA Talent', 5000, 'Software Engineer', 'Cupidatat cillum officia tempor non anim elit anim irure do nisi nulla laborum deserunt eu.', 1, NOW()),
  ('Total Infrastructure Limited', 7000, 'Civil Engineer', 'Cupidatat cillum officia tempor non anim elit anim irure do nisi nulla laborum deserunt eu.', 1, NOW()),
  ('Delivery Centric', 6000, 'Desktop Support Engineer', 'Cupidatat cillum officia tempor non anim elit anim irure do nisi nulla laborum deserunt eu.', 1, NOW()),
  ('Ryman Healthcare', 6500, 'System Administration', 'Cupidatat cillum officia tempor non anim elit anim irure do nisi nulla laborum deserunt eu.', 1, NOW()),
  ('Aroa Biosurgery', 5500, 'Engineer - Operation', 'Cupidatat cillum officia tempor non anim elit anim irure do nisi nulla laborum deserunt eu.', 1, NOW()),
  ('Samsung Electronics', 8500, 'Senior RAN Engineer', 'Cupidatat cillum officia tempor non anim elit anim irure do nisi nulla laborum deserunt eu.', 1, NOW());
