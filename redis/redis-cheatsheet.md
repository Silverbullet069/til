# Redis Cheatsheet

<!-- tl;dr starts -->

Redis is my most favorable Key-value store and NoSQL database in general.

<!-- tl;dr ends -->

## Overview

<!-- prettier-ignore -->
| Aspect | Description |
|--------|-------------|
| **Type** | In-memory database with optional disk persistence |
| **Performance** | 110,000 SET ops/sec, 81,000 GET ops/sec |
| **Memory Model** | Complex data structures simpler to manipulate in memory vs disk |
| **Data Types** | Rich: strings, hashes, lists, sets, sorted sets, HyperLogLog |
| **Atomicity** | Single operations atomic; MULTI/EXEC transactions; Lua scripts execute multiple Redis commands atomically, reduce network round trips|
| **Batch processing** | Pipelining, atomic unsupported |
| **Limitations** | Performance degrades when dataset exceeds available memory |
| **Replication** | Master-slave replication supported |
| **Use Cases** |- In general: Small, targeted data pieces retrieving with low latency requirements<br/>- Multiple local, low-usage CPU Redis `GET*` commands execution is more performant complex SQL JOINs<br/>- Caching<br/>- Message queues (Pub/Sub)<br/>- Web user sessions<br/>- Hit counters<br/>- Real-time data<br/>- Web server integration. |

## Naming convention

Redis use **colon-separated hierarchical naming**.

```
# general syntax
<namespace>:<entity>:<id>:<field>

# string
user:1:name
user:1:email
config:max_connections
counter:page_views

# hash
user:1            # a user with multiple fields
session:abc123    # a session with multiple properties

# lists
queue:jobs        # job queue
timeline:user:1   # user #1's timelines
noti:user:1       # user #1's notifications

# sets
tags:article:1    # tags for article #1
followers:user:1  # followers for user #1
online_users

# sorted sets
leaderboard:game:1  # game leaderboard
trending:posts      # posts that are trending on social media
events:2025:06      # everts sorted by year and month

# include type hints
hash:user:1
list:queue:jobs
set:user:1:permission

# include versioning
user:v2:1:profile
config:v1:database
```

## Redis client - `redis-cli`

Redis is built with client-server architecture in mind. A Redis client can send commands, execute Lua scripts, and interact with the database through the Redis protocol.

```sh

redis-cli -h hostname -p port                 # Basic connection
redis-cli -h hostname -p port -a password     # Password authentication
docker run -it --network some-network --rm redis redis-cli -h some-redis  # container name

redis-cli --latency                           # execute 100 PING/s to Redis instance
redis-cli                                     # access interactive shell
```

```ini
127.0.0.1:6379> PING                # test connection, output: PONG
127.0.0.1:6379> AUTH <password>     # authenticate to server
                                    # run "CONFIG SET requirepass <pass>" on server
127.0.0.1:6379> ECHO "message"      # echo a message
127.0.0.1:6379> SELECT [0-15]       # switch current db
127.0.0.1:6379> QUIT                # close connection
```

## Redis server

There are 2 ways to read and write Redis settings:

- Write directly into `/usr/local/etc/redis/redis.conf` file
- Call `redis-cli` on Redis instance and run `CONFIG ...` commands

```ini
127.0.0.1:6379> INFO                          # get all server info
127.0.0.1:6379> INFO <section>                # get server info about a section

127.0.0.1:6379> CONFIG GET *                  # get the value of ALL params
127.0.0.1:6379> CONFIG GET <param>            # get the value of param
127.0.0.1:6379> CONFIG SET <param> <value>    # change the value of param
127.0.0.1:6379> CONFIG REWRITE                # rewrite configuration file

127.0.0.1:6379> CLIENT LIST                   # show list of clients
127.0.0.1:6379> CLIENT GETNAME                # show current connection name
127.0.0.1:6379> CLIENT SETNAME <string>       # set current connection name

127.0.0.1:6379> DBSIZE                        # number of keys in current db
127.0.0.1:6379> DEBUG OBJECT <key>            # get debug info about a key
127.0.0.1:6379> FLUSHDB                       # remove all keys from current db
127.0.0.1:6379> FLUSHALL                      # remove all keys from all databases

127.0.0.1:6379> SAVE              # backup, or sync save the dataset to disk
                                  # `dump.rdb` is saved in your Redis directory
                                  # e.g. `/data`
                                  # to restore data, move `dump.rdb` to `/data`
127.0.0.1:6379> BGSAVE            # async save the dataset to disk
127.0.0.1:6379> BGREWRITEAOF      # async rewrite append-only file
127.0.0.1:6379> LASTSAVE          # show last successful save's UNIX timestamp
127.0.0.1:6379> SHUTDOWN SAVE     # shutdown with save
127.0.0.1:6379> SHUTDOWN NOSAVE   # shutdown without save

127.0.0.1:6379> MONITOR           # listen all requests received by the server
127.0.0.1:6379> SLOWLOG <subcommand> <args>   # manage Redis slow queries log
127.0.0.1:6379> TIME              # 1. current UNIX timestamp
                                  # 2. ms already elapsed in the current second

# ======================================================================= #
# Replication
# ======================================================================= #

# make server a slave of another instance
# or promotes it as a master (slave of itself)
127.0.0.1:6379> SLAVEOF <host> <port>

# what is the role of this instance, in the context of replication
127.0.0.1:6379> ROLE

# start replicating
127.0.0.1:6379> SYNC
```

## Data types

Redis return types:

- `OK`: the command run successfully.
- (integer) 0, 1, 2, ... N: the command has run successfully against N units
- Special output: `(nil)`, `-1`, ...

### Keys

A key is a string.

```ini
127.0.0.1:6379> INFO keyspace: show info about the current database (no. of keys in each db, ...)

# NOTE: use KEYS with extremely care in production environment
# NOTE: it can ruin performance when executed against large databases
127.0.0.1:6379> KEYS <regex>                  # show all keys matching the pattern
127.0.0.1:6379> KEYS *                        # show all keys inside the current db
127.0.0.1:6379> EXISTS <key>                  # check key existance
127.0.0.1:6379> DUMP <key>                    # return the serialized version of the key's value
127.0.0.1:6379> MOVE <key> <db>               # move the key to another db.
127.0.0.1:6379> DEL <key>                     # delete the key

127.0.0.1:6379> EXPIRE <key> <seconds>        # set expiry in seconds
127.0.0.1:6379> EXPIREAT <key> <seconds>      # same as EXPIRE, in Unix timestamp format.
127.0.0.1:6379> PERSIST <key>                 # removes the expiry
127.0.0.1:6379> TTL <key>                     # get remaining expiry time in seconds
127.0.0.1:6379> PTTL <key>                    # same as TTL, but in ms
```

### Strings

- map a string to another string.
- limit: max string value = 512MB

**Simple examples:**

```
127.0.0.1:6379> SET name "johndoe"
OK
127.0.0.1:6379> get name
"johndoe"
```

**Notable commands:**

```ini
127.0.0.1:6379> APPEND <key> <value>          # new value = old value + <value>
127.0.0.1:6379> STRLEN <key>                  # get value length

127.0.0.1:6379> GET <key>                     # get value
127.0.0.1:6379> GETRANGE <key> <start> <end>  # get a substring from value
127.0.0.1:6379> GETSET <key> <newvalue>       # set new value but return the old value

127.0.0.1:6379> SET <key> <value>                       # set value with no expiry
127.0.0.1:6379> SETEX <key> <value>                     # set value with expiry
127.0.0.1:6379> SETNX <key> <value>                     # set value only if key not existed before
127.0.0.1:6379> SETRANGE <key> <offset> <value>         # overwrite a part of the value, starting at the specified offset
127.0.0.1:6379> MSET <key1> <value1> [<key2> <value2> ...]    # set multiple key-value pairs
127.0.0.1:6379> MSETNX  <key1> <value1> [<key2> <value2> ...] # set multiple key-value pairs, only if none of the keys existed
127.0.0.1:6379> PSETEX <key> <value>                    # same as SETEX, but in ms

127.0.0.1:6379> INCR <key>                    # value + 1
127.0.0.1:6379> INCRBY <key> <inc>            # value + <inc>
127.0.0.1:6379> INCRBYFLOAT <key> <inc>       # same as INCRBY, but value in float

127.0.0.1:6379> DECR <key>                    # value - 1
127.0.0.1:6379> DECRBY <key> <dec>            # value - <dec>
```

### Hashes

- a list of string field-value pairs
- performance: most commands are O(1), listing-related and exp-related ones are O(n)
- limit: max field-value pairs = 2^32 - 1
- use cases: represent object

**Simple examples:**

```
127.0.0.1:6379> HMSET user:1 username johndoe password 123456
OK
127.0.0.1:6379> HGETALL user:1
1) "username"
2) "johndoe"
3) "password"
4) "123456z
```

**Notable commands:**

```ini
127.0.0.1:6379> HEXISTS <key> <field>                 # check if a hash field exists
127.0.0.1:6379> HLEN <key>                            # get the number of fields
127.0.0.1:6379> HINCRBY <key>                         # increment the integer value of a hash field

127.0.0.1:6379> HKEYS <key>                           # get all fields only
127.0.0.1:6379> HVALS <key>                           # get all values only

127.0.0.1:6379> HGET <key> <field>                    # get the value of a hash field
127.0.0.1:6379> HMGET <key> <field1> [<field2> ...]   # get the values of specified fields
127.0.0.1:6379> HGETALL <key>                         # get all the fields and values

127.0.0.1:6379> HSET <key> <field> <value>            # set string value of a field
127.0.0.1:6379> HSETNX <key> <field> <value>          # set string value of a field, only if field is non-existed
127.0.0.1:6379> HMSET <key> <field1> [<field2> ...]   # set new values for specified fields

127.0.0.1:6379> HDEL <key> <field1> [<field2> ...]    # delete one or more hash fields

# iterate fields and associated values inside a hash
# <key>: the name of the hash
# <cursor>: starting position (0 for first scan)
# <pattern>: glob-style pattern
# <count>: how many elements to return per iteration (it's a hint, not a strict limit, Redis may return less or more)
# This command is non-blocking and memory-efficient while scanning large hashes
# return: - next cursor (0 means scan completed), use it for the next scan
#         - array of field-value pairs
127.0.0.1:6379> HSCAN <key> <cursor> MATCH <pattern> COUNT <count>
```

### Lists

- a.k.a Linked List
- a list of strings, sorted by insertion order
- element can be added on the head or on the tail
- limit: max no. of elements = 2^32 - 1

**Examples:**

```ini

127.0.0.1:6379> lpush mocklist redis
(integer) 1
127.0.0.1:6379> lpush mocklist is
(integer) 2
127.0.0.1:6379> lpush mocklist awesome
(integer) 3
127.0.0.1:6379> lrange mocklist 0
(error) ERR wrong number of arguments for 'lrange' command
127.0.0.1:6379> lrange mocklist 0 10
1) "awesome"
2) "is"
3) "redis"
```

**Notable commands:**

```ini
127.0.0.1:6379> LLEN <key>                            # get length
127.0.0.1:6379> LINDEX <key> <index>                  # get an element based on its index
127.0.0.1:6379> LRANGE <key> <start> <stop>           # get a range of elements

127.0.0.1:6379> LPUSH <key> <value1> [<value2> ...]   # prepend 1 or more values
127.0.0.1:6379> LPUSHX <key> <value>                  # same as LPUSH, only if list existed
127.0.0.1:6379> RPUSH <key> <value1> [<value2> ...]   # append 1 or more values
127.0.0.1:6379> RPUSHX <key> <value>                  # same as RPUSH, only if list existed
127.0.0.1:6379> LINSERT <key> [BEFORE|AFTER] <pivot> <value>  # insert element before/after another element in a list

127.0.0.1:6379> LSET <key> <index> <value>            # set the value of an element by its index

127.0.0.1:6379> LPOP <key>                            # removes + gets the first element
127.0.0.1:6379> RPOP <key>                            # removes + gets the last element
127.0.0.1:6379> RPOPLPUSH <src> <dest>                # pop from <src>, push into <dest>
127.0.0.1:6379> LTRIM <key> <start> <stop>            # list contains only elements in the specified range

# <count>: how many elements to remove, and from which direction
# count > 0: remove <count> elements from the beginning (left/head) of the list
# count < 0: remove <count> elements from the end (right/tail) of the list
# count = 0: remove ALL occurance of the value from the list
# Output: no. of elements it removed
# Q: Why direction matters?
# A: Values can be duplicated in different positions.
127.0.0.1:6379> LREM <key> <count> <value>            # remove elements from a list
```

### Sets

- unordeded collection of strings
- add, remove, test set member existance in O(1)
- max no. of members in a set = 2^32 - 1

**Simple examples:**

```
127.0.0.1:6379> sadd mockset redis
(integer) 1
127.0.0.1:6379> sadd mockset mongodb
(integer) 1
127.0.0.1:6379> sadd mockset abcdefg
(integer) 1
127.0.0.1:6379> sadd mockset abcdefg
(integer) 0
127.0.0.1:6379> smembers mockset
1) "redis"
2) "mongodb"
3) "abcdefg" # there is only one element
```

**Notable examples:**

```ini
127.0.0.1:6379> SCARD <key>                           # get no. of members in a set
127.0.0.1:6379> SMEMBERS <key>                        # get all the members in a set

127.0.0.1:6379> SADD <key> <member1> [<member2> ...]  # add 1 or more members
127.0.0.1:6379> SREM <key> <member1> [<member2> ...]  # remove 1 or more members
127.0.0.1:6379> SPOP <key>                            # remove + return random member (random?)
127.0.0.1:6379> SDIFF <key1> [<key2> [<key3> ...]]    # subtracts multiple sets

127.0.0.1:6379> SMOVE <src> <dest> <member>           # move a member from one set to another

TODO: learn the rest commands
```

### Sorted Sets

- Similar to [Sets](#sets)
- Every member is associated with a score
- Using this score, non-numerical members can be sorted from smallest to grestest score.

**Simple examples:**

```
127.0.0.1:6379> zadd mocksortedset 0 redis
(integer) 1
127.0.0.1:6379> zadd mocksortedset 0 mongodb
(integer) 1
127.0.0.1:6379> zadd mocksortedset -1 abcdefg
(integer) 1
127.0.0.1:6379> zadd mocksortedset -1 abcdefg
(integer) 0
127.0.0.1:6379> zrangebyscore mocksortedset -10 10
1) "abcdefg"
2) "mongodb"
3) "redis"
127.0.0.1:6379> zadd mocksortedset 0 abcdefg
(integer) 0
127.0.0.1:6379> zrangebyscore mocksortedset 0 10
1) "mongodb"
2) "redis"
3) "abcdefg"
```

**Notable commands:**

```ini
TODO: learn the rest commands
```

### HyperLogLog

It's an algorithm using randomization in order to provide an approximation of the number of unique elements in a set using:

- a constant
- a small amount of memory.

- Limit: 2^64 items.

**Simple examples:**

```ini
127.0.0.1:6379> PFADD hyperloglog "redis"
(integer) 1
127.0.0.1:6379> PFADD hyperloglog "mongodb"
(integer) 1
127.0.0.1:6379> PFADD hyperloglog "mysql"
(integer) 1
127.0.0.1:6379> PFCOUNT hyperloglog
(integer) 3
127.0.0.1:6379> PFADD hyperloglog "sqlite"
(integer) 1
127.0.0.1:6379> PFADD hyperloglog "neo4j"
(integer) 1
127.0.0.1:6379> PFCOUNT hyperloglog
(integer) 5
```

**Notable commands:**

```ini
127.0.0.1:6379> PFADD <key> <element1> [<element2> ...]     # add element to the special set
127.0.0.1:6379> PFCOUNT <key>                               # count the element inside the special set
```

> **NOTE:** if you run `TYPE <key>`, it returns "string"

## Pub/Sub

- A message system where the senders (a.k.a publishers) sends the messages while the receivers (a.k.a subscribers) receive them.
- The link by which the messages are transferred is called channel.

**Simple examples:**

```
# Server
127.0.0.1:6379> SUBSCRIBE mockchannel
1) "subscribe"
2) "mockchannel"
3) (integer) 1
1) "message"
2) "mockchannel"
3) "Hello World from mockchannel"

# Client
127.0.0.1:6379> PUBLISH mockchannel "Hello World from mockchannel"
```

**Notable commands:**

```ini
# show the state of Pub/Sub system
127.0.0.1:6379> PUBSUB <subcommand> [<argument1> [<argument2> ...]]
127.0.0.1:6379> PUBSUB CHANNELS     # show list of subscribed channels

# listen for messages on channels
127.0.0.1:6379> SUBSCRIBE <channel1> [<channel2> ...]
# same as SUBSCRIBE, but instead of exact match, use regex pattern
127.0.0.1:6379> PSUBSCRIBE <regex1> [<regex2> ...]

# post a message to a channel
127.0.0.1:6379> PUBLISH <channel> <message>

# remove subscribed channels by specifying exact match
127.0.0.1:6379> UNSUBSCRIBE <channel1> [<channel2> ...]
# remove subscribed channels by regex
# NOTE: not PUN-SUBSCRIBE, it's P-UNSUBSCRIBE
127.0.0.1:6379> PUNSUBSCRIBE <pattern1> [<pattern2> ...]
```

## Transaction

Allow the execution of a group of commands in ONE single stop.

- All commands from one client are sequentially executed and served by the server. It's not possible for this server to serve requests from another client.
- Transaction is atomic.

**Simple examples:**

```ini
127.0.0.1:6379> multi
OK
127.0.0.1:6379(TX)> set tutorial redis
QUEUED
127.0.0.1:6379(TX)> get tutorial
QUEUED
127.0.0.1:6379(TX)> set visitors 2000
QUEUED
127.0.0.1:6379(TX)> incr visitors
QUEUED
127.0.0.1:6379(TX)> exec
1) OK
2) "redis"
3) OK
4) (integer) 2001
```

**Notable commands:**

```
127.0.0.1:6379> MULTI               # mark the start of transaction block
127.0.0.1:6379> EXEC                # execute all commands after MULTI
127.0.0.1:6379> DISCARD             # discard all commands after MULTI

127.0.0.1:6379> WATCH <key1> [<key2> ...]   # watch the keys to determine the
                                            # exec of MULTI/EXEC block
127.0.0.1:6379> UNWATCH                     # forget the watched keys
```

## Scripting

Add programmatical operations with Lua interpreter using `EVAL` command.

- Lua script gives you performance gain
- Lua script is transactional and is executed atomically. No other Redis command can run while a script is executing.
- Lua indexed tables start with 1, not 0.
- Best practice: provide keys which the script uses as `KEYS[]`, and all other arguments as `ARGV[]` instead of specifying `KEYS` as 0 then provide all keys within `ARGV[]` table.

**Examples:**

```
# Redis use no. of keys to create boundary between keys and args

127.0.0.1:6379> EVAL "return {KEYS[1], KEYS[2], ARGV[1], ARGV[2]}" 2 key1 key2 arg1 arg2
1) "key1"
2) "key2"
3) "arg1"
4) "arg2"

127.0.0.1:6379> SCRIPT LOAD "return {KEYS[1], KEYS[2], ARGV[1], ARGV[2]}"
"c0d2d6f81be75d67523d7c8ac69a932fbe1aa4e2"

127.0.0.1:6379> EVALSHA "c0d2d6f81be75d67523d7c8ac69a932fbe1aa4e2" 2 key1 key2 arg1 arg2
1) "key1"
2) "key2"
3) "arg1"
4) "arg2"
```

**Notable commands:**

```ini
127.0.0.1:6379> EVAL <script> <no-of-keys> <key1> [<key2> ...] <arg1> [<arg2> ...]    # execute Lua script
127.0.0.1:6379> EVALSHA <script> <no-of-keys> <key1> [<key2> ...] <arg1> [<arg2> ...]    # execute Lua script using SHA1, loaded into cache first
127.0.0.1:6379> SCRIPT LOAD <script>      # load the script into script cache
127.0.0.1:6379> SCRIPT EXISTS <sha1>      # check script existance
127.0.0.1:6379> SCRIPT FLUSH              # clear script cache
127.0.0.1:6379> SCRIPT KILL               # kill the script currently executed
```

## FAQs

### How to connect to Redis via UNIX Socket on Amazon Linux 2023 ?

```sh
# Cre: https://serverfault.com/a/1129059/1138548
sudo dnf install -y redis6
sudo systemctl start redis6
sudo systemctl enable redis6
sudo systemctl is-enabled redis6
redis6-server --version
redis6-cli ping

# NOTE: add the user who is owner of the application process (e.g. Nginx) to the
# NOTE: same group as `redis6`
sudo usermod -a -G redis6 ec2-user
```

```conf
# /etc/redis6/redis6.conf

# do not listen on a port
bind 0

# NOTE: redis.sock can only be created inside dicectory which allow `redis6` user
# NOTE: to write on. In this case, only `/tmp`
unixsocket /tmp/redis.sock

# set permissions for the socket
# NOTE: socket can be read/write by `redis6` user and group
unixsocketperm 770
```

### How to install Redis inside Docker?

```sh
# NOTE: Redis image drop privileges and switch to `redis` user by default
# NOTE: Don't specify --user="1000:1000" option
# NOTE: Ignore `vm.overcommit_memory` warning if persistence is disabled
# TODO: test if files and directories host permission need to be changed to 524xxx
docker run \
  --name=some-redis \
  --init \
  --rm \
  --read-only \
  --network=none \
  -v "./redis.conf:/usr/local/etc/redis/redis.conf:ro" \
  # persistence volume
  -v "./data:/data" \
  # :latest for Debian-based image
  redis:alpine \
  # persistance strategy
  # if at least 1 write operation was performed
  # save ONE snapshot of the database every 60 seconds
  # more log => stricter log level is better
  redis-server --save 60 1 --loglevel warning

# Connect via redis-cli
docker exec -it some-redis redis-cli

# Run the following command if persistence is enabled
echo "vm.overcommit_memory=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
cat /proc/sys/vm/overcommit_memory
```
