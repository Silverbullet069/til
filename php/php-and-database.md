# PHP and Database

<!-- tl;dr starts -->

When developing a PHP application that needs to interact with a database, you will need to know the definition of these terminologies: driver, driver with specification, API, PHP Extension, PHP Extension Framework.

<!-- tl;dr ends -->

## General concepts

### Driver

A low-level component that implements the protocol designed to communicate with a specific database management system (DBMS). _One_ driver is written in _one_ programming language and associates with _one_ DBMS.

```c
// libmysqlclient - the MySQL C API
#include <stdio.h>
#include <stdlib.h>
#include <mysql/mysql.h>

int main() {
  MYSQL *conn;
  MYSQL_RES *result;
  MYSQL_ROW row;

  // Initialize the MySQL client library
  conn = mysql_init(NULL);
  if (conn == NULL) {
      fprintf(stderr, "mysql_init() failed\n");
      return EXIT_FAILURE;
  }

  // Connect to the MySQL server
  if (mysql_real_connect(conn, "localhost", "username", "password",
                        "database_name", 0, NULL, 0) == NULL) {
      fprintf(stderr, "Connection error: %s\n", mysql_error(conn));
      mysql_close(conn);
      return EXIT_FAILURE;
  }

  printf("Connected to MySQL server successfully!\n");
}
```

### Driver with specification

With the birth of different DBMSs, came their plugins as well. Same problem, different drivers, designed and implemented differently. They're also low-level and aren't developer-friendly that it's hard for application developers to implement complex application features.

That's when **Drivers** that follow **standards and specifications** come in. First you create a database abstraction layer with interfaces, abstract classes, ... that follow the specification, then for each DBMS you implement the abstraction layer to create the driver for that DBMS.

| Driver               | Specification | DBMS  | Programming Language |
| -------------------- | :-----------: | :---: | :------------------: |
| MySQL Connector/J    |     JDBC      | MySQL |         Java         |
| MySQL Connector/ODBC |     ODBC      | MySQL |        C/C++         |
| PDO_MYSQL            |      PDO      | MySQL |         PHP          |

> **NOTE:** you're not actually calling the implementation, you're calling the abstract API and you will be redirected to concrete implementation. That's why some developers said "you're not actually calling the driver".

```java
// MySQL Connector/J API
import com.mysql.connector.jdbc.*;

MySQLConnection conn = new MySQLDataSource()
    .setServerName("localhost")
    .setDatabaseName("testdb")
    .setUser("username")
    .setPassword("password")
    .getConnection();
```

### API

APIs can appear in different contexts:

- **Programming Language APIs:** Java API, .NET Framework API, ...
- **OS APIs:** Windows API, POSIX API, iOS/macOS Cocoa API, Android API, ...
- **Database APIs:** MySQL Connector/J, MySQL Connector/ODBC, MongoDB Driver API, ...
- **Hardware APIs:** Camera API
- **Web Services APIs** (not to be mistaken with **Web APIs**): REST APIs, SOAP APIs, SOAP APIs, GraphQL APIs, ...
- **Web APIs:** APIs that only exists in browsers, maintained by browsers developers. They live outside of browsers' JavaScript Engine and give JavaScript developers access to browsers' functionality so they can serve their web applications better (i.e. DOM, Fetch, Timers, AJAX, ...)

> **NOTE:** JavaScript **Engine** and JavaScript **Runtime** are not interchangeable. JavaScript Runtime contains JavaScript Engine (Memory Heap, Call Stack), Web APIs and Event Loop.

## PHP Extensions for MySQL

**PHP Extensions** are the additional functionality to the PHP core. They exposed **Programming Language APIs**, which are classes, methods, functions, and variables from libraries and frameworks. Application developers creating features for their applications will need to call these APIs to carry out their desired tasks.

**PHP Extensions** are created from **PHP Extension Framework** - a system that allows PHP developers to write compiled languages code such as C, C++ or Rust to develop PHP extensions' features. _PHP libraries_ , which are modules writtin in PHP itself, aren't categorized as PHP Extensions.

For _PHP extensions for MySQL DBMS_, there are 2 PHP extensions: **MySQL improved** (`mysqli`) and **PHP Data Object (PDO)** with PDO_MYSQL driver:

- `mysqli` APIs are exposed to application developers and designed with dual interface: object-oriented and procedural.
- _PDO_MYSQL driver_ API is NOT exposed to application developers, instead it acts as the implementation of the database abstraction layer in **PDO**. The database abstraction layer exposes its API (now called **PDO API**) in object-oriented type.

> **NOTE:** Comparison of criterias between Object-oriented (OO) and Procedural APIs:
>
> | Options              | Object-oriented (OO) | Procedural (not Functional)      |
> | -------------------- | -------------------- | -------------------------------- |
> | Code elements        | Classes, methods     | Functions                        |
> | First-class citizens | Object               | Not object                       |
> | Complexity           | High                 | Low                              |
> | Scalability          | High                 | Depends                          |
> | Project scope        | Enterprise-level     | Simple website, pet project, ... |
>
> You shouldn't mix both styles for code clarity and coding style reasons.

In the past, in order to communicate with the MySQL DBMS, `mysqli` and PDO_MYSQL driver uses a low-level library that implements the required protocol called **MySQL Client Library** (otherwise known as `libmysqlclient`).

However, `libmysqlclient` is designed for C applications, it's not optimized for communication with PHP applications.

=> **MySQL Native Driver** (a.k.a `mysqlnd`) was developed as an alternative to `libmysqlclient` for PHP applications. It's more optimized in terms of memory and speed.

> **NOTE:** Comparison of features between `mysqli` and PDO with _PDO_MYSQL_ driver
>
> | Extension                       | MySQL improved (mysqli) | PDO with PDO MYSQL driver |
> | ------------------------------- | :---------------------: | :-----------------------: |
> | Development status              |         Active          |          Active           |
> | Charsets                        |           Yes           |            Yes            |
> | Server-side Prepared Statements |           Yes           |            Yes            |
> | Client-side Prepared Statements |           No            |            Yes            |
> | Stored Procedures               |           Yes           |            Yes            |
> | Multiple Statements             |           Yes           |           Most            |
> | Transaction                     |           Yes           |          Unknown          |
> | Enhanced Debugging              |           Yes           |          Unknown          |

### Connection

Connecting PHP applications with MySQL DBMS requires setting up a communication mechanism for processes: **Unix domain sockets** (only available in Unix or Unix-like OS such as distro used GNU/Linux) and **TCP/IP**.

```php
<?php

// localhost == connect using Unix domain sockets
$mysqli = new mysqli("localhost", "user", "password", "database");
echo $mysqli->host_info . "\n";

// 127.0.0.1 == connect using TCP/IP
$mysqli = new mysqli("127.0.0.1", "user", "password", "database", 3306);
echo $mysqli->host_info . "\n";

?>
```

Output:

```
Localhost via Unix socket
127.0.0.1 via TCP/IP
```

| Mechanism            | Unix domain sockets              | TCP/IP                                 |
| -------------------- | -------------------------------- | -------------------------------------- |
| Communication scope  | Intra-machine only               | Inter-machine capable                  |
| Addressing mechanism | Filesystem path                  | IP address and port                    |
| Performance          | Lower latency, higher throughput | Higher network overhead                |
| Special capabilities | File descriptor passing          | Error checking, Packet ordering        |
| Best use cases       | High-security local applications | Cross-platform, networked applications |

The connection operation has to be performed in 3 steps:

```
mysql_init() ===> mysqli::options() ===> mysqli::real_connect()
               or mysqli_options()    or mysqli_real_connect()
```

By default, every database connection opened by a script is either explicitly closed by the user during runtime, or released automatically at the end of the script. That is **non-persistent** database connection. This kind of connection will add overhead of establishing a new connection every time a script needs to talk to a database.

However, PHP Extensions for MySQL supports **persistent** database connections, which are a special kind of _pooled_ connections. That is to say the database connection is not closed or released but put into a pool for later reuse, if a connection to the same server using the same _username, password, socket, port and default database is opened_.

Web servers can spawn ONE or MANY PHP processes. Each PHP process can have its own connection pool and serve ONE or MANY non-persistent and persistent database connection requests:

- The total number of both persistent and non-persistent connections opened by a script is limited.
- The total number of persistent connections is limited.

Persistent connections in pool can either have its state **persisted**, or **reset before reuse**:

<!-- prettier-ignore -->
| Interpretation | Persisted | Reset before reuse |
| --- | --- | --- |
| Default | No | Yes |
| Rollback unfinished transaction | No | Yes |
| Reflect authorization change | No | Yes |
| Mechanism | Implicitly called `mysqli_change_user()` | Recompile the extension with the compile flag `MYSQLI_NO_CHANGE_USER_ON_PCONNECT` being set |
| Performance | Optimized | Expensive |
| Best for | Maximum performance applications | Safety-first, required transaction applications |

### Prepared Statements and Bound Parameters

A **Prepared Statement** is a feature, used to execute the same (or similar) SQL statements repeatedly with high efficiency.

Its behavior consists of 3 steps:

1. **Prepare**: A SQL statement template is created. It's sent to the database. Certain values are left unspecified called _parameters_ (or _bound parameters_), labeled `?`.

   > E.g. `insert into my_guests values (?, ?, ?)`

1. **Process**: The database parses, compiles and performs query optimization on the SQL statement template. It stores the result WITHOUT executing it.1.

1. **Execute**: The application binds the values to the parameters, and the database executes the statement. It can execute the statement as many times as it wants with different values but still get the most optimized performance.

Pros:

- Reduce parsing time, as the preparation on the query is done only once although being executed multiple times.
- Minimize bandwidth to the server, as only the parameters are needed to be sent, not the whole query.
- Useful against SQL injections, as parameter values which are transmitted later using different protocol need not be correctly escaped. Don't forget that data from external sources before inserting must be validated and sanitized. Also, if the statement template is not derived from external input, SQL injection can't occur.

## References

- [PHP Official Documentation's "MySQLi > Overview"](https://www.php.net/manual/en/mysqli.overview.php)
- [W3Schools's "PHP > PHP MySQL Prepared Statements"](https://www.w3schools.com/php/php_mysql_prepared_statements.asp)
