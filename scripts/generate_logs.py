import time
import random
import subprocess
import requests
import logging
import os

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("log-generator")

# Microservices endpoints
MICROSERVICE_ENDPOINTS = [
    "http://localhost:8001/login",
    "http://localhost:8001/logout",
    "http://localhost:8002/process",
    "http://localhost:8002/refund"
]

# Script paths
ACT_COMMAND = ["act", "-W", ".github/workflows/ci.yml", "-b"]
K8S_LOG_SCRIPT = "scripts/collect_k8s_logs.sh"
TERRAFORM_SCRIPT = "scripts/terraform-simulate.sh"

def trigger_microservice():
    endpoint = random.choice(MICROSERVICE_ENDPOINTS)
    try:
        response = requests.get(endpoint, timeout=5)
        logger.info(f"Triggered {endpoint}: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Failed to trigger {endpoint}: {e}")

def run_act_workflow():
    try:
        result = subprocess.run(ACT_COMMAND, check=True, capture_output=True, text=True)
        logger.info("Ran GitHub Actions workflow successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run GitHub Actions workflow: {e.stderr}")

def run_k8s_log_script():
    if os.path.exists(K8S_LOG_SCRIPT):
        try:
            result = subprocess.run([K8S_LOG_SCRIPT], check=True, capture_output=True, text=True)
            logger.info("Ran Kubernetes log collection script successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to run Kubernetes log script: {e.stderr}")
    else:
        logger.error(f"Kubernetes log script not found: {K8S_LOG_SCRIPT}")

def run_terraform_script():
    if os.path.exists(TERRAFORM_SCRIPT):
        try:
            result = subprocess.run([TERRAFORM_SCRIPT], check=True, capture_output=True, text=True)
            logger.info("Ran Terraform simulation script successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to run Terraform script: {e.stderr}")
    else:
        logger.error(f"Terraform script not found: {TERRAFORM_SCRIPT}")

def main():
    logger.info("Before running this script please make sure Docker and Minikube are running")
    logger.info("Run \"docker-compose up --build\" if not sure")
    logger.info("Run \"minikube start\" as well if not sure")
    logger.warning("Please don't forget to stop them after terminating the current script with Ctrl+C..")
    logger.warning("Use \"docker-compose down\" for stopping Docker processes")
    logger.warning("and \"minikube stop\" for stopping Minikube\n\n\n")

    logger.info("Starting log generation script")
    while True:
        # Randomly select a log source to trigger
        action = random.choice([
            trigger_microservice,
            run_act_workflow,
            run_k8s_log_script,
            run_terraform_script
        ])
        action()
        # Random sleep between 10 and 30 seconds
        sleep_time = random.randint(10, 30)
        logger.info(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
