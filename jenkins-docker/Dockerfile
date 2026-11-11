
FROM jenkins/jenkins:2.580.2-jdk21

USER root

# Install required utilities
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    awscli \
    jq \
    git \
    python3 \
    python3-pip \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
       -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
       > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Jenkins plugins
USER jenkins

RUN jenkins-plugin-cli --plugins \
    "workflow-aggregator" \
    "git" \
    "credentials-binding" \
    "pipeline-stage-view" \
    "docker-workflow" \
    "ws-cleanup"
