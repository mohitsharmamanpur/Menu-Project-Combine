import streamlit as st
import subprocess
import json
import requests
import yaml
import os
from datetime import datetime
import paramiko
from typing import Tuple

def log_command(command):
    """Log command to file"""
    with open("command_log.txt", "a") as f:
        f.write(f"{datetime.now()}: {command}\n")

def run_command(command, shell=True):
    """Run shell command and return result"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def run_ssh_command(command: str, client: paramiko.SSHClient) -> Tuple[str, str]:
    try:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        return output, error
    except Exception as e:
        return '', str(e)

def devops_section(sub_choice=None):
    st.markdown('<h1 class="section-header">⚙️ DevOps Automation Platform</h1>', unsafe_allow_html=True)
    
    if sub_choice == "🐳 Docker":
        docker_section()
    elif sub_choice == "⚙️ Jenkins":
        jenkins_section()
    elif sub_choice == "☸️ Kubernetes":
        kubernetes_section()
    else:
        st.info("Please select a DevOps tool from the sidebar.")

def docker_section():
    st.subheader("🐳 Docker SSH Automation Platform")
    st.markdown("---")
    st.subheader("🔐 SSH Connection Required")

    with st.sidebar.expander("🔧 SSH Connection Setup (for Docker)", expanded=True):
        host = st.text_input("Hostname / IP", placeholder="e.g. 192.168.1.10", key="docker_ssh_host")
        port = st.number_input("Port", min_value=1, max_value=65535, value=22, key="docker_ssh_port")
        username = st.text_input("Username", placeholder="e.g. root or ubuntu", key="docker_ssh_user")
        password = st.text_input("Password", type="password", key="docker_ssh_pass")

        if "docker_ssh_client" not in st.session_state:
            st.session_state.docker_ssh_client = None
        if "docker_ssh_connected" not in st.session_state:
            st.session_state.docker_ssh_connected = False

        if st.button("🔌 Connect via SSH (Docker)"):
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=host, port=int(port), username=username, password=password, timeout=10)
                st.session_state.docker_ssh_client = client
                st.session_state.docker_ssh_connected = True
                st.success("✅ SSH Connection Established Successfully!")
            except Exception as e:
                st.session_state.docker_ssh_connected = False
                st.session_state.docker_ssh_client = None
                st.error(f"❌ Connection Failed: {e}")

    if not st.session_state.docker_ssh_connected or st.session_state.docker_ssh_client is None:
        st.info("Please connect via SSH to automate Docker tasks.")
        return

    st.success("SSH Connected! You can now automate Docker tasks.")
    client = st.session_state.docker_ssh_client

    tab_names = [
        "📦 Images", "🚀 Containers", "🌐 Networks", "💾 Volumes", "🛠️ Compose", "📋 System", "🤖 Prompt"
    ]
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(tab_names)

    # --- Images ---
    with tab1:
        st.subheader("📦 Docker Images")
        if st.button("List Images"):
            output, error = run_ssh_command("docker images", client)
            st.code(output) if not error else st.error(error)
        image_name = st.text_input("Image Name to Remove", key="img_rm")
        if st.button("Remove Image") and image_name:
            output, error = run_ssh_command(f"docker rmi {image_name}", client)
            st.success(f"Removed image {image_name}") if not error else st.error(error)
        st.markdown("---")
        st.subheader("Build Image")
        build_name = st.text_input("Image Name (e.g. myapp:latest)", key="img_build")
        dockerfile = st.text_input("Dockerfile Path", value="./Dockerfile", key="img_build_dockerfile")
        if st.button("Build Image") and build_name and dockerfile:
            output, error = run_ssh_command(f"docker build -t {build_name} {dockerfile}", client)
            st.success(f"Built image {build_name}") if not error else st.error(error)
        if st.button("Prune Unused Images"):
            output, error = run_ssh_command("docker image prune -f", client)
            st.success("Pruned unused images.") if not error else st.error(error)

    # --- Containers ---
    with tab2:
        st.subheader("🚀 Docker Containers")
        if st.button("List Containers"):
            output, error = run_ssh_command("docker ps -a", client)
            st.code(output) if not error else st.error(error)
        run_img = st.text_input("Image to Run", key="ctr_run_img")
        run_name = st.text_input("Container Name", key="ctr_run_name")
        run_ports = st.text_input("Port Mapping (host:container)", value="8080:80", key="ctr_run_ports")
        if st.button("Run Container") and run_img and run_name:
            output, error = run_ssh_command(f"docker run -d --name {run_name} -p {run_ports} {run_img}", client)
            st.success(f"Started container {run_name}") if not error else st.error(error)
        ctr_id = st.text_input("Container ID/Name for Action", key="ctr_id")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Start") and ctr_id:
                output, error = run_ssh_command(f"docker start {ctr_id}", client)
                st.success(f"Started {ctr_id}") if not error else st.error(error)
        with col2:
            if st.button("Stop") and ctr_id:
                output, error = run_ssh_command(f"docker stop {ctr_id}", client)
                st.success(f"Stopped {ctr_id}") if not error else st.error(error)
        with col3:
            if st.button("Restart") and ctr_id:
                output, error = run_ssh_command(f"docker restart {ctr_id}", client)
                st.success(f"Restarted {ctr_id}") if not error else st.error(error)
        with col4:
            if st.button("Remove") and ctr_id:
                output, error = run_ssh_command(f"docker rm -f {ctr_id}", client)
                st.success(f"Removed {ctr_id}") if not error else st.error(error)
        if st.button("Prune Stopped Containers"):
            output, error = run_ssh_command("docker container prune -f", client)
            st.success("Pruned stopped containers.") if not error else st.error(error)

    # --- Networks ---
    with tab3:
        st.subheader("🌐 Docker Networks")
        if st.button("List Networks"):
            output, error = run_ssh_command("docker network ls", client)
            st.code(output) if not error else st.error(error)
        net_name = st.text_input("Network Name to Create", key="net_create")
        if st.button("Create Network") and net_name:
            output, error = run_ssh_command(f"docker network create {net_name}", client)
            st.success(f"Created network {net_name}") if not error else st.error(error)

    # --- Volumes ---
    with tab4:
        st.subheader("💾 Docker Volumes")
        if st.button("List Volumes"):
            output, error = run_ssh_command("docker volume ls", client)
            st.code(output) if not error else st.error(error)
        vol_name = st.text_input("Volume Name to Create", key="vol_create")
        if st.button("Create Volume") and vol_name:
            output, error = run_ssh_command(f"docker volume create {vol_name}", client)
            st.success(f"Created volume {vol_name}") if not error else st.error(error)

    # --- Compose ---
    with tab5:
        st.subheader("🛠️ Docker Compose")
        compose_file = st.text_input("Compose File Path (e.g. docker-compose.yml)", key="compose_file")
        if st.button("Up (Start Services)") and compose_file:
            output, error = run_ssh_command(f"docker compose -f {compose_file} up -d", client)
            st.success("Compose up executed.") if not error else st.error(error)
        if st.button("Down (Stop Services)") and compose_file:
            output, error = run_ssh_command(f"docker compose -f {compose_file} down", client)
            st.success("Compose down executed.") if not error else st.error(error)
        if st.button("List Compose Services") and compose_file:
            output, error = run_ssh_command(f"docker compose -f {compose_file} ps", client)
            st.code(output) if not error else st.error(error)

    # --- System ---
    with tab6:
        st.subheader("📋 Docker System Info & Prune")
        if st.button("System Info"):
            output, error = run_ssh_command("docker system info", client)
            st.code(output) if not error else st.error(error)
        if st.button("System Disk Usage"):
            output, error = run_ssh_command("docker system df", client)
            st.code(output) if not error else st.error(error)
        if st.button("System Prune"):
            output, error = run_ssh_command("docker system prune -f", client)
            st.success("System pruned.") if not error else st.error(error)

    # --- Prompt-based ---
    with tab7:
        st.subheader("🤖 Prompt-based Docker Automation (SSH)")
        prompt = st.text_input("Describe your Docker task (e.g. 'list all containers', 'remove image nginx', 'start container myapp', 'prune unused images')", key="docker_ssh_prompt")
        if st.button("🚀 Automate Docker Task") and prompt:
            import re
            command = None
            # Safe prompt-to-command mapping for Docker
            if re.search(r"list.*containers", prompt, re.I):
                command = "docker ps -a"
            elif re.search(r"list.*images", prompt, re.I):
                command = "docker images"
            elif re.search(r"remove.*image ([\w:.-]+)", prompt, re.I):
                match = re.search(r"remove.*image ([\w:.-]+)", prompt, re.I)
                if match:
                    image = match.group(1)
                    command = f"docker rmi {image}"
            elif re.search(r"remove.*container ([\w-]+)", prompt, re.I):
                match = re.search(r"remove.*container ([\w-]+)", prompt, re.I)
                if match:
                    container = match.group(1)
                    command = f"docker rm -f {container}"
            elif re.search(r"start.*container ([\w-]+)", prompt, re.I):
                match = re.search(r"start.*container ([\w-]+)", prompt, re.I)
                if match:
                    container = match.group(1)
                    command = f"docker start {container}"
            elif re.search(r"stop.*container ([\w-]+)", prompt, re.I):
                match = re.search(r"stop.*container ([\w-]+)", prompt, re.I)
                if match:
                    container = match.group(1)
                    command = f"docker stop {container}"
            elif re.search(r"restart.*container ([\w-]+)", prompt, re.I):
                match = re.search(r"restart.*container ([\w-]+)", prompt, re.I)
                if match:
                    container = match.group(1)
                    command = f"docker restart {container}"
            elif re.search(r"prune.*images", prompt, re.I):
                command = "docker image prune -f"
            elif re.search(r"prune.*containers", prompt, re.I):
                command = "docker container prune -f"
            elif re.search(r"build.*image ([\w:.-]+)", prompt, re.I):
                match = re.search(r"build.*image ([\w:.-]+)", prompt, re.I)
                if match:
                    image = match.group(1)
                    dockerfile = st.text_input("Dockerfile Path for Build", value="./Dockerfile", key="dockerfile_path")
                    if st.button("Build Image Now"):
                        command = f"docker build -t {image} {dockerfile}"
            elif re.search(r"run.*container ([\w-]+) from image ([\w:.-]+)", prompt, re.I):
                match = re.search(r"run.*container ([\w-]+) from image ([\w:.-]+)", prompt, re.I)
                if match:
                    container, image = match.group(1), match.group(2)
                    ports = st.text_input("Port Mapping (host:container)", value="8080:80", key="docker_run_ports")
                    if st.button("Run Container Now"):
                        command = f"docker run -d --name {container} -p {ports} {image}"
            elif re.search(r"list.*networks", prompt, re.I):
                command = "docker network ls"
            elif re.search(r"create.*network ([\w-]+)", prompt, re.I):
                match = re.search(r"create.*network ([\w-]+)", prompt, re.I)
                if match:
                    network = match.group(1)
                    command = f"docker network create {network}"
            elif re.search(r"list.*volumes", prompt, re.I):
                command = "docker volume ls"
            elif re.search(r"create.*volume ([\w-]+)", prompt, re.I):
                match = re.search(r"create.*volume ([\w-]+)", prompt, re.I)
                if match:
                    volume = match.group(1)
                    command = f"docker volume create {volume}"
            elif re.search(r"system info", prompt, re.I):
                command = "docker system info"
            elif re.search(r"system prune", prompt, re.I):
                command = "docker system prune -f"
            else:
                command = prompt  # fallback: treat as raw command
            if command:
                output, error = run_ssh_command(command, client)
                if error:
                    st.error(error)
                else:
                    st.code(output, language="bash")
            else:
                st.warning("Could not interpret the prompt. Please try a different description.")
        if st.button("❌ Disconnect (Docker SSH)"):
            st.session_state.docker_ssh_client.close()
            st.session_state.docker_ssh_connected = False
            st.success("🔌 Disconnected Successfully!")

def jenkins_section():
    st.subheader("⚙️ Jenkins Automation")
    
    # Jenkins configuration
    st.subheader("🔧 Jenkins Configuration")
    jenkins_url = st.text_input("Jenkins URL:", value="http://localhost:8080")
    username = st.text_input("Username:")
    api_token = st.text_input("API Token:", type="password")
    
    if st.button("🔗 Test Connection"):
        if jenkins_url and username and api_token:
            try:
                response = requests.get(f"{jenkins_url}/api/json", 
                                      auth=(username, api_token), 
                                      timeout=10)
                if response.status_code == 200:
                    st.success("✅ Jenkins connection successful!")
                    st.session_state.jenkins_config = {
                        'url': jenkins_url,
                        'username': username,
                        'api_token': api_token
                    }
                else:
                    st.error(f"Connection failed: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please provide Jenkins URL, username, and API token")
    
    # Jenkins operations
    if 'jenkins_config' in st.session_state:
        config = st.session_state.jenkins_config
        
        tab1, tab2, tab3 = st.tabs(["📋 Jobs", "🚀 Builds", "📊 Dashboard"])
        
        with tab1:
            st.subheader("📋 Jenkins Jobs")
            
            if st.button("🔄 Refresh Jobs"):
                try:
                    response = requests.get(f"{config['url']}/api/json?tree=jobs[name,url,color,builds[number,result,timestamp]]", 
                                          auth=(config['username'], config['api_token']))
                    if response.status_code == 200:
                        jobs_data = response.json()
                        st.session_state.jenkins_jobs = jobs_data['jobs']
                        st.success("Jobs refreshed!")
                    else:
                        st.error("Failed to fetch jobs")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            if 'jenkins_jobs' in st.session_state:
                jobs = st.session_state.jenkins_jobs
                
                for job in jobs:
                    with st.expander(f"📋 {job['name']} - {job.get('color', 'N/A')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button(f"▶️ Build {job['name']}", key=f"build_{job['name']}"):
                                try:
                                    response = requests.post(f"{job['url']}build", 
                                                          auth=(config['username'], config['api_token']))
                                    if response.status_code in [200, 201]:
                                        st.success(f"Build triggered for {job['name']}!")
                                        log_command(f"Jenkins: Triggered build for {job['name']}")
                                    else:
                                        st.error(f"Failed to trigger build: {response.status_code}")
                                except Exception as e:
                                    st.error(f"Error: {e}")
                        
                        with col2:
                            if st.button(f"📊 View {job['name']}", key=f"view_{job['name']}"):
                                st.write(f"Job URL: {job['url']}")
                                if 'builds' in job and job['builds']:
                                    st.write("Recent builds:")
                                    for build in job['builds'][:5]:
                                        st.write(f"- Build #{build['number']}: {build.get('result', 'N/A')}")
        
        with tab2:
            st.subheader("🚀 Build Management")
            
            job_name = st.text_input("Job Name for Build Operations:")
            if job_name:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("▶️ Trigger Build"):
                        try:
                            response = requests.post(f"{config['url']}/job/{job_name}/build", 
                                                  auth=(config['username'], config['api_token']))
                            if response.status_code in [200, 201]:
                                st.success(f"Build triggered for {job_name}!")
                                log_command(f"Jenkins: Triggered build for {job_name}")
                            else:
                                st.error(f"Failed to trigger build: {response.status_code}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with col2:
                    if st.button("⏸️ Stop Build"):
                        try:
                            response = requests.post(f"{config['url']}/job/{job_name}/lastBuild/stop", 
                                                  auth=(config['username'], config['api_token']))
                            if response.status_code == 200:
                                st.success(f"Build stopped for {job_name}!")
                            else:
                                st.error(f"Failed to stop build: {response.status_code}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                
                with col3:
                    if st.button("📋 Build History"):
                        try:
                            response = requests.get(f"{config['url']}/job/{job_name}/api/json?tree=builds[number,result,timestamp,duration]", 
                                                  auth=(config['username'], config['api_token']))
                            if response.status_code == 200:
                                build_data = response.json()
                                if 'builds' in build_data:
                                    st.write("Build History:")
                                    for build in build_data['builds'][:10]:
                                        st.write(f"- Build #{build['number']}: {build.get('result', 'N/A')} ({build.get('duration', 0)}ms)")
                            else:
                                st.error(f"Failed to fetch build history: {response.status_code}")
                        except Exception as e:
                            st.error(f"Error: {e}")
        
        with tab3:
            st.subheader("📊 Jenkins Dashboard")
            
            if st.button("📊 Get System Info"):
                try:
                    response = requests.get(f"{config['url']}/api/json", 
                                          auth=(config['username'], config['api_token']))
                    if response.status_code == 200:
                        system_info = response.json()
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Jobs", system_info.get('numJobs', 'N/A'))
                        with col2:
                            st.metric("Total Executors", system_info.get('numExecutors', 'N/A'))
                        with col3:
                            st.metric("Busy Executors", system_info.get('busyExecutors', 'N/A'))
                        with col4:
                            st.metric("Queue Length", system_info.get('queueLength', 'N/A'))
                        
                        st.json(system_info)
                    else:
                        st.error(f"Failed to fetch system info: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")

def kubernetes_section():
    st.subheader("☸️ Kubernetes Management")
    
    # Check if kubectl is available
    success, output, error = run_command("kubectl version --client")
    if not success:
        st.error("❌ kubectl not found. Please install kubectl to use Kubernetes features.")
        st.info("Install kubectl from: https://kubernetes.io/docs/tasks/tools/install-kubectl/")
        return
    
    st.success("✅ kubectl found!")
    
    # Create tabs for different K8s operations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Resources", "🚀 Deployments", "🌐 Services", "💾 ConfigMaps & Secrets", "📊 Monitoring"
    ])
    
    with tab1:
        st.subheader("📋 Kubernetes Resources")
        
        resource_type = st.selectbox("Resource Type:", [
            "pods", "deployments", "services", "configmaps", "secrets", "nodes", "namespaces"
        ])
        
        namespace = st.text_input("Namespace (leave empty for all):", value="default")
        
        if st.button(f"📋 List {resource_type}"):
            cmd = f"kubectl get {resource_type}"
            if namespace:
                cmd += f" -n {namespace}"
            cmd += " -o wide"
            
            success, output, error = run_command(cmd)
            if success:
                st.code(output)
                log_command(f"Kubernetes: Listed {resource_type}")
            else:
                st.error(f"Error: {error}")
    
    with tab2:
        st.subheader("🚀 Deployment Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Deployments")
            if st.button("📋 List Deployments"):
                success, output, error = run_command("kubectl get deployments -o wide")
                if success:
                    st.code(output)
                else:
                    st.error(f"Error: {error}")
        
        with col2:
            st.subheader("🔧 Scale Deployment")
            deployment_name = st.text_input("Deployment Name:")
            replicas = st.number_input("Number of Replicas:", min_value=0, max_value=10, value=1)
            
            if st.button("⚖️ Scale"):
                if deployment_name:
                    success, output, error = run_command(f"kubectl scale deployment {deployment_name} --replicas={replicas}")
                    if success:
                        st.success(f"Scaled {deployment_name} to {replicas} replicas!")
                        log_command(f"Kubernetes: Scaled deployment {deployment_name} to {replicas} replicas")
                    else:
                        st.error(f"Error: {error}")
                else:
                    st.warning("Please provide deployment name")
        
        # Deploy from YAML
        st.subheader("📄 Deploy from YAML")
        yaml_content = st.text_area("Paste your YAML configuration:", height=200)
        
        if st.button("🚀 Deploy"):
            if yaml_content:
                # Save YAML to temporary file
                with open("temp_deployment.yaml", "w") as f:
                    f.write(yaml_content)
                
                success, output, error = run_command("kubectl apply -f temp_deployment.yaml")
                if success:
                    st.success("Deployment applied successfully!")
                    log_command("Kubernetes: Applied deployment from YAML")
                else:
                    st.error(f"Error: {error}")
                
                # Clean up
                os.remove("temp_deployment.yaml")
            else:
                st.warning("Please provide YAML content")
    
    with tab3:
        st.subheader("🌐 Service Management")
        
        if st.button("📋 List Services"):
            success, output, error = run_command("kubectl get services -o wide")
            if success:
                st.code(output)
            else:
                st.error(f"Error: {error}")
        
        # Create service
        st.subheader("🌐 Create Service")
        service_name = st.text_input("Service Name:")
        service_type = st.selectbox("Service Type:", ["ClusterIP", "NodePort", "LoadBalancer"])
        port = st.number_input("Port:", min_value=1, max_value=65535, value=80)
        target_port = st.number_input("Target Port:", min_value=1, max_value=65535, value=80)
        
        if st.button("🌐 Create Service"):
            if service_name:
                cmd = f"kubectl expose deployment {service_name} --type={service_type} --port={port} --target-port={target_port}"
                success, output, error = run_command(cmd)
                if success:
                    st.success(f"Service {service_name} created!")
                    log_command(f"Kubernetes: Created service {service_name}")
                else:
                    st.error(f"Error: {error}")
            else:
                st.warning("Please provide service name")
    
    with tab4:
        st.subheader("💾 ConfigMaps & Secrets")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 ConfigMaps")
            if st.button("📋 List ConfigMaps"):
                success, output, error = run_command("kubectl get configmaps")
                if success:
                    st.code(output)
                else:
                    st.error(f"Error: {error}")
        
        with col2:
            st.subheader("🔐 Secrets")
            if st.button("📋 List Secrets"):
                success, output, error = run_command("kubectl get secrets")
                if success:
                    st.code(output)
                else:
                    st.error(f"Error: {error}")
    
    with tab5:
        st.subheader("📊 Kubernetes Monitoring")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Node Status"):
                success, output, error = run_command("kubectl get nodes -o wide")
                if success:
                    st.code(output)
                else:
                    st.error(f"Error: {error}")
        
        with col2:
            if st.button("📊 Pod Status"):
                success, output, error = run_command("kubectl get pods -o wide")
                if success:
                    st.code(output)
                else:
                    st.error(f"Error: {error}")
        
        # Resource usage
        st.subheader("📈 Resource Usage")
        if st.button("📈 Top Pods"):
            success, output, error = run_command("kubectl top pods")
            if success:
                st.code(output)
            else:
                st.error(f"Error: {error}")
        
        if st.button("📈 Top Nodes"):
            success, output, error = run_command("kubectl top nodes")
            if success:
                st.code(output)
            else:
                st.error(f"Error: {error}")
