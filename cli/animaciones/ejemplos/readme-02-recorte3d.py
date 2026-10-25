"""El Readme #02 · RAG — edición «Recorte 3D»: la misma de readme-02-recorte.py (cuaderno de ingeniería sobre papel cuadriculado)
más objetos 3D de papel y cartón (capa js3d de recorte.py): pila de documentos, pedazos con texto, lupa de cartón que escanea,
libro de cartón con contador en la portada y página que se arranca, servidor de cartón del homelab, bola de papel arrugado,
montón de hojas que crece y avión de papel de despedida. Sombras reales sobre la hoja.
El RAG se explica con un diagrama hecho a mano que se va armando (documentos → pedazos → búsqueda → pregunta+pedazos → respuesta),
con tickets de terminal, recortes, notas, sellos y marcatextos; acento azul. Arriba, en lugar de la pestaña, una etiqueta de cinta
con «README.md · #02 RAG» y la sección actual. Todo se mueve a 12 cps y cada hoja entra rasgada sobre la anterior.
Tiempos = readme/2/voz/voz-norm.wav (132.34 s), los mismos de readme-02.py.
Uso: SALIDA=~/Documents/Videos/readme/2/recorte3d REL=readme/2/recorte3d python3 ejemplos/readme-02-recorte3d.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import recorte as K
from recorte import titular, tacha, subraya, circulo, flecha, recorte, nota, sello, ticket, numero, N, logo, mano, fase, palomita, marca

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/readme/2/recorte3d')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 132.34
TOP = 300          # primer renglón útil (debajo de la etiqueta)
PIEZAS = []
AZ, RJ, VD = 'var(--azul)', 'var(--rojo)', 'var(--verde)'


def escena(pid, start, end, body, css='', sigue=True, seed=1, js3d=None):
    if sigue:
        end += K.COLA
    PIEZAS.append((pid, start, end, K.page(CSS + css, body, round(end - start, 2), S0=start, fondo='cuad', seed=seed, ac=AZ,
                                           js3d=(LIB3 + js3d) if js3d else None)))


# ───────── figuras de papel propias (se arman con P.papel / P.sombra de recorte.py)
LIB3 = r"""
await document.fonts.load('700 40px "JetBrains Mono"');await document.fonts.load('900 100px Archivo');
const V3=THREE.Vector3;
// lienzo con fibra de papel para texturas con texto
const lienzo=(w,h,col)=>{const c=document.createElement('canvas');c.width=Math.round(w*2);c.height=Math.round(h*2);const g=c.getContext('2d');
 g.fillStyle=col;g.fillRect(0,0,c.width,c.height);g.globalAlpha=.45;g.drawImage(P.TEX.image,0,0,c.width,c.height);g.globalAlpha=1;return [c,g]};
const textura=c=>{const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t};
// hoja con etiqueta mono y renglones (w,h px); curva leve
const hojaTxt=(w,h,label='',col='#fbf8f1',acc='#2457e6')=>{const [c,g]=lienzo(w,h,col);const k=2;
 g.fillStyle=acc;g.font=`700 ${Math.round(Math.min(h*.12,w*.11)*k)}px "JetBrains Mono"`;g.fillText(label,w*.1*k,h*.2*k);
 g.fillStyle='#d5cfc1';for(let i=0;i<5;i++){const y=(h*.32+i*h*.13);if(y>h*.9)break;g.fillRect(w*.1*k,y*k,w*(.8-.18*(i%2))*k,h*.055*k)}
 const geo=new THREE.PlaneGeometry(w/P.PX,h/P.PX,8,2);const p=geo.attributes.position;
 for(let i=0;i<p.count;i++){const x=p.getX(i)/(w/P.PX);p.setZ(i,Math.sin((x+.5)*Math.PI)*w/P.PX*.025)}geo.computeVertexNormals();
 return P.sombra(new THREE.Mesh(geo,new THREE.MeshStandardMaterial({map:textura(c),roughness:.95,side:THREE.DoubleSide})))};
// pila de hojas apiladas en z (n hojas de w×h px)
const pila=(n,w,h,label='doc',col='#fbf8f1')=>{const G=new THREE.Group(),H=[];
 for(let i=0;i<n;i++){const s=hojaTxt(w,h,`${label}_${i+1}.md`,col);s.position.z=i*.06;s.rotation.z=(P.h(i+3)-.5)*.25;G.add(s);H.push(s)}G.userData.H=H;return G};
// lupa de cartón (r = radio del aro en px)
const lupa=(r,col='#2457e6')=>{const G=new THREE.Group();
 G.add(new THREE.Mesh(new THREE.TorusGeometry(r/P.PX,r*.17/P.PX,14,48),P.papel(col)));
 const vid=new THREE.Mesh(new THREE.CircleGeometry(r/P.PX,40),new THREE.MeshStandardMaterial({color:'#cfe4ff',transparent:true,opacity:.28,roughness:.15}));G.add(vid);
 const mg=new THREE.Mesh(new THREE.BoxGeometry(r*.32/P.PX,r*1.25/P.PX,r*.22/P.PX),P.papel('#c9a26b'));mg.position.set(r*1.0/P.PX,-r*1.0/P.PX,0);mg.rotation.z=Math.PI/4;G.add(mg);
 return P.sombra(G)};
// libro de cartón cerrado (w,h,d px) con portada redibujable: libro.userData.portada(n)
const libro=(w,h,d,col='#cfab72')=>{const G=new THREE.Group();const [c,g]=lienzo(w,h,col);const tx=textura(c);
 const dib=n=>{g.fillStyle=col;g.fillRect(0,0,c.width,c.height);g.globalAlpha=.45;g.drawImage(P.TEX.image,0,0,c.width,c.height);g.globalAlpha=1;const k=2;
  g.fillStyle='#2a1c0c';g.fontStretch='extra-condensed';let fs=w*.24*k;g.font=`900 ${Math.round(fs)}px Archivo`;while(g.measureText('ENTERO').width>w*.78*k){fs*=.94;g.font=`900 ${Math.round(fs)}px Archivo`}
  g.fillText('LIBRO',w*.1*k,h*.27*k);g.fillText('ENTERO',w*.1*k,h*.27*k+fs*.92);
  g.fontStretch='normal';g.font=`700 ${Math.round(w*.075*k)}px "JetBrains Mono"`;g.fillText(`${n} páginas`,w*.1*k,h*.62*k);
  g.fillStyle='rgba(42,28,12,.25)';for(let i=0;i<4;i++)g.fillRect(w*.1*k,(h*.7+i*h*.06)*k,w*(.7-.12*(i%2))*k,h*.025*k);tx.needsUpdate=true};
 dib(1);G.userData.portada=dib;
 const tapa=P.papel(col),fr=new THREE.MeshStandardMaterial({map:tx,roughness:.95});
 const pz=d/P.PX;const cov=new THREE.Mesh(new THREE.BoxGeometry(w/P.PX,h/P.PX,pz*.12),[tapa,tapa,tapa,tapa,fr,tapa]);cov.position.z=pz*.44;G.add(cov);
 const bk=new THREE.Mesh(new THREE.BoxGeometry(w/P.PX,h/P.PX,pz*.12),tapa);bk.position.z=-pz*.44;G.add(bk);
 const pg=new THREE.Mesh(new THREE.BoxGeometry(w*.96/P.PX,h*.97/P.PX,pz*.8),P.papel('#f6f1e4'));pg.position.x=w*.02/P.PX;G.add(pg);
 const lomo=new THREE.Mesh(new THREE.BoxGeometry(w*.06/P.PX,h/P.PX,pz),tapa);lomo.position.x=-w*.48/P.PX;G.add(lomo);return P.sombra(G)};
// servidor de cartón: 3 bandejas con leds (userData.leds)
const servidor=(w,col='#3a3632')=>{const G=new THREE.Group(),L=[],hu=w*.3;
 for(let i=0;i<3;i++){const b=new THREE.Mesh(new THREE.BoxGeometry(w/P.PX,hu/P.PX,w*.55/P.PX),P.papel(col));b.position.y=(1-i)*hu*1.12/P.PX;G.add(b);
  const ra=new THREE.Mesh(new THREE.BoxGeometry(w*.42/P.PX,hu*.14/P.PX,.02),P.papel('#5a554e'));ra.position.set(w*.16/P.PX,b.position.y,w*.28/P.PX);G.add(ra);
  for(let j=0;j<3;j++){const l=new THREE.Mesh(new THREE.SphereGeometry(w*.035/P.PX,12,8),new THREE.MeshStandardMaterial({color:'#17a35a',emissive:'#17a35a',emissiveIntensity:1.2}));
   l.position.set((-w*.38+j*w*.1)/P.PX,b.position.y,w*.28/P.PX);G.add(l);L.push(l)}}
 G.userData.leds=L;return P.sombra(G)};
"""


CSS = '.tt .sf{color:var(--azul)}'


def fz(html, A, entra=None, sale=None):
    """fase() con entrada y salida a la vez: en recorte.py .fz.in pisa la animación de .fz.x, así que se anidan."""
    if entra is not None and sale is not None:
        return fase(fase(html, A, sale=sale), A, entra=entra)
    return fase(html, A, entra=entra, sale=sale)


def caja(txt, size=96, extra=''):
    return f'<div style="font-weight:900;font-stretch:62%;font-size:{size}px;line-height:.88;text-transform:uppercase;{extra}">{txt}</div>'


def ser(txt, size=48, extra=''):
    return f'<div class="ser" style="font-size:{size}px;line-height:1.05;{extra}">{txt}</div>'


def renglones(n, ancho=(92, 70, 84, 60, 88, 76), color='#d5cfc1', alto=14, gap=18):
    """Líneas grises de «texto» para hojas y pedazos."""
    return ''.join(f'<div style="height:{alto}px;width:{ancho[i % len(ancho)]}%;background:{color};border-radius:4px;margin-top:{gap}px"></div>' for i in range(n))


def pedazo(x, y, w, h, num, A, t, rot=0.0, seed=40, cls='', sale=None, color='#2457e6'):
    """Recorte pequeño = un «pedazo» de documento, con su número."""
    body = (f'<div class="mono" style="font-size:24px;font-weight:700;color:{color}">pedazo {num}</div>' + renglones(3, alto=11, gap=14))
    return recorte(x, y, w, h, body, A, t, sale=sale, rot=rot, seed=seed, cls=cls, cinta=False, pad='20px 24px')


def hoja_doc(x, y, w, h, titulo, A, t, rot=0.0, seed=50, n=9, sale=None, cls=''):
    body = f'<div class="mono" style="font-size:26px;font-weight:700">{titulo}</div>' + renglones(n)
    return recorte(x, y, w, h, body, A, t, sale=sale, rot=rot, seed=seed, cls=cls, pad='28px 30px')


# ───────────────────────── 0:00 · gancho: tu IA contesta sin conocer tus datos → se lo inventa → 3 pasos
S = 0.0; A = K.at(S)
escena('s0-gancho', S, 4.6,
       titular(['Tu IA contesta', '_sin tus datos_'], A, .15, top=TOP, size=150, seed=1)
       + ticket(80, 650, 920, [('<i>›</i> ¿qué dice <b>mi contrato</b>?', .3, .5), ('<i>🤖</i> probablemente… <i>(no lo leyó)</i>', 1.15, .6),
                               ('<i>arreglo:</i> <b>3 pasos</b>', 2.55, .4)], A, rot=-1.2, size=36)
       + nota(90, 1000, '¿tus docs?', A, 1.2, rot=-5, w=300, size=58)
       + nota(420, 1040, '¿tus notas?', A, 1.5, rot=4, w=300, size=58, color='#cfe0ff')
       + sello(440, 1290, 'Inventado', A, 1.9, size=88, rot=-8)
       + mano(110, 1500, '→ arreglo en 3 pasos', A, 2.6, size=70, color=AZ), seed=1,
       js3d=r"""const bo=P.bola(115,'#f6f1e6',5);scene.add(bo);
return t=>{const a=P.eb(P.k(t,1.9,.5));bo.visible=t>=1.9;bo.scale.setScalar(Math.max(.001,a));P.at(bo,880,1150+6*Math.sin(t*2),2.5);bo.rotation.set(t*.7,t*1.1+(1-a)*3,0)}""")

# ───────────────────────── 0:04 · RAG: que conteste con tus datos | en vez de todo, busca solo lo que sirve
S = 4.6; A = K.at(S)
f1 = (numero(70, TOP, 'RAG', A, 4.8, size=400, color=AZ)
      + recorte(80, 680, 920, 170, ser('<b style="font-family:Archivo;font-style:normal;font-weight:900;font-stretch:62%">R</b>etrieval-'
                                       '<b style="font-family:Archivo;font-style:normal;font-weight:900;font-stretch:62%">A</b>ugmented '
                                       '<b style="font-family:Archivo;font-style:normal;font-weight:900;font-stretch:62%">G</b>eneration', 62), A, 5.0, rot=-1.5, seed=60, pad='40px 44px')
      + ticket(80, 920, 700, [('<i>RAG =</i> <b>buscar</b> <i>→</i> <b>contestar</b>', 5.9, .6)], A, rot=1.2, size=38)
      + titular(['Contesta con', '_tus datos_'], A, 8.86, top=1130, size=150, seed=2)
      + sello(430, 1450, 'No se lo imagina', A, 10.5, size=60, rot=-7))
DOCS = ''   # ahora son hojas 3D (js3d de s1)
TROZOS = ''.join(pedazo(660, 560 + i * 230, 340, 200, ['014', '017', '031'][i], A, 19.95 + i * .14, rot=[-3, 2, -1.5][i], seed=70 + i) for i in range(3))
f2 = (titular(['En vez de', 'pasarle *todo*…'], A, 11.1, x=14.15, top=TOP, size=150, seed=3)
      + titular(['_Busca_', 'primero'], A, 14.3, x=19.8, top=TOP, size=150, seed=4)
      + titular(['Solo lo que', '*sirve*'], A, 19.9, top=TOP, size=160, seed=5)
      + DOCS
      + mano(110, 1110, 'todos tus documentos', A, 11.6, size=56)
      + sello(110, 1210, '✕ todos los docs', A, 12.9, size=56, rot=-6)
      + ticket(80, 1360, 920, [('<i>$</i> rag search <b>"tu pregunta"</b>', 14.3, .6), ('<i>contexto:</i> <b>3 pedazos</b> <i>· nada más</i>', 19.9, .6)], A, rot=-1, size=36)
      + flecha(600, 860, 650, 640, A, 19.95, color=AZ, curva=-.3)
      + TROZOS
      + circulo(830, 900, 420, 760, A, 20.4, color=AZ, seed=12))
escena('s1-rag', S, 21.85, fase(f1, A, sale=10.9) + fase(f2, A, entra=11.0), seed=2,
       js3d=r"""const pl=pila(6,190,240,'dato');scene.add(pl);
const D=[];for(let i=0;i<5;i++){const h=P.bisagra(hojaTxt(280,360,`doc_${i+1}.md`),360);scene.add(h);D.push(h)}
const lu=lupa(64);scene.add(lu);
const T=['014','017','031'].map(n=>{const h=hojaTxt(170,120,`pedazo ${n}`);scene.add(h);return h});
return t=>{const a=P.eb(P.k(t,5.0,.6));pl.visible=t>=5.0&&t<11.6;pl.scale.setScalar(Math.max(.001,a));P.at(pl,830,470,1.5);pl.rotation.set(.18,-.35+.1*Math.sin(t),(1-a)*.6);
 pl.userData.H.forEach((h,i)=>{h.position.y=Math.sin(t*1.4+i)*.04});P.barre(pl,t,10.9);
 D.forEach((h,i)=>{P.sube(h,t,11.3+i*.08);P.at(h,230+i*34,1000+i*30-10,1.2+i*.12);h.rotation.z=(-8+i*3.5)*Math.PI/180+(1-P.k(t,11.3+i*.08,.55))*.4;
  const sp=P.eio(P.k(t,19.3,.5));h.position.x+=(i-2)*sp*.25;});
 const l=P.eb(P.k(t,14.4,.45)),sw=Math.sin((t-14.4)*1.6);lu.visible=t>=14.4;lu.scale.setScalar(Math.max(.001,l));
 P.at(lu,470+70*sw,860+40*Math.cos((t-14.4)*1.3),4.2);lu.rotation.set(.25,-.2*sw,-.15);
 T.forEach((h,i)=>{const t0=19.55+i*.14,q=P.eio(P.k(t,t0,.4+i*.04));h.visible=t>=t0&&q<1;P.at(h,300+(830-300)*q,880+(660+i*230-880)*q,1.5+2.5*Math.sin(Math.PI*q));
  h.rotation.set(.5*Math.sin(Math.PI*q),.8*Math.sin(Math.PI*q),(1-q)*.6)})}""")

# ───────────────────────── 0:21 · 3 pasos: prepara (pedazos con significado, por idea) → busca (los que más se parecen) → contesta solo con eso
S = 21.85; A = K.at(S)
P4 = [(450, 640, '014'), (740, 640, '015'), (450, 880, '016'), (740, 880, '017')]
f1 = (titular(['Paso 1', '*prepara*'], A, 21.95, top=TOP, size=160, seed=6)
      + hoja_doc(80, 640, 320, 440, 'docs/', A, 22.2, rot=-3, seed=80, n=10)
      + ''.join(pedazo(x, y, 270, 200, n, A, 26.47 + i * .12, rot=[-3, 2, 3, -2][i], seed=81 + i) for i, (x, y, n) in enumerate(P4))
      + mano(690, 575, '✂ pedazos pequeños', A, 26.5, size=46, color=AZ)
      + circulo(875, 980, 330, 250, A, 27.6, color=AZ, seed=13)
      + mano(470, 1110, 'conserva su ' + marca('significado', A, 29.14), A, 29.0, size=56, color='var(--tinta)', rot=-2)
      + ticket(80, 1210, 920, [('<i>$</i> rag index ./docs <i>→</i> <b>pedazos</b>', 22.0, .6), ('<i>buscar</i> «cancelar plan» <i>≈</i> «dar de baja»', 29.95, .8)], A, rot=-1, size=34)
      + sello(80, 1470, 'Por idea ✓', A, 31.42, size=62, rot=-5, color=AZ)
      + sello(450, 1490, 'Palabra exacta ✕', A, 32.94, size=54, rot=6))
G6 = [(430 + (i % 3) * 190, 640 + (i // 3) * 200, f'0{10 + i * 4}') for i in range(6)]
f2 = (titular(['Paso 2', '*busca*'], A, 34.3, top=TOP, size=160, seed=7)
      + nota(80, 650, '¿cómo cancelo mi plan?', A, 34.5, rot=-4, w=300, size=54)
      + flecha(370, 760, 430, 720, A, 35.2, color=AZ, curva=.3)
      + circulo(515, 725, 220, 210, A, 37.0, color=AZ, seed=14) + circulo(705, 725, 220, 210, A, 37.15, color=AZ, seed=15)
      + circulo(515, 925, 220, 210, A, 37.3, color=AZ, seed=16)
      + mano(430, 1100, 'los que más se ' + marca('parecen', A, 38.31), A, 38.2, size=56, color='var(--tinta)', rot=-2)
      + ticket(80, 1260, 920, [('<i>$</i> rag search <b>"pregunta"</b> <i>→ top 3</i>', 34.4, .6)], A, rot=1, size=36))
f3 = (titular(['Paso 3', '*contesta*'], A, 39.3, top=TOP, size=160, seed=8)
      + nota(80, 650, '¿cómo cancelo mi plan?', A, 39.4, rot=-4, w=300, size=54)
      + mano(395, 740, '+', A, 39.6, size=110, color=AZ, rot=0)
      + ''.join(pedazo(460 + i * 26, 640 + i * 30, 220, 170, ['014', '017', '031'][i], A, 39.7 + i * .1, rot=[-4, 2, 5][i], seed=100 + i) for i in range(3))
      + flecha(740, 760, 830, 760, A, 42.43, color=AZ, curva=-.3)
      + logo('', 830, 680, 160, A, 42.5, rot=-8, bg='#2457e6', emoji='🤖')
      + mano(420, 930, 'pregunta + pedazos', A, 42.43, size=58, color=AZ)
      + ticket(80, 1060, 920, [('<i>ia(</i><b>pregunta</b><i>,</i> <b>pedazos</b><i>)</i>', 39.4, .6), ('<i>›</i> contesta <b>usando solo eso</b> <i>✓</i>', 43.65, .7)], A, rot=-1, size=36)
      + recorte(80, 1300, 600, 230, ser('«Ve a <b>Ajustes › Plan</b> y toca <i>Dar de baja</i>.»', 46), A, 44.2, rot=2, seed=110, pad='34px 40px')
      + sello(700, 1380, 'Solo eso', A, 45.76, size=70, rot=-8, color=AZ))
escena('s2-pasos', S, 47.0, fz(f1, A, sale=34.2) + fz(f2, A, entra=34.26, sale=39.2) + fz(f3, A, entra=39.28), seed=3,
       js3d=r"""const G6=[];for(let i=0;i<6;i++){const h=P.bisagra(hojaTxt(170,170,`pedazo 0${10+i*4}`),170);scene.add(h);G6.push(h)}
const lu=lupa(62);scene.add(lu);const HIT=[0,1,3];
const ruta=t=>{if(t<35.4)return[180,1075];if(t<36.2){const q=P.eio(P.k(t,35.4,.8));return[515+380*q,725]}
 if(t<37.0){const q=P.eio(P.k(t,36.2,.8));return[895-380*q,925]}const q=P.eio(P.k(t,37.0,.4));return[515+(200-515)*q,925+(1080-925)*q]};
return t=>{const vis=t>=34.6&&t<39.75;
 G6.forEach((h,i)=>{h.visible=vis&&t>=34.7+i*.07;P.sube(h,t,34.7+i*.07,.45);h.visible=vis&&t>=34.7+i*.07;
  const x=515+(i%3)*190,y=725+Math.floor(i/3)*200+85,j=HIT.indexOf(i),up=j<0?0:P.eb(P.k(t,37.0+j*.15,.45));
  P.at(h,x,y,1.0+up*2.2);h.rotation.z=[-3,2,-2,3,-1,2][i]*Math.PI/180;h.rotation.y=up*.25;if(up>0)h.rotation.x=-up*.35;
  h.scale.setScalar(1+.1*up);P.barre(h,t,39.2)});
 const l=P.eb(P.k(t,35.0,.45)),[x,y]=ruta(t);lu.visible=vis&&t>=35.0;lu.scale.setScalar(Math.max(.001,l));P.at(lu,x,y,4.5+.3*Math.sin(t*5));lu.rotation.set(.2,-.15,-.2+.1*Math.sin(t*3));P.barre(lu,t,39.2)}""")

# ───────────────────────── 0:47 · libro entero vs la página que ocupa
S = 47.0; A = K.at(S)
f1 = (titular(['¿Le das *todo*', 'el contexto?'], A, 47.1, top=TOP, size=150, seed=9)
      + sello(120, 1390, 'Libro entero', A, 50.81, size=70, rot=-6)
      + logo('', 700, 860, 170, A, 52.2, rot=12, bg='#2457e6', emoji='🔍')
      + mano(660, 1060, '…y que encuentre', A, 52.28, size=56, color=RJ)
      + mano(680, 1130, 'la página', A, 52.6, size=56, color=RJ))
f2 = (titular(['Con RAG:', 'solo *esa página*'], A, 54.9, top=TOP, size=150, seed=10)
      + recorte(220, 650, 640, 720, f'<div class="mono" style="font-size:28px;font-weight:700;color:#8a8579">pág. 217</div>'
                + renglones(4) + f'<div style="margin-top:22px;font-size:40px;font-weight:700;line-height:1.25">{marca("Cancela en Ajustes › Plan", A, 56.69)}</div>'
                + renglones(5), A, 55.1, rot=1.5, seed=121, pad='44px 48px')
      + nota(90, 1400, 'tu pregunta', A, 59.36, rot=-5, w=300, size=58)
      + flecha(400, 1480, 560, 1360, A, 59.5, color=AZ))
escena('s3-libro', S, 60.3, fase(f1, A, sale=54.85) + fase(f2, A, entra=54.9), seed=4,
       js3d=r"""const lb=P.bisagra(libro(440,560,120),560);scene.add(lb);let nv=-1;
const lc=libro(190,250,60);lc.userData.portada(412);const lcb=P.bisagra(lc,250);scene.add(lcb);
const pg=hojaTxt(230,290,'pág. 217');scene.add(pg);
const _e=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
return t=>{P.sube(lb,t,47.3,.6);lb.visible=t>=47.3&&t<55.5;P.at(lb,360,1270,1.6);lb.rotation.y=.32+.06*Math.sin(t*1.1);lb.userData.o.rotation.z=-.04;
 const n=Math.round(1+411*_e(P.k(t,48.8,1.4)));if(n!==nv){nv=n;lb.userData.o.userData.portada(n)}P.barre(lb,t,54.85);
 P.sube(lcb,t,54.95,.5);lcb.visible=t>=54.95;P.at(lcb,830,1590,1.4);lcb.rotation.y=-.35;
 const q=P.eio(P.k(t,55.0,.42));pg.visible=t>=55.0&&t<55.75;P.at(pg,830+(540-830)*q,1460+(1010-1460)*q,2.2+3*Math.sin(Math.PI*q)-1.6*q);
 pg.rotation.set(.9*Math.sin(Math.PI*q),-.6*(1-q),.4*(1-q));pg.scale.setScalar(1+.9*q)}""")

# ───────────────────────── 1:00 · mi ejemplo: el homelab recaba redes y proyectos → Claude contesta solo con eso (medio RAG)
S = 60.3; A = K.at(S)
RACK = ''.join(f'<div style="height:110px;margin-top:{16 if i else 0}px;border-radius:12px;background:#2a2926;display:flex;align-items:center;gap:14px;padding:0 26px">'
               + ''.join(f'<i class="led" style="width:20px;height:20px;border-radius:50%;background:#17a35a;box-shadow:0 0 14px #17a35a;animation:led .5s steps(1) {(i * 3 + j) * .17:.2f}s infinite"></i>' for j in range(3))
               + '<i style="flex:1;height:14px;margin-left:30px;background:#3d3b37;border-radius:6px"></i></div>' for i in range(3))
f1 = (titular(['Mi *homelab*'], A, 60.4, top=TOP, size=170, seed=11)
      + sello(640, 505, 'Medio RAG', A, 63.79, size=52, rot=-6, color=AZ)
      + numero(560, 620, N([(0, 0), (64.6, 1284, 3.0)], f='c'), A, 63.9, size=190, color=AZ)
      + mano(570, 790, 'registros recabados', A, 64.6, size=52)
      + logo('', 560, 990, 170, A, 66.77, rot=-8, bg='#ff8fb1', emoji='📣')
      + mano(540, 1180, 'redes sociales', A, 66.9, size=50)
      + logo('', 800, 990, 170, A, 67.51, rot=8, bg='#ffe14a', emoji='📁')
      + mano(810, 1180, 'proyectos', A, 67.6, size=50)
      + flecha(645, 975, 512, 900, A, 67.0, color=AZ, curva=.2) + flecha(885, 970, 512, 960, A, 67.7, color=AZ, curva=.15))
f2 = (titular(['Claude contesta', 'solo con *eso*'], A, 68.1, top=TOP, size=132, seed=12)
      + ticket(80, 650, 920, [('<i>›</i> claude: <b>¿cómo van mis redes?</b>', 68.05, .7), ('<i>contexto =</i> <b>datos guardados</b> <i>· nada más</i>', 70.45, .8)], A, rot=-1, size=36)
      + logo('claude', 760, 940, 220, A, 70.11, rot=-8, bg='#d97757', color='#fff')
      + recorte(80, 950, 600, 300, ser('Lo que se guardó en el homelab, <b>y nada más</b>.', 52), A, 70.6, rot=1.5, seed=131, pad='40px 44px')
      + sello(120, 1380, 'Solo esos datos', A, 72.46, size=72, rot=-6, color=AZ))
escena('s4-ejemplo', S, 77.3, fase(f1, A, sale=68.0) + fase(f2, A, entra=68.05),
       css='@keyframes led{50%{background:#0d4d2a;box-shadow:none}}', seed=5,
       js3d=r"""const sv=servidor(330);const sb=P.bisagra(sv,400);scene.add(sb);
return t=>{P.sube(sb,t,60.8,.6);sb.visible=t>=60.8&&t<68.6;P.at(sb,290,1060,1.8);sb.rotation.y=.42+.05*Math.sin(t*.9);
 sv.userData.leds.forEach((l,i)=>{const on=t>64.5?Math.sin(t*9+i*1.9)>-.2:i%3==0;l.material.emissiveIntensity=on?1.4:.08});P.barre(sb,t,68.0)}""")

# ───────────────────────── 1:17 · > ⚠️ Ojo: mal cortado · desactualizado · búsqueda equivocada → revisa qué encontró
S = 77.3; A = K.at(S)
CAB = titular(['&gt; ⚠️ *Ojo*'], A, 77.4, top=TOP, size=120, seed=13) + mano(520, 330, 'tres cuidados', A, 77.9, size=62, color=RJ)
c1 = (sello(80, 520, '⚠ 1/3', A, 79.5, size=64, rot=-6)
      + titular(['Pedazos mal', '_cortados_'], A, 79.6, top=640, size=150, seed=14)
      + recorte(80, 960, 460, 220, ser('«El plan cuesta…', 54), A, 80.52, rot=-4, seed=140, pad='60px 40px')
      + recorte(570, 990, 430, 220, ser('…$99 al mes»', 54, 'color:#8a8579'), A, 80.7, rot=5, seed=141, pad='60px 40px')
      + mano(470, 1230, '✂ a medias', A, 83.51, size=70, color=RJ))
c2 = (sello(80, 520, '⚠ 2/3', A, 83.94, size=64, rot=-6)
      + titular(['Datos', '_desactualizados_'], A, 84.0, top=640, size=120, seed=15)
      + nota(100, 960, 'precio 2024:<br>$79', A, 85.13, rot=-5, w=360, size=62)
      + mano(500, 1060, '≠', A, 85.4, size=140, color=RJ, rot=0)
      + nota(620, 960, 'hoy:<br>$99', A, 85.6, rot=4, w=360, size=62, color='#b8f0c8')
      + sello(380, 1400, 'Ya no es cierto', A, 89.62, size=66, rot=-7))
c3 = (sello(80, 520, '⚠ 3/3', A, 90.72, size=64, rot=-6)
      + titular(['Búsqueda', '_equivocada_'], A, 90.8, top=640, size=150, seed=16)
      + ticket(80, 980, 920, [('<i>busca</i> «baja» <i>→ trae</i> «bajar precio»', 91.0, .9)], A, rot=-1, size=36)
      + tacha(640, 1040, 330, A, 92.34, grosor=12)
      + sello(380, 1240, 'Trae lo que no es', A, 92.34, size=62, rot=6))
c4 = (titular(['_Revisa_ qué', 'encontró'], A, 96.45, top=520, size=160, seed=17)
      + ticket(80, 900, 920, [('<i>$</i> rag search <b>--show-sources</b>', 96.5, .7), ('<i>✓</i> pedazo 017 · pedazo 031', 97.61, .6)], A, rot=-1, size=36)
      + palomita(720, 1250, 200, A, 97.61, color=VD))
escena('s5-ojo', S, 99.4, CAB + fz(c1, A, entra=79.5, sale=83.9) + fz(c2, A, entra=83.94, sale=90.67) + fz(c3, A, entra=90.72, sale=96.35)
       + fz(c4, A, entra=96.4), seed=6,
       js3d=r"""const bo=P.bola(105,'#f3ecdc',11);scene.add(bo);
return t=>{const a=P.eb(P.k(t,81.0,.5)),r=P.k(t,81.0,.9);bo.visible=t>=81.0&&t<84.5;bo.scale.setScalar(Math.max(.001,a));
 P.at(bo,1180-(1180-820)*P.eo(r),1450,2.4);bo.rotation.set(t*.4,0,(1-P.eo(r))*6+t*.3);P.barre(bo,t,83.9)}""")

# ───────────────────────── 1:39 · ¿y el contexto largo? pocos docs: pásalos todos · miles: tokens, tiempo, se pierde a la mitad
S = 99.4; A = K.at(S)
f1 = (titular(['«Ya aguantan', 'mucho *contexto*»'], A, 99.6, top=TOP, size=140, seed=18)
      + mano(560, 600, 'es cierto ✓', A, 102.0, size=66, color=VD)
      + titular(['¿Pocos docs?'], A, 104.96, top=760, size=130, seed=19)
      + ''.join(hoja_doc(100 + i * 210, 980, 190, 250, f'{i + 1}.md', A, 105.1 + i * .1, rot=[-5, 3, -2, 4][i], seed=150 + i, n=5) for i in range(4))
      + sello(200, 1340, 'Pásale todos ✓', A, 107.34, size=70, rot=-5, color=AZ))
f2 = (titular(['¿Y con', '*miles*?'], A, 108.3, top=TOP, size=170, seed=20)
      + numero(80, 660, N([(0, 5), (108.3, 3000, 1.2)], f='c'), A, 108.3, size=230, color=AZ)
      + mano(90, 870, 'documentos', A, 109.12, size=56)
      + numero(560, 660, N([(0, 4), (109.7, 96, 1.4)], suf='%'), A, 109.7, size=230, color=RJ)
      + mano(570, 870, 'del límite', A, 110.0, size=56, color=RJ)
      + sello(90, 1020, '+ tokens', A, 110.87, size=72, rot=-6)
      + sello(500, 1070, '+ tiempo', A, 112.29, size=72, rot=5)
      + nota(300, 1180, 'se pierde<br>a la mitad 😵‍💫', A, 114.23, rot=-3, w=420, size=64, color='#ffd0dc'))
escena('s6-contexto', S, 115.5, fase(f1, A, sale=108.2) + fase(f2, A, entra=108.26), seed=7,
       js3d=r"""const G=new THREE.Group(),N=46,H=[];const mat=[P.papel('#fbf8f1'),P.papel('#f1ead9'),P.papel('#e8f0ff')];
for(let i=0;i<N;i++){const m=new THREE.Mesh(new THREE.BoxGeometry(180/P.PX,225/P.PX,6/P.PX),mat[i%3]);m.position.z=i*6/P.PX;m.rotation.z=(P.h(i)-.5)*.22;m.position.x=(P.h(i+9)-.5)*.25;G.add(m);H.push(m)}
P.sombra(G);scene.add(G);
return t=>{const g=P.eio(P.k(t,108.3,1.2)),n=Math.max(5,Math.round(N*g));G.visible=t>=108.4;
 H.forEach((m,i)=>{m.visible=i<n});const w=P.k(t,114.23,.8);
 P.at(G,830,1580,.5);G.rotation.set(-1.05,.32,.12*Math.sin(Math.PI*w)*Math.sin(t*14));G.scale.setScalar(Math.max(.001,P.eb(P.k(t,108.4,.4))))}""")

# ───────────────────────── 1:55 · funciona hoy → si tus datos ya no caben, ponlo a buscar antes de contestar
S = 115.5; A = K.at(S)
f1 = (titular(['Funciona', '*hoy*'], A, 115.6, top=TOP, size=200, seed=21)
      + palomita(780, 430, 190, A, 117.92, color=VD)
      + recorte(80, 760, 920, 200, ser('Con los modelos que tenemos <b>en 2026</b>.', 56), A, 116.3, rot=-1.5, seed=160, pad='46px 46px'))
f2 = (titular(['¿Ya no', '_caben_?'], A, 119.9, top=TOP, size=170, seed=22)
      + ticket(80, 680, 920, [('<i>si</i> <b>datos &gt; chat</b> <i>→</i>', 119.9, .6), ('<i>  1.</i> busca <i>· 2.</i> contesta', 122.0, .6)], A, rot=-1, size=38)
      + sello(600, 330, 'No caben', A, 121.25, size=60, rot=-8)
      + mano(120, 1240, 'busca primero', A, 122.93, size=60, color=AZ)
      + flecha(360, 1120, 650, 1120, A, 123.4, color=AZ, curva=-.2)
      + logo('', 660, 1020, 200, A, 123.72, rot=8, bg='#17a35a', emoji='💬')
      + mano(640, 1240, 'luego contesta', A, 123.72, size=60, color=VD))
escena('s7-hoy', S, 124.7, fase(f1, A, sale=119.75) + fase(f2, A, entra=119.82), seed=8,
       js3d=r"""const lu=lupa(72);scene.add(lu);
return t=>{const a=P.eb(P.k(t,122.93,.45));lu.visible=t>=122.93;lu.scale.setScalar(Math.max(.001,a));P.at(lu,215+18*Math.sin(t*2.2),1110+10*Math.cos(t*1.7),3.5);
 lu.rotation.set(.25,-.3+.15*Math.sin(t*1.5),-.2+(1-a)*2)}""")

# ───────────────────────── 2:04 · resumen para guardar + pregunta
S = 124.7; A = K.at(S)
LISTA = ''.join(recorte(80, 820 + i * 175, 920, 150, f'<div style="display:flex;align-items:center;gap:26px;height:100%">'
                        f'<span class="mono" style="font-size:44px;font-weight:700;color:var(--azul);width:70px">{n}</span>{caja(t, 76)}</div>', A, t0,
                        rot=[-1.5, 1.2, -1, 1.5][i], seed=170 + i, pad='18px 40px', cinta=False)
                for i, (n, t, t0) in enumerate([('1', 'Prepara', 125.1), ('2', 'Busca', 125.35), ('3', 'Contesta', 125.6), ('&gt;', '⚠️ Revisa', 126.0)]))
escena('s8-pregunta', S, 128.75,
       titular(['¿Le pasas *todo*', 'a tu IA o la pones', 'a _buscar_ primero?'], A, 124.9, top=TOP, size=120, seed=23)
       + LISTA + mano(560, 1530, 'cuéntame 👇', A, 126.4, size=66, color=RJ), seed=9)

# ───────────────────────── 2:08 · cierre: «nos vemos cuando toque actualizar este README»
S = 128.75; A = K.at(S)
escena('s9-cierre', S, FIN,
       titular(['Nos vemos cuando', 'toque *actualizar*', 'este README'], A, 128.8, top=TOP, size=130, seed=24)
       + ticket(80, 820, 920, [('<i>⌘S</i> <b>README.md</b>', 129.0, .5)], A, rot=-1, size=44)
       + sello(400, 1060, '✓ guardado', A, 130.0, size=80, rot=-6, color=VD), sigue=False, seed=10,
       js3d=r"""const av=P.avion(250);scene.add(av);
return t=>{const q=P.k(t,129.3,2.3);av.visible=t>=129.3&&q<1;P.at(av,-140+1340*q,1430-180*q+40*Math.sin(q*9),4+2*Math.sin(Math.PI*q));
 av.rotation.set(-.35+.15*Math.sin(q*9),-Math.PI/2+.25,.25*Math.cos(q*9))}""")

# ───────────────────────── etiqueta de cinta arriba (todo el video, transparente): README.md · #02 RAG + sección actual
SECC = [(0.0, '# RAG'), (4.6, '## ¿Qué es?'), (21.85, '## Paso 1 · Prepara'), (34.2, '## Paso 2 · Busca'), (39.25, '## Paso 3 · Contesta'),
        (47.0, '## Libro vs página'), (60.3, '## Mi ejemplo'), (77.3, '&gt; ⚠️ Ojo'), (99.4, '## ¿Y el contexto largo?'), (115.5, '## Funciona hoy'),
        (124.7, '## Tu turno'), (128.75, '✓ guardado')]
A = K.at(0)
SEC = ''.join(f'<span class="sc" style="--d:{A(t)};{f"--x:{A(SECC[i + 1][0])};" if i + 1 < len(SECC) else ""}">{n}</span>' for i, (t, n) in enumerate(SECC))
ETQ_CSS = """
.lab{position:absolute;left:30px;right:30px;top:52px;height:150px;z-index:90;transform:rotate(-1deg);background:#ece2c8;
  box-shadow:0 8px 16px rgba(0,0,0,.22);animation:labIn .45s cubic-bezier(.2,1.3,.4,1) both;
  clip-path:polygon(0 6%,3% 0,6% 7%,9% 1%,12% 6%,100% 0,98% 22%,100% 40%,98% 62%,100% 80%,98% 100%,0 100%,2% 78%,0 56%,2% 34%)}
.lab:before{content:'';position:absolute;inset:0;background:url("FIBRA");opacity:.5}
@keyframes labIn{from{transform:translateY(-220px) rotate(-6deg)}to{transform:rotate(-1deg)}}
.lab .rd{position:absolute;left:44px;top:22px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:42px;color:#171513}
.lab .rd i{font-style:normal;color:var(--azul)}
.lab .sc{position:absolute;left:44px;top:80px;font-family:'Caveat',cursive;font-weight:700;font-size:54px;color:var(--azul);white-space:nowrap;opacity:0;
  animation:capIn .3s steps(2) var(--d) forwards}
.lab .sc[style*="--x"]{animation:capIn .3s steps(2) var(--d) forwards,capOut .01s linear var(--x) forwards}
@keyframes capIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}@keyframes capOut{to{opacity:0}}
.lab .nr{position:absolute;right:50px;top:30px;padding:8px 22px;border:6px solid var(--azul);border-radius:12px;color:var(--azul);font-weight:900;font-stretch:62%;
  font-size:62px;line-height:1;text-transform:uppercase;transform:rotate(4deg)}
""".replace('FIBRA', K.FIBRA)
ETQ = f'<div class="lab"><div class="rd">README.md <i>· #02 RAG</i></div>{SEC}<div class="nr">#02</div></div>'
PIEZAS.append(('etiqueta', 0.0, FIN, K.page(ETQ_CSS, ETQ, FIN, S0=0.0, transparente=True)))
PRE = 'rmr3d2-'

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
        rel = os.environ.get('REL', 'readme/2/recorte3d')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
