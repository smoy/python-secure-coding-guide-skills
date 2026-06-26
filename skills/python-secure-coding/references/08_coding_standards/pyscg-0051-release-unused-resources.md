# pyscg-0051: Release Unused Resources

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-404 (Improper Resource Shutdown or Release).

## Rule

Explicitly release every OS-backed resource (file handle, socket, database connection, custom resource) when it is no longer needed. Use the `with` statement for context-manager resources; for non-context-manager resources, deactivate and clear them explicitly before the reference is dropped.

## Why

Unlike plain Python objects, OS-backed resources are not freed by garbage collection alone. Accumulated unreleased handles cause file descriptor exhaustion, memory leaks, or stalled network connections. Long-running scripts, threads, and multiprocessing make this worse because handles pile up over time.

## Non-compliant

```py
my_list = []

def append_resource(name):
    resource = {"name": name, "active": True}
    my_list.append(resource)

append_resource("A")
append_resource("B")
# Resources never deactivated or removed — list retains them indefinitely
```

## Compliant

```py
my_list = []

def append_resource(name):
    resource = {"name": name, "active": True}
    my_list.append(resource)

append_resource("A")
append_resource("B")

# Explicitly release each resource, then clear the list
for resource in my_list:
    resource["active"] = False
my_list.clear()
```

> For file/socket/DB resources, prefer `with open(...) as f` or `with socket.create_connection(...) as conn` — the context manager calls `__exit__` (which closes the handle) even if an exception occurs.
