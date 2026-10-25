"""El Log #09 · Claude Duet · edición «Recorte 3D»: primera plana de papel (titulares que golpean, tachones, marcatextos,
sellos, tickets y recortes con cinta, hojas que entran rasgadas, 12 cps) + objetos 3D de papel y cartón con sombras reales
(medallas con logos recortados que se levantan como pop-up, ícono de app de cartón, maletín, laptop, sello de goma, lupa).
Arriba, cabecera de periódico con cintillo rojo que corre los datos (la cinta de El Log de esta edición).
Base: ellog-08-recorte3d.py. Tiempos = voz recortada de noticias/9 (voz/voz-norm.wav, 92.95 s).
Uso: SALIDA=~/Documents/Videos/noticias/9/animaciones REL=noticias/9/animaciones python3 ejemplos/ellog-09-recorte3d.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import recorte as K
import ellog_gloss as G
from recorte import titular, tacha, subraya, circulo, flecha, recorte, nota, sello, ticket, numero, N, logo, mano, fase, palomita, marca

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/noticias/9/animaciones')))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 92.95
TOP = 330          # primer renglón útil (debajo de la cabecera)
CLA = '#d97757'    # naranja Claude
PIEZAS = []


def escena(pid, start, end, body, fondo='papel', css='', ac='var(--rojo)', sigue=True, seed=1, js3d=None):
    if sigue:
        end += K.COLA
    PIEZAS.append((pid, start, end, K.page(css, body, round(end - start, 2), S0=start, fondo=fondo, seed=seed, ac=ac,
                                          js3d=LIB3D + js3d if js3d else None)))


SVG = {n: G.svgpath(n) for n in ('claude', 'anthropic', 'meta', 'openai')}
# piezas de papel propias de este video
LIB3D = 'const SVG=' + json.dumps(SVG) + r""";
const medalla=(d,s,bg,fg='#ffffff')=>{const G=new THREE.Group();
 const disc=new THREE.Mesh(new THREE.CylinderGeometry(P.u(s/2),P.u(s/2),P.u(18),56),[P.papel('#f3ede0'),P.papel(bg),P.papel(bg)]);disc.rotation.x=Math.PI/2;G.add(disc);
 const gl=P.recorte(d,s*.6,fg,10);gl.position.z=P.u(15);G.add(gl);return P.sombra(G)};
// ícono de app: cuadro de cartón con el logo recortado encima
const appicon=(d,s,bg,fg='#ffffff')=>{const G=new THREE.Group();G.add(P.caja(s,s,s*.14,bg,false));
 const gl=P.recorte(d,s*.58,fg,12);gl.position.z=P.u(s*.07+8);G.add(gl);return P.sombra(G)};
const maletin=(w)=>{const G=new THREE.Group(),h=w*.68,d=w*.3;G.add(P.caja(w,h,d,'#a0662f',false));
 const fr=new THREE.Mesh(new THREE.BoxGeometry(P.u(w*1.01),P.u(h*.08),P.u(d*1.02)),P.papel('#6b4220'));fr.position.y=P.u(h*.18);G.add(fr);
 const asa=new THREE.Mesh(new THREE.TorusGeometry(P.u(w*.16),P.u(w*.035),10,28,Math.PI),P.papel('#6b4220'));asa.position.y=P.u(h/2);G.add(asa);
 for(const x of[-1,1]){const c=new THREE.Mesh(new THREE.BoxGeometry(P.u(w*.08),P.u(h*.12),P.u(8)),P.papel('#e2b74a'));c.position.set(P.u(x*w*.3),P.u(h*.18),P.u(d/2+3));G.add(c)}
 return P.sombra(G)};
// sello de goma: mango de madera + perilla + base con hule rojo
const sello3=(w)=>{const G=new THREE.Group();
 const base=new THREE.Mesh(new THREE.BoxGeometry(P.u(w),P.u(w*.22),P.u(w*.6)),P.papel('#3a3a42'));G.add(base);
 const hule=new THREE.Mesh(new THREE.BoxGeometry(P.u(w*.94),P.u(w*.06),P.u(w*.56)),P.papel('#e3342a'));hule.position.y=P.u(-w*.14);G.add(hule);
 const m=new THREE.Mesh(new THREE.CylinderGeometry(P.u(w*.1),P.u(w*.14),P.u(w*.55),20),P.papel('#c9a26b'));m.position.y=P.u(w*.38);G.add(m);
 const k=new THREE.Mesh(new THREE.SphereGeometry(P.u(w*.19),20,14),P.papel('#c9a26b'));k.position.y=P.u(w*.72);G.add(k);return P.sombra(G)};
const lupa=(r)=>{const G=new THREE.Group();G.add(new THREE.Mesh(new THREE.TorusGeometry(P.u(r),P.u(r*.17),14,48),P.papel('#2457e6')));
 G.add(new THREE.Mesh(new THREE.CircleGeometry(P.u(r),48),P.papel('#dfe8ff',{transparent:true,opacity:.5})));
 const hd=new THREE.Mesh(new THREE.BoxGeometry(P.u(r*.34),P.u(r*1.25),P.u(r*.32)),P.papel('#c9a26b'));hd.position.set(P.u(r*1.18),P.u(-r*1.18),0);hd.rotation.z=Math.PI/4;G.add(hd);return P.sombra(G)};
"""


def caja(txt, size=96, extra=''):
    return f'<div style="font-weight:900;font-stretch:62%;font-size:{size}px;line-height:.88;text-transform:uppercase;{extra}">{txt}</div>'


def ser(txt, size=48, extra=''):
    return f'<div class="ser" style="font-size:{size}px;line-height:1.05;{extra}">{txt}</div>'


# ───────── 0:00 · «Dicen que Claude es solo para programar» (tachado) → hoy Anthropic sacó Claude Duet | un agente para negocios pequeños
S = 0.0; A = K.at(S)
f1 = (titular(['Dicen que Claude', 'es solo para', 'programar'], A, .2, x=4.9, top=TOP, size=130, seed=2)
      + tacha(70, TOP + 285, 560, A, 2.75, grosor=16)
      + titular(['Anthropic sacó', '*Claude Duet*'], A, 3.19, x=4.9, top=760, size=140, seed=3)
      + sello(90, 1110, 'Hoy', A, 2.93, size=110, rot=-8))
f2 = (titular(['Un _agente_ para', 'negocios', '*pequeños*'], A, 5.15, top=TOP, size=140, seed=4)
      + nota(80, 840, '¿Trabajas por<br>tu cuenta?', A, 7.82, rot=-4, w=360, size=58)
      + nota(560, 870, '¿Tienes un<br>negocio?', A, 9.24, rot=4, w=360, size=58, color='#ffd0dc')
      + sello(60, 1290, 'Más pensado para ti', A, 11.59, size=54, rot=-5))
escena('e00-gancho', S, 12.86, fase(f1, A, sale=4.9) + fase(f2, A, entra=5.0), css=f'.tt .sf{{color:{CLA}}}', ac=CLA, seed=1, js3d=r"""
const cl=P.bisagra(medalla(SVG.claude,300,'#d97757'),300);P.at(cl,820,1500,1.6);cl.rotation.z=.08;scene.add(cl);
const mt=maletin(270);const mg=P.bisagra(mt,190);P.at(mg,820,1610,1.6);mg.rotation.z=-.06;scene.add(mg);
return t=>{P.sube(cl,t,4.17,.6);cl.userData.o.rotation.y=.25*Math.sin(t*1.4);P.barre(cl,t,4.9);
 P.sube(mg,t,5.9,.6);mt.rotation.y=-.35+.15*Math.sin(t*1.1)}""")

# ───────── 0:13 · no viene en el chat de siempre → su propia app (iPhone y Android) | se pelea con Muse (Meta) y Dots (OpenAI)
S = 12.86; A = K.at(S)
CUERDAS = ''.join(f'<div class="rcw" style="left:30px;top:{1250 + i * 52}px;width:1020px;height:20px;--d:{A(19.5 + i * .08)};--r:{[-1, .5, -.4][i]}deg;z-index:12">'
                  f'<div class="rc" style="height:100%;padding:0;background:{["#e3342a", "#f3eee4", "#e3342a"][i]}"></div></div>' for i in range(3))
f1 = (titular(['No viene en el', '*chat* de siempre'], A, 13.41, x=15.5, top=TOP, size=140, seed=6)
      + recorte(80, 680, 560, 170, ser('💬 el chat de siempre', 54), A, 14.3, rot=-3, seed=21, sale=15.5, pad='40px 44px')
      + tacha(100, 790, 500, A, 14.97, grosor=16, color='#ff6b6b')
      + titular(['Su propia', '_app_'], A, 15.65, top=TOP, size=170, seed=7)
      + sello(110, 1300, 'iPhone', A, 18.02, size=76, rot=-6, color='#ff6b6b')
      + sello(600, 1300, 'Android', A, 18.37, size=76, rot=5, color='#3ee08a'))
f2 = (titular(['Y se pelea con', '*Muse* y *Dots*'], A, 19.42, top=TOP, size=140, seed=8)
      + CUERDAS
      + mano(150, 1150, 'Duet', A, 19.6, size=64, color=CLA)
      + mano(395, 1150, 'Muse · Meta', A, 21.04, size=60, color='#7aa7ff')
      + mano(705, 1150, 'Dots · OpenAI', A, 22.14, size=60, color='#f3eee4'))
escena('e01-app', S, 23.76, fase(f1, A, sale=19.3) + fase(f2, A, entra=19.4), fondo='negra', css=f'.negra .tt .sf{{color:{CLA}}}', ac=CLA, seed=2, js3d=r"""
const ap=P.bisagra(appicon(SVG.claude,300,'#d97757'),300);P.at(ap,540,1170,1.6);ap.rotation.z=-.05;scene.add(ap);
const M=[[SVG.claude,'#d97757','#ffffff',230,19.6],[SVG.meta,'#0866ff','#ffffff',540,21.3],[SVG.openai,'#1b1a18','#ffffff',850,22.4]].map(([d,bg,fg,x,t0])=>{
 const g=P.bisagra(medalla(d,230,bg,fg),230);P.at(g,x,1110,1.6);scene.add(g);return [g,t0]});
return t=>{P.sube(ap,t,16.77,.6);ap.userData.o.rotation.y=.3*Math.sin(t*1.2);P.barre(ap,t,19.3);
 for(const [g,t0] of M){P.sube(g,t,t0,.6);g.userData.o.rotation.y=.25*Math.sin(t*1.5+t0);g.rotation.z=.05*Math.sin(t*2+t0)}}""")

# ───────── 0:24 · un agente no solo contesta: hace tareas por ti | para profesionales y pequeños negocios, no tanto para el desarrollador
S = 23.76; A = K.at(S)
TAREAS = ''.join(f'<div class="fade0" style="--d:{A(t)};font-family:Caveat;font-weight:700;font-size:54px;line-height:1.15">☑ {x}</div>'
                 for x, t in [('agenda tus juntas', 28.15), ('arma reportes', 28.45), ('revisa tus apps', 28.75)])
f1 = (titular(['Un agente no', 'solo *contesta*'], A, 23.94, top=TOP, size=150, seed=9)
      + ticket(90, 700, 900, [('<i>›</i> ¿me ayudas con esto?', 25.3, .5), ('<i>🤖</i> claro, aquí tienes…', 25.9, .5)], A, rot=-1.5, size=36)
      + titular(['Hace _tareas_', 'por ti'], A, 26.58, top=980, size=150, seed=10)
      + recorte(90, 1320, 560, 290, TAREAS, A, 28.0, rot=-2, seed=22, pad='30px 40px'))
f2 = (titular(['Para *profesionales*', 'y pequeños', '_negocios_'], A, 30.93, top=TOP, size=130, seed=11)
      + mano(560, 300 + 400, 'según Anthropic', A, 30.3, size=56, color=CLA)
      + recorte(90, 800, 700, 170, caja('&lt;/&gt; desarrollador', 64, 'white-space:nowrap'), A, 35.71, rot=-2.5, seed=23, pad='50px 40px')
      + tacha(110, 895, 620, A, 36.4, grosor=9)
      + nota(560, 1040, 'lleva su negocio<br>desde el teléfono', A, 37.22, rot=4, w=440, size=54))
escena('e02-negocios', S, 40.78, fase(f1, A, sale=29.3) + fase(f2, A, entra=29.4), css=f'.tt .sf{{color:{CLA}}}', ac=CLA, seed=3, js3d=r"""
const mt=maletin(280);const mg=P.bisagra(mt,195);P.at(mg,330,1560,1.6);mg.rotation.z=.05;scene.add(mg);
const lp=P.laptop(230,'#2b2b30','#6ea8ff');P.at(lp,800,1500,2);lp.rotation.set(.35,-.5,0);scene.add(lp);
return t=>{P.sube(mg,t,32.82,.6);mt.rotation.y=.35+.12*Math.sin(t*1.1);
 lp.visible=t>35.6;const a=P.eb(P.k(t,35.6,.5));lp.scale.setScalar(Math.max(.01,a));
 lp.userData.tapa.rotation.x=-1.85+1.75*P.eio(P.k(t,36.4,.5));lp.userData.pantalla.material.emissiveIntensity=t>36.6?0:.35}""")

# ───────── 0:41 · ojo: vista previa de investigación | lo publicaron The Verge, MacRumors, Engadget | no significa que sea mejor: nadie lo ha probado a fondo
S = 40.78; A = K.at(S)
f1 = (titular(['Pero ojo:', '*vista previa*'], A, 40.88, x=48.8, top=TOP, size=160, seed=12)
      + sello(90, 780, 'Vista previa de investigación', A, 42.21, size=52, rot=-5)
      + nota(90, 960, 'versión de<br>prueba', A, 44.92, rot=-4, w=380, size=64)
      + mano(530, 1100, 'puede cambiar…', A, 46.91, size=66)
      + mano(560, 1200, '¡y bastante!', A, 47.87, size=80))
f2 = (titular(['Lo publicaron', 'en *medios*'], A, 50.86, x=54.7, top=TOP, size=150, seed=13)
      + recorte(90, 720, 560, 190, caja('The Verge', 104), A, 51.87, rot=-3, seed=24, pad='40px 44px', sale=54.7)
      + recorte(450, 960, 560, 190, caja('MacRumors', 104), A, 52.73, rot=3, seed=25, pad='40px 44px', sale=54.7)
      + recorte(120, 1200, 560, 190, caja('Engadget', 104), A, 53.45, rot=-2, seed=26, pad='40px 44px', sale=54.7))
COMP = ''.join(recorte(70 + i * 320, 760, 290, 170, caja(n, 92, f'text-align:center;color:{c}'), A, t, rot=[-3, 2, -2][i], seed=27 + i, pad='36px 20px')
               for i, (n, c, t) in enumerate([('Duet', CLA, 58.35), ('Muse', '#0866ff', 59.38), ('Dots', '#171513', 59.97)]))
f3 = (titular(['No significa', 'que sea *mejor*'], A, 57.12, top=TOP, size=140, seed=14)
      + COMP
      + mano(250, 960, '¿?', A, 58.82, size=90) + mano(570, 960, '¿?', A, 59.6, size=90)
      + sello(80, 1110, 'Nadie lo ha probado a fondo', A, 60.97, size=54, rot=-4))
escena('e03-preview', S, 63.30, fase(f1, A, sale=48.8) + fase(f2, A, entra=48.9, sale=54.7) + fase(f3, A, entra=54.8), seed=4, js3d=r"""
const st=sello3(220);scene.add(st);
const lp=lupa(80);const lg=P.bisagra(lp,250);P.at(lg,820,1520,2.2);lg.rotation.z=.15;scene.add(lg);
return t=>{st.visible=t>41.5;const c=P.k(t,41.5,.71),b=c<1?Math.sin(c*Math.PI):0;
 P.at(st,820,1500+160*(1-P.eo(P.k(t,41.5,.5)))-40*b,2.4);st.rotation.set(.35,.4+.2*Math.sin(t),.05*Math.sin(t*2));
 if(t>42.21&&t<42.6)st.scale.set(1.08,.9,1.08);else st.scale.setScalar(Math.max(.01,P.eb(P.k(t,41.5,.4))));P.barre(st,t,48.8);
 P.sube(lg,t,61.7,.6);lp.position.x=P.u(30*Math.sin(t*1.6));lp.rotation.y=.3*Math.sin(t*1.1)}""")

# ───────── 1:03 · la pelea de los agentes salió de la terminal y llegó a los teléfonos | Meta, OpenAI y ahora Anthropic: tres grandes | un nuevo jugador para comparar
S = 63.30; A = K.at(S)
f1 = (titular(['La pelea de los', '*agentes*'], A, 63.4, top=TOP, size=140, seed=15)
      + ticket(90, 720, 700, [('<i>$</i> claude --agente', 65.5, .6), ('<i>›</i> salió de la terminal…', 66.1, .6)], A, rot=-2, size=38)
      + flecha(560, 980, 760, 1160, A, 66.4, color='#ff6b6b')
      + mano(380, 1190, '…y llegó a los teléfonos', A, 66.53, size=64, color='#ff6b6b'))
f2 = (titular(['Tres de las', '*grandes*'], A, 70.09, top=TOP, size=160, seed=16)
      + mano(150, 1100, 'Meta', A, 68.1, size=62, color='#7aa7ff')
      + mano(440, 1100, 'OpenAI', A, 68.65, size=62, color='#f3eee4')
      + mano(730, 1100, 'Anthropic', A, 69.47, size=62, color=CLA)
      + mano(140, 1230, 'peleando por lo mismo', A, 71.76, size=66))
f3 = (titular(['¿Usas o desarrollas', '*agentes*?'], A, 73.76, top=TOP, size=104, seed=17)
      + titular(['Un *nuevo*', 'jugador'], A, 76.70, top=720, size=170, seed=18)
      + nota(560, 1100, 'para comparar:<br>☐ Muse ☐ Dots<br>☐ Duet', A, 77.68, rot=4, w=440, size=52))
escena('e04-pelea', S, 79.18, fase(f1, A, sale=67.9) + fase(f2, A, entra=68.0, sale=73.6) + fase(f3, A, entra=73.7), fondo='negra',
       css='.negra .tt .sf{color:#ff6b6b}', seed=5, js3d=r"""
const M=[[SVG.meta,'#0866ff','#ffffff',230,68.1],[SVG.openai,'#1b1a18','#ffffff',540,68.65],[SVG.anthropic,'#f0eee6','#191919',850,69.47]].map(([d,bg,fg,x,t0])=>{
 const g=P.bisagra(medalla(d,230,bg,fg),230);P.at(g,x,1050,1.6);scene.add(g);return [g,t0]});
const nv=P.bisagra(medalla(SVG.claude,240,'#d97757'),240);P.at(nv,300,1500,1.6);nv.rotation.z=-.08;scene.add(nv);
return t=>{for(const [g,t0] of M){P.sube(g,t,t0,.6);g.userData.o.rotation.y=.25*Math.sin(t*1.5+t0);P.barre(g,t,73.6)}
 P.sube(nv,t,76.84,.6);nv.userData.o.rotation.y=.3*Math.sin(t*1.3)}""")

# ───────── 1:19 · cierre: dale una revisada (lista de espera) · Claude ya no es solo para programar · ¿qué tarea le dejarías a un agente?
S = 79.18; A = K.at(S)
f1 = (titular(['Dale una', '*revisada*'], A, 79.33, top=TOP, size=170, seed=19)
      + sello(90, 720, 'Lista de espera · Pro y Max EE. UU.', A, 81.11, size=44, rot=-4)
      + titular(['Claude _ya no_ es', 'solo para', 'programar'], A, 83.19, top=930, size=140, seed=20)
      + mano(110, 1330, '¡ya no!', A, 83.74, size=80, color=CLA))
f2 = (titular(['¿Qué tarea le', 'dejarías a un', '*agente*?'], A, 86.6, top=TOP, size=140, seed=21)
      + mano(110, 760, 'cuéntame 👇', A, 85.93, size=64))
escena('e05-cierre', S, FIN, fase(f1, A, sale=85.7) + fase(f2, A, entra=85.8), css=f'.tt .sf{{color:{CLA}}}', ac=CLA, sigue=False, seed=6, js3d=r"""
const ap=P.bisagra(appicon(SVG.claude,230,'#d97757'),230);P.at(ap,820,1560,1.6);ap.rotation.z=.07;scene.add(ap);
return t=>{P.sube(ap,t,80.42,.6);ap.userData.o.rotation.y=.3*Math.sin(t*1.2);P.barre(ap,t,85.7)}""")

# ───────── «Sígueme»: nota adhesiva + comentario tecleado (transparente, sobre el cierre)
SEG_INI = 85.9
S = SEG_INI; A = K.at(S)
_r = 'Contestar correos, sin duda 😅'
SEG = (nota(570, 1250, '<div style="font-size:44px">Sígueme</div><div style="font-family:Archivo;font-weight:900;font-stretch:62%;font-size:84px;line-height:.9;text-transform:uppercase">El Log</div>'
            '<div style="font-size:40px;margin-top:6px">cada semana · Armando</div>', A, 86.0, rot=5, w=430, size=60)
       + sello(640, 1600, 'Seguir ✓', A, 86.8, size=60, rot=-4, color='var(--verde)')
       + recorte(60, 1280, 480, 330, '<div class="ser" style="font-size:40px;line-height:1.1">🤖 ¿Qué tarea le dejarías a un agente?</div>'
                 f'<div style="margin-top:18px;font-family:Caveat;font-weight:700;font-size:38px;color:var(--azul)">'
                 f'<span style="display:inline-block;white-space:nowrap;clip-path:inset(0 100% 0 0);animation:tip 1s steps({len(_r) + 1}) {A(87.4)} forwards">{_r}</span></div>',
                 A, 86.4, rot=-3, seed=31))
PIEZAS.append(('seguir', SEG_INI, FIN, K.page('', SEG, round(FIN - SEG_INI, 2), S0=SEG_INI, transparente=True)))

# ───────── cabecera de periódico + cintillo rojo de última hora (todo el video, encima de todo)
CORRIDO = ['Anthropic lanza Claude Duet: un agente para profesionales y pequeños negocios', 'App propia para iOS y Android, y también en claude.ai',
           'Vista previa de investigación: por ahora solo Pro y Max en EE. UU., con lista de espera', 'Pide permiso antes de enviar, pagar, firmar o borrar',
           'Compite con Muse de Meta y Dots de OpenAI', 'Lo reportaron The Verge, MacRumors y Engadget', 'Nadie lo ha probado a fondo todavía']
CAPS = [(0.0, 'Ya no solo código'), (12.86, 'Su propia app'), (23.76, 'Para negocios'), (40.78, 'Vista previa'), (63.30, 'La pelea'),
        (79.18, 'Tu opinión')]
A = K.at(0)
CAPH = ''.join(f'<span class="cp" style="--d:{A(t)};{f"--x:{A(CAPS[i + 1][0])};" if i + 1 < len(CAPS) else ""}">{i + 1:02d} · {n}</span>' for i, (t, n) in enumerate(CAPS))
TICK = '<span>⚠</span>'.join(f'<span>{c}</span>' for c in CORRIDO)
CABE_CSS = """
.cab{position:absolute;left:0;right:0;top:0;height:250px;z-index:90;background:#f3ecdf;box-shadow:0 10px 24px rgba(0,0,0,.35);animation:cabIn .45s cubic-bezier(.2,1.3,.4,1) both}
.cab:before{content:'';position:absolute;inset:0;background:url("FIBRA");opacity:.45}
@keyframes cabIn{from{transform:translateY(-260px)}to{transform:none}}
.cab .mh{position:absolute;left:44px;right:44px;top:22px;height:108px;display:flex;align-items:flex-end;justify-content:space-between;border-bottom:5px double #171513;padding-bottom:6px}
.cab .lg{font-family:'Instrument Serif',serif;font-size:112px;line-height:.8;letter-spacing:-.02em}
.cab .lg i{color:var(--rojo)}
.cab .ed{text-align:right;font-weight:800;font-stretch:75%;text-transform:uppercase;font-size:24px;letter-spacing:.08em;line-height:1.3}
.cab .ed b{display:block;font-size:30px;color:var(--rojo)}
.cab .cp{position:absolute;right:44px;top:142px;font-weight:900;font-stretch:62%;font-size:40px;text-transform:uppercase;opacity:0;animation:capIn .3s steps(2) var(--d) forwards}
.cab .cp[style*="--x"]{animation:capIn .3s steps(2) var(--d) forwards,capOut .01s linear var(--x) forwards}
@keyframes capIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:none}}@keyframes capOut{to{opacity:0}}
.cab .ul{position:absolute;left:44px;top:146px;font-weight:900;font-stretch:62%;font-size:36px;text-transform:uppercase;color:#fff;background:var(--rojo);padding:2px 16px;
  animation:lat 1s steps(1) infinite}
@keyframes lat{50%{background:#171513}}
.tick{position:absolute;left:0;right:0;top:196px;height:54px;background:var(--rojo);overflow:hidden;display:flex;align-items:center}
.tick .mv{display:flex;gap:30px;white-space:nowrap;font-weight:800;font-stretch:80%;font-size:30px;color:#fff;text-transform:uppercase;animation:mv 70s linear infinite;padding-left:1080px}
@keyframes mv{to{transform:translateX(-100%)}}
""".replace('FIBRA', K.FIBRA)
CABE = (f'<div class="cab"><div class="mh"><div class="lg">El <i>Log</i></div><div class="ed"><b>Edición del día</b>N.º 09 · agentes</div></div>'
        f'<span class="ul">⚠ Última hora</span>{CAPH}<div class="tick"><div class="mv">{TICK}<span>⚠</span>{TICK}</div></div></div>')
PIEZAS.append(('cabecera', 0.0, FIN, K.page(CABE_CSS, CABE, FIN, S0=0.0, transparente=True)))
PRE = 'ellr3d9-'

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
        rel = os.environ.get('REL', 'noticias/9/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
