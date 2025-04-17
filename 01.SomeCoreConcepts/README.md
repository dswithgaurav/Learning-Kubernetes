# Kubernetes Cluster Setup & Deployment Guide

This guide will walk you through setting up a Kubernetes cluster and deploying your application using standard Kubernetes tools.


## 🔧 What You Need to Set Up

To run applications on Kubernetes, you need to set up the basic infrastructure:

- **Create a Kubernetes Cluster**
  - Includes both **Master Nodes** (control plane) and **Worker Nodes** (where your workloads run)
- **Install Kubernetes Components on Each Node**
  - `kubelet`, `kube-proxy`, and `kube-apiserver` (for control plane)
- **Additional Resources (Optional but Often Required)**
  - Load balancers (e.g., for exposing services)
  - Filesystems or volumes for persistent storage


## ⚙️ What Kubernetes Does

Once your cluster is up and running:

- Kubernetes **creates and manages your Pods** (the smallest deployable unit).
- It ensures your configuration goals (e.g., number of replicas, container image, etc.) are **consistently met**.
- Kubernetes continuously **monitors the state** of your system and performs self-healing.



## 🛠 Installation & Setup

### 1. Cluster Requirements

- **Master Node(s)**: 1 or more (to manage the cluster)
- **Worker Node(s)**: 1 or more (to run workloads)

### 2. Tooling (for Local Development)

You can simulate a cluster using **Minikube** and interact with it using **kubectl**.

#### ✅ Setup on macOS

```bash
# Install kubectl (Kubernetes CLI)
brew install kubectl
kubectl version --client

# Install Minikube (local Kubernetes)
brew install minikube
minikube start

# Enable metrics for autoscaling and monitoring
minikube addons enable metrics-server

# Check the status of your Minikube cluster
minikube status

minikube dashboard
```



## 📦 Understanding Kubernetes Objects

Kubernetes operates using **objects** that describe your desired cluster state. Common types include:

- **Pods**: The smallest unit, containing one or more containers.
- **Deployments**: Manage replicas of Pods and allow for updates/rollbacks.
- **Services**: Provide networking abstraction.
- **Volumes**: Handle persistent data storage.

Objects can be created in two ways:

- **Imperatively**: Using commands (e.g., `kubectl create`)
- **Declaratively**: Using YAML configuration files

> 🧠 **Note**: Pods are ephemeral — they can be stopped and replaced by Kubernetes anytime. For stability, use higher-level objects like **Deployments**.


## 🚀 Using the Deployment Object

A **Deployment** helps manage multiple replicas of a Pod and ensures high availability and scalability.

### Why Use a Deployment?

- Define the **desired state**, Kubernetes maintains it.
- **Scale** easily by changing replica count.
- **Roll back** to previous versions if needed.
- Avoid managing Pods directly — let Kubernetes do it.

### Example Deployment

```bash
# View current deployments and pods
kubectl get deployments
kubectl get pods

# Create a deployment with a custom Docker image
kubectl create deployment first-app --image=gaurav98094/k8sapp
```

### Service Object
Note :  Pods IP keeps on changing.
- Exposes Pods to the Cluster or Externally.
- Services group Pods with a shared IP.
- Services can allow external access to Pods.

```bash
kubectl expose deployment first-app --type=LoadBalancer --port=8080
kubectl get services

minikube service first-app
```

### Scaling
```bash
kubectl scale deployment/first-app --replicas=3
```


### Update/Rollback Deployment
```bash
docker build -t gaurav98094/k8sapp:2
docker push

kubectl set image deployment/first-app gaurav98094/k8sapp=gaurav98094/k8sapp:2
kubectl rollout status deployment/first-app

# If some error in rollback
kubectl rollout undo deployment/first-app

kubectl rollout undo deployment/first-app --to-revision=1
```

#### Clean Environment
```
kubectl delete deployment <dep_name>
```

### Declarative Approach in K8s
```bash

kubectl apply -f=deployment.yaml
kubectl apply -f service.yaml



kubectl delete -f deployment.yaml

# Delete a albel
kubectl delete deployments,services -l group=example
```