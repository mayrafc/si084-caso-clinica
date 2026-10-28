#!/bin/bash
set -u
mkdir -p evidencias
for p in $(seq 8080 8090); do curl -s -o /dev/null --max-time 1 -w "127.0.0.1:$p  HTTP %{http_code}\n" http://127.0.0.1:$p/; done | grep -v 'HTTP 000' | tee evidencias/E1_aplicaciones.txt
curl -s http://127.0.0.1:8081/ | grep -i -E 'pruebas|<!--' | tee -a evidencias/E1_aplicaciones.txt
curl -s http://127.0.0.1:8088/ | tee -a evidencias/E1_aplicaciones.txt
curl -sI http://127.0.0.1:8080/ | tee evidencias/E2_servidor.txt
curl -s http://127.0.0.1:8080/robots.txt | tee evidencias/E3_metarchivos.txt
curl -s -o /dev/null -w 'security.txt  HTTP %{http_code}\n' http://127.0.0.1:8080/.well-known/security.txt | tee -a evidencias/E3_metarchivos.txt
curl -s http://127.0.0.1:8080/ | grep -n -E '<!--|generator' | tee evidencias/E4_contenido.txt
curl -s http://127.0.0.1:8080/resultados/ | grep -n -i -E '<!--|contraseña' | tee -a evidencias/E4_contenido.txt
curl -s http://127.0.0.1:8080/ | grep -o -E "/wp-[a-z]+/[^\"']*\?ver=[0-9.]+" | tee evidencias/E5_componentes.txt
for r in citas resultados postula admin; do echo "== /$r/"; curl -s http://127.0.0.1:8080/$r/ | grep -o -E '<form[^>]*>|<input[^>]*>|<select[^>]*>|<option>[^<]*|<textarea[^>]*>'; done | tee evidencias/E6_entradas.txt
curl -s http://127.0.0.1:8080/respaldos/ | tee evidencias/E7_expuestos.txt
curl -s -o /dev/null -w '/admin/  HTTP %{http_code}\n' http://127.0.0.1:8080/admin/ | tee -a evidencias/E7_expuestos.txt
for h in Strict-Transport-Security Content-Security-Policy X-Frame-Options X-Content-Type-Options Set-Cookie; do v=$(curl -sI http://127.0.0.1:8080/ | grep -i "^$h:" | cut -d' ' -f2- | tr -d '\r'); echo "$h: ${v:-AUSENTE}"; done | tee evidencias/E8_cabeceras.txt
echo 'HTTPS 127.0.0.1:443 NO EJECUTADO: fuera de los puertos 8080-8090 del alcance autorizado y ocupado por un servicio Greenbone ajeno. No se atribuye su estado al caso.' | tee -a evidencias/E8_cabeceras.txt
