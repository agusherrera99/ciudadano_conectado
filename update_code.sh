REPO_PATH="/home/usuario/apps/ciudadano_conectado"
LOG_FILE="/home/usuario/apps/ciudadano_update.log"
EMAIL="modernizacion@lasflores.gob.ar"

ERROR_LOG=$(mktemp)
HAS_ERROR=false

log_error() {
    local message="$1"
    echo "ERROR: $message" | tee -a "$LOG_FILE" "$ERROR_LOG"
    HAS_ERROR=true
}

# enviar todos los errores acumulados por email
send_error_report() {
    if [ "$HAS_ERROR" = true ]; then
        echo -e "Actualización de Ciudadano Conectado fallida en $(date)\n" > "$ERROR_LOG.email"
        cat "$ERROR_LOG" >> "$ERROR_LOG.email"
        cat "$ERROR_LOG.email" | mail -s "Errores en actualización de Ciudadano Conectado" "$EMAIL"
        rm "$ERROR_LOG.email"
    fi
    rm "$ERROR_LOG"
}

trap send_error_report EXIT

cd $REPO_PATH || {
    log_error "No se pudo acceder al directorio del repositorio"
    exit 1
}

if [ -f requirements.txt ]; then
    cp requirements.txt requirements.txt.old
fi

git fetch origin main || {
    log_error "Fallo al obtener cambios del repositorio remoto"
    exit 1
}

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main) || {
    log_error "Error al obtener el hash del commit remoto"
    exit 1
}

if [ $LOCAL != $REMOTE ]; then
    echo "$(date): Hay cambios disponibles, actualizando..." | tee -a "$LOG_FILE"

    git pull origin main || {
        log_error "Fallo al realizar git pull"
        exit 1
    }

    if [ -f requirements.txt.old ] && ! cmp -s requirements.txt requirements.txt.old; then
        echo "Cambios detectados en requirements.txt, reconstruyendo contenedor..." | tee -a "$LOG_FILE"
        docker-compose build ciudadano-web || {
            log_error "Fallo al reconstruir el contenedor"
            exit 1
        }
        docker-compose up -d || {
            log_error "Fallo al levantar los contenedores"
            exit 1
        }
    fi

    echo "Ejecutando migraciones y collectstatic en el contenedor..." | tee -a "$LOG_FILE"
    
    docker exec ciudadano-web python3 manage.py makemigrations || {
        log_error "Fallo al ejecutar makemigrations"
    }
    
    docker exec ciudadano-web python3 manage.py migrate || {
        log_error "Fallo al ejecutar migrate"
    }
    
    docker exec ciudadano-web python3 manage.py collectstatic --no-input --clear || {
        log_error "Fallo al ejecutar collectstatic"
    }

    # Solo reinicia si no hubo errores en los pasos anteriores
    if [ "$HAS_ERROR" = false ]; then
        echo "Reiniciando contenedor..." | tee -a "$LOG_FILE"
        docker-compose restart ciudadano-web || {
            log_error "Fallo al reiniciar el contenedor"
        }
    fi

    if [ "$HAS_ERROR" = false ]; then
        echo "Actualización completada con éxito." | tee -a "$LOG_FILE"
    else
        echo "Actualización completada con errores. Revisa el log para más detalles." | tee -a "$LOG_FILE"
    fi
else
    echo "$(date): El repositorio está actualizado, no es necesario actualizar." | tee -a "$LOG_FILE"
fi

# Limpieza del archivo temporal de requirements
if [ -f requirements.txt.old ]; then
    rm requirements.txt.old
fi