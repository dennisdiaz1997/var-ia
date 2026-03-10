# VAR-IA Data Engineering

Preparación de datos históricos de la UEFA Champions League para el sistema VAR-IA.

## Estructura

data/
raw/ -> dataset original
processed/ -> dataset limpio para modelos

scripts/
build_dataset.py -> construye dataset unificado
clean_data.py -> limpieza de datos
feature_engineering.py -> generación de features

## Instalación

pip install -r requirements.txt

## Ejecución

python scripts/build_dataset.py
python scripts/clean_data.py
python scripts/feature_engineering.py