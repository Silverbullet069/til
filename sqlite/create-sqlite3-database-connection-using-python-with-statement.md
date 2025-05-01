# Create SQLite database connection using Python with statement

When using `with` statement, the connection automatically:

- Creates a ACID transaction.
- Commits the transaction when exiting normally (no exceptions).
- Rolls back if an exception occurs.
- Closes the connection when `with` block ends.

However, if you want to commit changes before the `with` block ends, typically to archive nested transaction from a single connection, you must use `connection.commit()` method.

```py
# Auto-commit example - no explicit commit needed
import sqlite3

with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO table VALUES (?)', ('data',))
    # No conn.commit() needed - automatically commits when with block ends

# Multiple transaction example - explicit commit needed
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO table VALUES (?)', ('data1',))
    conn.commit()  # Commit first transaction

    cursor.execute('INSERT INTO table VALUES (?)', ('data2',))
    conn.commit()  # Commit second transaction
```

> NOTE: you can use either `cursor` or `conn` to execute SQL command, they're basically the same, just different standard practices.
