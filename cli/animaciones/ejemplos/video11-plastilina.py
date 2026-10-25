"""Video 11 · cuántos tokens le ahorra a Claude su equipo de procesos (devlog) · edición «Plastilina» (claymation).
Los clips enseñan su panel de Procesos en la laptop (centro del cuadro): las tarjetas van ARRIBA, sobre el monitor grande,
para no tapar la demo. Él pidió varias escenas a pantalla completa: números de la semana, video→texto, huellas de significado (único tramo sin clip),
consulta en copia de solo lectura y «Claude sigue pensando»; donde enseña el panel queda el clip o una tarjeta arriba.
Reutiliza CSS, figuras 3D y ayudantes de video10-plastilina.py.
Tiempos = timeline final de videos/11 (151.62 s; ver CORRE abajo).
Uso: SALIDA=~/Documents/Videos/videos/11/animaciones REL=videos/11/animaciones python3 ejemplos/video11-plastilina.py [ids…]   (SOLO_HTML=1 para revisar)
Los archivos salen con prefijo «gpl11-».
"""
import importlib.util, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import plastilina as P
from plastilina import letras, bloque, chip, N

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('v10pl', os.path.join(HERE, 'video10-plastilina.py'))
V10 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V10)
CSS, LIB3D, bt, sb, rw, onoff = V10.CSS, V10.LIB3D, V10.bt, V10.sb, V10.rw, V10.onoff

CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/videos/11/animaciones')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PRE = 'gpl11-'
FIN = 158.67
PIEZAS = []

LIB = LIB3D + r"""
const moneda=(r)=>{const G=C.grupo();G.add(C.cil(r,r*.32,'#ffd36b'));const c=C.cil(r*.62,r*.36,'#ffc23d');G.add(c);return C.sombra(G)};
const engrane=(r,c)=>{const G=C.grupo();G.add(C.dona(r*.72,r*.28,c));for(let i=0;i<8;i++){const d=C.caja(r*.36,r*.36,r*.4,c,r*.1);const a=i*Math.PI/4;
 d.position.set(Math.cos(a)*C.u(r),Math.sin(a)*C.u(r),0);d.rotation.z=a;G.add(d)}return C.sombra(G)};
const camara=(w)=>{const G=C.grupo();G.add(C.caja(w,w*.66,w*.42,'#3b3340'));const l=C.cil(w*.26,w*.3,'#9fd3ff');l.rotation.x=Math.PI/2;l.position.z=C.u(w*.3);G.add(l);
 const f=C.caja(w*.24,w*.14,w*.2,'#ff6b6b');f.position.set(C.u(w*.3),C.u(w*.38),0);G.add(f);return C.sombra(G)};
const candado=(w)=>{const G=C.grupo();G.add(C.caja(w,w*.8,w*.4,'#ffd36b'));const a=C.dona(w*.3,w*.08,'#c9b6ff');a.position.y=C.u(w*.42);G.add(a);
 const o=C.bola(w*.1,'#3b3340');o.position.z=C.u(w*.21);G.add(o);return C.sombra(G)};
"""


def tarjeta(pid, start, dur, body, js3d, sale=True):
    """Tarjeta transparente sobre la cámara; al final todo se aplasta contra la mesa (sin desvanecido)."""
    A = P.at(start)
    if sale:
        body = f'<div class="fz x" style="--x:{A(round(start + dur - .55, 2))}">{body}</div>'
    PIEZAS.append((pid, start, round(start + dur, 2), P.page(CSS, body, dur, S0=start, transparente=True, js3d=LIB + js3d)))


def escena(pid, S, E, body, js3d, fondo, ac):
    """Escena a pantalla completa: entra con mancha de plastilina y al salir la mancha se recoge hacia el centro (sin desvanecido).
    La salida va suave a 30 cps (no a los 12 cps del stop-motion): aplastada en 5 pasos se veía trabada y rebotando."""
    DS = round(E - S + .12, 2)
    css = (CSS + f'body .mesa{{animation:mancha .65s steps(8) both,recoge .45s cubic-bezier(.45,0,.75,1) {DS - .6:.2f}s forwards}}'
           '@keyframes recoge{from{clip-path:circle(1110px at 540px 960px)}to{clip-path:circle(0px at 540px 960px)}}')
    html = P.page(css, body, DS, S0=S, fondo=fondo, entra=(540, 1300), ac=ac, js3d=LIB + js3d)
    html = html.replace('</body>', "<script>{const _s=window.__seek;window.__seek=s=>{_s(s);for(const a of document.getAnimations())"
                        "if(a.animationName==='recoge'){a.pause();a.currentTime=s*1000}};"
                        f"window.__liso=[[{DS - .62:.2f},{DS:.2f}]];window.__seek(0)}}</script></body>")
    PIEZAS.append((pid, S, round(S + DS, 2), html))


def aplasta_y(objs, X):
    return ''.join(f'C.aplasta({o},t,{X});' for o in objs)


# ───────── 0:06 · «si la pones a navegar por su cuenta, cada paso te va a costar ~1500 tokens»
S = 6.2; A = P.at(S); X = S + 6.6 - .55
tarjeta('c01-paso', S, 6.6,
        bloque(60, 190, 660, sb('si la pones a navegar sola', 34) + bt('🧭 cada paso', 60)
               + bt(f'≈ {N([(0, 0), (8.7, 1500, 2.2)], f="c")} <span style="font-size:46px">tokens</span>', 104, 'white-space:nowrap;color:#ff6b6b;margin-top:6px'),
               A, 6.5, color='#fff8ef'),
        r"""const M=[];for(let i=0;i<4;i++){const m=moneda(70);scene.add(m);M.push(m)}
return t=>{M.forEach((m,i)=>{C.cae(m,t,8.7+i*.55,500);""" + aplasta_y(['m'], X) + r"""P3(m,870,560-i*30,2+i*.2,t,i,1.15,0,.1*(i%2?1:-1))})}""")

# ───────── 0:20 · ESCENA · «esta última semana ~503 ejecuciones y ~10 millones de tokens que Claude no tuvo que gastar»
S = 19.6; A = P.at(S)
escena('e1-semana', S, 30.59,
       letras(['Esta última', '*semana*'], A, S + .2, top=230, size=130)
       + bloque(70, 660, 940, bt(f'⚙️ {N([(0, 0), (22.4, 503, 1.3)])}', 150, 'white-space:nowrap') + sb('ejecuciones', 40), A, 21.6, color='#fff8ef')
       + bloque(70, 1060, 940, bt(f'≈ {N([(0, 0), (25.6, 10000000, 2.0)], f="c")}', 120, 'white-space:nowrap;color:#2f9e6a')
                + rw(sb('tokens que Claude no tuvo que gastar 💸', 40), A, 27.6), A, 25.3, color='#fff8ef'),
       r"""const g=engrane(110,'#9b6bff');scene.add(g);const M=[];for(let i=0;i<6;i++){const m=moneda(80);scene.add(m);M.push(m)}
return t=>{C.brota(g,t,21.7);P3(g,300,1500,3,t,1,.2,-.3,-t*1.6);
 M.forEach((m,i)=>{C.cae(m,t,25.8+i*.3,600);P3(m,800,1520-i*32,2+i*.15,t,i+2,1.2,0,0)})}""", 'menta', '#2f9e6a')

# ───────── 0:30 · «cada hora abre mi Chrome: capturas de mis redes y precios de Mercado Libre y Amazon; Claude solo recibe las capturas recortadas»
S = 30.75; A = P.at(S); X = S + 10.55 - .55
tarjeta('c03-capturas', S, 10.55,
        bloque(60, 180, 700, bt('⏰ cada hora', 64) + sb('abre mi Chrome y toma capturas', 32, 'margin-bottom:8px')
               + chip('📸 mis redes', A, 33.0, '#ffb3c7') + chip('🏷️ Mercado Libre', A, 36.5, '#ffe600') + chip('Amazon', A, 37.4, '#ffc79a')
               + rw(bt('✂️ a Claude le llegan recortadas', 44, 'white-space:nowrap'), A, 38.6, 'margin-top:16px'), A, 30.85, color='#fff8ef'),
        r"""const cm=camara(150);scene.add(cm);
return t=>{C.cae(cm,t,32.6,520);C.aplasta(cm,t,""" + f'{X}' + r""");const fl=t>33&&((t*12|0)%9==0);cm.children[2].material.emissive.set(fl?'#ffffff':'#000000');P3(cm,890,400,2.5,t,1,.3,-.5,.05)}""")

# ───────── 0:46 · «aquí se va la mayoría de mi consumo: casi más de 6 millones de tokens solo de navegación»
S = 45.6; A = P.at(S); X = S + 7.2 - .55
tarjeta('c04-navegacion', S, 7.2,
        bloque(60, 190, 660, sb('aquí se va la mayoría', 34) + bt(f'🔥 +{N([(0, 0), (46.9, 6, 1.2)])} millones', 90, 'white-space:nowrap;color:#ff6b6b')
               + rw(sb('de tokens · solo navegando', 34), A, 48.1), A, 45.8, color='#fff09a'),
        r"""const M=[];for(let i=0;i<7;i++){const m=moneda(60);scene.add(m);M.push(m)}
return t=>{M.forEach((m,i)=>{C.cae(m,t,46.9+i*.18,560);C.aplasta(m,t,""" + f'{X}' + r""");P3(m,870+(i%2)*14,620-i*24,2+i*.15,t,i,1.2,0,0)})}""")

# ───────── 0:53 · ESCENA · «Claude no puede escuchar mis videos → audios a texto con el segundo exacto; 1 min de video ≈ 36 mil tokens, así nada más lee mi texto»
S = 53.0; A = P.at(S)
LINEAS = [('[00:00.1] Mira, cada punto que ves aquí…', 59.2, 1.0), ('[00:05.8] Así que si la pones a navegar…', 60.3, 1.0)]
TX = ''.join(f'<div style="margin-top:8px"><span class="ty mono2" style="--d:{A(t)};--td:{d}s;--n:{len(s_)};font-size:34px">{s_}</span></div>' for s_, t, d in LINEAS)
escena('e2-texto', S, 69.65,
       letras(['Claude no', 'puede *escuchar*'], A, S + .9, top=230, size=120, sale=61.6)
       + letras(['1 minuto', 'de *video*…'], A, 62.1, top=230, size=130)
       + bloque(70, 700, 940, bt('🎙️ → 📝 audios a texto', 62, 'white-space:nowrap') + rw(sb('con el segundo exacto de cada frase', 36), A, 59.6) + TX,
                A, 56.6, sale=61.6, color='#fff8ef')
       + bloque(70, 700, 940, bt(f'🎞️ ≈ {N([(0, 0), (64.6, 36000, 1.4)], f="c")}', 120, 'white-space:nowrap;color:#ff6b6b') + sb('tokens por verlo', 40), A, 62.8, color='#fff8ef')
       + bloque(70, 1090, 940, bt('📝 así, solo lee mi texto ✓', 58, 'white-space:nowrap;color:#2f9e6a'), A, 66.6, color='#a8e6cf'),
       r"""const H=[];for(let i=0;i<3;i++){const h=hojita(130,['#fff8ef','#ffe3ea','#e1f1ff'][i]);scene.add(h);H.push(h)}
const v=C.caja(240,170,60,'#3b3340');scene.add(v);const pl=C.cono(46,70,'#ff6b6b');pl.rotation.z=-Math.PI/2;v.add(pl);pl.position.z=C.u(40);
return t=>{H.forEach((h,i)=>{C.cae(h,t,57.0+i*.25,600);C.aplasta(h,t,61.4);P3(h,300+i*240,1300,2+i*.3,t,i,.15,-.35+i*.35,(i-1)*.12)});
 C.cae(v,t,63.0,600);P3(v,330,1330,2,t,5,.3,.4,0)}""", 'cielo', '#3f6fe0')

# ───────── 1:10 · escena a pantalla completa (sin clip): «luego otro saca las huellas de significado de cada guion» (ya en el timeline nuevo)
S = 69.65; A = P.at(S)
HUE = (letras(['Huellas de', '*significado*'], A, S + .15, top=230, size=130)
       + bloque(70, 1430, 940, bt('📜 cada guion → 🧬 su huella', 54, 'white-space:nowrap') + '<div style="margin-top:10px">'
                + chip('= embeddings', A, S + 2.7, '#c9b6ff') + '</div>', A, S + 1.2, color='#fff8ef'))
JS1 = r"""const H=[],R=[];const COL=['#ff6b6b','#ff9f43','#ffd36b','#4cc38a','#5b8cff','#9b6bff'];
for(let i=0;i<3;i++){const h=hojita(120,['#fff8ef','#ffe3ea','#e1f1ff'][i]);scene.add(h);H.push(h);const r=[];
 for(let j=0;j<6;j++){const b=C.bola(26,COL[(j*(i+2))%6]);scene.add(b);r.push(b)}R.push(r)}
return t=>{const l=t-""" + f'{S}' + r""";
 H.forEach((h,i)=>{C.cae(h,t,""" + f'{S}' + r"""+.3+i*.2,500);P3(h,190,760+i*200,2,t,i,.12,.35,(i-1)*.1)});
 R.forEach((r,i)=>r.forEach((b,j)=>{C.brota(b,t,""" + f'{S}' + r"""+1.8+i*.2+j*.05);const p=C.eio(C.k(l,1.8+i*.2+j*.05,.45));P3(b,300+p*(110+j*105),760+i*200-Math.sin(Math.PI*p)*60,3,t,i*6+j)}))}"""
escena('e5-huellas', S, 73.47, HUE, JS1, 'lila', '#9b6bff')

# ───────── 1:28 · ESCENA · «cuando le pregunto algo de mis datos, Claude escribe la consulta, un proceso la corre en una copia de solo lectura y él solo lee las respuestas»
S = 87.96; A = P.at(S)
_q = 'SELECT … FROM mis_datos'
PASOS = [('🧠 Claude escribe la consulta', 90.3), ('⚙️ un proceso la corre', 91.6), ('🔒 en una copia de solo lectura', 93.2), ('📄 Claude solo lee la respuesta', 95.4)]
escena('e3-consulta', S, 98.75,
       letras(['Preguntas sobre', 'mis *datos*'], A, S + .2, top=230, size=120)
       + bloque(70, 660, 760, rw(bt(PASOS[0][0], 50, 'white-space:nowrap'), A, PASOS[0][1])
                + f'<div style="margin:8px 0 6px 70px"><span class="ty mono2" style="--d:{A(90.9)};--td:.8s;--n:{len(_q)};font-size:34px;color:#3f6fe0">{_q}</span></div>'
                + ''.join(rw(bt(n, 50, 'white-space:nowrap;margin-top:22px'), A, t) for n, t in PASOS[1:]), A, 90.1, color='#fff8ef'),
       r"""const p=pila(80,'#c9b6ff');scene.add(p);const k=candado(110);scene.add(k);
return t=>{C.brota(p,t,91.7);P3(p,880,1250,2,t,1,.35,0,0);C.cae(k,t,93.3,600);P3(k,880,1480,3,t,2,.2,-.3,0)}""", 'limon', '#e08a00')

# ───────── 2:10 · ESCENA · «Claude sigue haciendo la parte de pensar; le quité mirar, escuchar y buscar → un script en Python o Node»
S = 129.5; A = P.at(S)
QUITE = [('👀 mirar', 135.0), ('👂 escuchar', 135.8), ('🔎 buscar', 136.7)]
qt = ''.join(f'<span class="chip" style="--d:{A(t)};--b:#ffb3c7;font-size:44px;text-decoration:line-through;text-decoration-thickness:5px">{n}</span>' for n, t in QUITE)
escena('e4-pensar', S, 146.7,
       letras(['Claude sigue', '*pensando* 🧠'], A, S + .2, top=230, size=130)
       + bloque(70, 680, 940, sb('lo único que le quité:', 40) + f'<div style="margin-top:6px">{qt}</div>', A, 132.6, color='#fff8ef')
       + bloque(70, 1020, 940, bt('📜 eso lo hace un script', 62, 'white-space:nowrap') + '<div style="margin-top:10px">'
                + chip('🐍 Python', A, 144.6, '#fff09a') + chip('🟩 Node', A, 145.4, '#a8e6cf') + '</div>', A, 142.2, color='#fff8ef'),
       r"""const g=engrane(90,'#ff9f43');scene.add(g);
return t=>{C.brota(g,t,142.3);P3(g,860,1400,2,t,1,.2,-.3,-t*1.8)}""", 'rosa', '#e0457b')

# ───────── 2:32 · Sígueme + «¿tú qué le quitarías a tu IA para que gaste menos?»
S = 151.7; A = P.at(S)
BOTON = (f'<div style="position:relative;height:64px;margin-top:14px">'
         + onoff(f'<span class="chip" style="--b:#ff6b6b;color:#fff;animation:none">Seguir</span>', A, 152.0, 152.8, 'position:absolute;left:0;top:0')
         + onoff(f'<span class="chip" style="--b:#a8e6cf;animation:none">Siguiendo ✓</span>', A, 152.8, None, 'position:absolute;left:0;top:0') + '</div>')
SEG = (bloque(600, 190, 410, sb('Sígueme', 34) + bt('Armando', 80) + sb('homelab · IA · código', 30) + BOTON, A, 151.9, color='#ffb3c7')
       + bloque(60, 240, 500, bt('✂️ ¿Tú qué le quitarías a tu IA?', 46) + rw(sb('para que gaste menos 💬', 32, 'margin-top:8px'), A, 154.6), A, 152.6, color='#fff8ef'))
PIEZAS.append(('seguir', S, FIN, P.page(CSS, SEG, round(FIN - S, 2), S0=S, transparente=True,
                                       js3d=LIB + r"""const M=[];for(let i=0;i<3;i++){const m=moneda(54);scene.add(m);M.push(m)}
return t=>{M.forEach((m,i)=>{C.cae(m,t,155.0+i*.25,500);P3(m,330+i*120,700,3,t,i,1.2,0,0)})}""")))
# Las piezas desde 1:16 se escribieron con el timeline anterior; luego se cortaron dos arranques falsos («Luego, otro saca las huellas
# de…» y «…un proceso que se ejecuta para bajar de…») y todo lo de después se adelantó 7.05 s. El contenido de cada pieza es relativo a
# su inicio, así que solo se recorre.
CORRE, DT = 76.0, -7.05
PIEZAS = [(pid, round(a + DT, 2), round(b + DT, 2), h) if a > CORRE else (pid, a, b, h) for pid, a, b, h in PIEZAS]
FIN = round(FIN + DT, 2)
PIEZAS.sort(key=lambda p: p[1])

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    trabajos = []
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path, f'{b - a:.2f}'); continue
        trabajos.append((path, b - a, f'{OUT}/{PRE}{pid}.webm'))

    def uno(tr):
        h, d, o = tr
        for _ in range(2):
            r = subprocess.run(['node', CAP, h, f'{d:.2f}', o], capture_output=True, text=True)
            if r.returncode == 0:
                return f'ok {os.path.basename(o)}'
        return f'FALLO {os.path.basename(o)}: {r.stderr[-300:]}'
    with ThreadPoolExecutor(int(os.environ.get('P', 6))) as ex:
        for r in ex.map(uno, sorted(trabajos, key=lambda x: -x[1])):
            print(r, flush=True)
    if not solo:
        rel = os.environ.get('REL', 'videos/11/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
