# Database Schema Migration

<!-- tl;dr starts -->

The hardest part of maintenaning a large-scale enterprise applications deployed worldwide is changing database schema. Even harder is the challenge of making schema changes without any downtime.

<!-- tl;dr ends -->

Can be found in **Step 2: Create an issue and research the problem** of my **How you should build a feature** article, after you find yourself needing to change the database schema in order to realize new features.

## Key techniques

### 1. Version control

Put a SemVer version control tag to schemas.

### 2. Backward-compatible migration process

It's rarely possible to have application code and database schema changes go out at the exact same instance in time. Application servers and database servers are separated and scaled worldwide by cloud providers, it's very hard to orchestrate the update with exact precision to ensure no-downtime. Therefore:

- Design a new schema change that can be applied without changing the application code that uses it. E.g. add new columns, new tables, ...

- Ship that change to database servers and backfill the data into the new schema. Ensure the update is 100% covered on all database servers.

- Ship new application code that uses the new schema. Ensure the update is 100% covered on all database servers.

- Ship a new schema change without unused elements. E.g. drop old columns, old tables, ...

It's long and tedious, but it's still do-able.

### 3. Using 3rd-party tools that support this functionality

- Python Web Framework Django: [Migrations](https://docs.djangoproject.com/en/4.1/topics/migrations/).
- GitHub's Online Schema-migration Tool for MySQL: [github/gh-ost](https://github.com/github/gh-ost)

## Reference

- [Simon Willison's Blog "Software Engineering Practice: Rock solid database migrations"](https://simonwillison.net/2022/Oct/1/software-engineering-practices/#rock-solid-migrations/)
