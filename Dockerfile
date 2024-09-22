# Use the base image for Python setup
# Reuse the stage from Dockerfile.build
FROM xcov19-setup AS run

# Set the working directory
WORKDIR /app

# Bust cached build if --build CACHEBUST=<some data> is passed 
# to ensure updated source code is built
ARG CACHEBUST
COPY --chown=nonroot:nonroot --chmod=555 xcov19 xcov19/
COPY --chown=nonroot:nonroot --chmod=555 Makefile .
COPY --chown=nonroot:nonroot --chmod=555 *.sh .

USER nonroot:nonroot

# Set the start command
ARG START_CMD="make run"
ENV START_CMD=${START_CMD}
RUN if [ -z "${START_CMD}" ]; then echo "Unable to detect a container start command" && exit 1; fi
CMD ${START_CMD}