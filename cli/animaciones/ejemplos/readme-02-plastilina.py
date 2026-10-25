"""El Readme #02 · RAG — edición «Plastilina» (claymation): el RAG explicado con plastilina 3D sobre fondos pastel.
Documentos = hojitas de plastilina que se cortan en pedacitos de colores; una lupa de plastilina busca y los pedacitos que
coinciden brincan; el robot de plastilina «se come» solo esos pedazos y contesta. Letras gorditas que caen y se aplastan,
bloques de plastilina, stop-motion a 12 cps con temblor de mano, y cada sección entra como una mancha que se aplasta.
Arriba, banda de plastilina con «README.md · #02 RAG» y la sección actual. Tiempos = los de readme-02-recorte.py (132.34 s).
Uso: SALIDA=~/Documents/Videos/readme/2/plastilina REL=readme/2/plastilina python3 ejemplos/readme-02-plastilina.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import plastilina as P
import ellog_gloss as G
from plastilina import letras, bloque, chip, numero, N, ap

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/readme/2/plastilina')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 132.34
TOP = 280          # primer renglón útil (debajo de la banda)
PIEZAS = []
C = P.PAS
AZ, RJ, VD, NA, MO = '#5b8cff', '#ff6b6b', '#4cc38a', '#ff9f43', '#9b6bff'

# figuras de plastilina del Readme (se anteponen al js3d de cada escena)
LIB3 = r"""
const {PX}=C,U=p=>p/PX;
C.hojita=(w,h,c='#fff8ef',lc=['#5b8cff','#ff6b6b','#4cc38a'])=>{const G=C.grupo();G.add(C.caja(w,h,26,c,12));
 for(let i=0;i<3;i++){const l=C.caja(w*(.68-i*.14),h*.08,12,lc[i%lc.length],6);l.position.set(U(-w*(.04+i*.07)),U(h*.26-i*h*.22),U(16));G.add(l)}return G};
C.pedacito=(s,c)=>C.caja(s,s,s,c,s*.32);
C.lupa=(r,c='#ff9f43')=>{const G=C.grupo();G.add(C.dona(r,r*.24,c));
 const v=new THREE.Mesh(new THREE.CylinderGeometry(U(r*.82),U(r*.82),U(10),40),C.barro('#cfeaff'));v.rotation.x=Math.PI/2;C.sombra(v);G.add(v);
 const m=C.capsula(r*.2,r*.9,c);m.position.set(U(r*1.05),U(-r*1.05),0);m.rotation.z=Math.PI/4;G.add(m);return G};
C.robot=(w,c='#c9b6ff')=>{const G=C.grupo();G.add(C.caja(w,w*.82,w*.7,c,w*.22));
 for(const x of[-1,1]){const e=C.bola(w*.13,'#fff8ef');e.position.set(U(x*w*.2),U(w*.1),U(w*.33));G.add(e);
  const p=C.bola(w*.06,'#3b3340');p.position.set(U(x*w*.2),U(w*.1),U(w*.44));G.add(p)}
 const a=C.capsula(w*.04,w*.22,'#9b6bff');a.position.y=U(w*.55);G.add(a);const b=C.bola(w*.08,'#ff6b6b');b.position.y=U(w*.72);G.add(b);
 const boca=C.caja(w*.36,w*.08,w*.08,'#3b3340',w*.03);boca.position.set(0,U(-w*.2),U(w*.34));G.add(boca);G.userData.boca=boca;
 for(const x of[-1,1]){const o=C.bola(w*.09,'#ffb3c7');o.position.set(U(x*w*.36),U(-w*.06),U(w*.3));G.add(o)}return G};
C.libro=(w,c='#ff6b6b')=>{const G=C.grupo();G.add(C.caja(w,w*1.3,w*.5,c,w*.07));
 const p=C.caja(w*.9,w*1.2,w*.44,'#fff8ef',w*.04);p.position.set(U(w*.08),0,0);G.add(p);
 const l=C.caja(w*.5,w*.1,w*.06,'#fff09a',w*.03);l.position.set(U(-w*.05),U(w*.3),U(w*.26));G.add(l);return G};
C.servidor=(w)=>{const G=C.grupo(),L=[];for(let i=0;i<3;i++){const s=C.caja(w,w*.34,w*.8,'#5a5375',w*.1);s.position.y=U((i-1)*w*.38);G.add(s);
  for(let j=0;j<3;j++){const m=C.barro('#4cc38a',{emissive:'#4cc38a',emissiveIntensity:.2});const l=new THREE.Mesh(new THREE.SphereGeometry(U(w*.045),20,14),m);
   l.position.set(U(-w*.33+j*w*.12),U((i-1)*w*.38),U(w*.41));G.add(l);L.push(l)}}G.userData.leds=L;return G};
C.conito=(h,c='#ff9f43')=>{const G=C.grupo();const k=C.cono(h*.36,h,c);G.add(k);const b=C.dona(h*.22,h*.07,'#fff8ef');b.rotation.x=Math.PI/2;b.position.y=U(h*.02);G.add(b);
 const s=C.caja(h*.9,h*.12,h*.9,c,h*.04);s.position.y=U(-h*.52);G.add(s);return G};
C.disquete=(w)=>{const G=C.grupo();G.add(C.caja(w,w,w*.14,'#5b8cff',w*.1));const s=C.caja(w*.5,w*.34,w*.05,'#d9d6e0',w*.03);s.position.set(U(w*.06),U(w*.3),U(w*.08));G.add(s);
 const l=C.caja(w*.72,w*.42,w*.05,'#fff8ef',w*.04);l.position.set(0,U(-w*.2),U(w*.08));G.add(l);return G};
C.palomita=(s,c='#4cc38a')=>{const G=C.grupo();const a=C.capsula(s*.09,s*.34,c);a.rotation.z=Math.PI/4;a.position.set(U(-s*.22),U(-s*.08),0);G.add(a);
 const b=C.capsula(s*.09,s*.7,c);b.rotation.z=-Math.PI/5;b.position.set(U(s*.14),U(s*.12),0);G.add(b);return G};
C.chipt=(s,c='#3b3340')=>{const G=C.grupo();G.add(C.caja(s,s,s*.22,c,s*.12));const n=C.caja(s*.5,s*.5,s*.1,'#ffd36b',s*.08);n.position.z=U(s*.13);G.add(n);
 for(const sd of[-1,1])for(let i=0;i<3;i++){const p=C.capsula(s*.04,s*.12,'#d9d6e0');p.rotation.z=Math.PI/2;p.position.set(U(sd*s*.6),U((i-1)*s*.28),0);G.add(p)}return G};
C.cable=(pts,c,r=11)=>{const cu=new THREE.CatmullRomCurve3(pts.map(([x,y])=>new THREE.Vector3((x-540)/PX,(960-y)/PX,1)));
 return C.sombra(new THREE.Mesh(new THREE.TubeGeometry(cu,80,U(r),14),C.barro(c)))};
// decoración de tecnología en el borde de abajo: chip con cable (fijo, con temblor)
C.deco=(c1,c2)=>{const ch=C.chipt(120);scene.add(ch);const cb=C.cable([[-40,1840],[200,1760],[380,1830],[470,1775]],c1);scene.add(cb);
 const cb2=C.cable([[610,1775],[760,1840],[1120,1790]],c2,9);scene.add(cb2);
 return t=>{ch.rotation.set(.35,-.3,0);C.pon(ch,540,1775,1.2,t,90)}};
"""

DECO_TXT = lambda A, t, c1, c2: (letras(['{ }'], A, t, top=1690, size=120, color=c1) + letras(['&lt;/&gt;'], A, t + .15, top=1700, size=100, color=c2, align='right'))


def escena(pid, start, end, body, js3d, fondo='crema', ac=RJ, sigue=True, entra=(540, 1300), deco=(AZ, RJ)):
    if sigue:
        end += P.COLA
    A = P.at(start)
    js = LIB3 + f"const _deco=C.deco('{deco[0]}','{deco[1]}');const _u=(()=>{{{js3d}}})();return t=>{{_deco(t);_u(t)}};"
    PIEZAS.append((pid, start, end, P.page(CSS, body + DECO_TXT(A, start + .5, deco[0], deco[1]), round(end - start, 2), S0=start, fondo=fondo, entra=entra, ac=ac, js3d=js)))


CSS = '.pz .mono{font-size:34px}.pz .big{font-size:52px;font-weight:700;line-height:1.05}'


def fz(html, A, entra, sale=None):
    """Fase DOM: aparece de golpe en `entra`; sus letras/bloques salen solos en `sale` y el contenedor se apaga 0.5 s después."""
    return ap(html, A, entra, None if sale is None else sale + .5)


def mono(txt):
    return f'<div class="mono">{txt}</div>'


# ───────────────────────── 0:00 · gancho: tu IA contesta sin conocer tus datos → se lo inventa → 3 pasos
S = 0.0; A = P.at(S)
escena('s0-gancho', S, 4.6,
       letras(['Tu IA contesta', '*sin* tus datos'], A, .15, top=TOP, size=112)
       + bloque(80, 1180, 600, mono('› ¿qué dice <b>mi contrato</b>?') + mono('🤖 probablemente…'), A, .3)
       + bloque(700, 1120, 300, '<div class="big">¿tus docs?</div>', A, 1.2, color=C['limon'], extra='transform-origin:center')
       + bloque(700, 1290, 300, '<div class="big">¿tus notas?</div>', A, 1.5, color=C['cielo'])
       + bloque(80, 1400, 600, '<div class="big">🙈 inventado</div>', A, 1.9, color=C['rosa'])
       + bloque(80, 1540, 560, '<div class="tt">→ arreglo en <b>3 pasos</b></div>', A, 2.55, color=C['menta']),
       r"""const rb=C.robot(300);scene.add(rb);const q=[0,1,2].map(i=>{const b=C.bola(26-i*5,'#ff6b6b');scene.add(b);return b});
return t=>{C.brota(rb,t,.3,.7);const n=t>1.1&&t<1.9?Math.sin(t*18)*.25:0;rb.rotation.set(.15,-.35+n,.05*Math.sin(t*3));C.pon(rb,540,820,2,t,1);
 q.forEach((b,i)=>{C.brota(b,t,1.2+i*.15,.4);C.pon(b,720+i*55,640-i*70,3,t,2+i)})}""", fondo='crema', ac=MO)

# ───────────────────────── 0:04 · RAG: que conteste con tus datos | en vez de todo, busca solo lo que sirve
S = 4.6; A = P.at(S)
f1 = (numero('RAG', 70, TOP, 330, A, 4.8, color=AZ)
      + bloque(80, 660, 920, '<div class="big"><b style="color:#5b8cff">R</b>etrieval-<b style="color:#ff6b6b">A</b>ugmented <b style="color:#4cc38a">G</b>eneration</div>'
               + chip('RAG = buscar → contestar', A, 5.9, C['limon']), A, 5.0, sale=10.9)
      + letras(['Contesta con', '*tus* *datos*'], A, 8.86, top=1000, size=120, sale=10.9)
      + bloque(80, 1340, 560, '<div class="big">✓ no se lo imagina</div>', A, 10.5, color=C['menta'], sale=10.9))
f2 = (letras(['En vez de', 'pasarle *todo*…'], A, 11.1, top=TOP, size=120, sale=14.15)
      + letras(['*Busca*', 'primero'], A, 14.3, top=TOP, size=130, sale=19.8)
      + letras(['Solo lo que', '*sirve*'], A, 19.9, top=TOP, size=130)
      + bloque(80, 1180, 470, '<div class="tt">todos tus docs</div>' + chip('✕ todos', A, 12.9, C['rosa']), A, 11.6)
      + bloque(80, 1400, 920, mono('$ rag search <b>"tu pregunta"</b>') + chip('contexto: 3 pedazos · nada más', A, 19.9, C['cielo']), A, 14.3))
escena('s1-rag', S, 21.85, fz(f1, A, S, 10.9) + fz(f2, A, 11.0),
       r"""const H=[0,1,2,3,4].map(i=>{const h=C.hojita(230,290,'#fff8ef');scene.add(h);return h});
const lp=C.lupa(95);scene.add(lp);const PZ=['#5b8cff','#ff6b6b','#4cc38a'].map(c=>{const p=C.pedacito(80,c);scene.add(p);return p});
return t=>{H.forEach((h,i)=>{C.brota(h,t,11.3+i*.08,.5);C.aplasta(h,t,19.85+i*.03,.4);h.rotation.set(.2,.35,(i-2)*.08);C.pon(h,300+i*14,880-i*40,1.5+i*.4,t,10+i)});
 const g=C.k(t,14.5,5);const lx=t<19.9?560+260*Math.sin(g*Math.PI*2.2):790,ly=t<19.9?820+120*Math.cos(g*Math.PI*3):770;
 C.cae(lp,t,14.4,600);C.aplasta(lp,t,21.2,.4);lp.rotation.set(.3,-.3,.2*Math.sin(t*2));C.pon(lp,lx,ly,4,t,20);
 PZ.forEach((p,i)=>{C.brota(p,t,19.95+i*.14,.5);const j=C.k(t,20.4+i*.12,.5);p.userData.dy=U(140)*Math.sin(Math.PI*j);
  p.rotation.set(.4,.6+t*.8,.2);C.pon(p,330+i*130,1000,3,t,30+i)})}""", fondo='cielo', ac=AZ, deco=(MO, NA))

# ───────────────────────── 0:21 · 3 pasos: prepara (pedazos con significado) → busca (los que más se parecen) → contesta solo con eso
S = 21.85; A = P.at(S)
f1 = (letras(['Paso 1', '*prepara*'], A, 21.95, top=TOP, size=140, sale=34.2)
      + bloque(80, 1150, 920, '<div class="big">✂ pedazos pequeños</div>' + chip('conserva su significado', A, 29.14, C['limon']), A, 26.47, sale=34.2)
      + bloque(80, 1380, 920, mono('buscar «cancelar plan» ≈ «dar de baja»') + chip('✓ por idea', A, 31.42, C['menta']) + chip('✕ palabra exacta', A, 32.94, C['rosa']),
               A, 29.95, sale=34.2))
f2 = (letras(['Paso 2', '*busca*'], A, 34.3, top=TOP, size=140, sale=39.2)
      + bloque(80, 560, 430, '<div class="big">¿cómo cancelo mi plan?</div>', A, 34.5, color=C['limon'], sale=39.2)
      + bloque(80, 1280, 920, '<div class="big">los que más se parecen</div>' + chip('$ rag search → top 3', A, 38.31, C['cielo']), A, 38.2, sale=39.2))
f3 = (letras(['Paso 3', '*contesta*'], A, 39.3, top=TOP, size=140)
      + bloque(80, 560, 430, '<div class="big">¿cómo cancelo mi plan?</div>', A, 39.4, color=C['limon'])
      + bloque(80, 1180, 920, '<div class="tt">pregunta + pedazos</div>' + chip('› contesta usando solo eso ✓', A, 43.65, C['menta']), A, 42.43)
      + bloque(80, 1400, 650, '<div class="big">«Ve a Ajustes › Plan y toca <b>Dar de baja</b>.»</div>', A, 44.2, color=C['cielo'])
      + bloque(760, 1420, 250, '<div class="big">solo eso</div>', A, 45.76, color=C['rosa']))
escena('s2-pasos', S, 47.0, fz(f1, A, S, 34.2) + fz(f2, A, 34.26, 39.2) + fz(f3, A, 39.28),
       r"""const doc=C.hojita(300,380,'#fff8ef');scene.add(doc);
const COL=['#5b8cff','#ff6b6b','#4cc38a','#ffd36b','#9b6bff','#ff9f43'];
const P4=[0,1,2,3].map(i=>{const p=C.pedacito(120,COL[i]);scene.add(p);return p});
const P6=[0,1,2,3,4,5].map(i=>{const p=C.pedacito(110,COL[i]);scene.add(p);return p});const lp=C.lupa(85);scene.add(lp);
const rb=C.robot(260);scene.add(rb);const P3=[0,1,2].map(i=>{const p=C.pedacito(90,COL[i]);scene.add(p);return p});
const HIT=[0,2,4];
return t=>{
 // paso 1: la hoja se parte en 4 pedacitos
 C.brota(doc,t,22.2,.6);C.aplasta(doc,t,26.35,.3);doc.rotation.set(.2,.3,-.06);C.pon(doc,540,800,2,t,1);
 P4.forEach((p,i)=>{C.brota(p,t,26.47+i*.12,.5);C.aplasta(p,t,34.1,.3);const j=C.k(t,29.14,.5);p.userData.dy=U(60)*Math.sin(Math.PI*j);
  p.rotation.set(.35,.5+.2*Math.sin(t+i),.1);C.pon(p,360+(i%2)*360,690+Math.floor(i/2)*230,3,t,2+i)});
 // paso 2: lupa sobre 6 pedacitos; los 3 que coinciden brincan
 P6.forEach((p,i)=>{C.brota(p,t,34.7+i*.07,.45);C.aplasta(p,t,39.1,.3);const hit=HIT.includes(i);const j=hit?C.k(t,37.0+HIT.indexOf(i)*.15,.6):0;
  p.userData.dy=U(hit?(t>37?120:0):0)*(j<1?Math.sin(Math.PI*j*.5):1);p.rotation.set(.35,.4+(hit&&t>37?t*1.5:0),0);
  C.pon(p,620+(i%3)*150,860+Math.floor(i/3)*190,3,t,10+i,hit&&t>37?1.15:1)});
 const g=C.k(t,35.0,2.0);C.cae(lp,t,35.0,500);C.aplasta(lp,t,39.1,.3);lp.rotation.set(.3,-.3,.15*Math.sin(t*3));
 C.pon(lp,t<37?620+300*g:770,t<37?790+40*Math.sin(t*4):760,5,t,20);
 // paso 3: el robot se come los 3 pedazos
 C.brota(rb,t,39.5,.6);rb.rotation.set(.15,-.3+.1*Math.sin(t*2),0);rb.userData.boca.scale.y=t>42.4&&t<43.4?1+5*Math.abs(Math.sin((t-42.4)*9)):1;C.pon(rb,800,880,2,t,30);
 P3.forEach((p,i)=>{C.cae(p,t,39.7+i*.1,400);const m=C.eio(C.k(t,42.43+i*.12,.5));C.aplasta(p,t,42.9+i*.12,.15);
  p.rotation.set(.4,.5+t,0);C.pon(p,330+i*120+(800-330-i*120)*m,880-60*Math.sin(Math.PI*m),3+m,t,40+i,1-.5*m)})}""",
       fondo='menta', ac=VD, deco=(AZ, MO))

# ───────────────────────── 0:47 · libro entero vs la página que ocupa
S = 47.0; A = P.at(S)
f1 = (letras(['¿Le das *todo*', 'el contexto?'], A, 47.1, top=TOP, size=120, sale=54.85)
      + bloque(80, 1180, 560, '<div class="big">📕 libro entero</div><div class="tt">' + N([(0, 1), (48.8, 412, 1.4)]) + ' páginas</div>', A, 47.6, sale=54.85)
      + bloque(80, 1440, 560, '<div class="big">…y que encuentre la página</div>', A, 52.28, color=C['rosa'], sale=54.85))
f2 = (letras(['Con RAG:', 'solo *esa* *página*'], A, 54.9, top=TOP, size=120)
      + bloque(80, 1180, 920, '<div class="tt">pág. 217</div><div class="big">Cancela en <b style="color:#ff6b6b">Ajustes › Plan</b></div>', A, 55.3)
      + bloque(80, 1420, 380, '<div class="big">tu pregunta</div>', A, 59.36, color=C['limon']))
escena('s3-libro', S, 60.3, fz(f1, A, S, 54.85) + fz(f2, A, 54.9),
       r"""const lb=C.libro(300,'#ff6b6b');scene.add(lb);const lp=C.lupa(80);scene.add(lp);const hj=C.hojita(300,380,'#fff8ef',['#ffd36b','#ff6b6b','#5b8cff']);scene.add(hj);
return t=>{C.cae(lb,t,47.3,700);C.aplasta(lb,t,54.8,.35);lb.rotation.set(.25,.55+.08*Math.sin(t),0);C.pon(lb,400,820,2,t,1);
 C.brota(lp,t,52.2,.5);C.aplasta(lp,t,54.8,.3);lp.rotation.set(.3,-.3,.3*Math.sin(t*2));C.pon(lp,760+60*Math.sin(t*2.5),780+50*Math.cos(t*2),5,t,2);
 C.brota(hj,t,55.1,.6);const f=t>56.69?1:0;hj.rotation.set(.15,.2*Math.sin(t*1.2),-.05);hj.userData.dy=U(30)*Math.sin(t*2)*f;C.pon(hj,540,780,2.5,t,3,1+.08*f)}""",
       fondo='limon', ac=RJ, deco=(RJ, AZ))

# ───────────────────────── 1:00 · mi ejemplo: el homelab recaba redes y proyectos → Claude contesta solo con eso (medio RAG)
S = 60.3; A = P.at(S)
f1 = (letras(['Mi *homelab*'], A, 60.4, top=TOP, size=150, sale=68.0)
      + bloque(620, 470, 380, '<div class="big">medio RAG</div>', A, 63.79, color=C['limon'], sale=68.0)
      + numero(N([(0, 0), (64.6, 1284, 3.0)], f='c'), 560, 640, 170, A, 63.9, color=MO)
      + bloque(560, 830, 440, '<div class="tt">registros recabados</div>', A, 64.6, sale=68.0)
      + bloque(80, 1240, 440, '<div class="big">📣 redes sociales</div>', A, 66.77, color=C['rosa'], sale=68.0)
      + bloque(560, 1240, 440, '<div class="big">📁 proyectos</div>', A, 67.51, color=C['limon'], sale=68.0))
f2 = (letras(['Claude contesta', 'solo con *eso*'], A, 68.1, top=TOP, size=112)
      + bloque(80, 600, 920, mono('› claude: <b>¿cómo van mis redes?</b>') + chip('contexto = datos guardados · nada más', A, 70.45, C['cielo']), A, 68.05)
      + bloque(80, 1200, 560, '<div class="big">Lo que se guardó en el homelab, <b>y nada más</b>.</div>', A, 70.6, color=C['menta'])
      + bloque(80, 1460, 500, '<div class="big">solo esos datos</div>', A, 72.46, color=C['rosa']))
escena('s4-ejemplo', S, 77.3, fz(f1, A, S, 68.0) + fz(f2, A, 68.05),
       r"""const sv=C.servidor(260);scene.add(sv);const L=sv.userData.leds;const B=['#ff6b6b','#ffd36b','#5b8cff','#4cc38a'].map(c=>{const b=C.bola(34,c);scene.add(b);return b});
const cl=C.logo(""" + json.dumps(G.svgpath('claude')) + r""",250,'#e98a68',50);scene.add(cl);
return t=>{C.brota(sv,t,60.8,.6);C.aplasta(sv,t,67.95,.35);sv.rotation.set(.2,.45,0);C.pon(sv,300,880,2,t,1);
 L.forEach((l,i)=>{l.material.emissiveIntensity=t>64.5&&Math.sin(t*9+i*1.7)>0?1.1:.15});
 B.forEach((b,i)=>{const t0=[66.8,67.0,67.5,67.7][i];const m=C.eio(C.k(t,t0,.5));b.visible=t>=t0&&m<1;const sx=i<2?280:780,sy=1200;
  C.pon(b,sx+(300-sx)*m,sy+(880-sy)*m-160*Math.sin(Math.PI*m),4,t,10+i)});
 C.brota(cl,t,70.11,.6);cl.rotation.set(.2,.3*Math.sin(t*1.3),t*.4);C.pon(cl,820,1030,3,t,20)}""",
       fondo='lila', ac=MO, deco=(MO, VD))

# ───────────────────────── 1:17 · > ⚠️ Ojo: mal cortado · desactualizado · búsqueda equivocada → revisa qué encontró
S = 77.3; A = P.at(S)
CAB = letras(['&gt; ⚠️ *Ojo*'], A, 77.4, top=TOP, size=120) + bloque(80, 450, 400, '<div class="tt">tres cuidados</div>', A, 77.9, color=C['limon'], sale=96.35)
c1 = (bloque(80, 600, 260, '<div class="big" style="white-space:nowrap">⚠ 1/3</div>', A, 79.5, color=C['durazno'], sale=83.9)
      + letras(['Pedazos mal', '*cortados*'], A, 79.6, top=740, size=120, sale=83.9)
      + bloque(80, 1120, 460, '<div class="big">«El plan cuesta…</div>', A, 80.52, sale=83.9)
      + bloque(580, 1180, 420, '<div class="big" style="opacity:.6">…$99 al mes»</div>', A, 80.7, sale=83.9)
      + bloque(80, 1400, 360, '<div class="big">✂ a medias</div>', A, 83.51, color=C['rosa'], sale=83.9))
c2 = (bloque(80, 600, 260, '<div class="big" style="white-space:nowrap">⚠ 2/3</div>', A, 83.94, color=C['durazno'], sale=90.67)
      + letras(['Datos', '*desactualizados*'], A, 84.0, top=740, size=104, sale=90.67)
      + bloque(80, 1100, 400, '<div class="big">precio 2024:<br>$79</div>', A, 85.13, color=C['limon'], sale=90.67)
      + numero('≠', 500, 1110, 150, A, 85.4, color=RJ)
      + bloque(620, 1100, 380, '<div class="big">hoy:<br>$99</div>', A, 85.6, color=C['menta'], sale=90.67)
      + bloque(80, 1420, 520, '<div class="big">ya no es cierto</div>', A, 89.62, color=C['rosa'], sale=90.67))
c3 = (bloque(80, 600, 260, '<div class="big" style="white-space:nowrap">⚠ 3/3</div>', A, 90.72, color=C['durazno'], sale=96.35)
      + letras(['Búsqueda', '*equivocada*'], A, 90.8, top=740, size=120, sale=96.35)
      + bloque(80, 1120, 920, mono('busca «baja» → trae «bajar precio»'), A, 91.0, sale=96.35)
      + bloque(80, 1360, 560, '<div class="big">trae lo que no es</div>', A, 92.34, color=C['rosa'], sale=96.35))
c4 = (letras(['*Revisa* qué', 'encontró'], A, 96.45, top=600, size=130)
      + bloque(80, 1000, 920, mono('$ rag search <b>--show-sources</b>') + chip('✓ pedazo 017 · pedazo 031', A, 97.61, C['menta']), A, 96.5))
escena('s5-ojo', S, 99.4, CAB + fz(c1, A, 79.5, 83.9) + fz(c2, A, 83.94, 90.67) + fz(c3, A, 90.72, 96.35) + fz(c4, A, 96.4),
       r"""const K=[0,1,2].map(i=>{const k=C.conito(150);scene.add(k);return k});const lp=C.lupa(90);scene.add(lp);const ok=C.palomita(240);scene.add(ok);
return t=>{K.forEach((k,i)=>{const t0=[79.5,83.94,90.72][i];C.cae(k,t,t0,600);C.aplasta(k,t,96.3,.35);k.rotation.set(.15,.4*Math.sin(t+i),0);
  const w=t>t0+.6&&t<t0+1.4?Math.sin(t*20)*.12:0;k.rotation.z=w;C.pon(k,640+i*150,520,2.5,t,1+i)});
 C.brota(lp,t,96.5,.5);lp.rotation.set(.3,-.3,.2*Math.sin(t*2));C.pon(lp,760+40*Math.sin(t*3),1400,4,t,10);
 C.brota(ok,t,97.61,.6);ok.rotation.set(.2,.3*Math.sin(t),0);C.pon(ok,380,1430,3,t,11)}""",
       fondo='rosa', ac=RJ, deco=(NA, AZ))

# ───────────────────────── 1:39 · ¿y el contexto largo? pocos docs: pásalos todos · miles: tokens, tiempo, se pierde a la mitad
S = 99.4; A = P.at(S)
f1 = (letras(['«Ya aguantan', 'mucho *contexto*»'], A, 99.6, top=TOP, size=112, sale=108.2)
      + bloque(640, 540, 360, '<div class="big">es cierto ✓</div>', A, 102.0, color=C['menta'], sale=108.2)
      + letras(['¿Pocos docs?'], A, 104.96, top=720, size=110, sale=108.2)
      + bloque(80, 1360, 560, '<div class="big">pásale todos ✓</div>', A, 107.34, color=C['cielo'], sale=108.2))
f2 = (letras(['¿Y con', '*miles*?'], A, 108.3, top=TOP, size=130)
      + numero(N([(0, 5), (108.3, 3000, 1.2)], f='c'), 80, 600, 170, A, 108.3, color=AZ)
      + numero(N([(0, 4), (109.7, 96, 1.4)], suf='%'), 600, 600, 170, A, 109.7, color=RJ)
      + bloque(80, 780, 920, '<div class="tt">documentos · del límite</div>' + chip('+ tokens', A, 110.87, C['rosa']) + chip('+ tiempo', A, 112.29, C['durazno']), A, 109.12)
      + bloque(560, 1460, 440, '<div class="big">se pierde a la mitad 😵‍💫</div>', A, 114.23, color=C['lila']))
escena('s6-contexto', S, 115.5, fz(f1, A, S, 108.2) + fz(f2, A, 108.26),
       r"""const F=[0,1,2,3].map(i=>{const h=C.hojita(170,220);scene.add(h);return h});
const M=[...Array(14)].map((_,i)=>{const h=C.hojita(150,190,['#fff8ef','#fff09a','#cfeaff','#ffd0dc'][i%4]);scene.add(h);return h});const rb=C.robot(220);scene.add(rb);
return t=>{F.forEach((h,i)=>{C.brota(h,t,105.1+i*.1,.5);C.aplasta(h,t,108.15,.3);h.rotation.set(.2,.3,[-.1,.06,-.04,.08][i]);C.pon(h,180+i*240,1030,2,t,1+i)});
 M.forEach((h,i)=>{const t0=108.3+i*.12;C.cae(h,t,t0,500,.45);const r=Math.floor(i/4),c=i%4;
  h.rotation.set(.25,.4,(C.h(i)-.5)*.6+(t>114.2?.15*Math.sin(t*6+i):0));C.pon(h,180+c*70+r*20,1360-r*70-c*12,1.5+i*.25,t,10+i)});
 C.brota(rb,t,110.5,.6);const mar=t>114.23?C.k(t,114.23,.4):0;rb.rotation.set(.15+.12*mar*Math.sin(t*5),-.3+.6*mar*Math.sin(t*4),.25*mar*Math.sin(t*7));C.pon(rb,800,1220,2,t,30)}""",
       fondo='cielo', ac=AZ, deco=(VD, MO))

# ───────────────────────── 1:55 · funciona hoy → si tus datos ya no caben, ponlo a buscar antes de contestar
S = 115.5; A = P.at(S)
f1 = (letras(['Funciona', '*hoy*'], A, 115.6, top=TOP, size=160, sale=119.75)
      + bloque(80, 760, 920, '<div class="big">Con los modelos que tenemos <b>en 2026</b>.</div>', A, 116.3, color=C['limon'], sale=119.75))
f2 = (letras(['¿Ya no', '*caben*?'], A, 119.9, top=TOP, size=140)
      + bloque(620, 330, 380, '<div class="big">no caben</div>', A, 121.25, color=C['rosa'])
      + bloque(80, 650, 920, mono('si <b>datos &gt; chat</b> →') + chip('1. busca · 2. contesta', A, 122.0, C['limon']), A, 119.9)
      + bloque(80, 1380, 400, '<div class="big">busca primero</div>', A, 122.93, color=C['cielo'])
      + bloque(560, 1380, 440, '<div class="big">luego contesta</div>', A, 123.72, color=C['menta']))
escena('s7-hoy', S, 124.7, fz(f1, A, S, 119.75) + fz(f2, A, 119.82),
       r"""const ok=C.palomita(200);scene.add(ok);const lp=C.lupa(100);scene.add(lp);const rb=C.robot(240);scene.add(rb);
const fl=C.capsula(16,170,'#ff9f43');scene.add(fl);const pu=C.cono(36,60,'#ff9f43');scene.add(pu);
return t=>{C.brota(ok,t,117.92,.6);C.aplasta(ok,t,119.7,.3);ok.rotation.set(.2,.3*Math.sin(t),0);C.pon(ok,500,610,3,t,1);
 C.brota(lp,t,122.93,.5);lp.rotation.set(.3,-.3,.2*Math.sin(t*2));C.pon(lp,280,1130,4,t,2);
 C.brota(fl,t,123.4,.4);fl.rotation.set(0,0,Math.PI/2);C.pon(fl,540,1140,3,t,3);C.brota(pu,t,123.4,.4);pu.rotation.set(0,0,-Math.PI/2);C.pon(pu,640,1140,3,t,4);
 C.brota(rb,t,123.72,.6);rb.rotation.set(.15,-.4+.1*Math.sin(t*2),0);C.pon(rb,820,1130,2,t,5)}""",
       fondo='menta', ac=VD, deco=(AZ, NA))

# ───────────────────────── 2:04 · resumen para guardar + pregunta
S = 124.7; A = P.at(S)
LISTA = ''.join(bloque(80, 720 + i * 170, 920, f'<div class="big"><span style="color:{c}">{n}</span>&nbsp; {t}</div>', A, t0, color=bg)
                for i, (n, t, t0, c, bg) in enumerate([('1', 'Prepara', 125.1, AZ, C['blanco']), ('2', 'Busca', 125.35, RJ, C['blanco']),
                                                       ('3', 'Contesta', 125.6, VD, C['blanco']), ('&gt;', '⚠️ Revisa', 126.0, NA, C['durazno'])]))
escena('s8-pregunta', S, 128.75,
       letras(['¿Le pasas *todo*', 'a tu IA o la pones', 'a *buscar* primero?'], A, 124.9, top=TOP, size=92)
       + LISTA + bloque(600, 1420, 400, '<div class="big">cuéntame 👇</div>', A, 126.4, color=C['rosa']),
       r"""const P3=['#5b8cff','#ff6b6b','#4cc38a'].map(c=>{const p=C.pedacito(70,c);scene.add(p);return p});
return t=>{P3.forEach((p,i)=>{C.brota(p,t,125.1+i*.25,.45);const j=C.k(t,126.6+i*.15,.6);p.userData.dy=U(70)*Math.sin(Math.PI*j);p.rotation.set(.4,.5+t,0);C.pon(p,180+i*120,1520,3,t,1+i)})}""",
       fondo='limon', ac=MO, deco=(RJ, VD))

# ───────────────────────── 2:08 · cierre: «nos vemos cuando toque actualizar este README»
S = 128.75; A = P.at(S)
escena('s9-cierre', S, FIN,
       letras(['Nos vemos cuando', 'toque *actualizar*', 'este README'], A, 128.8, top=TOP, size=100)
       + bloque(80, 700, 560, mono('⌘S <b>README.md</b>'), A, 129.0)
       + bloque(80, 900, 460, '<div class="big">✓ guardado</div>', A, 130.0, color=C['menta']),
       r"""const dq=C.disquete(320);scene.add(dq);const ok=C.palomita(160);scene.add(ok);
return t=>{C.cae(dq,t,129.3,700);dq.rotation.set(.25,-.35+.1*Math.sin(t*1.5),.05);C.pon(dq,620,1230,2,t,1);
 C.brota(ok,t,130.0,.5);ok.rotation.set(.2,.3*Math.sin(t),0);C.pon(ok,880,1050,4,t,2)}""",
       sigue=False, fondo='crema', ac=AZ, deco=(VD, RJ))

# ───────────────────────── banda de plastilina arriba (todo el video, transparente): README.md · #02 RAG + sección actual
SECC = [(0.0, '# RAG'), (4.6, '## ¿Qué es?'), (21.85, '## Paso 1 · Prepara'), (34.2, '## Paso 2 · Busca'), (39.25, '## Paso 3 · Contesta'),
        (47.0, '## Libro vs página'), (60.3, '## Mi ejemplo'), (77.3, '&gt; ⚠️ Ojo'), (99.4, '## ¿Y el contexto largo?'), (115.5, '## Funciona hoy'),
        (124.7, '## Tu turno'), (128.75, '✓ guardado')]
A = P.at(0)
SEC = ''.join(ap(f'<span class="sc">{n}</span>', A, t, SECC[i + 1][0] if i + 1 < len(SECC) else None) for i, (t, n) in enumerate(SECC))
ETQ_CSS = """
.ban{position:absolute;left:28px;right:28px;top:22px;height:118px;z-index:90;border-radius:44px;background:#c9b6ff;
  box-shadow:inset 0 -12px 0 rgba(0,0,0,.1),inset 0 10px 16px rgba(255,255,255,.5),0 14px 0 rgba(0,0,0,.12),0 24px 30px rgba(60,30,30,.22);
  animation:pzin .6s steps(7) both,tiembla .5s steps(1) infinite}
.ban .rd{position:absolute;left:40px;top:18px;font-weight:700;font-size:40px;color:#3b3340}
.ban .rd i{font-style:normal;color:#fff8ef;text-shadow:0 3px 0 rgba(0,0,0,.18)}
.ban .sc{position:absolute;left:40px;top:64px;font-family:Nunito;font-weight:900;font-size:38px;color:#5a3fb8;white-space:nowrap}
.ban .nr{position:absolute;right:28px;top:20px;width:150px;height:78px;border-radius:40px;background:#ff6b6b;color:#fff8ef;font-weight:700;font-size:46px;
  display:flex;align-items:center;justify-content:center;box-shadow:inset 0 -8px 0 rgba(0,0,0,.12),0 8px 0 rgba(0,0,0,.1)}
"""
ETQ = f'<div class="ban"><div class="rd">README.md <i>· #02 RAG</i></div>{SEC}<div class="nr">#02</div></div>'
PIEZAS.append(('etiqueta', 0.0, FIN, P.page(ETQ_CSS, ETQ, FIN, S0=0.0, transparente=True)))
PRE = 'rmp2-'

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
        rel = os.environ.get('REL', 'readme/2/plastilina')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
