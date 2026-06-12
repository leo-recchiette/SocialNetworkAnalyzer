# Running the SNA tool with Docker

This is the easiest way to run the whole stack. `docker compose` builds one
application image (PHP 7.4 + Python 2.7) and starts it alongside Neo4j, MySQL,
and an optional MySQL web UI — no manual conda/PEAR/Neo4j/MySQL setup needed.

## Prerequisites

- Docker Engine + the Docker Compose plugin (`docker compose version`).
- Outbound internet on the **first** start (the Neo4j image downloads the APOC
  plugin; the build downloads pip/PyPI/PEAR packages and NLTK corpora and
  `git clone`s py2neo 4.3.0 from GitHub — it was removed from PyPI).
- ~2–3 GB free disk for images and the build.
- **Apple Silicon (M1/M2/M3) or other arm64 hosts:** `neo4j:3.5` and `mysql:5.7`
  ship no arm64 images, and the Python 2.7 scientific wheels (numpy/scipy/…) are
  x86_64-only, so every service is pinned to `platform: linux/amd64` in
  [docker-compose.yml](docker-compose.yml) and runs under emulation. Nothing to
  do — just expect a slower first build. For better performance, optionally
  enable Docker Desktop → Settings → General → *Use Rosetta for x86_64/amd64
  emulation*.

## Quick start

```bash
docker compose up --build
```

Then open:

| URL                              | What                                            |
|----------------------------------|-------------------------------------------------|
| http://localhost:8080            | The SNA application (register, upload, explore)  |
| http://localhost:7474            | Neo4j Browser (`neo4j` / `snapassword`)          |
| http://localhost:8081            | Adminer — MySQL UI (server `mysql`, `root`/`snapassword`) |

Bolt is published on `localhost:7687` so the in-browser graph (neovis.js) can
talk to Neo4j directly.

Stop with `Ctrl-C`, or run detached with `docker compose up --build -d` and
stop with `docker compose down`.

## What's in the stack

| Service   | Image            | Role |
|-----------|------------------|------|
| `app`     | built here       | PHP gateway (`server.php`) + static frontend + the Python 2.7 backend it `shell_exec`s |
| `neo4j`   | `neo4j:3.5`      | Graph store. APOC auto-installed; `apoc.refactor.mergeNodes` (FB dumper) is allowed |
| `mysql`   | `mysql:5.7`      | `users` + `word_frequency` tables; schema auto-created on first boot |
| `adminer` | `adminer:4`      | Optional MySQL web UI |

The app image bundles both runtimes because `server.php` calls
`python <script>.py` on the same filesystem; they cannot be split into separate
containers.

## Configuration

All wiring lives in [docker-compose.yml](docker-compose.yml). The app reads its
DB connection from environment variables (see
[server/dbConnector.py](server/dbConnector.py)):

```
NEO4J_HOST NEO4J_PORT NEO4J_USER NEO4J_PASSWORD
MYSQL_HOST MYSQL_PORT MYSQL_USER MYSQL_PASSWORD MYSQL_DATABASE
```

### Changing the Neo4j password (important)

The browser-side graph (neovis.js) connects to Neo4j **from your browser**, so
its password is shipped in client JS and cannot read compose env vars. If you
change `NEO4J_AUTH` / `NEO4J_PASSWORD` in `docker-compose.yml`, also update
`server_password` in
[static/visualization/graphVisualization/graphVisualization.js](static/visualization/graphVisualization/graphVisualization.js)
to match, then rebuild (`docker compose up --build`). The default is
`snapassword` in all three places.

## Data persistence

Graph data and SQL rows survive restarts via named volumes (`neo4j_data`,
`neo4j_plugins`, `mysql_data`). Uploaded dump files are **not** persisted — they
are extracted, loaded into Neo4j, and deleted by `server.php` as part of
processing, so they live only briefly inside the container.

Wipe everything (including the databases) and start clean:

```bash
docker compose down -v
```

## Troubleshooting

- **`no matching manifest for linux/arm64/v8` on `docker compose up`.** You're on
  an arm64 host (Apple Silicon). `neo4j:3.5` / `mysql:5.7` have no arm64 images.
  The compose file already pins every service to `platform: linux/amd64`; if you
  hit this, make sure those `platform:` keys are still present and that Docker
  Desktop can run amd64 images (it can by default, via QEMU/Rosetta).
- **MySQL schema didn't appear.** The init SQL in `docker/mysql/init/` runs only
  when the data volume is empty (first boot). After changing it, recreate:
  `docker compose down -v && docker compose up --build`.
- **Neo4j marked unhealthy at first / APOC missing.** First boot downloads APOC
  and warms up the DB; the healthcheck allows 60s. With no internet on first
  boot the plugin can't download — give it network once, or bind-mount the
  matching `apoc-*-all.jar` into the `/plugins` volume and drop
  `NEO4JLABS_PLUGINS`.
- **App can't reach a database.** From inside containers the hosts are the
  service names `neo4j` / `mysql`, not `localhost` — that's what compose sets.
  Check with `docker compose logs app` / `neo4j` / `mysql`.
- **Graph panel stays empty / Bolt errors in the browser console.** Confirm port
  `7687` is published and the `graphVisualization.js` password matches Neo4j.

## Notes

This is a legacy stack (Python 2.7, MySQL 5.7, Neo4j 3.5) pinned for
compatibility with the existing code — appropriate for local/dev use, not as-is
for production. See [README.md](README.md) for the manual (non-Docker) setup and
[CLAUDE.md](CLAUDE.md) for the architecture.
