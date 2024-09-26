Proxies a request to a given URL by making the request on the server and returning the response.
Headers and body will be preserved, therefore the behavior should be identical to making the request directly.

Useful to bypass CORS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Usage
Given your server is running on `https://proxy.example.com`.

Instead of making a request to a URL directly, prepend the proxy server URL.
For example, instead of making a request to `https://cors-protected-site.com/anything` run the request
with `https://proxy.example-com/https://cors-protected-site.com/anything`.

Headers and body (if available) will be preserved as if making the request directly. Therefore, header-based authentication 
or sending some form data will still work.


### Setup using docker compose
- Clone this repository
- Start the server with `docker compose up -d --build`
- The server will start on port `9996` by default. This can be chagedin the `docker-compose.yml` file.

### Configure the caching behavior
You can configure the caching behavior of the server by setting some environment variables in the [`docker-compose.yml`](./docker-compose.yml) file.
There are four caching modes available by setting the `CACHE_MODE` environment variable:

| **`CACHE_MODE`**      | Description                                     | Additional settings                                                                                                                                                                                   |
|-----------------------|-------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `sqlite`              | Saves the responses in a SQLite database        | Set the `SQLITE_FILE` environment variable to modify the cache file. Defaults to `data/cache.db`.                                                                                                     |
| `mysql`               | Connects to a MySQL-database to cache responses | Requires setting `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD` and `MYSQL_DATABASE` environment variables accordingly. `MYSQL_PORT` can be used if the MySQL server is running on a non-standard port. |
| `memory`  _(default)_ | Uses an in-memory cache to store responses      | _(none)_                                                                                                                                                                                              |
| `none`                | Disables caching completely.                    | _(none)_                                                                                                                                                                                              |

If an unrecognized value is set for `CACHE_MODE`, no caching will be used.
See the [`examples`](./examples) for some example docker compose configurations.
