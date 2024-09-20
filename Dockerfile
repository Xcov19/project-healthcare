# Use the base image for Python setup
# Reuse the stage from Dockerfile.build
FROM xcov19-setup AS run

USER nonroot:nonroot

# Set the start command
ARG START_CMD="make run"
ENV START_CMD=${START_CMD}
RUN if [ -z "${START_CMD}" ]; then echo "Unable to detect a container start command" && exit 1; fi
CMD ${START_CMD}