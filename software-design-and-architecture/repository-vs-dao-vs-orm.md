# Repository Versus DAO Versus ORM

<!-- tl;dr starts -->

According to [Roadmap.sh](https://roadmap.sh/software-design-architecture), Repository Pattern is categorized as an **Enterprise Pattern** to solve the problem when applications need to access data from data sources. I'm using TypeScript to demonstrate.

<!-- tl;dr ends -->

## Problem

Engineers always want to separate code that implements _business logic_ (or _business logic layer_) from code that implements _data access logic_ for the sake of separation of concerns. Business should not know how they get the data from a particular data source.

The solution is to provide an **abstraction layer** between _business logic_ and _data access logic_. This layer provides a simple, black-boxed, consistent API to access ANY DATA SOURCES.

## Overview solutions

1. Data Access Object (DAO)

DAO is a _design pattern_ found in Data Access Layer of the Three-tier Architecture.

DAO implements CRUD methods to interact with a specific table or all tables at once in RDBMS.

Controller and Service don't need to write raw SQL query anymore.

DAO facilitate the act of writing logic once, writing implementation for DBMS many.

2. Object-Relational Mapping (ORM)

ORM is a _programming technique_ for converting data between an in-memory objects system and a RDBMS inside of an OOP language.

More specifically, instead of writing raw SQL queries, ORM tools abstract away the complexity of working with a RDBMS and allow engineers to interact with one using a higher-level, OO API.

ORM maps the objects and their fields in the code to the tables and their rows and vice versa.

From the ORM technique, engineers create ORM tools using a different number of patterns:

- ODB (C++), ORMLite (Java), Entity Framework (ADO.NET), DBIx (Perl): DAO.
- MikroORM (TypeScript): Data Mapper, Unit of Work, Identity Map.
- ...

ORMs are flexible. Since they may not cover all of the RDBMS features, the limitation is mitigated by allowing engineers to write raw SQL queries.

3. Repository Pattern

Repository is design pattern that abstracts access to all storage concerns, whether they're RDBMS, Non-RDBMS, Text file, ... locally or remotely connected via Web Services APIs.

**NOTE**: Repository Pattern is a Domain Driven Design (DDD) concept. I don't do DDD. 95% of the time using an ORM is enough (by a guy on Reddit and I believe him).

## Reference

- [Roadmap.sh's "Software Design and Architecture "](https://roadmap.sh/software-design-architecture?fl=0)
- [Wikipedia's "Data access object"](https://en.wikipedia.org/wiki/Data_access_object)
- [MikroORM](https://mikro-orm.io/)
- [Java DAO vs Repository Patterns](https://www.baeldung.com/java-dao-vs-repository)
- [DTO - DAO - ORM - Entity - Business Domain](https://techmaster.vn/posts/36750/dto-dao-orm-entity-business-domain)
- [MikeSW's answer on "repository pattern vs ORM"](https://stackoverflow.com/a/10160679)
