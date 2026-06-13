# syntax=docker/dockerfile:1
#
# The app is a PHP gateway (server.php) + a React/Mantine frontend (built by
# the node stage below) that shells out to Python 2.7 scripts on the SAME
# filesystem (PHP `shell_exec('python ...')`). PHP and Python must therefore
# live in one image. Base = official PHP 7.4 + Apache on Debian 11 "bullseye",
# which still ships python2 via apt.

# ---------------------------------------------------------------------------
# Stage 1: build the React/Mantine frontend (Vite). Output: /app/dist
# ---------------------------------------------------------------------------
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package.json ./
RUN npm install
COPY frontend/ ./
# vite.config.js sets outDir ../dist, which inside this stage is /dist - keep
# everything under /app instead
RUN npm run build -- --outDir /app/dist --emptyOutDir

# ---------------------------------------------------------------------------
# Stage 2: PHP + Python runtime image
# ---------------------------------------------------------------------------
FROM php:7.4-apache

# ---------------------------------------------------------------------------
# System packages: Python 2.7 + the shared libs the scientific wheels dlopen.
#   libgomp1     -> scikit-learn 0.20.4 (OpenMP) fails to import without it
#   libgfortran5 / libquadmath0 / libgcc-s1 -> back the numpy/scipy wheels
# ---------------------------------------------------------------------------
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        python2 python2-dev \
        ca-certificates curl git \
        libgomp1 libgfortran5 libquadmath0 libgcc-s1; \
    rm -rf /var/lib/apt/lists/*; \
    # server.php invokes `python ...`; make that resolve to Python 2.7
    ln -sf /usr/bin/python2 /usr/local/bin/python

# ---------------------------------------------------------------------------
# pip for Python 2.7. The dedicated 2.7 bootstrap endpoint installs pip 20.3.4
# (+ setuptools<45, wheel) — the generic get-pip.py is Python 3 only now.
# ---------------------------------------------------------------------------
RUN set -eux; \
    curl -fsSL https://bootstrap.pypa.io/pip/2.7/get-pip.py -o /tmp/get-pip.py; \
    python2 /tmp/get-pip.py; \
    rm /tmp/get-pip.py; \
    python2 -m pip --version

# ---------------------------------------------------------------------------
# Python dependencies (copied first so this layer caches across code changes).
# ---------------------------------------------------------------------------
COPY docker/requirements.txt /tmp/requirements.txt
RUN python2 -m pip install --no-cache-dir -r /tmp/requirements.txt

# ---------------------------------------------------------------------------
# NLTK corpora used by server/dataSearcher/nlp/nlp.py: stopwords (italian +
# english) and punkt (word_tokenize).
# ---------------------------------------------------------------------------
ENV NLTK_DATA=/usr/share/nltk_data
RUN python2 -m nltk.downloader -d "$NLTK_DATA" stopwords punkt

# ---------------------------------------------------------------------------
# PEAR Mail packages used by server.php to read the first message of an .mbox
# (require_once 'Mail/Mbox.php' / 'Mail/mimeDecode.php'). Mail_mimeDecode is
# stable; Mail_Mbox is only released as beta, so widen preferred_state first.
# They install under /usr/local/lib/php, already on PHP's default include_path.
# ---------------------------------------------------------------------------
RUN set -eux; \
    pear channel-update pear.php.net; \
    pear config-set preferred_state beta; \
    pear install --alldeps Mail_mimeDecode Mail_Mbox

# ---------------------------------------------------------------------------
# PHP runtime config (500M upload limits, quiet error output).
# ---------------------------------------------------------------------------
COPY docker/php/sna.ini /usr/local/etc/php/conf.d/sna.ini

# ---------------------------------------------------------------------------
# Application code. Explicit COPYs (not `COPY .`) keep the Dockerfile,
# docker-compose.yml and docker/ — which contain dev passwords — out of the
# web-served docroot. .dockerignore drops .pyc/.git/uploaded dumps.
# The frontend (index.html + hashed assets/ + vendor/) comes from the node
# build stage.
# ---------------------------------------------------------------------------
COPY server.php /var/www/html/
COPY --from=frontend /app/dist/ /var/www/html/
COPY server/ /var/www/html/server/
COPY uploads/ /var/www/html/uploads/

# Python import roots. The in-repo `sys.path.append('~/...')` lines never
# expand `~`, so they are dead no-ops; PYTHONPATH is how dbConnector / nlp /
# wordsFrequency / mailSender actually resolve. SNA_BASE tells server.php where
# the Python scripts live.
ENV PYTHONPATH=/var/www/html/server:/var/www/html/server/dataSearcher/nlp \
    SNA_BASE=/var/www/html

# Apache (www-data) shell_execs python and creates uploads/<user>/ at runtime.
RUN chown -R www-data:www-data /var/www/html/uploads

EXPOSE 80
# CMD inherited from base image: apache2-foreground
