from flask import Flask, render_template, request, jsonify, send_file
import os
import subprocess
import json
import shutil
from datetime import datetime
import tempfile
import zipfile
from io import BytesIO

app = Flask(__name__)

class PlaybookGenerator:
    def __init__(self):
        self.project_name = "ansible-catalyst-config"
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.date_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def create_project_structure(self, base_path):
        """Crear la estructura completa del proyecto"""
        project_path = os.path.join(base_path, self.project_name)
        
        # Crear estructura de directorios
        directories = [
            "playbooks",
            "inventory/group_vars",
            "inventory/host_vars", 
            "group_vars/all",
            "host_vars",
            "roles/common/tasks",
            "roles/common/handlers",
            "roles/common/templates",
            "roles/common/files",
            "roles/common/vars",
            "roles/common/defaults",
            "roles/catalyst_config/tasks",
            "roles/catalyst_config/handlers",
            "roles/catalyst_config/templates",
            "roles/catalyst_config/files",
            "roles/catalyst_config/vars",
            "roles/catalyst_config/defaults",
            "scripts",
            "docs",
            "logs",
            "vault"
        ]
        
        for directory in directories:
            dir_path = os.path.join(project_path, directory)
            os.makedirs(dir_path, exist_ok=True)
            
        return project_path
    
    def create_configuration_files(self, project_path):
        """Crear todos los archivos de configuración"""
        
        # README.md
        readme_content = '''# 🚀 Proyecto Ansible para Switch Catalyst

Este proyecto automatiza la configuración de switches Cisco Catalyst usando Ansible.

## 📁 Estructura del Proyecto

```
ansible-catalyst-config/
├── playbooks/          # Playbooks principales
├── inventory/          # Archivos de inventario
│   ├── group_vars/     # Variables por grupos
│   └── host_vars/      # Variables por host
├── roles/              # Roles de Ansible
│   ├── common/         # Rol común
│   └── catalyst_config/ # Configuración específica de Catalyst
├── scripts/            # Scripts auxiliares
├── docs/               # Documentación
├── logs/               # Logs de ejecución
└── vault/              # Archivos cifrados con ansible-vault
```

## 🚀 Inicio Rápido

1. **Configura el inventario**: Edita `inventory/hosts.yml`
2. **Configura las credenciales**: Usa `ansible-vault` para cifrar credenciales
3. **Ejecuta el setup**: `./scripts/setup.sh`
4. **Ejecuta el playbook**: `./scripts/run.sh`

## 📋 Prerrequisitos

- Python 3.6+
- Ansible 2.9+
- Colección cisco.ios

## 🔐 Seguridad

- Usa `ansible-vault` para cifrar credenciales
- No commites credenciales en texto plano
- Configura SSH keys cuando sea posible

## 📖 Documentación

Ver `docs/` para documentación detallada.
'''
        
        # inventory/hosts.yml
        inventory_content = '''---
all:
  children:
    catalyst_switches:
      hosts:
        switch1:
          ansible_host: 192.168.1.10
          ansible_user: admin
          ansible_connection: network_cli
          ansible_network_os: ios
          # Usar ansible-vault para cifrar la contraseña:
          # ansible_password: !vault |
          #   $ANSIBLE_VAULT;1.1;AES256
          #   ...
        # switch2:
        #   ansible_host: 192.168.1.11
        #   ansible_user: admin
        #   ansible_connection: network_cli
        #   ansible_network_os: ios
      vars:
        # Variables comunes para todos los switches Catalyst
        ansible_python_interpreter: "{{ ansible_playbook_python }}"
        ansible_command_timeout: 30
        ansible_connect_timeout: 30
'''

        # group_vars/all/main.yml
        global_vars_content = '''---
# Variables globales para el proyecto
ntp_servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org

dns_servers:
  - 8.8.8.8
  - 8.8.4.4

# Configuraciones de logging
logging_buffered_size: 51200
logging_level: informational

# Banner de login
login_banner: |
  ************************************************************
  * Acceso autorizado únicamente                            *
  * Todas las actividades son monitoreadas                  *
  ************************************************************
'''

        # group_vars/catalyst_switches/main.yml
        catalyst_vars_content = '''---
# Variables específicas para switches Catalyst
vlans:
  - id: 10
    name: "USERS"
    description: "VLAN para usuarios"
  - id: 20
    name: "SERVERS"
    description: "VLAN para servidores"
  - id: 99
    name: "MANAGEMENT"
    description: "VLAN de administración"

# Configuración de spanning tree
spanning_tree_mode: rapid-pvst
spanning_tree_portfast_default: true

# Configuración de SSH
ssh_version: 2
ssh_timeout: 60
'''

        # playbooks/site.yml
        site_playbook_content = '''---
- name: 🚀 Configuración completa de switches Cisco Catalyst
  hosts: catalyst_switches
  gather_facts: false
  strategy: free
  serial: "{{ batch_size | default(5) }}"
  
  pre_tasks:
    - name: 📊 Recopilar facts del dispositivo
      cisco.ios.ios_facts:
        gather_subset: all
      tags: always
    
    - name: 📋 Mostrar información del dispositivo
      debug:
        msg: |
          Dispositivo: {{ ansible_net_hostname | default('N/A') }}
          Versión IOS: {{ ansible_net_version | default('N/A') }}
          Modelo: {{ ansible_net_model | default('N/A') }}
          Memoria: {{ ansible_net_memtotal_mb | default('N/A') }} MB
      tags: always

  roles:
    - role: common
      tags: [common, base]
    - role: catalyst_config  
      tags: [catalyst, config]
  
  post_tasks:
    - name: 💾 Guardar configuración
      cisco.ios.ios_config:
        save_when: always
      tags: [save, always]
    
    - name: ✅ Configuración completada
      debug:
        msg: "✅ Switch {{ inventory_hostname }} configurado exitosamente"
      tags: always
'''

        # roles/common/tasks/main.yml
        common_tasks_content = '''---
- name: 🏷️ Configurar hostname
  cisco.ios.ios_config:
    lines:
      - "hostname {{ inventory_hostname }}"
  tags: hostname

- name: 🕐 Configurar NTP
  cisco.ios.ios_config:
    lines:
      - "ntp server {{ item }}"
  loop: "{{ ntp_servers }}"
  tags: ntp

- name: 🗃️ Configurar logging
  cisco.ios.ios_config:
    lines:
      - "logging buffered {{ logging_buffered_size }}"
      - "logging console {{ logging_level }}"
  tags: logging

- name: 📢 Configurar banner de login
  cisco.ios.ios_banner:
    banner: login
    text: "{{ login_banner }}"
    state: present
  tags: banner

- name: 🔐 Configurar SSH
  cisco.ios.ios_config:
    lines:
      - "ip ssh version {{ ssh_version }}"
      - "ip ssh time-out {{ ssh_timeout }}"
      - "line vty 0 4"
      - "transport input ssh"
  tags: ssh
'''

        # roles/catalyst_config/tasks/main.yml
        catalyst_tasks_content = '''---
- name: 🌐 Configurar VLANs
  cisco.ios.ios_vlans:
    config:
      - vlan_id: "{{ item.id }}"
        name: "{{ item.name }}"
    state: merged
  loop: "{{ vlans }}"
  tags: vlans

- name: 🌳 Configurar Spanning Tree
  cisco.ios.ios_config:
    lines:
      - "spanning-tree mode {{ spanning_tree_mode }}"
      - "spanning-tree portfast default"
    parents: "global"
  when: spanning_tree_portfast_default | default(false)
  tags: stp

- name: 🔧 Aplicar configuraciones específicas del switch
  cisco.ios.ios_config:
    lines: "{{ host_specific_config | default([]) }}"
  when: host_specific_config is defined
  tags: host_specific
'''

        # ansible.cfg
        ansible_cfg_content = '''[defaults]
inventory = inventory/hosts.yml
host_key_checking = False
timeout = 30
gathering = explicit
log_path = logs/ansible.log
stdout_callback = yaml
callback_whitelist = timer, profile_tasks

[inventory]
enable_plugins = yaml, ini

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o UserKnownHostsFile=/dev/null

[privilege_escalation]
become = False
'''

        # scripts/setup.sh
        setup_script_content = '''#!/bin/bash
# Script de configuración inicial

set -euo pipefail

GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

echo -e "${GREEN}🔧 Preparando entorno Ansible...${NC}"

# Verificar que estamos en el directorio correcto
if [[ ! -f "ansible.cfg" ]]; then
    echo "❌ Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Instalar/actualizar colecciones
echo -e "${YELLOW}📦 Instalando colecciones de Ansible...${NC}"
ansible-galaxy collection install cisco.ios --force

# Verificar conectividad
echo -e "${YELLOW}🔍 Verificando conectividad con los hosts...${NC}"
ansible all -m ping || echo -e "${YELLOW}⚠️  Algunos hosts no responden al ping${NC}"

echo -e "${GREEN}✅ Entorno preparado correctamente${NC}"
echo -e "${GREEN}👉 Ejecuta './scripts/run.sh' para aplicar la configuración${NC}"
'''

        # scripts/run.sh
        run_script_content = '''#!/bin/bash
# Script para ejecutar el playbook principal

set -euo pipefail

GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

echo -e "${GREEN}▶️  Ejecutando playbook principal...${NC}"

# Opciones por defecto
PLAYBOOK="playbooks/site.yml"
INVENTORY="inventory/hosts.yml"
EXTRA_ARGS=""

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --check)
            EXTRA_ARGS="$EXTRA_ARGS --check"
            shift
            ;;
        --diff)
            EXTRA_ARGS="$EXTRA_ARGS --diff"
            shift
            ;;
        --tags)
            EXTRA_ARGS="$EXTRA_ARGS --tags $2"
            shift 2
            ;;
        --limit)
            EXTRA_ARGS="$EXTRA_ARGS --limit $2"
            shift 2
            ;;
        -h|--help)
            echo "Uso: $0 [opciones]"
            echo "Opciones:"
            echo "  --check    Ejecutar en modo check (dry-run)"
            echo "  --diff     Mostrar diferencias"
            echo "  --tags     Ejecutar solo tags específicos"
            echo "  --limit    Limitar a hosts específicos"
            echo "  -h, --help Mostrar esta ayuda"
            exit 0
            ;;
        *)
            echo "Opción desconocida: $1"
            echo "Usa -h para ver la ayuda"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}📋 Configuración:${NC}"
echo -e "  Playbook: $PLAYBOOK"
echo -e "  Inventario: $INVENTORY"
echo -e "  Argumentos adicionales: $EXTRA_ARGS"
echo

# Ejecutar playbook
ansible-playbook -i "$INVENTORY" "$PLAYBOOK" $EXTRA_ARGS

echo -e "${GREEN}✅ Ejecución completada${NC}"
'''

        # scripts/verify.sh
        verify_script_content = '''#!/bin/bash
# Script de verificación post-configuración

set -euo pipefail

echo "🔍 Verificando configuración de los switches..."

ansible catalyst_switches -i inventory/hosts.yml -m cisco.ios.ios_command -a "commands='show version'"

echo "✅ Verificación completada"
'''

        # docs/GETTING_STARTED.md
        getting_started_content = '''# 🚀 Guía de Inicio

## Configuración Inicial

1. **Editar inventario**: Modifica `inventory/hosts.yml` con tus dispositivos
2. **Configurar credenciales**: Usa ansible-vault para cifrar contraseñas
3. **Personalizar variables**: Edita archivos en `group_vars/` y `host_vars/`

## Comandos Útiles

```bash
# Preparar entorno
./scripts/setup.sh

# Ejecutar configuración completa
./scripts/run.sh

# Ejecutar solo verificación (dry-run)
./scripts/run.sh --check

# Ejecutar tags específicos
./scripts/run.sh --tags vlans

# Limitar a hosts específicos  
./scripts/run.sh --limit switch1

# Verificar configuración
./scripts/verify.sh
```

## Cifrado de Credenciales

```bash
# Crear archivo de contraseñas cifrado
ansible-vault create vault/passwords.yml

# Editar archivo cifrado
ansible-vault edit vault/passwords.yml

# Usar en playbook
ansible-playbook playbooks/site.yml --ask-vault-pass
```
'''

        # Escribir todos los archivos
        files_to_create = {
            'README.md': readme_content,
            'inventory/hosts.yml': inventory_content,
            'group_vars/all/main.yml': global_vars_content,
            'group_vars/catalyst_switches/main.yml': catalyst_vars_content,
            'playbooks/site.yml': site_playbook_content,
            'roles/common/tasks/main.yml': common_tasks_content,
            'roles/catalyst_config/tasks/main.yml': catalyst_tasks_content,
            'ansible.cfg': ansible_cfg_content,
            'scripts/setup.sh': setup_script_content,
            'scripts/run.sh': run_script_content,
            'scripts/verify.sh': verify_script_content,
            'docs/GETTING_STARTED.md': getting_started_content
        }
        
        for file_path, content in files_to_create.items():
            full_path = os.path.join(project_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Hacer scripts ejecutables
        script_files = ['scripts/setup.sh', 'scripts/run.sh', 'scripts/verify.sh']
        for script in script_files:
            script_path = os.path.join(project_path, script)
            if os.path.exists(script_path):
                os.chmod(script_path, 0o755)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_project():
    try:
        data = request.get_json()
        project_name = data.get('project_name', 'ansible-catalyst-config')
        
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        
        # Generar proyecto
        generator = PlaybookGenerator()
        generator.project_name = project_name
        project_path = generator.create_project_structure(temp_dir)
        generator.create_configuration_files(project_path)
        
        # Crear ZIP
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, temp_dir)
                    zip_file.write(file_path, arc_name)
        
        zip_buffer.seek(0)
        
        # Limpiar directorio temporal
        shutil.rmtree(temp_dir)
        
        return {
            'success': True,
            'message': 'Proyecto generado exitosamente',
            'download_ready': True
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error al generar el proyecto: {str(e)}'
        }, 500

@app.route('/download')
def download_project():
    try:
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        
        # Generar proyecto
        generator = PlaybookGenerator()
        project_path = generator.create_project_structure(temp_dir)
        generator.create_configuration_files(project_path)
        
        # Crear ZIP
        zip_path = os.path.join(temp_dir, 'playbook-AROM.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, temp_dir)
                    zip_file.write(file_path, arc_name)
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name='playbook-AROM.zip',
            mimetype='application/zip'
        )
        
    except Exception as e:
        return f'Error al descargar: {str(e)}', 500

@app.route('/preview')
def preview_structure():
    """Mostrar la estructura del proyecto que se generará"""
    structure = {
        "ansible-catalyst-config/": {
            "README.md": "file",
            "ansible.cfg": "file",
            "playbooks/": {
                "site.yml": "file"
            },
            "inventory/": {
                "hosts.yml": "file",
                "group_vars/": "folder",
                "host_vars/": "folder"
            },
            "group_vars/": {
                "all/": {
                    "main.yml": "file"
                },
                "catalyst_switches/": {
                    "main.yml": "file"
                }
            },
            "host_vars/": "folder",
            "roles/": {
                "common/": {
                    "tasks/": {"main.yml": "file"},
                    "handlers/": "folder",
                    "templates/": "folder",
                    "files/": "folder",
                    "vars/": "folder",
                    "defaults/": "folder"
                },
                "catalyst_config/": {
                    "tasks/": {"main.yml": "file"},
                    "handlers/": "folder",
                    "templates/": "folder",
                    "files/": "folder",
                    "vars/": "folder",
                    "defaults/": "folder"
                }
            },
            "scripts/": {
                "setup.sh": "file",
                "run.sh": "file",
                "verify.sh": "file"
            },
            "docs/": {
                "GETTING_STARTED.md": "file"
            },
            "logs/": "folder",
            "vault/": "folder"
        }
    }
    
    return jsonify(structure)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)