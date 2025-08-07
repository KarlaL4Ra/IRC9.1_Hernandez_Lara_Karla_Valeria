# 🚀 Playbook AROM - Generador de Proyectos Ansible

Una aplicación web que replica la funcionalidad del script bash multiplataforma para crear estructuras de proyectos Ansible orientados a la configuración de switches Cisco Catalyst.

## 🌟 Características

- **Interfaz Web Intuitiva**: Genera proyectos Ansible desde el navegador
- **Estructura Completa**: Crea toda la estructura de directorios y archivos necesarios
- **Basado en Best Practices**: Implementa las mejores prácticas de Ansible
- **Descarga Directa**: Descarga el proyecto completo en formato ZIP
- **Multiplataforma**: Compatible con Rocky/Kali/Ubuntu/CentOS (como el script original)

## 📁 Estructura Generada

```
ansible-catalyst-config/
├── README.md
├── ansible.cfg
├── playbooks/
│   └── site.yml
├── inventory/
│   ├── hosts.yml
│   ├── group_vars/
│   └── host_vars/
├── group_vars/
│   ├── all/
│   │   └── main.yml
│   └── catalyst_switches/
│       └── main.yml
├── roles/
│   ├── common/
│   │   ├── tasks/main.yml
│   │   ├── handlers/
│   │   ├── templates/
│   │   ├── files/
│   │   ├── vars/
│   │   └── defaults/
│   └── catalyst_config/
│       ├── tasks/main.yml
│       ├── handlers/
│       ├── templates/
│       ├── files/
│       ├── vars/
│       └── defaults/
├── scripts/
│   ├── setup.sh
│   ├── run.sh
│   └── verify.sh
├── docs/
│   └── GETTING_STARTED.md
├── logs/
└── vault/
```

## 🚀 Inicio Rápido

### Usando Docker (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd playbook-AROM

# Ejecutar con Docker Compose
docker-compose up -d

# Acceder a la aplicación
open http://localhost:5000
```

### Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py

# Acceder a la aplicación
open http://localhost:5000
```

## 🎯 Uso

1. **Accede a la aplicación** en tu navegador
2. **Configura el nombre del proyecto** (opcional)
3. **Haz clic en "Generar Proyecto"**
4. **Descarga el archivo ZIP** con la estructura completa
5. **Extrae y usa** tu proyecto Ansible

## 🔧 Funcionalidades Incluidas

### Configuraciones Automáticas
- ✅ Configuración de hostname
- ✅ Servidores NTP
- ✅ Configuración de logging
- ✅ Banners de seguridad
- ✅ Configuración SSH
- ✅ VLANs automáticas
- ✅ Spanning Tree Protocol
- ✅ Variables organizadas por grupos

### Scripts Auxiliares
- ✅ `setup.sh` - Preparación del entorno
- ✅ `run.sh` - Ejecución de playbooks
- ✅ `verify.sh` - Verificación post-configuración

### Documentación
- ✅ README completo
- ✅ Guía de inicio rápido
- ✅ Ejemplos de uso
- ✅ Configuración de ansible-vault

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Containerización**: Docker & Docker Compose
- **Generación**: Estructura de archivos automática
- **Compresión**: ZIP para descarga

## 📋 Prerrequisitos del Proyecto Generado

- Python 3.6+
- Ansible 2.9+
- Colección cisco.ios
- Acceso SSH a los switches

## 🔐 Seguridad

El proyecto generado incluye:
- Configuración para ansible-vault
- Plantillas para cifrado de credenciales
- Configuración SSH segura
- Banners de seguridad

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está basado en el script original de "Zhapy el Imparable" y mantiene el mismo espíritu de automatización y facilidad de uso.

## 🙏 Créditos

- **Script Original**: Zhapy el Imparable v2.1
- **Adaptación Web**: Playbook AROM
- **Compatibilidad**: Rocky/Kali/Ubuntu/CentOS

---

**¡Automatiza tu infraestructura de red con facilidad! 🚀**