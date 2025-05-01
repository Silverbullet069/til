# Design Decisions in Flask

<!-- tl;dr starts -->

I've always loved to read design decisions of a famous software piece. Writing code is easy, but designing isn't.

<!-- tl;dr ends -->

## 1. Explicit Application Object

```py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'
```

Instead of:

```py
from hypothetical_flask import route

@route('/'
def index():
    return 'Hello, World!'
```

4 major reasons behind this:

1. Implicit application objects required that there may only be one instance at the time. But there are time that more than one application is needed, such as unit testing.
2. Subclass the base class Flask to alter its behavior. This would not be possible if the application objects were created ahead of time, based on a class that isn't even exposed.
3. Package name must be a part of application object's initialization. Whenever a Flask instance is created, package name `__name__` must be passed into the constructor.
4. "Explicit is better than implicit". The application object is your WSGI application and user don't need to remember anything else. Apply WSGI middlewares by wrapping it (there are alternatives) with the object and done.

## 2. The Routing System

Flask used Werkzeug routing system, which was designed to:

- **Automatically order routes by complexity**.
  Routes that are ordered arbitrarily will still work as expected. This is crucial if developers want to properly implemented **decorator-based routing**. Since decorators could be fired in undefined order when the application is split into multiple modules.
- **Each route's URL is unique.** If a route is ambiguous, Werkzeug will redirect to a canonical URL.

## 3. One Template Engine

Flask depends on one template engine: Jinja2, not a pluggable template engine interface. That's a design decision regarding server-side rendering technique so I don't need to know about it.

## 4. What does "micro" mean and what it does not?

- **NOT** fitting whole web applicatiion into a single Python file.
- **NOT** lacking in functionality.

Au contraire: Flask aims to keep the core "simple" yet "extensible", since each user's use cases are different.

Flask decide:

- WSGI technology: Werkzeug
- Template engine: Jinja2. Keep in mind that this is easy to change.

Flask won't decide the following, there are numerous extensions has been maintained separatedly that handled them:

- Database integration.
- Form validation.
- Upload handling.
- Open authentication.

## 5. Thread Local Objects

Or "context local objects".

### Idea

- Each thread gets its own copy of data.
- Data is isolated between different requests.
- The data disappears when the request is done.

This way, even when many users use Flask application at the same time, everyone's data stays separate.

### Common objects

- `request`: info about the current request.
- `session`: user session data.
- `g`: general purpose storage for the request that you can put your own things inside.
- `current_app`: return Flask application object.

### Pros

Easy to write a traditional web applications.

### Cons

Inappropriate for large applications where they're deployed on servers that are not based on the concept of threads.

> **NOTE:** Application can be scaled by creating multiple processes using standalone WSGI servers like `gunicorn` or `uWSGI`.

## 6. Async/await and ASGI support

Traditionally, Flask as a WSGI application, uses **one worker** to handle **one request/response cycle**. When Python support asynchronous operations, to remain backwards compatible with the existing code that's synchronous, Flask's way of doing asynchronous operations is different from Async-first (ASGI) frameworks:

- When a request comes in to an async view function, Flask start an event loop in a separate thread, run the view function there, then return the result.

- Async-first (or ASGI) frameworks, on the other hand, start the event loop on the main thread to execute coroutine.

Even for async views, each request still ties up to one worker. The bright side is async code can be run. The number of requests an application can handle at one time will remain the same when NOT using async views. So a performance cost is introduced when compared to other ASGI frameworks.

If you want to squeeze to the last drop of optimization in async, use `Quart`. It's Flask but implemented ASGI.

When the end points of asynchronous operations like database is overloaded, creating deadlock, late requests have to wait deadlocks from prior requests being unlock and therefore suffers from performance degradation.

That's when Queue structure and Queue management tool comes in.

## References

- https://flask.palletsprojects.com/en/stable/design/
- https://flask.palletsprojects.com/en/stable/async-await/
