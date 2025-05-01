# Tips and Tricks for SQLite

I would like to organize best practices when using SQLite database.

- Enable printing human-readable outputs

```
# ~/.sqliterc
Ref: https://dba.stackexchange.com/a/40672/279781
.mode column
.headers on
.separator ROW "\n"
.nullvalue NULL

# CLI
# Ref: https://dba.stackexchange.com/a/219988/279781
sqlite> .mode column
sqlite> .headers on
sqlite> .separator row '\n'
sqlite> .nullvalue NULL
```
