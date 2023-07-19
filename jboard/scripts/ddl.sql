-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id serial PRIMARY KEY,
  role TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE jobs (
  id serial PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  company TEXT NOT NULL,
  salary INTEGER NOT NULL,
  author_id INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES users (id)
);
