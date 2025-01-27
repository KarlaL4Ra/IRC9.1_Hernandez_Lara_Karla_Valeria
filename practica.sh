#!/bin/bash

# Variables
DIR="/home/karla/IRC9.1_Hernandez_Lara_Karla_Valeria"
FILE="$DIR/archivo.txt"
BACKUP_PREFIX="archivo_backup_"

# Función para crear la carpeta si no existe
create_directory() {
    if [ ! -d "$DIR" ]; then
        echo "La carpeta no existe. Creándola..."
        mkdir -p "$DIR"
    else
        echo "La carpeta ya existe."
    fi
}

# Función para manejar el archivo principal
handle_file() {
    if [ ! -f "$FILE" ]; then
        echo "El archivo principal no existe. Creándolo..."
        echo "Este es el contenido inicial del archivo." > "$FILE"
    else
        echo "El archivo ya existe. Creando un respaldo..."
        create_backup
    fi
}

# Función para crear un respaldo del archivo
create_backup() {
    TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
    BACKUP_FILE="${DIR}/${BACKUP_PREFIX}${TIMESTAMP}.txt"
    cp "$FILE" "$BACKUP_FILE"
    echo "Respaldo creado: $BACKUP_FILE"
}

# Lógica principal del script
create_directory
handle_file
