from pathlib import Path
import hashlib

root=Path('/caso')
e=root/'evidencias'
required=['E1_aplicaciones.txt','E2_servidor.txt','E3_metarchivos.txt','E4_contenido.txt','E5_componentes.txt','E6_entradas.txt','E7_expuestos.txt','E8_cabeceras.txt']
for name in required:
    if not (e/name).is_file() or not (e/name).stat().st_size:
        raise ValueError('Evidencia ausente/vacía: '+name)
records=[]
for p in sorted(e.glob('*.txt')):
    if p.name=='SHA256SUMS.txt':continue
    records.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix())
(e/'SHA256SUMS.txt').write_text('\n'.join(records)+'\n',encoding='utf-8')
print('Selladas',len(records),'evidencias TXT; ocho pruebas presentes.')
