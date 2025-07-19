import streamlit as st
import subprocess
import paramiko
from typing import Optional, Tuple

# --- Add background image and overlay CSS for UI/UX consistency ---
st.markdown("""
<style>
body, .stApp {
    background-image: linear-gradient(rgba(30,30,30,0.85), rgba(30,30,30,0.85)), url('https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
</style>
""", unsafe_allow_html=True)

def run_ssh_command(command: str, client: paramiko.SSHClient) -> Tuple[str, str]:
    try:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        return output, error
    except Exception as e:
        return '', str(e)

def linux_section():
    st.header("🐧 Linux SSH Automation Platform")
    st.markdown("---")
    st.subheader("🔐 SSH Connection Required")

    with st.sidebar.expander("🔧 SSH Connection Setup (for Linux)", expanded=True):
        host = st.text_input("Hostname / IP", placeholder="e.g. 192.168.1.10", key="linux_ssh_host")
        port = st.number_input("Port", min_value=1, max_value=65535, value=22, key="linux_ssh_port")
        username = st.text_input("Username", placeholder="e.g. root or ubuntu", key="linux_ssh_user")
        password = st.text_input("Password", type="password", key="linux_ssh_pass")

        if "linux_ssh_client" not in st.session_state:
            st.session_state.linux_ssh_client = None
        if "linux_ssh_connected" not in st.session_state:
            st.session_state.linux_ssh_connected = False

        if st.button("🔌 Connect via SSH (Linux)"):
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=host, port=int(port), username=username, password=password, timeout=10)
                st.session_state.linux_ssh_client = client
                st.session_state.linux_ssh_connected = True
                st.success("✅ SSH Connection Established Successfully!")
            except Exception as e:
                st.session_state.linux_ssh_connected = False
                st.session_state.linux_ssh_client = None
                st.error(f"❌ Connection Failed: {e}")

    if not st.session_state.linux_ssh_connected or st.session_state.linux_ssh_client is None:
        st.info("Please connect via SSH to automate Linux tasks.")
        return

    st.success("SSH Connected! You can now automate Linux tasks with a prompt.")
    client = st.session_state.linux_ssh_client

    st.markdown("---")
    st.subheader("🤖 Prompt-based Linux Automation (SSH)")
    prompt = st.text_input("Describe your Linux task (e.g. 'create a folder test', 'list files', 'show disk usage', 'add user john', 'install package nginx', 'restart service ssh', 'extract tar.gz', etc.)", key="linux_ssh_prompt")
    if st.button("🚀 Automate Linux Task") and prompt:
        import re
        command = None
        # Prompt-to-command mapping for all major Linux tasks
        # File/Directory
        if re.search(r"create.*folder.* ([\w-]+)", prompt, re.I):
            match = re.search(r"create.*folder.* ([\w-]+)", prompt, re.I)
            if match:
                folder = match.group(1)
                command = f"mkdir -p {folder}"
        elif re.search(r"delete.*folder.* ([\w-]+)", prompt, re.I):
            match = re.search(r"delete.*folder.* ([\w-]+)", prompt, re.I)
            if match:
                folder = match.group(1)
                command = f"rm -rf {folder}"
        elif re.search(r"create.*file.* ([\w.-]+)", prompt, re.I):
            match = re.search(r"create.*file.* ([\w.-]+)", prompt, re.I)
            if match:
                file = match.group(1)
                command = f"touch {file}"
        elif re.search(r"delete.*file.* ([\w.-]+)", prompt, re.I):
            match = re.search(r"delete.*file.* ([\w.-]+)", prompt, re.I)
            if match:
                file = match.group(1)
                command = f"rm -f {file}"
        elif re.search(r"list.*files", prompt, re.I):
            command = "ls -l"
        elif re.search(r"view.*file.* ([\w.-]+)", prompt, re.I):
            match = re.search(r"view.*file.* ([\w.-]+)", prompt, re.I)
            if match:
                file = match.group(1)
                command = f"cat {file}"
        elif re.search(r"move.* ([\w.-]+) to ([\w./-]+)", prompt, re.I):
            match = re.search(r"move.* ([\w.-]+) to ([\w./-]+)", prompt, re.I)
            if match:
                src, dst = match.group(1), match.group(2)
                command = f"mv {src} {dst}"
        elif re.search(r"copy.* ([\w.-]+) to ([\w./-]+)", prompt, re.I):
            match = re.search(r"copy.* ([\w.-]+) to ([\w./-]+)", prompt, re.I)
            if match:
                src, dst = match.group(1), match.group(2)
                command = f"cp -r {src} {dst}"
        # System Info
        elif re.search(r"current directory|pwd", prompt, re.I):
            command = "pwd"
        elif re.search(r"disk usage", prompt, re.I):
            command = "df -h"
        elif re.search(r"memory usage", prompt, re.I):
            command = "free -h"
        elif re.search(r"cpu info", prompt, re.I):
            command = "lscpu"
        elif re.search(r"processes|ps aux", prompt, re.I):
            command = "ps aux"
        elif re.search(r"uptime", prompt, re.I):
            command = "uptime"
        elif re.search(r"logged.*users", prompt, re.I):
            command = "who"
        # Networking
        elif re.search(r"ip address", prompt, re.I):
            command = "hostname -I"
        elif re.search(r"network interfaces", prompt, re.I):
            command = "ip a"
        elif re.search(r"ping ([\w.-]+)", prompt, re.I):
            match = re.search(r"ping ([\w.-]+)", prompt, re.I)
            if match:
                host = match.group(1)
                command = f"ping -c 4 {host}"
        elif re.search(r"open ports", prompt, re.I):
            command = "ss -tuln"
        # User Management
        elif re.search(r"list users", prompt, re.I):
            command = "cut -d: -f1 /etc/passwd"
        elif re.search(r"add user ([\w-]+)", prompt, re.I):
            match = re.search(r"add user ([\w-]+)", prompt, re.I)
            if match:
                user = match.group(1)
                command = f"sudo useradd {user}"
        elif re.search(r"delete user ([\w-]+)", prompt, re.I):
            match = re.search(r"delete user ([\w-]+)", prompt, re.I)
            if match:
                user = match.group(1)
                command = f"sudo userdel {user}"
        elif re.search(r"change password for ([\w-]+)", prompt, re.I):
            match = re.search(r"change password for ([\w-]+)", prompt, re.I)
            if match:
                user = match.group(1)
                passwd = st.text_input(f"New password for {user}", type="password", key="passwd_input")
                if st.button("Set Password") and passwd:
                    command = f"echo '{user}:{passwd}' | sudo chpasswd"
        # Package Management
        elif re.search(r"update packages", prompt, re.I):
            command = "sudo apt update"
        elif re.search(r"upgrade packages", prompt, re.I):
            command = "sudo apt upgrade -y"
        elif re.search(r"install package ([\w.-]+)", prompt, re.I):
            match = re.search(r"install package ([\w.-]+)", prompt, re.I)
            if match:
                pkg = match.group(1)
                command = f"sudo apt install -y {pkg}"
        elif re.search(r"remove package ([\w.-]+)", prompt, re.I):
            match = re.search(r"remove package ([\w.-]+)", prompt, re.I)
            if match:
                pkg = match.group(1)
                command = f"sudo apt remove -y {pkg}"
        # Permissions
        elif re.search(r"change owner of ([\w./-]+) to ([\w:-]+)", prompt, re.I):
            match = re.search(r"change owner of ([\w./-]+) to ([\w:-]+)", prompt, re.I)
            if match:
                target, owner = match.group(1), match.group(2)
                command = f"sudo chown {owner} {target}"
        elif re.search(r"change permissions of ([\w./-]+) to ([0-7]{3,4})", prompt, re.I):
            match = re.search(r"change permissions of ([\w./-]+) to ([0-7]{3,4})", prompt, re.I)
            if match:
                target, mode = match.group(1), match.group(2)
                command = f"chmod {mode} {target}"
        # Archive/Compression
        elif re.search(r"compress ([\w./-]+) to ([\w.-]+\.tar\.gz)", prompt, re.I):
            match = re.search(r"compress ([\w./-]+) to ([\w.-]+\.tar\.gz)", prompt, re.I)
            if match:
                src, out = match.group(1), match.group(2)
                command = f"tar -czvf {out} {src}"
        elif re.search(r"extract ([\w.-]+\.tar\.gz) to ([\w./-]+)", prompt, re.I):
            match = re.search(r"extract ([\w.-]+\.tar\.gz) to ([\w./-]+)", prompt, re.I)
            if match:
                tar, dest = match.group(1), match.group(2)
                command = f"tar -xzvf {tar} -C {dest}"
        elif re.search(r"compress ([\w./-]+) to ([\w.-]+\.zip)", prompt, re.I):
            match = re.search(r"compress ([\w./-]+) to ([\w.-]+\.zip)", prompt, re.I)
            if match:
                src, out = match.group(1), match.group(2)
                command = f"zip -r {out} {src}"
        elif re.search(r"extract ([\w.-]+\.zip) to ([\w./-]+)", prompt, re.I):
            match = re.search(r"extract ([\w.-]+\.zip) to ([\w./-]+)", prompt, re.I)
            if match:
                zipf, dest = match.group(1), match.group(2)
                command = f"unzip {zipf} -d {dest}"
        # System Control
        elif re.search(r"shutdown", prompt, re.I):
            command = "sudo shutdown now"
        elif re.search(r"reboot", prompt, re.I):
            command = "sudo reboot"
        # Process Management
        elif re.search(r"list top processes", prompt, re.I):
            command = "top -b -n 1 | head -20"
        elif re.search(r"kill process ([0-9]+)", prompt, re.I):
            match = re.search(r"kill process ([0-9]+)", prompt, re.I)
            if match:
                pid = match.group(1)
                command = f"kill -9 {pid}"
        elif re.search(r"kill process named ([\w-]+)", prompt, re.I):
            match = re.search(r"kill process named ([\w-]+)", prompt, re.I)
            if match:
                pname = match.group(1)
                command = f"pkill -9 {pname}"
        # Service Management
        elif re.search(r"start service ([\w-]+)", prompt, re.I):
            match = re.search(r"start service ([\w-]+)", prompt, re.I)
            if match:
                svc = match.group(1)
                command = f"sudo systemctl start {svc}"
        elif re.search(r"stop service ([\w-]+)", prompt, re.I):
            match = re.search(r"stop service ([\w-]+)", prompt, re.I)
            if match:
                svc = match.group(1)
                command = f"sudo systemctl stop {svc}"
        elif re.search(r"restart service ([\w-]+)", prompt, re.I):
            match = re.search(r"restart service ([\w-]+)", prompt, re.I)
            if match:
                svc = match.group(1)
                command = f"sudo systemctl restart {svc}"
        elif re.search(r"enable service ([\w-]+)", prompt, re.I):
            match = re.search(r"enable service ([\w-]+)", prompt, re.I)
            if match:
                svc = match.group(1)
                command = f"sudo systemctl enable {svc}"
        elif re.search(r"disable service ([\w-]+)", prompt, re.I):
            match = re.search(r"disable service ([\w-]+)", prompt, re.I)
            if match:
                svc = match.group(1)
                command = f"sudo systemctl disable {svc}"
        elif re.search(r"service status ([\w-]+)", prompt, re.I):
            match = re.search(r"service status ([\w-]+)", prompt, re.I)
            if match:
                svc = match.group(1)
                command = f"systemctl status {svc}"
        # Crontab
        elif re.search(r"view crontab", prompt, re.I):
            command = "crontab -l"
        elif re.search(r"add cron job (.+)", prompt, re.I):
            match = re.search(r"add cron job (.+)", prompt, re.I)
            if match:
                cron = match.group(1)
                command = f'(crontab -l; echo "{cron}") | crontab -'
        elif re.search(r"remove cron job (.+)", prompt, re.I):
            match = re.search(r"remove cron job (.+)", prompt, re.I)
            if match:
                cron = match.group(1)
                command = f'crontab -l | grep -v "{cron}" | crontab -'
        # Log Management
        elif re.search(r"view log ([\w./-]+)", prompt, re.I):
            match = re.search(r"view log ([\w./-]+)", prompt, re.I)
            if match:
                logf = match.group(1)
                command = f"tail -n 50 {logf}"
        elif re.search(r"search logs for ([\w-]+) in ([\w./-]+)", prompt, re.I):
            match = re.search(r"search logs for ([\w-]+) in ([\w./-]+)", prompt, re.I)
            if match:
                keyword, logf = match.group(1), match.group(2)
                command = f"grep '{keyword}' {logf}"
        # Hardware Info
        elif re.search(r"block devices", prompt, re.I):
            command = "lsblk"
        elif re.search(r"usb devices", prompt, re.I):
            command = "lsusb"
        elif re.search(r"pci devices", prompt, re.I):
            command = "lspci"
        # Firewall
        elif re.search(r"firewall status", prompt, re.I):
            command = "sudo ufw status"
        elif re.search(r"enable firewall", prompt, re.I):
            command = "sudo ufw enable"
        elif re.search(r"disable firewall", prompt, re.I):
            command = "sudo ufw disable"
        elif re.search(r"allow port ([0-9]+)", prompt, re.I):
            match = re.search(r"allow port ([0-9]+)", prompt, re.I)
            if match:
                port = match.group(1)
                command = f"sudo ufw allow {port}"
        elif re.search(r"deny port ([0-9]+)", prompt, re.I):
            match = re.search(r"deny port ([0-9]+)", prompt, re.I)
            if match:
                port = match.group(1)
                command = f"sudo ufw deny {port}"
        # Mount/Unmount
        elif re.search(r"list mounted drives", prompt, re.I):
            command = "mount"
        elif re.search(r"mount ([\w./-]+) to ([\w./-]+)", prompt, re.I):
            match = re.search(r"mount ([\w./-]+) to ([\w./-]+)", prompt, re.I)
            if match:
                dev, mnt = match.group(1), match.group(2)
                command = f"sudo mount {dev} {mnt}"
        elif re.search(r"unmount ([\w./-]+)", prompt, re.I):
            match = re.search(r"unmount ([\w./-]+)", prompt, re.I)
            if match:
                dev = match.group(1)
                command = f"sudo umount {dev}"
        # Env Vars
        elif re.search(r"list env vars", prompt, re.I):
            command = "printenv"
        elif re.search(r"set env var ([\w_]+)=(.+)", prompt, re.I):
            match = re.search(r"set env var ([\w_]+)=(.+)", prompt, re.I)
            if match:
                var, val = match.group(1), match.group(2)
                command = f"export {var}={val}"
        elif re.search(r"unset env var ([\w_]+)", prompt, re.I):
            match = re.search(r"unset env var ([\w_]+)", prompt, re.I)
            if match:
                var = match.group(1)
                command = f"unset {var}"
        # Scripting
        elif re.search(r"run script ([\w./-]+)", prompt, re.I):
            match = re.search(r"run script ([\w./-]+)", prompt, re.I)
            if match:
                script = match.group(1)
                command = f"bash {script}"
        # Fallback: treat as raw command
        else:
            command = prompt
        if command:
            output, error = run_ssh_command(command, client)
            if error:
                st.error(error)
            else:
                st.code(output, language="bash")
        else:
            st.warning("Could not interpret the prompt. Please try a different description.")
    if st.button("❌ Disconnect (Linux SSH)"):
        st.session_state.linux_ssh_client.close()
        st.session_state.linux_ssh_connected = False
        st.success("🔌 Disconnected Successfully!")
