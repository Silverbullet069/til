# Using SQLite Full-text Search with Python

I would like to create a SQLite database for Today I Learned posts that utilizes full-text search to assists with search and filter features on website that I planned to deploy in the future

```sql
-- content table
CREATE TABLE IF NOT EXISTS til (
    path TEXT PRIMARY KEY,
    slug TEXT,
    url TEXT,
    topic TEXT,
    title TEXT,
    body TEXT,
    html TEXT,
    summary TEXT,
    created TEXT,
    created_utc TEXT,
    updated TEXT,
    updated_utc TEXT
);

-- external content FTS5 table
CREATE VIRTUAL TABLE IF NOT EXISTS til_fts USING fts5(
    title,
    body,
    content='til',
    content_rowid='path'
);

-- In case of data in content table exists before the creation of external content FTS5 table, the til_fts must be rebuilt to ensure maximum consistency
-- Docs: https://www.sqlite.org/fts5.html#external_content_table_pitfalls
INSERT INTO til_fts(til_fts) VALUES('rebuild');


-- Keep FTS5 table in sync
-- Docs: https://www.sqlite.org/fts5.html#external_content_tables
CREATE TRIGGER IF NOT EXISTS til_ai AFTER INSERT ON til BEGIN
    INSERT INTO til_fts(rowid, title, body)
    VALUES (new.path, new.title, new.body);
END;

CREATE TRIGGER IF NOT EXISTS til_ad AFTER DELETE ON til BEGIN
    DELETE FROM til_fts WHERE rowid = old.path;
END;

CREATE TRIGGER IF NOT EXISTS til_au AFTER UPDATE ON til BEGIN
    DELETE FROM til_fts WHERE rowid = old.path;
    INSERT INTO til_fts(rowid, title, body)
    VALUES (new.path, new.title, new.body);
END;
```

## References

- [C. C. Python Programming's "Using SQLite FTS (Full-Text Search) with Python"](https://medium.com/@ccpythonprogramming/using-sqlite-fts-full-text-search-with-python-5d749ea29859)
