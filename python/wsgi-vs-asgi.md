# WSGI versus ASGI

<!-- tl;dr starts -->

I've seen blog posts talk about WSGI and ASGI when using Python web frameworks like Flask, Sanic, ... but haven't had the chance to know what they are.

<!-- tl;dr ends -->

## WSGI

**WSGI**, or **Web Server Gateway Interface**, is a standard, a specification that defined how HTTP Server can interact with Python application through an Application Server.

**WSGI** in Python has many counterparts in other programming language: **Rack** in Ruby or **Servlets** in Java.

### History

Historically, this was the flow of HTTP Request/Response before WSGI specification:

```
(the same could apply to `nginx`)
Apache httpd (HTTP Server) <-> mod_proxy <=> Application Server <=> Python application
```

Normal web servers like Apache `httpd` or `nginx` are called "HTTP servers", they run on port 80 and handle static files efficiently, but they don't know how to communicate with Python application.

Then, specialized Application Server than can run Python application came in. They can:

- Keep Python interpreter in memory so that it does not need to be restarted on each request.
- Can start multiple processes and handle multi-threading.
- Can't run on port 80 and not good at handle static files.

The request is received by HTTP server, proxied to Application Server, then Application Server engages the Python application. The Python application outputs response, it get proxied back to HTTP server.

At then, the Application Server wasn't standardized. People settled on WSGI specification that defined how WSGI (Application) Server should interact with WSGI (Python) application. Since then, Python web frameworks have focused on creating different WSGI applications so they can be published by different WSGI servers.

### Components

WSGI standard is used to build 2 components: WSGI _server_ and WSGI \_application. They depends on each other: WSGI server converts HTTP request to standardized WSGI environment, WSGI application received the environment and return a WSGI response, and then WSGI server converts the WSGI resposne to HTTP response.

```d2
HTTP Request/Response Flow with WSGI: {
  shape: sequence_diagram

  client_browser: "Client Browser"
  http_wsgi_server: "HTTP+WSGI Server"
  wsgi_app: "WSGI Application"

  client_browser.t1 -> http_wsgi_server.t1: "HTTP Request"

  convert_http_req_to_wsgi_env_dict: "Convert HTTP to WSGI" {
    http_wsgi_server.t1 -> http_wsgi_server.t1: "Create WSGI\nEnvironment\nDictionary from\nHTTP Request"
  }

  http_wsgi_server.t1 -> wsgi_app.t1: "Standardized WSGI Environment"
  wsgi_app.t1 -> http_wsgi_server.t1: "WSGI Response"

  convert_wsgi_res_to_http_res: "Convert WSGI to HTTP" {
    http_wsgi_server.t1 -> http_wsgi_server.t1: "Create HTTP\nResponse\n from WSGI\nResponse"
  }

  http_wsgi_server.t1 -> client_browser.t1: "HTTP Response"
  http_wsgi_server."WSGI Server acts as a translator."
}
```

Illustation by sequence diagram:

![HTTP Request/Response Flow with WSGI](http-req-res-flow-with-wsgi.svg)

### WSGI servers

WSGI servers can be classified into two categories: **integrated WSGI+HTTP servers** and **standalone WSGI servers**:

- **Integrated WSGI+HTTP servers**: specialized servers that directly involve into request handling without proxying. They are optimized for development environment and should NOT be used in production environment.

> E.g. [Flask's Werkzeug](https://stackoverflow.com/a/50153051/9122512) is a single-threaded server. If one people is currently waiting for a 20-seconds SQL query to complete, other users connecting to the server will be blocked.

- **Standalone WSGI servers**: servers that are optimized for production environments and typically operate behind high-performance C-implemented HTTP servers that act as reverse proxies to ensure security, efficiency, [stability and reliability](https://www.linkedin.com/posts/hany-mostafa-064b552a_stability-reliability-and-resilience-are-activity-7129592089469722624-q83y).

> From a technical perspective, these servers implement a multi-process architecture where the application is pre-loaded before forking into multiple worker processes to handle concurrent requests. While some servers offer multi-threading capabilities within workers, this requires thread-safe application implementation. The multi-process approach is generally preferred for its simplicity and process isolation.

Some notable WSGI servers:

- Werkzeug - Flask's built-in WSGI+HTTP server.
- Gunicorn - pure, production-grade Python WSGI server.
  - `Apache <-> mod_proxy <-> Gunicorn (WSGI server) <-> Flask (Python WSGI application)`
- Waitress - pure Python WSGI server.
- mod_wsgi - WSGI server integrated with Apache httpd server.
  - `Apache <-> mod_wsgi (WSGI server) <-> Flask (Python WSGI application)` (recommended)
- uWSGI - production-grade server suite.
- ...

The HTTP server that get separated from WSGI server is called a "reverse proxy". Notable HTTP servers are: nginx, Apache httpd, ...

The duo I often seen is **uWSGI + nginx**.

> NOTE: When hosting Flask application, you will need to [tell Flask it is behind a Proxy](https://flask.palletsprojects.com/en/stable/deploying/proxy_fix/).

WSGI applications, but they are referred as "Python web frameworks", Two brightest star in the line are Flask and Django.

## ASGI
