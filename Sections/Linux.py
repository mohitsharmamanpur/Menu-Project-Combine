import streamlit as st
import subprocess
import paramiko

def linux_section():
    st.header("🐧 Linux Command Executor (Local)")
    user_input = st.text_input("Enter Linux command (e.g. ls, pwd, whoami, mkdir testdir, cat file.txt)")
    if st.button("Run Linux Command"):
        if user_input.strip() == "":
            st.warning("Please enter a command.")
        else:
            try:
                result = subprocess.getoutput(user_input)
                st.code(result, language="bash")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("🔐 SSH Remote Command Executor")

    with st.sidebar.expander("🔧 SSH Connection Setup", expanded=True):
        host = st.text_input("Hostname / IP", placeholder="e.g. 192.168.1.10", key="ssh_host")
        port = st.number_input("Port", min_value=1, max_value=65535, value=22, key="ssh_port")
        username = st.text_input("Username", placeholder="e.g. root or ubuntu", key="ssh_user")
        password = st.text_input("Password", type="password", key="ssh_pass")

        if "ssh_client" not in st.session_state:
            st.session_state.ssh_client = None
        if "connected" not in st.session_state:
            st.session_state.connected = False

        if st.button("🔌 Connect via SSH"):
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=host, port=port, username=username, password=password, timeout=10)
                st.session_state.ssh_client = client
                st.session_state.connected = True
                st.success("✅ SSH Connection Established Successfully!")
            except Exception as e:
                st.session_state.connected = False
                st.session_state.ssh_client = None
                st.error(f"❌ Connection Failed: {e}")

    if st.session_state.connected:
        st.subheader("🖥️ Execute Linux Commands Remotely (SSH)")
        command = st.text_input("Enter Linux Command (Remote)", key="ssh_cmd")
        if st.button("▶️ Run Command (SSH)"):
            if command.strip() == "":
                st.warning("⚠️ Please enter a command.")
            else:
                try:
                    stdin, stdout, stderr = st.session_state.ssh_client.exec_command(command)
                    output = stdout.read().decode()
                    error = stderr.read().decode()
                    if output:
                        st.code(output, language="bash")
                    if error:
                        st.error(error)
                except Exception as e:
                    st.error(f"⚠️ Error running command: {e}")
        if st.button("❌ Disconnect"):
            st.session_state.ssh_client.close()
            st.session_state.connected = False
            st.success("🔌 Disconnected Successfully!")
    else:
        st.info("📝 Please enter SSH credentials and click 'Connect via SSH' to begin.")
