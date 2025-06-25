# Nginx Cheatsheet

<!-- tl;dr starts -->

My favorite [open-source](https://github.com/nginx/nginx) HTTP web server, reverse proxy (load balancer), content cache, TCP/UDP proxy server and mail proxy server.

<!-- tl;dr ends -->

## The differences between TCP Proxy vs HTTP Proxy vs SOCKS5 Proxy

| Topic | TCP Proxy | HTTP Proxy | SOCKS5 Proxy |
| --- | --- | --- | --- |
| OSI Layer | Layer 4 (Transport layer) | Layer 7 (Application Layer) [^1] | Layer 5 (Session Layer) |
| Description | Forward raw TCP packets between a client and a destination server.<br/>It doesn't understand Layer 7 protocol (HTTP, FTP, SMTP, SSH, ...) | Understands HTTP protocol, interpret HTTP Request and HTTP Response to fulfill operations | Routes network packets between a client and a destination server. The latest version, SOCKS5, support authentication, UDP, IPv6 |
| Use Cases | - Basic, fast load balancing for TCP-based applications<br/>- Port forwarding<br/>- Bypass IP-based firewalls<br/>- Hiding the origin server's IP address from the client (and vice-versa)<br/>- Lower overhead than higher-level proxy (HTTP, SOCKS5, ...) if no DPI is involved | - Web caching<br/>- Content filtering (block access to APIs based on client's metadata)<br/>- Anonymity (hide the client's IP address from the destination server)<br/>- Access control and logging<br/>- Modify HTTP headers. | - Bypass firewall<br/>- Routing TCP/UDP traffic for any Layer 7 protocol.<br/>- Enhanced anonymity (DNS resolution by proxy) |
| Cons | No application-level awareness | Introduce more latency than a TCP proxy, due to parsing and processing application-layer data | Client app must support SOCKS protocol + introduce overhead due to the negotiation. |

---

**TCP Proxy:**
1. Client ===TCP connection==> Proxy
2. Proxy ===TCP connection==> Dest
3. Client <==TCP segments==> Proxy <==TCP segments==> Dest

---

**HTTP Proxy:**
1. Client ===HTTP Request==> Proxy
2. Proxy parses the HTTP Request, modify it, check against filtering rules, or return cached, ...
3. No cache? Modified? Proxy ===new HTTP Request==> Dest.
4. Dest ===HTTP Response==> Proxy
5. Proxy ===HTTP Response (cached, modified)==> Client

For "HTTPS" Proxy:
1. Client ===HTTP Request with command HTTP CONNECT ==> Proxy
2. Proxy ===TCP tunnel=== Dest.
3. Client ===SSL handshake==>Dest

Proxy won't be able to intercept HTTP Requests from clients anymore, unless it uses SSL termination:
- Clients install a certificate issued by the Proxy
- Proxy terminate SSL, inspect the content, modify, ... then finally re-encrypt and send to Dest.

However, this break E2E encryption model. Clients will see Proxy's certificate instead of Destination server's certificate.

---

**SOCKS5 Proxy:**
1. Client app (SOCKS-aware) connects to Proxy.
2. Client negotiates an auth method with proxy (none, password-based, ...)
3. After auth, Client specify command (CONNECT for TCP, UDP ASSOCIATE for UDP), Destination server's IP address + port.
4. Proxy ===TCP connection/UDP relay==> Dest
5. Proxy relay traffic between Client and Dest.

- Proxy won't be able to interpret the application data being transmitted.
- Proxy can perform DNS resolution on proxy side, which hides client's IP and DNS. Dest can only see proxy's IP.

[^1]: [What is layer 7 of the Internet?](https://www.cloudflare.com/learning/ddos/what-is-layer-7/)
[^2]: 

## The differences between Reverse Proxy vs Forward Proxy

<!-- prettier-ignore -->
| Topic | Forward Proxy | Reverse Proxy |
| --- | --- | --- |
| Connection | Connect private to public IP space | Connect public to private IP space |
| Security | Trust the client | Trust the server |



## Nginx Configuration File syntax

```ini
# ============================== MAIN CONTEXT =============================== #

# feature-specific configuration files
# stored in /etc/nginx/conf.d
include conf.d/http;
include conf.d/stream;
include conf.d/exchange-enhanced;

# NOTE: user directive makes sense only if the master process runs with
# super-user privileges
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /run/nginx.pid;

# block directive
# Top-level directive "events"
# define general connection processing
events {
    # Connection types: 
    # - Client-to-Nginx connections
    # - Internal connections (within the Nginx edge)
    # - Nginx-to-backend services upstream connections to.

    # Value depends on the hardware, software, whether you're serving static files or proxying to backends
    # - small site = <1024/process
    # - high traffic = 4096-8192/process
    # - very high traffic = >16384/process

    # Total theoretical capacity = # of Worker process * 1024
    # NOTE: OS may limit # of file descriptors available, prevent you fron reaching this theoretical capacity.

    # each Nginx Worker process can handle <= 1024 concurrent connections at the same time
    worker_connections  1024;
}

# Top-level directive "http"
# define HTTP traffic to multiple virtual servers
http {
    # directives in the `http` context go here
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    # NOTE: the same setting on the server calling Nginx must have the same value 
    # (e.g. AWS CloudFront)
    keepalive_timeout  65;

    # include block directives (e.g. server block) inside this http block directive
    #include /etc/nginx/conf.d/*.conf;

    # `server` blocks are diffrent by ports and server names
    # NOTE: two virtual servers can't listen on the same port
    # nginx use them to determine which server processes a request
    # nginx tests the URI specified in request's header
    # against the parameters of the `location` directives defined in `server` block
    server {
        listen       80;
        listen  [::]:80;
        server_name  localhost;

        #access_log  /var/log/nginx/host.access.log  main;

        # prefix match syntax
        location / {
            root    /usr/share/nginx/html;
            index   index.html index.htm;
        }

        # create internal redirect
        error_page 404 /custom_404.html;

        # exact match syntax
        location = /custom_404.html {

            # NOTE: usually `root` directive is ignored in the location block
            # NOTE: it automatically matches the `root` directive in the server block
            # NOTE: being explicit helps you anticipate future change from server block
            root /usr/share/nginx/html;

            # ensures custom 404 page must be accessed through internal redirects
            # e.g. via error_page directive, not direct external requests
            internal;
        }

        # Q: what if there are several maching `location` blocks?
        # A: the block with the longest prefix will be chosen
        location /images/ {
            # Q: why not `root /data/images` ?
            # A: the /images/ prefix will be implicitly used
            root /data;
        }

        # create internal redirect
        error_page 500 502 503 504 /custom_50x.html;

        # exact match syntax
        location = /custom_50x.html {
            root /usr/share/nginx/html;
            internal;
        }

        # Test 502 Bad Gateway error
        location /testing {
            # specify where to forward request for processing

            # unix domain sockets are a common way to communicate with FastCGI processes
            # for better performance, compared to TCP connections
            fastcgi_pass unix:/does/not/exist
            #fastcgi_pass unix:/var/run/php/php8.1-fpm.sock     # PHP-FPM, read-write permission
        }

        #location ~ <regex>         # case-sensitive regex
        #location ~* <regex>        # case-insensitive regex
        #location ^~ /path          # priority prefix match, blocks matching subsequent prefixes that're longer

        #rewrite ^/rewriteme/(.*)$ /$1 last;    # a request for /rewriteme/foobar will become a request to /foobar and a location is search...

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }

    # ========================================================================= #
    # Gzip Compression                                                          #
    # ========================================================================= #
    gzip  on;

    # add "Vary: Accept-Encoding" HTTP header
    # return diff responses depends on whether the client supports compression
    gzip_vary on;

    # sets a minimum file size threshold of 1024 bytes (1 KB) before comporession is applied
    # not everytime compression is good
    gzip_min_length 1024;

    # 1-9
    # 6=good balance between compression ratio and CPU usage
    gzip_comp_level 6;

    # MIME type
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript;
        # NOTE: don't compress image/video, they're already compressed formats
        # NOTE: only text-based content benefits the most

    # ========================================================================= #
    # Optimal Buffer Size                                                       #
    # ========================================================================= #

    # if the client req's body < 128k, it's stored entirely in memory
    # if the client req's body > 128k, excess data is written to a tmp file on disk
    client_body_buffer_size 128k;

    # prevents clients from sending excessively large requests
    # if a client tries to send a req body > 50MB, Nginx return a 413 Request Entity Too Large
    client_max_body_size 50m;

    # ========================================================================= #
    # Example #1: HTTP Forward Proxy to Telegram server                         #
    # ========================================================================= #
    
    # Client will be AWS CloudFront

    server {
        listen       80;
        # listen  [::]:80;  # AWS CloudFront don't support IPv6 if using signed URLs/cookies
        server_name  iamhung.top;

        location /telegram {
            # gzip on;  # most are *.ts and *.vtt files
            
            # Forward request to Telegram API
            # Terminate the original request and create a new request
            # URL tranformation: http://iamhung.top/telegram/bot<token>/sendDocument
            # Proxied request: https://api.telegram.org/bot<token>/sendDocument
            # Use cases:
            # - Bypass reginal restrictions: if Telegram API is blocked in some regions, such as my country
            # - SSL Termination: clients can use HTTP to Nginx and Nginx uses HTTPS to Telegram. The latter connection must be secure.
            # - API Key protection: hide bot tokens from client-side code
            # - Rate Limiting: control access to Telegram API, appropriate to its rate limits
            # - Caching: buffer responses for better performance (
            proxy_pass https://api.telegram.org;

            # Without it, the Telegram server will receive `Host: iamhung.top` header
            # Telegram servers expect the requests are for them, not for my Nginx server
            # Ensure hostname validation + SSL certificate validation
            proxy_set_header Host api.telegram.org;

            # buffer the complete response from Telegram server before sending it to the client
            proxy_buffering on;

            # buffer response headers and the beginning of the response body
            proxy_buffer_size 128k;

            # the no. of buffers and their size for response body
            proxy_buffers 4 256k;

            # the size of buffers that are allocated for sending data to clients
            proxy_busy_buffers_size 256k;

            # Total buffer capacity: 4 * 256k + 128k = 1152k
            # Memory efficient: 256k can be sent to clients while still buffering
            # Validation: 256k < (1024k - 256k) = 256k < 768k
            # After filling 256k, it could be sent to the client immediately
            # The rest 768k will continue to receive data from Telegram
        }
    }
}

# ...
stream {
    # configuration specific to TCP/UDP affecting virtual servers
    server {
        # configuration of TCP virtual server 1
    }
}
```

## Reverse Proxy for PHP web application

```ini
server {
    listen      80;
    server_name example.org www.example.org;
    # global root, no per-location root
    root        /data/www;

    location / {
        index   index.html index.php;
    }
    
    location ~* \.(gif|jpg|png)$ {
        # set cache headers telling browsers and intermediate caches to store these images for 30 days
        # improve website performance by reducing server requests for static assets
        # best for assets that are unchanged for a long time
        expires 30d;
    }

    location ~ \.php$ {
        # where to forward FastCGI requests
        fastcgi_pass  localhost:9000;   # might be PHP-FPM

        # tells PHP-FPM: which script file to execute
        # set env var SCRIPT_FILENAME to the full filesystem path to the requested script
        # the absolute path made by: web root directory + script path from URL
        fastcgi_param SCRIPT_FILENAME
                    $document_root$fastcgi_script_name;

        # pulls in a standard set of FastCGI parameters from Nginx's configuration files
        # e.g. REQUEST_METHOD, QUERY_STRING, CONTENT_TYPE
        include       fastcgi_params;
    }
}
```

## Proxy traffic to a Jenkins app server

Benefits:

- Acts as a TLS termination proxy
- Static file serving
- Load balancing

```conf
# defint backend server pool
upstream app_server {
    server 127.0.0.1:8080 fail_timeout=0; # never mark the server as unavailable, even if the server becomes unresponsive
}

server {
    listen  80;
    listen [::]:80 default ipv6only=on; # make this virtual server handles IPv6 traffic by default, ensuring it only handles IPv6 requests
    server_name ci.yourcompanyname.com;

    location / {
        # proxy_set_header: modify HTTP headers when Nginx acts as a reverse proxy
        # proxy_redirect:

        # retain client's IP address
        # if the incoming request already has an X-Forwarded-For header (meaning it passed through other proxies) this variable will append the client's IP address to the existing list.
        # If no such header exists, it will create one with just the client's IP address.
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # retain original "Host" header in client's request
        # a client's request specify "Host" as the domain name of Nginx proxy server (e.g. example.com)
        # when the request pass through Nginx proxy server, it changes the "Host" header to match the upstream server's address, which is "localhost:8080"
        # upstream server receive request from Nginx proxy server will see "Host" set to "localhost:8080", not "example.com".
        # Therefore create breakage on some features
        proxy_set_header Host $http_host;   # 

        # When nginx acts as a reverse proxy, upstream servers sometimes send HTTP redirect responses (301, 302, ...) the contain URLs pointing back to themselves
        # By default, nginx automatically rewrites these redirect URLs to match the client's perspective: that is to replace the upstream server's address with Nginx proxy server's address
        # Setting it off will retain the upstream server's address
        proxy_redirect off;

        # Attempt serving files in a specific order
        # first, it tries to find and serve a file that matches the exact URI path requested by the client $uri (e.g. <root>/foobar)
        # if the file doesn't exist on the filesystem, Nginx will fallback to the second option @app_server, it will try to find it there
        try_files $uri @app_server;
    }

    # named location block
    # it's not a file or a directory, any directives use this will ref to this separately defined location block
    location @app_server {
        proxy_pass http://app_server;
    }
}
```

## AWS CloudFront

```conf
server {
    # ...
    # Optional: Add a header to verify requests (can be checked by CloudFront later if desired,
    # but the primary security here is the tunnel itself)
    # add_header X-Origin-Server "MyVideoOrigin" always;

    location ~* ^/streaming/.*\.(m3u8|ts|vtt)$ {
        add_header Cache-Control "public, max-age=315360000"; # 10 years, CloudFront will respect it
        try_files $uri =404;
        autoindex off; # disable directory listing, users can't browse directory contents
    }
    # ...
}
```

## `lua-resty-redis` API

```conf
location / {
    try_files $uri $uri/ =404;
    autoindex off; # disable directory listing, users can't browse directory contents
}

server {
    location / {
        content_by_lua_block {
            local redis = require "resty.redis"
            local red = redis:new()

            -- max time to connect to Redis server
            -- max time to send data to Redis server
            -- max time to wait for response from Redis server
            red:set_timeouts(100, 100, 100); -- local Redis
            -- red:set_timeouts(3000, 1000, 3000); -- remote Redis
            -- red:set_timeouts(500, 200, 1000); -- balanced

            local ok, err = red:connect("unix:/path/to/redis.sock");    -- UNIX domain socket
            -- local ok, err = red:connect("127.0.0.1", 6379);          -- IP address
            -- local ok, err = red:connect("redis.openresty.com", 6379);-- hostname, required resolver
            
        }
    }
}
```

## References

- [carlessanagustin/Nginx_Cheat_Sheet.md](https://gist.github.com/carlessanagustin/9509d0d31414804da03b)
