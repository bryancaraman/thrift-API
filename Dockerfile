# python3.10 -m venv venv
FROM python:3.10

# Common practice is to update all packages
RUN apt-get update -y && apt-get install graphviz xdg-utils -y

# Copy our requirements first, so that this layer is cached
COPY requirements.txt /app/

# Install our requirements
RUN pip install -r /app/requirements.txt

# Tell docker to use the /app folder as our working directory
VOLUME /cart_api
WORKDIR /

# Run the command
ENV API_PORT 8000
CMD gunicorn --bind=0.0.0.0:$API_PORT cart_api.api:api --access-logfile - --reload --reload-extra-file /swagger/api.json
