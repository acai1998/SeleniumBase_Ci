#!/bin/bash

DOCKERHUB_USER="imacaiy"
LOCAL_IMAGE="seleniumbase-test:latest"
REMOTE_IMAGE="${DOCKERHUB_USER}/seleniumbase-test:latest"

# 读取环境变量中的密码，推荐先 export DOCKERHUB_PASS=你的token
echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin || { echo "登录失败！"; exit 1; }

docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE} || { echo "打标签失败！"; exit 1; }

docker push ${REMOTE_IMAGE} || { echo "推送失败！"; exit 1; }

echo "完成，镜像已上传到 Docker Hub: ${REMOTE_IMAGE}"
