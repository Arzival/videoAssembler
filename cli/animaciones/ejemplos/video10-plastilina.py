"""Video 10 · la Legion 5 llega al homelab (devlog) · edición «Plastilina» (claymation).
Bloques de plastilina pegados sobre la cámara (mitad de arriba, sin tapar la demo) con una figura 3D de plastilina por tarjeta:
laptop Legion con su etiqueta de $9,000, chip/RAM/GPU que caen uno por uno, cajitas que brincan de ZenBook a Legion, hojitas de
transcripción, GPU con ventiladores, bases de datos que se pasan bolitas; una sola escena a pantalla completa (respaldo mutuo)
con dos laptops de plastilina que se desinflan al caer. Todo cae, brota y se aplasta a 12 cps (sin desvanecidos).
Tiempos = timeline final de videos/10 (115.62 s), los mismos de video10-recorte.py.
Uso: SALIDA=~/Documents/Videos/videos/10/plastilina REL=videos/10/plastilina python3 ejemplos/video10-plastilina.py [ids…]   (SOLO_HTML=1 para revisar)
Los archivos salen con prefijo «gpl10-».
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import plastilina as P
from plastilina import letras, bloque, chip, N

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/videos/10/plastilina')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
PRE = 'gpl10-'
FIN = 115.62
PIEZAS = []
C = P.PAS

CSS = """
.bt{font-weight:700;line-height:.95;letter-spacing:-.01em}
.rw{animation:pzin .5s steps(6) var(--d) both}
.on{opacity:0;animation:apo .01s steps(1) var(--d) forwards}
.onoff{opacity:0;animation:apo .01s steps(1) var(--d) forwards,apc .01s steps(1) var(--q) forwards}
.fz{position:absolute;inset:0}
.fz.x{transform-origin:50% 60%;animation:aplastaT .45s steps(5) var(--x) forwards}
@keyframes aplastaT{40%{transform:scale(1.08,.9)}100%{transform:scale(1.35,0)}}
.br{height:46px;border-radius:999px;transform-origin:left center;transform:scaleX(0);box-shadow:inset 0 -8px 0 rgba(0,0,0,.12),0 6px 0 rgba(0,0,0,.08);
  animation:barra .9s steps(9) var(--d) forwards}
@keyframes barra{60%{transform:scaleX(1.06,1)}100%{transform:scaleX(1)}}
.ty{display:inline-block;white-space:nowrap;clip-path:inset(0 100% 0 0);animation:tipo var(--td,1s) steps(var(--n,20)) var(--d) forwards}
@keyframes tipo{to{clip-path:inset(0 -4% 0 0)}}
.mono2{font-family:Nunito;font-weight:900}
.pz .chip{font-size:30px}
"""

# figuras de plastilina propias (componen C.caja/C.bola/C.dona/C.cil); P3 = rotación fija + C.pon (temblor de stop-motion)
LIB3D = r"""
const P3=(o,x,y,z,t,i,rx=0,ry=0,rz=0,base=1)=>{o.rotation.set(rx,ry,rz);C.pon(o,x,y,z,t,i,base)};
const laptop=(w,cuerpo,pant)=>{const G=C.grupo(),d=w*.66;G.add(C.caja(w,w*.09,d,cuerpo));
 const tapa=C.grupo();tapa.position.set(0,C.u(w*.045),C.u(-d/2));G.add(tapa);
 const lid=C.caja(w,d*.95,w*.07,cuerpo);lid.position.y=C.u(d*.47);tapa.add(lid);
 const sc=new THREE.Mesh(new THREE.PlaneGeometry(C.u(w*.8),C.u(d*.74)),C.barro(pant,{emissive:pant,emissiveIntensity:.35}));sc.position.set(0,C.u(d*.47),C.u(w*.037));tapa.add(sc);
 G.userData.tapa=tapa;G.userData.sc=sc;return C.sombra(G)};
const abre=(lp,p)=>{lp.userData.tapa.rotation.x=1.45*(1-p)-.28*p};
const chip=(w)=>{const G=C.grupo();G.add(C.caja(w,w,w*.22,'#4cc38a'));const top=C.caja(w*.62,w*.62,w*.14,'#3b3340');top.position.z=C.u(w*.14);G.add(top);
 for(let i=0;i<4;i++)for(const s of[-1,1]){const p=C.caja(w*.1,w*.14,w*.08,'#ffd36b');p.position.set(C.u((i-1.5)*w*.22),C.u(s*w*.56),0);G.add(p)}return C.sombra(G)};
const ram=(w)=>{const G=C.grupo();G.add(C.caja(w,w*.3,w*.09,'#4cc38a'));for(let i=0;i<5;i++){const c=C.caja(w*.13,w*.15,w*.07,'#3b3340');c.position.set(C.u((i-2)*w*.18),C.u(w*.02),C.u(w*.06));G.add(c)}
 const g=C.caja(w*.86,w*.05,w*.08,'#ffd36b');g.position.y=C.u(-w*.14);G.add(g);return C.sombra(G)};
const gpu=(w)=>{const G=C.grupo(),F=[];G.add(C.caja(w,w*.52,w*.2,'#3b3340'));
 for(const s of[-1,1]){const f=C.grupo();f.position.set(C.u(s*w*.24),0,C.u(w*.11));f.add(C.dona(w*.17,w*.035,'#9fd3ff'));f.add(C.bola(w*.05,'#9fd3ff'));
  for(let b=0;b<3;b++){const a=C.caja(w*.24,w*.06,w*.02,'#c9b6ff');a.rotation.z=b*2.094;a.position.set(Math.cos(b*2.094)*C.u(w*.09),Math.sin(b*2.094)*C.u(w*.09),0);f.add(a)}
  G.add(f);F.push(f)}
 const pci=C.caja(w*.6,w*.06,w*.1,'#ffd36b');pci.position.y=C.u(-w*.29);G.add(pci);G.userData.F=F;return C.sombra(G)};
const hojita=(w,c='#fff8ef')=>{const G=C.grupo();G.add(C.caja(w,w*1.3,w*.1,c,w*.05));for(let i=0;i<4;i++){const l=C.caja(w*(i==3?.4:.66),w*.07,w*.05,'#b9a9b5',w*.02);
 l.position.set(C.u(i==3?-w*.13:0),C.u(w*.4-i*w*.22),C.u(w*.06));G.add(l)}return C.sombra(G)};
const pila=(r,c)=>{const G=C.grupo();for(let i=0;i<3;i++){const d=C.cil(r,r*.55,c);d.position.y=C.u((i-1)*r*.68);G.add(d)}return C.sombra(G)};
const sobre=(w)=>{const G=C.grupo();G.add(C.caja(w,w*.66,w*.12,'#fff8ef',w*.06));for(const s of[-1,1]){const f=C.caja(w*.62,w*.06,w*.05,'#5b8cff',w*.02);
 f.rotation.z=s*.55;f.position.set(C.u(s*w*.22),C.u(w*.13),C.u(w*.07));G.add(f)}return C.sombra(G)};
const pasto=(w)=>{const G=C.grupo();G.add(C.caja(w,w*.7,w,'#a9745b'));const p=C.caja(w*1.04,w*.26,w*1.04,'#4cc38a');p.position.y=C.u(w*.4);G.add(p);
 for(let i=0;i<5;i++){const h=C.cono(w*.06,w*.22,'#4cc38a');h.position.set(C.u((C.h(i)-.5)*w*.8),C.u(w*.6),C.u((C.h(i+9)-.5)*w*.8));G.add(h)}return C.sombra(G)};
"""


def tarjeta(pid, start, dur, body, js3d, sale=True):
    """Tarjeta transparente sobre la cámara; al final todo se aplasta contra la mesa (sin desvanecido)."""
    A = P.at(start)
    if sale:
        body = f'<div class="fz x" style="--x:{A(round(start + dur - .55, 2))}">{body}</div>'
    PIEZAS.append((pid, start, round(start + dur, 2), P.page(CSS, body, dur, S0=start, transparente=True, js3d=LIB3D + js3d)))


def bt(txt, size=72, extra=''):
    return f'<div class="bt" style="font-size:{size}px;{extra}">{txt}</div>'


def sb(txt, size=32, extra=''):
    return f'<div class="sb" style="font-size:{size}px;{extra}">{txt}</div>'


def rw(html, A, t, extra=''):
    return f'<div class="rw" style="--d:{A(t)};{extra}">{html}</div>'


def onoff(html, A, t, q=None, extra=''):
    qq = f'--q:{A(q)};' if q is not None else '--q:9999s;'
    return f'<div class="onoff" style="--d:{A(t)};{qq}{extra}">{html}</div>'


# ───────── 0:00 · «esta laptop me costó $9,000 pesos usada y va a ser el músculo de mi homelab»
S = 0.2; A = P.at(S); X = S + 4.1 - .55
tarjeta('c01-precio', S, 4.1,
        bloque(70, 290, 620, sb('mi nueva laptop', 36) + bt(f'${N([(0, 0), (.9, 9000, .9)], f="c")}<span style="font-size:48px"> MXN</span>', 150, 'white-space:nowrap;color:#3b3340')
               + chip('♻️ usada', A, 2.0, '#a8e6cf'), A, .25, color='#ffc79a')
        + bloque(110, 700, 820, bt('💪 el músculo de mi homelab', 54, 'color:#fff;white-space:nowrap'), A, 2.8, color='#ff6b6b'),
        r"""const lp=laptop(240,'#3b3340','#9b6bff');scene.add(lp);
return t=>{C.cae(lp,t,.5,500);C.aplasta(lp,t,""" + f'{X}' + r""");abre(lp,C.eio(C.k(t,1.2,.6)));P3(lp,860,560,2,t,1,.42,-.45,0)}""")

# ───────── 0:08 · Ryzen 7 (8 núcleos · 16 hilos) · 16 GB de RAM expandible · ⭐ lo más importante: RTX 3050 Ti de 4 GB
S = 8.3; A = P.at(S); X = S + 15.0 - .55
FILAS = [('🧠 Ryzen 7', '8 núcleos · 16 hilos', 9.0), ('🧩 16 GB de RAM', 'y se puede expandir', 13.2), ('🎮 RTX 3050 Ti', '4 GB de memoria', 20.8)]
fl = ''.join(rw(bt(n, 58) + sb(s_, 30, 'margin:2px 0 18px'), A, t) for n, s_, t in FILAS)
tarjeta('c02-specs', S, 15.0,
        bloque(60, 250, 650, bt('Lenovo Legion 5', 66) + sb('la encontré en Marketplace', 32, 'margin-bottom:22px') + fl, A, 8.5, color='#fff8ef')
        + bloque(120, 900, 560, bt('⭐ lo más importante', 52, 'white-space:nowrap'), A, 18.9, color='#fff09a'),
        r"""const ch=chip(120);scene.add(ch);const rm=ram(190);scene.add(rm);const gp=gpu(210);scene.add(gp);
return t=>{const x=""" + f'{X}' + r""";
 C.cae(ch,t,9.0,600);C.aplasta(ch,t,x);P3(ch,880,450,2,t,1,.35,-.4,0);
 C.cae(rm,t,13.2,600);C.aplasta(rm,t,x);P3(rm,880,640,2,t,2,.3,-.35,.05);
 C.cae(gp,t,20.8,600);C.aplasta(gp,t,x);P3(gp,880,840,2.5,t,3,.25,-.45,0);for(const f of gp.userData.F)f.rotation.z=-t*6}""")

# ───────── 0:33 · trabajo pesado: capturas de mis redes · precios que rastreo (Mercado Libre, Amazon) · hoy ZenBook → Legion
S = 33.0; A = P.at(S); X = S + 10.6 - .55
tarjeta('c03-tareas', S, 10.6,
        bloque(70, 250, 640, bt('Trabajo pesado', 64) + rw(bt('📸 capturas de mis redes', 44), A, 34.8, 'margin-top:14px')
               + rw(bt('🏷️ precios que rastreo', 44), A, 36.9, 'margin-top:8px')
               + '<div style="margin-top:10px">' + chip('Mercado Libre', A, 38.9, '#ffe600') + chip('Amazon', A, 39.8, '#ffc79a') + '</div>', A, 33.2, color='#fff09a')
        + bloque(70, 760, 400, bt('💻 hoy: ZenBook', 46, 'white-space:nowrap'), A, 40.6, color='#9fd3ff')
        + bloque(600, 760, 400, bt('🎮 Legion', 52, 'white-space:nowrap;color:#fff'), A, 41.9, color='#ff6b6b'),
        r"""const K=[];for(let i=0;i<3;i++){const c=C.caja(64,64,64,['#ff9f43','#c9b6ff','#4cc38a'][i]);scene.add(c);K.push(c)}
return t=>{K.forEach((c,i)=>{C.brota(c,t,40.8+i*.12);C.aplasta(c,t,""" + f'{X}' + r""");
 const p=C.eio(C.k(t,41.65+i*.12,.6));const x=180+i*90+p*500,y=700-Math.sin(Math.PI*p)*220;P3(c,x,y,3,t,i,.4,.6+p*3,0)})}""")

# ───────── 0:44 · después: pasar todos los videos a texto, para un análisis
S = 43.9; A = P.at(S); X = S + 5.9 - .55
LINEAS = [('$ transcribe mis_videos/*.mp4', 44.4, .7), ('→ transcripción lista ✓', 45.3, .5), ('«Esta laptop me costó 9,000…»', 46.2, 1.2)]
TX = ''.join(f'<div style="margin-top:6px"><span class="ty mono2" style="--d:{A(t)};--td:{d}s;--n:{len(s_)};font-size:34px">{s_}</span></div>' for s_, t, d in LINEAS)
tarjeta('c05-texto', S, 5.9,
        bloque(70, 280, 720, bt('🎞️ → 📝', 60) + TX + '<div style="margin-top:14px">' + chip('🔬 para un análisis', A, 48.5, '#c9b6ff') + '</div>', A, 44.0, color='#fff8ef'),
        r"""const H=[];for(let i=0;i<3;i++){const h=hojita(110,['#fff8ef','#ffe3ea','#e1f1ff'][i]);scene.add(h);H.push(h)}
return t=>{H.forEach((h,i)=>{C.cae(h,t,45.3+i*.2,500);C.aplasta(h,t,""" + f'{X}' + r""");P3(h,900,330+i*170,2+i*.3,t,i,.15,-.35+i*.15,(i-1)*.12)})}""")

# ───────── 0:59 · animaciones 3D: Mac 1× · ZenBook 9× más lenta · Legion con GPU → las 3 juntas, más rápido
S = 58.9; A = P.at(S); X = S + 10.6 - .55
BARRAS = [('🍎 Mac', '14%', '#3b3340', '1×', 59.7), ('💻 ZenBook', '100%', '#ff6b6b', '9× más lento', 61.2), ('🎮 Legion', '26%', '#4cc38a', 'GPU ⚡', 64.8)]
br = ''
for n, w, c, x, t in BARRAS:
    br += (rw(bt(n, 44), A, t - .3, 'margin-top:16px')
           + f'<div style="position:relative;height:50px;margin-top:6px"><div class="br" style="width:{w};background:{c};--d:{A(t)}"></div>'
           + f'<div class="on bt" style="position:absolute;{"right:12px;top:4px;color:#fff" if w == "100%" else f"left:calc({w} + 16px);top:2px"};font-size:38px;--d:{A(t + .8)}">{x}</div></div>')
tarjeta('c04-render', S, 10.6,
        bloque(60, 250, 690, bt('Animaciones 3D', 64) + sb('las de todos mis videos', 32) + br, A, 59.1, color='#fff8ef')
        + bloque(110, 900, 760, bt('🤝 las 3 juntas → más rápido', 48, 'white-space:nowrap'), A, 66.3, color='#a8e6cf'),
        r"""const gp=gpu(220);scene.add(gp);
return t=>{C.cae(gp,t,64.8,600);C.aplasta(gp,t,""" + f'{X}' + r""");P3(gp,885,620,2.5,t,1,.25,-.5,0);const v=6+20*C.eio(C.k(t,65.6,1.2));for(const f of gp.userData.F)f.rotation.z=-t*v}""")

# ───────── 1:10 · escena a pantalla completa: respaldo mutuo (local 0–19.1 → video 69.5–88.6)
S = 69.5; A = P.at(S)


def L(t):
    return S + t


def estado(html, t, q, color):
    return onoff(f'<span class="chip" style="--d:0s;--b:{color};animation:none">{html}</span>', A, L(t), L(q) if q is not None else None, 'margin-top:8px')


ZB = (bt('💻 ZenBook', 56) + estado('● en línea', .6, 5.2, '#a8e6cf') + estado('✕ caída', 5.3, 14.6, '#ff6b6b') + estado('● respaldo', 14.7, None, '#9fd3ff'))
LG = (bt('🎮 Legion', 56) + estado('● respaldo', 1.1, 6.2, '#9fd3ff') + estado('⚡ tomó el control', 6.3, 14.6, '#a8e6cf') + estado('✕ caída', 14.7, None, '#ff6b6b'))
SERV = [('🗄️ Base de datos', 9.8), ('⚙️ Servicios', 10.7), ('🧭 Mi hub', 11.4)]
sv = ''
for n, t in SERV:
    sv += (f'<div style="display:flex;justify-content:space-between;align-items:center;margin:6px 0">{rw(bt(n, 46), A, L(t))}'
           f'<div style="position:relative;width:260px;height:52px">'
           + onoff(bt('→ Legion', 42, 'color:#2f9e6a;text-align:right'), A, L(t), L(15.8), 'position:absolute;right:0;top:0')
           + onoff(bt('→ ZenBook', 42, 'color:#3f6fe0;text-align:right'), A, L(15.8), None, 'position:absolute;right:0;top:0') + '</div></div>')
TG = (f'<div style="display:flex;align-items:center;gap:24px"><div style="font-size:70px">✈️</div><div>{sb("Telegram · ahora", 30, "color:#fff")}'
      f'{bt("La ZenBook se cayó · la Legion tomó el control", 40, "color:#fff")}</div></div>')
RESP = (letras(['Respaldo', '*mutuo*'], A, L(.1), top=260, size=130, sale=L(4.8))
        + letras(['Si se cae la', '*ZenBook*…'], A, L(5.0), top=260, size=120, sale=L(14.3))
        + letras(['…y si cae la', '*Legion*'], A, L(14.5), top=260, size=120)
        + bloque(70, 860, 430, ZB, A, L(.4), color='#fff8ef')
        + bloque(580, 860, 430, LG, A, L(.9), color='#fff8ef')
        + bloque(70, 1150, 940, sv, A, L(9.6), color='#fff09a')
        + bloque(70, 1440, 760, TG, A, L(13.0), sale=L(14.3), color='#5b8cff')
        + bloque(130, 1440, 820, bt('🔁 la ZenBook vuelve a hacer todo', 50, 'white-space:nowrap'), A, L(16.4), color='#ffb3c7'))
JS1 = r"""const zb=laptop(250,'#5b8cff','#e1f1ff');scene.add(zb);const lg=laptop(250,'#3b3340','#c9b6ff');scene.add(lg);
const B=[];for(let i=0;i<3;i++){const b=C.bola(34,['#ff9f43','#9b6bff','#4cc38a'][i]);scene.add(b);B.push(b)}
const sb=sobre(150);scene.add(sb);const RED=new THREE.Color('#ff6b6b');
return t=>{const l=t-""" + f'{S}' + r""";
 // ZenBook: cae en 5.3 (se desinfla y pantalla roja), regresa en 14.7
 C.cae(zb,t,""" + f'{L(.4)}' + r""",500);const dz=C.k(l,5.3,.5)*(1-C.k(l,14.7,.6));const sz=1-.42*C.eio(dz);
 zb.userData.sq=[(zb.userData.sq||[1,1])[0]*(1+.15*dz),(zb.userData.sq||[1,1])[1]*sz];abre(zb,1-.85*C.eio(dz));
 zb.userData.sc.material.color.set(dz>.3?'#ff6b6b':'#e1f1ff');zb.userData.sc.material.emissive.set(dz>.3?'#ff2a3a':'#e1f1ff');P3(zb,285,700,2,t,1,.42,.35,0);
 // Legion: toma el control en 6.3 (pantalla late), cae en 14.7
 C.cae(lg,t,""" + f'{L(.9)}' + r""",500);const dl=C.k(l,14.7,.5);const sl=1-.42*C.eio(dl);
 lg.userData.sq=[(lg.userData.sq||[1,1])[0]*(1+.15*dl),(lg.userData.sq||[1,1])[1]*sl];abre(lg,1-.85*C.eio(dl));
 const on=l>6.3&&l<14.6;lg.userData.sc.material.emissiveIntensity=on?.4+.4*Math.abs(Math.sin(l*4)):.35;
 lg.userData.sc.material.color.set(dl>.3?'#ff6b6b':'#c9b6ff');lg.userData.sc.material.emissive.set(dl>.3?'#ff2a3a':'#c9b6ff');P3(lg,795,700,2,t,2,.42,-.35,0);
 // servicios = bolitas que brotan junto a la Legion y en 15.8 brincan a la ZenBook
 B.forEach((b,i)=>{C.brota(b,t,""" + f'{L(9.8)}' + r"""+[0,.9,1.6][i]);const p=C.eio(C.k(l,15.8+i*.1,.6));const x=760+i*70-p*500,y=560-Math.sin(Math.PI*p)*200;P3(b,x,y,4,t,i+3)});
 // aviso de Telegram: sobre que vuela, se posa y se aplasta en 14.3
 const f=C.eio(C.k(l,12.4,.6));sb.visible=l>12.4;C.aplasta(sb,t,""" + f'{L(14.3)}' + r""");P3(sb,1250-f*325,1380+f*150,4,t,7,.2,-.4+f*.4,.25*(1-f))}"""
PIEZAS.append(('s1-respaldo', S, round(S + 19.1, 2),
               P.page(CSS + 'body{transform-origin:50% 80%;animation:fuera .45s steps(5) 18.55s forwards}@keyframes fuera{40%{transform:scale(1.06,.9)}100%{transform:scale(1.3,0)}}',
                      RESP, 19.1, S0=S, fondo='cielo', entra=(540, 1300), ac='#5b8cff', js3d=LIB3D + JS1)))

# ───────── 1:29 · bases de datos copiadas al segundo → cambio rápido y simple
S = 88.57; A = P.at(S); X = S + 8.8 - .55
CICLO = [(0, 0)]
for i in range(7):
    t0 = 91.17 + i
    CICLO += [(t0, 0.9, 0.9), (t0 + .92, 0.0, .05)]
tarjeta('c06-replica', S, 8.8,
        bloque(70, 260, 400, bt('💻 ZenBook', 54, 'white-space:nowrap') + sb('base de datos', 32), A, 89.07, color='#9fd3ff')
        + bloque(610, 260, 400, bt('🎮 Legion', 54, 'white-space:nowrap') + sb('copia exacta', 32), A, 89.47, color='#c9b6ff')
        + bloque(150, 800, 780, bt(f'⏱ última copia: hace {N(CICLO, f="1")} s', 46, 'white-space:nowrap')
                 + '<div style="margin-top:8px">' + chip('⚡ cambio rápido y simple', A, 95.17, '#a8e6cf') + '</div>', A, 91.0, color='#fff8ef'),
        r"""const a=pila(64,'#9fd3ff');scene.add(a);const b=pila(64,'#c9b6ff');scene.add(b);const bo=C.bola(30,'#ff9f43');scene.add(bo);
return t=>{const x=""" + f'{X}' + r""";C.brota(a,t,89.3);C.aplasta(a,t,x);P3(a,270,600,2,t,1,.35,0,0);C.brota(b,t,89.7);C.aplasta(b,t,x);P3(b,810,600,2,t,2,.35,0,0);
 bo.visible=t>91.17&&t<x;const c=Math.max(0,t-91.17)%1,p=C.eio(Math.min(1,c/.9));P3(bo,270+p*540,560-Math.sin(Math.PI*p)*170,4,t,3)}""")

# ───────── 1:48 · Sígueme + «¿qué le pondrías a una 2.ª compu?» → «Un servidor de Minecraft 😅»
S = 108.37; A = P.at(S)
_r = 'Un servidor de Minecraft 😅'
BOTON = (f'<div style="position:relative;height:64px;margin-top:14px">'
         + onoff(f'<span class="chip" style="--b:#ff6b6b;color:#fff;animation:none">Seguir</span>', A, 108.6, 109.4, 'position:absolute;left:0;top:0')
         + onoff(f'<span class="chip" style="--b:#a8e6cf;animation:none">Siguiendo ✓</span>', A, 109.4, None, 'position:absolute;left:0;top:0') + '</div>')
SEG = (bloque(600, 280, 410, sb('Sígueme', 34) + bt('Armando', 80) + sb('homelab · IA · código', 30) + BOTON, A, 108.5, color='#ffb3c7')
       + bloque(70, 330, 480, bt('🖥️ ¿Qué le pondrías a una 2.ª compu?', 44)
                + f'<div style="margin-top:16px"><span class="ty bt" style="--d:{A(111.0)};--td:1s;--n:{len(_r) + 1};font-size:36px;color:#3f6fe0">{_r}</span></div>',
                A, 109.9, color='#fff8ef'))
PIEZAS.append(('seguir', S, FIN, P.page(CSS, SEG, round(FIN - S, 2), S0=S, transparente=True,
                                       js3d=LIB3D + r"""const pa=pasto(120);scene.add(pa);return t=>{C.brota(pa,t,112.0);P3(pa,320,800,3,t,1,.45,.6+.3*Math.sin(t*.8),0)}""")))
PIEZAS.sort(key=lambda p: p[1])

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path, f'{b - a:.2f}'); continue
        r = subprocess.run(['node', CAP, path, f'{b - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'videos/10/plastilina')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
