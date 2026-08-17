#!/bin/bash

export KUBECONFIG="/mnt/c/Users/iurid/.kube/config"

DEPLOYMENT="deployment.yaml"
SERVICE="service.yaml"

echo "Verificando o Minikube..."

if ! /mnt/c/ProgramData/chocolatey/bin/minikube.exe version >/dev/null 2>&1; then
    echo "Minikube não está instalado."
    exit 1
fi

echo "Minikube encontrado."

echo "Verificando o status do Minikube..."

if ! /mnt/c/ProgramData/chocolatey/bin/minikube.exe status --format='{{.Host}}' 2>/dev/null | grep -q "Running"; then
    echo "Iniciando o Minikube..."
    /mnt/c/ProgramData/chocolatey/bin/minikube.exe start --driver=docker

    if [ $? -ne 0 ]; then
        echo "Erro ao iniciar o Minikube."
        exit 1
    fi
else
    echo "O Minikube já está em execução."
fi

echo "Configurando o kubectl para usar o Minikube..."

kubectl.exe config use-context minikube

echo "Verificando conexão com o Kubernetes..."

kubectl.exe get nodes

if [ $? -ne 0 ]; then
    echo "Não foi possível conectar ao Kubernetes."
    exit 1
fi

echo "Aplicando o deployment..."

kubectl.exe apply -f "$DEPLOYMENT"

if [ $? -ne 0 ]; then
    echo "Erro ao aplicar o deployment."
    exit 1
fi

echo "Aplicando o service..."

kubectl.exe apply -f "$SERVICE"

if [ $? -ne 0 ]; then
    echo "Erro ao aplicar o service."
    exit 1
fi

echo "Aguardando os pods ficarem prontos..."

kubectl.exe wait --for=condition=available --timeout=60s deployment/backend-ebac-python

if [ $? -ne 0 ]; then
    echo "Os pods não ficaram prontos dentro do tempo esperado."
    exit 1
fi

echo "Iniciando o port-forward para localhost:8000 -> service porta 80..."

kubectl.exe port-forward svc/backend-ebac-python-service 8000:80 > /tmp/backend-port-forward.log 2>&1 &

PORT_FORWARD_PID=$!

sleep 3

if ! kill -0 "$PORT_FORWARD_PID" 2>/dev/null; then
    echo "Erro ao iniciar o port-forward."
    cat /tmp/backend-port-forward.log
    exit 1
fi

echo "Abrindo a aplicação no navegador..."

explorer.exe "http://localhost:8000"

echo "A aplicação está rodando em: http://localhost:8000"
echo "Pressione Ctrl+C para encerrar o port-forward e sair."

wait "$PORT_FORWARD_PID"