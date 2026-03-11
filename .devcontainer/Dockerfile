FROM jupyter/base-notebook:latest

# Install Node.js 20 via conda-forge (avoids requiring curl or external apt repos)
RUN mamba install -y -c conda-forge nodejs=20 git \
    && mamba clean --all -y

# Install tslab globally and register TypeScript and JavaScript kernels
RUN npm install -g tslab \
    && tslab install --python=python3

# Pre-install npm dependencies into a fixed path so the Jupyter kernel
# can find them immediately via NODE_PATH, without waiting for postCreateCommand
COPY package.json /opt/lab-deps/package.json
RUN cd /opt/lab-deps && npm install

ENV NODE_PATH=/opt/lab-deps/node_modules
