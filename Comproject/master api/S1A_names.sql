CREATE TABLE event_names (
  id INTEGER,
  tgid TEXT NOT NULL,
  name TEXT NOT NULL,
  color TEXT NOT NULL,
  bg TEXT NOT NULL,
  PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE INDEX idx_start ON events (start);
CREATE INDEX idx_end ON events (end);