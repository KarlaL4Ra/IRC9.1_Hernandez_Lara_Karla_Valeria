import subprocess

def run_playbook(playbook_name):
    playbook_path = f"playbooks/{playbook_name}"
    try:
        result = subprocess.check_output(
            ['ansible-playbook', playbook_path, '-i', 'localhost,'],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return f"Error ejecutando playbook:\n{e.output}"
