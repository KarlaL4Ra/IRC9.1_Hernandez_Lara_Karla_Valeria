#!/bin/bash

# Declaración de URLs
declare -a urls=("https://uvm.mx/" "https://upotosina.edu.mx/" "https://moodle.plataforma-utslp.net/")

# Archivo de registro
file=urls2.log

# Tiempo de espera entre iteraciones (en segundos)
sleep_time=10  # Puedes modificar esta variable para cambiar el intervalo

# Número máximo de iteraciones (opcional, establece en 0 para ejecutar infinitamente)
max_iterations=0

# Contador de iteraciones
iteration=0

# Bucle principal
while true; do
    # Incrementa el contador de iteraciones
    iteration=$((iteration + 1))
    
    # Imprime la fecha actual en el archivo de registro
    printf "$(date)\n" > "$file"

    # Itera sobre cada URL y registra el estado
    for url in "${urls[@]}"; do
        status=$(curl -m 10 -s -I "$url" | head -n 1 | awk '{print $2}')
        printf "$url,$status\n" >> "$file"
    done

    # Muestra el contenido del archivo de registro con formato
    column -s, -t "$file"

    # Verifica si se alcanzó el número máximo de iteraciones
    if ((max_iterations > 0 && iteration >= max_iterations)); then
        echo "Número máximo de iteraciones alcanzado ($max_iterations). Saliendo del script."
        break
    fi

    # Espera antes de la próxima iteración
    sleep "$sleep_time"
done
