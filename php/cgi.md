# CGI

<!-- tl;dr starts -->

This is an interface specification allowing external programs to interact with web servers.

<!-- tl;dr ends -->

Back in the day, when there are a lot of web servers (Apache, NGINX, IIS, ...) and a lot of programming languages whose runtime can generate dynamic content for web pages (PHP, Perl, Python, JS (NodeJS)...), you will need a specification that allows any webservers can execute any back-end programs. And that's CGI.

**How CGI works:**

1. A user sends a request to the web server.
1. The server reconginizes it's a CGI request and forwards it to the CGI program.
1. The CGI program processes the request and generates output.
1. The web server sends this output back to the user's browser.

**Why CGI is legacy now:**

CGI applications run in separate processes, which are created at the start of each request and torn down at the end. This model makes CGI programs very simple to implement, but limits efficiency and scalability:

- At high loads, OS overhead for process creation and destruction becomes significant.
- Limits resource reuse methods: reusing database connection, in-memory caching, ...

## Reference

- [Wikipedia "FastCGI"](https://en.wikipedia.org/wiki/FastCGI)
