# Caso Clínica Santa Lucía

Entrega SI-084 de Chire Ramos, Mayra Fernanda, código 2021072620. El plan está en [PLAN.md](PLAN.md) y el PDF en [output/pdf](output/pdf). Etiqueta de entrega: `examen-u2`.

La infraestructura original del paquete docente se conserva sin modificaciones. Son páginas estáticas que simulan señales de seguridad; no equivalen a un portal clínico real. Lea primero `documentos/ALCANCE-AUTORIZADO.md`.

## Ejecución con Docker

```powershell
docker compose up -d --wait
docker build -t si084-herramientas -f herramientas/Dockerfile .
docker run --rm --network host --mount "type=bind,source=$($PWD.Path),target=/caso" -w /caso si084-herramientas bash herramientas/reconocimiento.sh
docker run --rm --mount "type=bind,source=$($PWD.Path),target=/caso" si084-herramientas python herramientas/generar_pdf.py
docker run --rm --mount "type=bind,source=$($PWD.Path),target=/caso" si084-herramientas bash -c 'sha256sum -c evidencias/SHA256SUMS.txt'
docker compose down
```

El reconocimiento usa la red host de Docker Desktop habilitada en este equipo y solo HTTP GET/HEAD a 127.0.0.1:8080-8090. Libere previamente 8080, 8081 y 8088. No añada pruebas a endpoints ni envíos de formularios. E8 omite 443 por estar fuera del alcance firmado y ocupado por Greenbone. Esta limitación queda expresada en el plan.

El PDF es una exportación local reproducible de PLAN.md mediante Docker, con el mismo contenido y tipografía de informe. Si el docente exige la impresión exacta de GitHub, abra PLAN.md en la etiqueta y use Ctrl+P, Guardar como PDF. Revise personalmente el plan y entregue el PDF al aula virtual.

No regenere evidencias tras sellar la entrega sin crear una revisión nueva y recalcular el manifiesto. Los archivos de infraestructura, incluidos los respaldos ficticios, proceden del ZIP docente; no fueron descargados desde el servidor durante el reconocimiento.
