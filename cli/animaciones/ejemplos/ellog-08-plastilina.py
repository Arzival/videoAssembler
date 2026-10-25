"""El Log #08 · edición «Plastilina» (claymation): todo modelado en plastilina sobre fondos pastel. Letras gorditas que caen y se
aplastan, bloques de plastilina aplanada, números y figuras 3D (logos, escudo, muñequito, teclado de bolitas, ventanitas, robot
con lupa) que caen, brotan y se aplastan con temblor de stop-motion a 12 cps. Arriba, la cinta de El Log en plastilina con la
etiqueta «ÚLTIMA HORA» que late y una franja que corre los datos.
Tiempos = voz recortada de noticias/8 (97.46 s), los mismos de ellog-08-recorte.py.
Uso: SALIDA=~/Documents/Videos/noticias/8/plastilina REL=noticias/8/plastilina python3 ejemplos/ellog-08-plastilina.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import plastilina as P
import ellog_gloss as G
from plastilina import bloque, chip, N, numero, ap
import re


def letras(lineas, *a, **k):
    """P.letras con *acento de varias palabras* (la librería solo lo toma por palabra)."""
    lineas = [re.sub(r'\*([^*]+?)\*', lambda m: ' '.join(f'*{w}*' for w in m.group(1).split(' ')), ln) for ln in lineas]
    return P.letras(lineas, *a, **k)

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/noticias/8/plastilina')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 97.46
TOP = 210          # primer renglón útil (debajo de la cinta, que ocupa 0–150)
C_ = P.PAS
BL = '#fff8ef'     # blanco plastilina (texto sobre fondo oscuro)
PIEZAS = []
CSS = """
.tip{display:inline-block;white-space:nowrap;clip-path:inset(0 100% 0 0);animation:tipx 1s steps(26) var(--d) forwards}
@keyframes tipx{to{clip-path:inset(0 0 0 0)}}
.cod{font-family:Nunito;font-weight:800;font-size:34px;line-height:1.55;white-space:pre;color:#c8f7d8}
.cod i{font-style:normal;color:#9d93b8}.cod b{color:#ffb3c7}
"""

# figuras extra de plastilina (se anteponen al js3d de cada escena)
LIB = r"""const PX=C.PX;
C.escudo=(s,c)=>{const w=s/PX,sh=new THREE.Shape();sh.moveTo(0,w*.55);sh.quadraticCurveTo(w*.3,w*.5,w*.45,w*.42);sh.lineTo(w*.45,w*.05);
 sh.quadraticCurveTo(w*.42,-w*.42,0,-w*.6);sh.quadraticCurveTo(-w*.42,-w*.42,-w*.45,w*.05);sh.lineTo(-w*.45,w*.42);sh.quadraticCurveTo(-w*.3,w*.5,0,w*.55);
 const g=new THREE.ExtrudeGeometry(sh,{depth:w*.12,bevelEnabled:true,bevelThickness:w*.09,bevelSize:w*.07,bevelSegments:8,curveSegments:32});g.center();
 const m=new THREE.Mesh(g,C.barro(c));return C.sombra(m)};
C.ventana=(w,c)=>{const G=C.grupo();const b=C.caja(w,w*.72,w*.22,c,w*.1);G.add(b);const bar=C.caja(w*.98,w*.17,w*.25,'#3b3340',w*.07);bar.position.y=w*.28/PX;G.add(bar);
 ['#ff6b6b','#ffd36b'].forEach((k,i)=>{const d=C.bola(w*.045,k);d.position.set((-w*.38+i*w*.11)/PX,w*.28/PX,w*.14/PX);G.add(d)});
 const l1=C.caja(w*.62,w*.07,w*.05,'#ffffff',w*.03);l1.position.set(-w*.08/PX,w*.02/PX,w*.12/PX);G.add(l1);
 const l2=C.caja(w*.42,w*.07,w*.05,'#ffffff',w*.03);l2.position.set(-w*.18/PX,-w*.14/PX,w*.12/PX);G.add(l2);G.userData.b=b;return G};
C.robot=(w,c)=>{const G=C.grupo();G.add(C.caja(w,w*.8,w*.7,c,w*.22));[-1,1].forEach(s=>{const e=C.bola(w*.1,'#3b3340');e.position.set(s*w*.2/PX,w*.06/PX,w*.36/PX);G.add(e)});
 const bo=C.capsula(w*.05,w*.26,'#3b3340');bo.rotation.z=Math.PI/2;bo.position.set(0,-w*.2/PX,w*.36/PX);G.add(bo);
 const an=C.cil(w*.035,w*.3,'#3b3340');an.position.y=w*.55/PX;G.add(an);const tp=C.bola(w*.09,'#ff6b6b');tp.position.y=w*.72/PX;G.add(tp);
 [-1,1].forEach(s=>{const o=C.bola(w*.13,c);o.position.set(s*w*.52/PX,0,0);G.add(o)});return G};
C.lupa=(w,c='#ffd36b')=>{const G=C.grupo();G.add(C.dona(w*.33,w*.09,c));const h=C.capsula(w*.075,w*.38,'#a9745b');h.rotation.z=Math.PI/4;h.position.set(w*.4/PX,-w*.4/PX,0);G.add(h);return G};
C.muneco=(h,c)=>{const G=C.grupo();G.add(C.capsula(h*.22,h*.34,c));const ca=C.bola(h*.2,'#ffc79a');ca.position.y=h*.42/PX;G.add(ca);
 const le=C.caja(h*.36,h*.08,h*.06,'#3b3340',h*.03);le.position.set(0,h*.45/PX,h*.18/PX);G.add(le);
 const al=C.cil(h*.26,h*.05,'#3b3340');al.position.y=h*.58/PX;G.add(al);const co=C.cil(h*.16,h*.17,'#3b3340');co.position.y=h*.67/PX;G.add(co);return G};
C.teclado=(w,c)=>{const G=C.grupo();G.add(C.caja(w,w*.4,w*.1,c,w*.05));const K=[];const cs=['#ffb3c7','#a8e6cf','#9fd3ff','#ffd36b','#c9b6ff'];
 for(let r=0;r<4;r++)for(let k=0;k<9;k++){const b=C.bola(w*.038,cs[(r+k)%5]);b.position.set((-w*.4+k*w*.1)/PX,(w*.13-r*w*.085)/PX,w*.07/PX);G.add(b);K.push(b)}G.userData.K=K;return G};
C.columna=(r,h,c)=>{const G=C.grupo();const m=C.capsula(r,h,c);m.position.y=(h/2+r)/PX;G.add(m);return G};
"""


def escena(pid, start, end, body, fondo='crema', entra=(540, 1300), ac='#ff6b6b', js3d=None, sigue=True):
    if sigue:
        end += P.COLA
    PIEZAS.append((pid, start, end, P.page(CSS, body, round(end - start, 2), S0=start, fondo=fondo, entra=entra, ac=ac,
                                           js3d=(LIB + js3d) if js3d else None)))


def cod(lineas, A):
    """Líneas de terminal que aparecen de golpe: [(texto, t)]."""
    return ''.join(ap(f'<div class="cod">{tx}</div>', A, t) for tx, t in lineas)


# ───────── 0:00 · «Dicen que PHP está muerto…» → dos fallos críticos | ¿Laravel, WordPress o PHP? → te toca actualizar
S = 0.0; A = P.at(S)
b = (letras(['Dicen que PHP', 'está *muerto*…'], A, .3, top=TOP, size=110, sale=5.0)
     + letras(['Dos fallos', '*críticos*'], A, 1.8, top=470, size=160, sale=5.0)
     + bloque(70, 1300, 600, '<div class="tt">🚨 Alerta de seguridad</div>' + ap('<div class="sb mono">CVE-2026-109618</div>', A, 3.0)
              + ap('<div class="sb mono">CVE-2026-109619</div>', A, 3.6) + chip('urgente', A, 2.5, '#ff9a9a'), A, 2.4, sale=5.0)
     + letras(['¿Laravel, WordPress', 'o *PHP*?'], A, 5.2, top=TOP, size=110)
     + ap(bloque(150, 1010, 780, '<div class="tt" style="text-align:center">o cualquier cosa en PHP</div>', A, 8.8, color='#ffd36b'), A, 8.8)
     + letras(['Te toca', '*actualizar*'], A, 9.2, top=1210, size=150)
     + bloque(640, 1560, 330, '<div class="tt" style="text-align:center">¡ahorita!</div>', A, 9.8, color='#ff9a9a'))
escena('e00-alerta', S, 10.9, b, fondo='rosa', entra=(540, 960), ac='#ff4f6d', js3d="const PH=" + json.dumps(G.svgpath('php'))
       + ",LV=" + json.dumps(G.svgpath('laravel')) + ",WP=" + json.dumps(G.svgpath('wordpress')) + r""";
const ph=C.logo(PH,380,'#8f9bff',70);scene.add(ph);
const lv=C.logo(LV,210,'#ff6b6b',60);scene.add(lv);const wp=C.logo(WP,210,'#5b8cff',60);scene.add(wp);const p2=C.logo(PH,240,'#8f9bff',60);scene.add(p2);
return t=>{C.cae(ph,t,2.2,700);C.aplasta(ph,t,4.8);const miedo=t>2.9&&t<4.8?Math.sin(t*44)*.07:0;ph.rotation.set(.3,.2*Math.sin(t*.9),miedo);C.pon(ph,690,1040,2,t,1);
 C.cae(lv,t,6.6,600);lv.rotation.set(.25,.25*Math.sin(t),0);C.pon(lv,220,770,2,t,2);
 C.cae(wp,t,7.2,600);wp.rotation.set(.25,-.25*Math.sin(t),0);C.pon(wp,540,800,2,t,3);
 C.cae(p2,t,8.6,600);p2.rotation.set(.3,.2*Math.sin(t*1.1),0);C.pon(p2,860,770,2,t,4)}""")

# ───────── 0:11 · se llama PHP2Shell · lo encontraron con IA
S = 10.9; A = P.at(S)
b = (letras(['Lo llamaron'], A, 11.0, top=TOP, size=110)
     + bloque(70, 390, 940, '<div style="font-size:190px;font-weight:700;line-height:1;color:#fff8ef;text-align:center;text-shadow:0 8px 0 rgba(0,0,0,.18)">PHP2Shell</div>',
              A, 11.4, color='#ff6b6b')
     + ap(bloque(560, 700, 420, '<div class="tt" style="font-size:38px">así le pusieron ✌️</div>', A, 13.6, color='#ffd36b'), A, 13.6)
     + letras(['Lo encontraron', 'con *IA*'], A, 14.7, top=900, size=130)
     + bloque(70, 1330, 470, '<div class="tt" style="font-size:40px">🤖 la IA ayudó<br>a hallarlo</div>', A, 16.0, color='#9fd3ff'))
escena('e01-php2shell', S, 17.0, b, fondo='lila', entra=(150, 400), ac='#7d5cff', js3d=r"""
const rb=C.robot(250,'#9fd3ff');scene.add(rb);const lp=C.lupa(170);scene.add(lp);
return t=>{C.brota(rb,t,15.6,.7);rb.rotation.set(.15,-.35+.2*Math.sin(t*1.3),0);C.pon(rb,790,1440,2.5,t,1);
 C.brota(lp,t,15.9,.6);lp.rotation.set(.2,.3*Math.sin(t*1.5),-.3);C.pon(lp,620,1300+20*Math.sin(t*3),3.5,t,2)}""")

# ───────── 0:17 · PHP saca un parche hoy · dos fallos de 9.2 | del 0 al 10 → casi lo máximo
S = 17.0; A = P.at(S)
b = (letras(['PHP saca un', '*parche* hoy'], A, 17.1, top=TOP, size=130, sale=21.5)
     + bloque(70, 560, 940, '<div class="tt">php.net › versión de seguridad</div>' + ap('<div class="sb">✓ corrige 2 fallos</div>', A, 21.7), A, 18.2, sale=25.2, color='#e2f7ee')
     + letras(['Dos fallos', 'de *9.2*'], A, 21.7, top=TOP, size=130, sale=25.2)
     + ap(numero(N([(0, 0), (24.1, 9.2, 1.0)], f='1'), 70, 880, 420, A, 24.0, color='#ff6b6b'), A, 24.0, sale=25.2)
     + ap(bloque(80, 1360, 420, '<div class="tt">de 10 posibles</div>', A, 24.6, color='#ffd36b'), A, 24.6, sale=25.2)
     + letras(['Del 0 al 10…'], A, 25.4, top=TOP, size=140, sale=29.9)
     + ap(f'<div style="position:absolute;left:80px;top:860px">{chip("😌 nada grave", A, 26.8, "#a8e6cf")}</div>'
          f'<div style="position:absolute;right:80px;top:860px">{chip("😱 lo máximo", A, 27.1, "#ff9a9a")}</div>', A, 26.8)
     + ap(numero('9.2', 760, 440, 140, A, 29.3, color='#ff4f6d'), A, 29.3)
     + letras(['Casi lo', '*máximo*'], A, 30.1, top=1050, size=160)
     + bloque(90, 1450, 380, '<div class="tt" style="text-align:center">🔥 crítico</div>', A, 31.6, color='#ff9a9a'))
escena('e02-parche', S, 32.85, b, fondo='menta', entra=(900, 1500), ac='#e2354b', js3d=r"""
const es=C.escudo(280,'#9fd3ff');scene.add(es);
const cs=['#4cc38a','#6fcf8f','#9bd98a','#c6df7d','#e8d86f','#ffcf5c','#ffb04f','#ff9147','#ff7246','#ff5a4c','#ff4560'];
const R=cs.map((c,i)=>{const b=C.bola(34,c);scene.add(b);return b});const mk=C.capsula(30,60,'#3b3340');scene.add(mk);
return t=>{C.cae(es,t,21.9,700);C.aplasta(es,t,25.0);const rojo=t>24.1;es.material.color.set(rojo?'#ff8a8a':'#9fd3ff');
 es.rotation.set(.2,.35*Math.sin(t*.9)+(rojo&&t<25?Math.sin(t*40)*.06:0),0);C.pon(es,880,1150,2,t,1);
 R.forEach((b,i)=>{C.brota(b,t,26.8+i*.03,.5);b.rotation.set(0,0,0);C.pon(b,110+i*86,770,2,t,10+i)});
 C.cae(mk,t,29.2,500);mk.rotation.set(0,0,0);C.pon(mk,110+9.2*86,690,2.4,t,30)}""")

# ───────── 0:33 · ejecución remota de código → corre comandos en tu servidor | tu teclado a un desconocido
S = 32.85; A = P.at(S)
TERM = cod([('<i>desconocido@tu-servidor:~$</i>', 38.8), ('$ whoami', 39.6), ('<b>www-data</b>', 40.2), ('$ ls /var/www', 40.9), ('$ cat config.php', 41.6)], A)
b = (letras(['Ejecución', '*remota*', 'de código'], A, 32.95, top=TOP, size=140, sale=37.8, color=BL)
     + bloque(70, 760, 620, '<div class="tt" style="color:#fff8ef">🔓 sin iniciar sesión</div>', A, 36.6, sale=37.8, color='#ff6b6b')
     + letras(['Corre *comandos*', 'en tu servidor'], A, 38.0, top=TOP, size=100, sale=42.5, color=BL)
     + bloque(70, 470, 940, TERM, A, 38.6, sale=42.5, color='#2b2540')
     + letras(['Tu *teclado*', 'a un', 'desconocido'], A, 42.7, top=TOP, size=140, color=BL))
escena('e03-remoto', S, 45.4, b, fondo='noche', entra=(150, 1600), ac='#ff9f43', js3d=r"""
const mu=C.muneco(330,'#5b4b7a');scene.add(mu);const tc=C.teclado(380,'#fff8ef');scene.add(tc);
const tc2=C.teclado(560,'#fff8ef');scene.add(tc2);const mu2=C.muneco(360,'#5b4b7a');scene.add(mu2);
return t=>{C.brota(mu,t,38.8,.7);C.aplasta(mu,t,42.4);mu.rotation.set(0,-.3+.2*Math.sin(t*1.2),0);C.pon(mu,830,1330,2,t,1);
 C.brota(tc,t,40.9,.6);C.aplasta(tc,t,42.4);tc.rotation.set(-.55,.15,0);C.pon(tc,450,1420,2,t,2);
 tc.userData.K.forEach((k,i)=>{k.position.z=(t>41&&Math.sin(t*14+i*2.1)>.7?.02:.07)*380/PX});
 C.cae(tc2,t,43.5,700);tc2.rotation.set(-.5,-.15,0);C.pon(tc2,420,1050,2,t,3);
 C.cae(mu2,t,44.2,600);mu2.rotation.set(0,.35,0);C.pon(mu2,820,1360,2,t,4)}""")

# ───────── 0:45 · no es cualquier cosa · millones de sitios · sitios en alerta | Hacker News: Países Bajos (sin confirmar)
S = 45.4; A = P.at(S)
QUOTE = ('<div class="tt" style="font-size:46px;line-height:1.2">«' + ap('El centro de ciberseguridad', A, 55.6).replace('<div', '<span').replace('</div>', '</span>')
         + ' ' + ap('de <b style="color:#ff6b00">Países Bajos</b>', A, 57.1).replace('<div', '<span').replace('</div>', '</span>')
         + ' ' + ap('quedó fuera de línea', A, 58.3).replace('<div', '<span').replace('</div>', '</span>')
         + ' ' + ap('por usar PHP', A, 59.1).replace('<div', '<span').replace('</div>', '</span>') + '»</div>')
b = (letras(['No es cualquier', '*cosa*'], A, 45.5, top=TOP, size=130, sale=46.9)
     + letras(['*Millones*', 'de sitios'], A, 47.0, top=TOP, size=150, sale=49.7)
     + letras(['Sitios en', '*alerta*'], A, 49.9, top=TOP, size=150, sale=52.8)
     + bloque(520, 1480, 480, '<div class="tt" style="font-size:38px">📰 «sitios en alerta», dicen los medios</div>', A, 51.5, sale=52.8, color='#ffd36b')
     + letras(['Lo que dicen en', '*Hacker News*'], A, 53.0, top=TOP, size=110)
     + bloque(70, 560, 940, QUOTE, A, 54.2, color='#fff8ef')
     + letras(['Ojo: aún', '*sin confirmar*'], A, 60.0, top=1280, size=120)
     + bloque(640, 1530, 360, '<div class="tt" style="text-align:center;font-size:38px">⚠️ sin confirmar</div>', A, 60.2, color='#ff9a9a'))
escena('e04-sitios', S, 63.5, b, fondo='limon', entra=(900, 300), ac='#ff7a1a', js3d="const YC=" + json.dumps(G.svgpath('ycombinator')) + r""";
const V=[];const cs=['#9fd3ff','#ffb3c7','#a8e6cf','#c9b6ff','#ffc79a'];
for(let i=0;i<20;i++){const v=C.ventana(150,cs[i%5]);scene.add(v);V.push(v)}
const yc=C.logo(YC,170,'#ff7a1a',50);scene.add(yc);
return t=>{V.forEach((v,i)=>{const c=i%4,r=Math.floor(i/4),t0=47.3+((i*7)%20)*.08;C.brota(v,t,t0,.5);C.aplasta(v,t,52.5+i*.01);
  const roja=(i*11)%4==0&&t>50.2+(i%7)*.18;v.userData.b.material.color.set(roja?'#ff6b6b':cs[i%5]);
  v.rotation.set(.15,((i*37)%9-4)*.04,((i*13)%7-3)*.03+(roja?Math.sin(t*30+i)*.05:0));C.pon(v,170+c*245,700+r*190,2,t,i)});
 C.cae(yc,t,53.1,600);yc.rotation.set(.25,.3*Math.sin(t*.9),0);C.pon(yc,920,330,2.5,t,40)}""")

# ───────── 1:03 · PHP no es malo · la IA ya encuentra fallos · saldrán más seguido | no lo dejes para después
S = 63.5; A = P.at(S)
CODE = cod([('<i>&lt;?php</i>', 67.6), ("$user = $_GET['id'];", 67.6), ("include($page . '.php');", 67.6), ('<b>echo render($tpl);   ← fallo</b>', 69.2),
            ('<b>$db-&gt;query($sql);   ← fallo</b>', 70.1)], A)
b = (letras(['PHP no es', '*malo*'], A, 63.6, top=TOP, size=150, sale=67.2)
     + bloque(640, 260, 320, '<div class="tt" style="text-align:center;font-size:60px">✓</div>', A, 66.5, sale=67.2, color='#a8e6cf')
     + letras(['La IA ya encuentra', '*fallos*'], A, 67.4, top=TOP, size=105, sale=71.0)
     + bloque(70, 520, 720, CODE, A, 67.6, sale=73.0, color='#2b2540')
     + letras(['Saldrán más', '*seguido*'], A, 71.1, top=TOP, size=140, sale=73.0)
     + letras(['No lo dejes', 'para *después*'], A, 73.3, top=TOP, size=140)
     + bloque(100, 720, 470, '<div class="tt">📌 Actualizar<br>después…</div>' + ap('<div style="position:absolute;left:30px;right:30px;top:110px;height:14px;border-radius:7px;background:#ff4f6d"></div>', A, 74.6),
              A, 73.8, color='#ffd36b')
     + numero('¡HOY!', 520, 900, 200, A, 75.9, color='#ff4f6d'))
escena('e05-ia', S, 76.6, b, fondo='cielo', entra=(540, 1700), ac='#3d6bff', js3d=r"""
const rb=C.robot(230,'#c9b6ff');scene.add(rb);const lp=C.lupa(190,'#ffd36b');scene.add(lp);
const B=[0,1,2].map(i=>{const c=C.columna(40,60+i*90,['#a8e6cf','#ffd36b','#ff9a9a'][i]);scene.add(c);return c});
return t=>{C.brota(rb,t,67.6,.7);C.aplasta(rb,t,72.8);rb.rotation.set(.1,-.4+.2*Math.sin(t*1.1),0);C.pon(rb,880,1080,2.5,t,1);
 C.brota(lp,t,67.9,.6);C.aplasta(lp,t,72.8);const sx=R=>R;lp.rotation.set(.2,.2,-.3);C.pon(lp,330+220*Math.sin(t*1.3),1180+60*Math.cos(t*1.7),4,t,2);
 B.forEach((c,i)=>{C.brota(c,t,72.3+i*.2,.5);C.aplasta(c,t,73.0);c.rotation.set(0,.3,0);C.pon(c,300+i*200,1420,2,t,10+i)})}""")

# ───────── 1:17 · ¿qué versión tienes? · corre php -v · ya con el parche (versiones por rama) | PHP no está muerto · hoy lo actualizamos
S = 76.6; A = P.at(S)
RAMAS = [('8.5', '8.5.12', 83.2, '#ffd36b'), ('8.4', '8.4.27', 83.5, '#a8e6cf'), ('8.3', '8.3.36', 83.8, '#ffb3c7'), ('8.2', '8.2.35', 84.1, '#9fd3ff')]
NOTAS = ''.join(bloque(70 + (i % 2) * 490, 930 + (i // 2) * 300, 450, f'<div class="sb">rama {r}</div><div class="tt" style="font-size:70px">{v} ✓</div>', A, t, sale=86.0, color=c)
                for i, (r, v, t, c) in enumerate(RAMAS))
TERM2 = cod([('<i>$</i> php -v', 79.9), ('PHP 8.4.<b>27</b> (cli)', 80.6), ('<i># compárala con la última de tu rama</i>', 81.8)], A)
b = (letras(['¿Qué versión', '*tienes*?'], A, 76.7, top=TOP, size=140, sale=79.4)
     + letras(['Corre', '*php -v*'], A, 79.6, top=TOP, size=140, sale=83.0)
     + bloque(70, 560, 940, TERM2, A, 79.8, sale=86.0, color='#2b2540')
     + letras(['Ya con el', '*parche*'], A, 83.2, top=TOP, size=140, sale=86.0)
     + NOTAS
     + letras(['PHP *no* está', 'muerto'], A, 86.2, top=TOP, size=150)
     + letras(['Tan vivo que hoy', 'lo *actualizamos*'], A, 88.3, top=1260, size=100))
escena('e06-version', S, 91.1, b, fondo='menta', entra=(200, 900), ac='#1fa35f', js3d="const PH=" + json.dumps(G.svgpath('php')) + r""";
const ph=C.logo(PH,420,'#8f9bff',80);scene.add(ph);const co=C.bola(70,'#ff4f6d');scene.add(co);
return t=>{if(t<86.2){ph.visible=false;co.visible=false;return}
 const inf=C.k(t,87.2,.9),w=inf<1?Math.sin(inf*Math.PI*2.5)*(1-inf)*.4:0;ph.visible=true;
 ph.userData.sq=[1+.25*(1-inf)+w*.5,Math.max(.12,.12+.88*inf)-w*.4];ph.rotation.set(.3,.25*Math.sin(t*.9),0);C.pon(ph,540,880,2,t,1);
 C.brota(co,t,89.8,.5);const lat=1+.12*Math.max(0,Math.sin(t*9));co.rotation.set(0,0,0);C.pon(co,850,1050,3.5,t,2,lat)}""")

# ───────── 1:31 · cierre: ¿cada cuánto actualizas tu servidor? (abajo entra «Sígueme»)
S = 91.1; A = P.at(S)
b = (letras(['¿Cada cuánto', 'actualizas tu', '*servidor*?'], A, 91.2, top=TOP, size=115)
     + bloque(70, 650, 940, '<div class="tt" style="font-size:56px">📅 Siempre al día</div>', A, 92.1, color='#a8e6cf')
     + bloque(70, 850, 940, '<div class="tt" style="font-size:56px">🔥 Cuando algo truena</div>', A, 92.9, color='#ffb3c7')
     + letras(['cuéntame 👇'], A, 93.4, top=1060, size=70, color='#ff6b6b'))
escena('e07-cierre', S, FIN, b, fondo='crema', entra=(800, 1100), sigue=False)

# ───────── «Sígueme» (transparente, sobre el cierre)
SEG_INI = 93.9
S = SEG_INI; A = P.at(S)
SEG = (bloque(570, 1180, 440, '<div class="sb">Sígueme</div><div class="tt" style="font-size:66px">Armando</div><div class="sb">El Log · cada semana</div>'
              + chip('Seguir ✓', A, 94.8, '#a8e6cf'), A, 94.0, color='#ffd36b')
       + bloque(70, 1180, 470, '<div class="tt" style="font-size:38px">🛠️ ¿Cada cuánto actualizas?</div>'
                f'<div class="sb" style="margin-top:14px;color:#3d6bff;opacity:1"><span class="tip" style="--d:{A(95.3)}">Cada semana, ya aprendí 😅</span></div>',
                A, 94.4, color='#fff8ef'))
PIEZAS.append(('seguir', SEG_INI, FIN, P.page(CSS, SEG, round(FIN - SEG_INI, 2), S0=SEG_INI, transparente=True)))

# ───────── cinta de El Log en plastilina (todo el video, encima de todo)
CORRIDO = ['PHP 8.5.12, 8.4.27, 8.3.36 y 8.2.35 corrigen los dos fallos', 'CVE-2026-109618 y CVE-2026-109619: 9.2 de 10',
           'Ejecución de código sin iniciar sesión', 'Parche de emergencia: salió un día antes por una filtración',
           'Los encontraron investigadores de Calif, Wiz y OpenAI', 'Hacker News: lo de Países Bajos aún no está confirmado', 'Revisa tu versión: php -v']
CAPS = [(0.0, 'Alerta'), (10.9, 'PHP2Shell'), (17.0, 'El parche'), (32.85, 'Ejecución remota'), (45.4, 'Sitios en alerta'), (63.5, 'La IA'),
        (76.6, 'Tu versión'), (91.1, 'Tu opinión')]
A = P.at(0)
CAPH = ''.join(ap(f'<span class="cp">{i + 1:02d} · {n}</span>', A, t, CAPS[i + 1][0] if i + 1 < len(CAPS) else None) for i, (t, n) in enumerate(CAPS))
TICK = '<span>🔸</span>'.join(f'<span>{c}</span>' for c in CORRIDO)
CINTA_CSS = """
.cin{position:absolute;left:18px;right:18px;top:14px;height:84px;z-index:90;border-radius:42px;background:#fff8ef;display:flex;align-items:center;gap:18px;padding:0 26px;
  box-shadow:inset 0 -10px 0 rgba(0,0,0,.07),inset 0 8px 14px rgba(255,255,255,.6),0 12px 0 rgba(0,0,0,.1),0 22px 28px rgba(60,30,30,.22);animation:pzin .6s steps(7) both}
.cin .lg{font-weight:700;font-size:50px;white-space:nowrap}.cin .lg i{font-style:normal;color:#ff4f6d}
.cin .ul{padding:6px 18px;border-radius:999px;background:#ff4f6d;color:#fff8ef;font-weight:700;font-size:28px;white-space:nowrap;
  box-shadow:inset 0 -5px 0 rgba(0,0,0,.15);animation:late .5s steps(2) infinite}
@keyframes late{50%{transform:scale(1.12,.92)}}
.cin .cps{margin-left:auto;position:relative;width:330px;height:50px}
.cin .cps .ap{position:absolute;right:0;top:0}
.cin .cp{display:block;font-family:Nunito;font-weight:900;font-size:30px;white-space:nowrap;padding:6px 18px;border-radius:999px;background:#c9b6ff}
.tk{position:absolute;left:30px;right:30px;top:104px;height:46px;z-index:89;border-radius:23px;background:#ff6b6b;overflow:hidden;display:flex;align-items:center;
  box-shadow:inset 0 -6px 0 rgba(0,0,0,.12),0 8px 14px rgba(60,30,30,.2)}
.tk .mv{display:flex;gap:28px;white-space:nowrap;font-family:Nunito;font-weight:900;font-size:26px;color:#fff8ef;padding-left:200px;animation:mv 70s linear infinite}
@keyframes mv{to{transform:translateX(-100%)}}
"""
CINTA = (f'<div class="cin"><span class="lg">El <i>Log</i> · N.º 08</span><span class="ul">⚠ ÚLTIMA HORA</span><div class="cps">{CAPH}</div></div>'
         f'<div class="tk"><div class="mv">{TICK}<span>🔸</span>{TICK}</div></div>')
PIEZAS.append(('cinta', 0.0, FIN, P.page(CSS + CINTA_CSS, CINTA, FIN, S0=0.0, transparente=True)))
PRE = 'ellp8-'

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b_, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path, f'{b_ - a:.2f}'); continue
        r = subprocess.run(['node', CAP, path, f'{b_ - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'noticias/8/plastilina')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b_, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b_, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
