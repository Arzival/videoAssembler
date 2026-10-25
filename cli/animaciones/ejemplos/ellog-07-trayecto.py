"""El Log #07 · diseño «Trayecto» con la cinta de noticiero arriba.
Reutiliza los ayudantes de ellog-06-trayecto.py (tray, baraja, escena, contadores) y solo cambia guion y tiempos.
Tiempos = voz recortada de noticias/7 (voz/voz-norm.wav, 131.83 s). Necesita internet al capturar.
Uso: SALIDA=noticias/7/animaciones REL=noticias/7/animaciones python3 ejemplos/ellog-07-trayecto.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('ellog06t', os.path.join(HERE, 'ellog-06-trayecto.py'))
M = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(M)
G, T, D, js = M.G, M.T, M.D, M.js
tray, baraja, K, BG = M.tray, M.baraja, M.K, M.BG
TX, TW, TK, CYT = M.TX, M.TW, M.TK, M.CYT
escena, st, fase, gl, em, N, below = M.escena, M.st, M.fase, M.gl, M.em, M.N, M.below
VIO, GRIS, CORAL, AMB, CIAN = M.VIO, M.GRIS, M.CORAL, M.AMB, M.CIAN
VERDE = BG.format(a='#d2fbe4', b='#3ee08a')
AZUL = BG.format(a='#dbe8ff', b='#6ea8ff')

FIN = 131.83
M.PIEZAS = []
PIEZAS = M.PIEZAS
D.FIN = FIN
D.NOTICIAS = [(0.0, 'fin', '01', 'Spotify saca la música hecha con IA'),
              (36.3, 2, '02', 'DeepSeek publica su motor de inferencia'),
              (68.3, 'amb', '03', 'Mistral anuncia Voxtral 3'),
              (93.3, 'gris', '04', 'OpenAI: sus modelos ya manejan COBOL'),
              (123.0, 0, '✓', '¿Dejarías que una IA migre tu sistema?')]
D.CORRIDO = ['Spotify: más de 500 millones de canciones con IA fuera de tus recomendaciones', 'Lo dice la propia empresa: quitó IA y spam en el último año',
             'Membresías de podcast en 34 regiones: Spotify se queda con el 10 %', 'DeepSeek: framework de inferencia de alto rendimiento para sus modelos',
             'Hacker News: casi 2,000 puntos y más de 700 comentarios', 'Estados Unidos veta DeepSeek en sus agencias federales',
             'Mistral anuncia Voxtral 3 en su sitio oficial', 'OpenAI: sus modelos ayudan a migrar COBOL en bancos · sin cifras']

LIB = M.LIB + r"""
R.mic=(w)=>{const G=R.group();const gr=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.32),40,28),R.metal('#c9d2de',{roughness:.35}));gr.position.y=R.u(w*.55);G.add(gr);
 const mesh=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.33),24,16),R.metal('#e8ecf3',{wireframe:true}));mesh.position.y=gr.position.y;G.add(mesh);
 const band=new THREE.Mesh(new THREE.TorusGeometry(R.u(w*.33),R.u(w*.03),16,60),R.metal('#9aa3b5'));band.position.y=gr.position.y;band.rotation.x=Math.PI/2;G.add(band);
 const body=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.17),R.u(w*.12),R.u(w*.9),40),R.gloss('#1b1e26',{roughness:.25}));body.position.y=R.u(-w*.1);G.add(body);
 const led=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.04),16,12),R.gloss('#3ee08a',{emissive:'#3ee08a',emissiveIntensity:1.5}));led.position.set(0,R.u(w*.15),R.u(w*.15));G.add(led);G.userData.led=led;return G};
R.bank=(w)=>{const G=R.group(),m=R.metal('#d9dbe2',{roughness:.2});const base=R.rbox(w,w*.1,w*.5,w*.02,m);base.position.y=R.u(-w*.42);G.add(base);
 const top=R.rbox(w*.96,w*.08,w*.48,w*.02,m);top.position.y=R.u(w*.18);G.add(top);
 for(let i=0;i<4;i++){const c=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.06),R.u(w*.07),R.u(w*.5),28),R.gloss('#f1eeee',{roughness:.3}));c.position.set(R.u(-w*.33+i*w*.22),R.u(-w*.12),R.u(w*.1));G.add(c)}
 const s=new THREE.Shape();s.moveTo(-w*.52/R.PX,0);s.lineTo(w*.52/R.PX,0);s.lineTo(0,w*.3/R.PX);s.lineTo(-w*.52/R.PX,0);
 const roof=new THREE.Mesh(new THREE.ExtrudeGeometry(s,{depth:w*.46/R.PX,bevelEnabled:true,bevelThickness:.05,bevelSize:.04,bevelSegments:3}),m);roof.position.set(0,R.u(w*.22),R.u(-w*.23));G.add(roof);return G};
R.punch=(w)=>{const G=R.group();G.add(R.rbox(w,w*.45,w*.02,w*.03,R.gloss('#f1d9a8',{roughness:.5})));const hm=R.gloss('#2c2b2e');
 for(let r=0;r<5;r++)for(let c=0;c<14;c++){if((r*7+c*3)%4)continue;const h=R.rbox(w*.03,w*.05,w*.03,w*.005,hm);h.position.set(R.u(-w*.42+c*w*.065),R.u(w*.14-r*w*.07),R.u(w*.012));G.add(h)}
 return G};
"""

SIG = {
    1: [('🐋', 'DeepSeek', '0:36', 2), ('🇪🇺', 'Mistral', '1:08', 'amb')],
    2: [('🇪🇺', 'Mistral', '1:08', 'amb'), ('🏦', 'COBOL', '1:33', 'gris')],
    3: [('🏦', 'COBOL', '1:33', 'gris'), ('💬', 'Tu opinión', '2:03', 0)],
    4: [('💬', 'Tu opinión', '2:03', 0)],
}

# ───────── 0:00 · #01 Spotify quita más de 500 M de canciones con IA de tus recomendaciones; lo dice la empresa
S = 0.0; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'fin', 0.2, A, gl('spotify'), 'Spotify · recomendaciones', ring=(N(K((0, 0), (1.7, 500, 1.4))) + 'M', K((0, 0), (1.7, 100, 1.4))),
          btn=('Siguiente', 11.8),
          mL=('Quitó', N(K((0, 0), (1.7, 500, 1.4))) + ' M canciones', 1.7), mR=('Hechas con', '<b>IA</b>', 4.2),
          bar=K((0, 0), (1.7, 100, 1.4)),
          cols=[('Fuera de', 'tus recomendaciones', 4.85), ('', '', None), ('Ahora', 'artistas reales', 10.9)],
          stops=[('Si abres', 'tu Spotify', 6.4), ('Te recomienda', 'música real', 10.3)],
          thumbs=[('🎧', VERDE, 6.4), ('🎤', VERDE, 10.9)])
c2 = tray(TX, CYT, TW, TK, 'gris', 12.4, A, em('📣'), 'Lo dice la propia empresa', ring=(N(K((0, 0), (16.5, 1, .3), (20.2, 2, .3))) + '/2', K((0, 0), (16.5, 50, .5), (20.2, 100, .5))),
          btn=('Siguiente', 21.9),
          mL=('Quitó', '<b>IA y spam</b>', 16.5), mR=('Ajustó', 'su <b>sistema</b>', 18.9),
          bar=K((0, 0), (16.5, 50, .6), (20.2, 100, .6)),
          cols=[('Periodo', 'último año', 15.6), ('Fuera', 'IA · spam', 17.7), ('Destaca', 'música real', 20.5)])
escena('e00-spotify', S, 22.4, 'fin', fase(1, 0, A(12.1)) + fase(2, A(12.2)),
       f"""<div class="p1">{st([('<em>Spotify</em> limpia<br>la música IA', 0.3, 6.1), ('Más artistas<br><em>reales</em>', 6.2, None)], S, 88)}{baraja(CYT, TK, A, 0.6, SIG[1])}{c1}</div>
<div class="p2">{st([('Ojo: lo dice<br>la <em>empresa</em>', 12.3, 18.0), ('Destaca la<br>música <em>real</em>', 18.1, None)], S, 88)}{baraja(CYT, TK, A, 12.5, SIG[1])}{c2}
 {below('📣 lo dice la propia empresa', 1420, 13.2, A, 'pill', '--r:-3deg;')}</div>""",
LIB + r"""const vy=R.vinyl(170,'#3ee08a');R.scene.add(vy);const V=vy.userData.V;
return t=>{const a=R.eb(R.k(t,.6,.9)),c=R.eio(R.k(t,12.0,.8));vy.scale.setScalar(Math.max(.001,a));
 R.at(vy,540,1650+12*Math.sin(t*1.4),2);vy.rotation.set(.5+.1*Math.sin(t*1.1)-c*.3,(1-a)*3+.35*Math.sin(t*.8),0);V.rotation.z=-t*3}""")

# ───────── 0:22 · #01 (parte 2): membresías de podcast en 34 regiones, Spotify se queda el 10 %
S = 22.4; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'fin', 22.55, A, gl('spotify'), 'Membresías de podcast', ring=(N(K((0, 0), (24.5, 34, 1.2))), K((0, 0), (24.5, 100, 1.2))),
          btn=('Siguiente', 35.8),
          mL=('Regiones', N(K((0, 0), (24.5, 34, 1.2))), 24.5), mR=('Spotify se queda', N(K((0, 0), (29.5, 10, 1.0)), suf=' %'), 29.5),
          bar=K((0, 0), (24.5, 60, 1.2), (29.5, 100, 1.0)),
          cols=[('Para', 'podcasts', 27.0), ('Comisión', '10 %', 29.6), ('Además de', 'Patreon', 35.3)],
          stops=[('Si tienes', 'un podcast', 32.4), ('Otra forma', 'de cobrar', 34.0)],
          thumbs=[('🎙️', VERDE, 32.4), ('💸', VERDE, 34.0)])
escena('e01-podcast', S, 36.3, 'fin', '',
       f"""<div class="p1">{st([('Membresías de<br><em>podcast</em>', 22.5, 31.5), ('Otra forma<br>de <em>cobrar</em>', 31.6, None)], S, 88)}{baraja(CYT, TK, A, 22.7, SIG[1])}{c1}</div>""",
LIB + r"""const mc=R.mic(230);R.scene.add(mc);
return t=>{const a=R.eb(R.k(t,22.8,.9));mc.scale.setScalar(Math.max(.001,a));R.at(mc,540,1660+10*Math.sin(t*1.5),2);
 mc.rotation.set(.12+.05*Math.sin(t*1.2),(1-a)*3+.5*Math.sin(t*.8),.08*Math.sin(t*.9));mc.userData.led.material.emissiveIntensity=1+.8*Math.abs(Math.sin(t*3))}""")

# ───────── 0:36 · #02 DeepSeek publica su framework de inferencia; lo más movido del día en Hacker News
S = 36.3; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 2, 36.45, A, gl('deepseek'), 'DeepSeek · inferencia', ring=('⚡', K((0, 0), (39.6, 100, 1.2))),
          btn=('Siguiente', 44.5),
          mL=('Publicó un', '<b>framework</b>', 38.7), mR=('De', '<b>alto rendimiento</b>', 41.6),
          bar=K((0, 0), (39.6, 100, 1.4)),
          cols=[('Qué', 'inferencia', 40.6), ('', '', None), ('Para', 'sus propios modelos', 43.0)],
          stops=[('Del lado de', 'los modelos', 36.8), ('Corre', 'sus modelos', 43.3)],
          thumbs=[('🐋', AZUL, 38.0), ('🚀', AZUL, 41.6)])
c2 = tray(TX, CYT, TW, TK, 'amb', 45.0, A, gl('ycombinator'), 'Hacker News', ring=('🔥', K((0, 0), (46.4, 100, 1.0))),
          mL=('Puntos', N(K((0, 0), (48.3, 2000, 1.2)), f='c'), 48.3), mR=('Comentarios', N(K((0, 0), (50.2, 700, 1.0))) + '+', 50.2),
          bar=K((0, 0), (48.3, 70, 1.2), (50.2, 100, 1.0)),
          cols=[('Fue', 'lo más movido', 46.5), ('', '', None), ('Del', 'día', 47.3)])
escena('e02-deepseek', S, 52.3, 2, fase(1, 0, A(44.7)) + fase(2, A(44.8)),
       f"""<div class="p1">{st([('<em>DeepSeek</em> publica<br>su motor', 36.4, 39.5), ('Inferencia de<br><em>alto rendimiento</em>', 39.6, None)], S, 86)}{baraja(CYT, TK, A, 36.6, SIG[2])}{c1}</div>
<div class="p2">{st([('Lo más <em>movido</em><br>del día', 44.9, None)], S, 88)}{baraja(CYT, TK, A, 45.1, SIG[2])}{c2}</div>""",
LIB + "const DS=" + js(G.svgpath('deepseek')) + ",YC=" + js(G.svgpath('ycombinator')) + r""";
const ds=R.shape(DS,280,3,R.gloss('#4d6bfe',{emissive:'#4d6bfe',emissiveIntensity:.2,roughness:.16,metalness:.3}),.6);R.scene.add(ds);
const yc=R.shape(YC,220,4,R.gloss('#ff6600',{emissive:'#ff6600',emissiveIntensity:.2,roughness:.16}),.6);R.scene.add(yc);
return t=>{const a=R.eb(R.k(t,36.8,.9)),o=R.eo(R.k(t,44.4,.4)),b=R.eb(R.k(t,45.3,.8)),hot=R.k(t,48.3,3.0);
 ds.visible=t<44.9;ds.scale.setScalar(Math.max(.001,a*(1-o)));R.at(ds,540,1660+10*Math.sin(t*1.4),2);ds.rotation.set(.15+.05*Math.sin(t*1.1),(1-a)*3+.5*Math.sin(t*.8)+R.eio(R.k(t,39.6,1.2))*6.283,0);
 yc.visible=t>45.2;yc.scale.setScalar(Math.max(.001,b*(1+.12*Math.sin(Math.PI*hot))));R.at(yc,540,1660+10*Math.sin(t*1.5),2);yc.rotation.set(.15,(1-b)*3+.45*Math.sin(t*.9),0);
 yc.material.emissiveIntensity=.2+.5*hot}""")

# ───────── 0:52 · #02 (parte 2): el mismo día que EE. UU. lo veta en sus agencias; si lo alojas, revisa el repo oficial
S = 52.3; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 1, 52.45, A, em('🏛️'), 'El mismo día', ring=('🚫', K((0, 0), (55.5, 100, 1.0))),
          btn=('Siguiente', 57.9),
          mL=('Estados Unidos', '<b>lo veta</b>', 55.5), mR=('En sus', '<b>agencias</b>', 56.5),
          bar=K((0, 0), (55.5, 100, 1.2)), ac0='#ff4d5e',
          cols=[('Dónde', 'agencias federales', 56.6), ('', '', None), ('Qué', 'DeepSeek', 57.2)])
c2 = tray(TX, CYT, TW, TK, 'gris', 58.4, A, gl('github'), 'Si lo alojas tú', ring=('✓', K((0, 0), (63.3, 100, 1.0))),
          btn=('Siguiente', 67.6),
          mL=('Revisa el', '<b>repo oficial</b>', 63.3), mR=('Marca', 'cómo <b>desplegar</b>', 66.4),
          bar=K((0, 0), (60.1, 40, .8), (63.3, 100, .8)),
          cols=[('Si corres', 'DeepSeek', 59.0), ('O piensas', 'alojarlo', 60.0), ('Revisa', 'el repositorio', 63.6)],
          stops=[('Antes de', 'desplegar', 64.6), ('Sigue', 'lo oficial', 66.5)],
          thumbs=[('📦', GRIS, 64.6), ('🚀', GRIS, 66.5)])
escena('e03-eeuu', S, 68.3, 1, fase(1, 0, A(58.1)) + fase(2, A(58.2)),
       f"""<div class="p1">{st([('Y el mismo <em>día</em>…', 52.4, 54.3), ('EE. UU. lo <em>veta</em>', 54.4, None)], S, 88)}{c1}
 {below('🚫 vetado en agencias federales', 1420, 56.8, A, 'pill bad', '--r:-3deg;')}</div>
<div class="p2">{st([('¿Lo vas a<br><em>alojar</em>?', 58.3, 62.8), ('Revisa el<br><em>repo oficial</em>', 62.9, None)], S, 88)}{baraja(CYT, TK, A, 58.5, SIG[2])}{c2}</div>""",
LIB + "const SH=" + js(D.SHIELD) + ",GH=" + js(G.svgpath('github')) + r""";
const sh=R.shape(SH,230,5,R.gloss('#8d96a8',{emissive:'#ff2a3a',emissiveIntensity:0,roughness:.16}));R.scene.add(sh);
const gh=R.shape(GH,230,3,R.metal('#e8ecf3',{roughness:.16}),.5);R.scene.add(gh);
return t=>{const a=R.eb(R.k(t,52.8,.9)),o=R.eo(R.k(t,57.8,.4)),b=R.eb(R.k(t,58.7,.8)),v=R.k(t,55.5,.6);
 sh.visible=t<58.2;sh.scale.setScalar(Math.max(.001,a*(1-o)));R.at(sh,540+(v>0&&v<1?Math.sin(t*40)*10:0),1650+10*Math.sin(t*1.4),2);sh.rotation.set(.15,(1-a)*3+.4*Math.sin(t*1.1),0);
 sh.material.color.set(v>.5?'#ff8a8a':'#8d96a8');sh.material.emissiveIntensity=.45*v;
 gh.visible=t>58.6;gh.scale.setScalar(Math.max(.001,b));R.at(gh,540,1660+10*Math.sin(t*1.5),2);gh.rotation.set(.15,(1-b)*3+.45*Math.sin(t*.9)+R.eio(R.k(t,63.3,.8))*6.283,0)}""")

# ───────── 1:08 · #03 Mistral anuncia Voxtral 3; aún sin detalles, 360 puntos en HN → alternativa abierta o barata
S = 68.3; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'amb', 68.45, A, gl('mistralai'), 'Mistral · Voxtral 3', ring=('3', K((0, 0), (74.3, 100, 1.0))),
          btn=('Siguiente', 80.6),
          mL=('Laboratorio', '<b>europeo</b>', 72.0), mR=('Anunció', '<b>Voxtral 3</b>', 74.3),
          bar=K((0, 0), (72.0, 40, .8), (74.3, 100, .8)),
          cols=[('Fuera de', 'EE. UU.', 69.7), ('Dónde', 'sitio oficial', 75.6), ('Detalles', 'aún no', 78.9)],
          stops=[('De', 'referencia', 72.7), ('Lo que trae', 'sin detallar', 79.6)],
          thumbs=[('🇪🇺', AMB, 72.0), ('❓', AMB, 79.6)])
c2 = tray(TX, CYT, TW, TK, 'amb', 81.1, A, gl('ycombinator'), 'Hacker News', ring=(N(K((0, 0), (82.8, 360, 1.2))), K((0, 0), (82.8, 100, 1.2))),
          btn=('Siguiente', 92.6),
          mL=('Puntos', '~' + N(K((0, 0), (82.8, 360, 1.2))), 82.8), mR=('Comentarios', '~' + N(K((0, 0), (84.2, 100, 1.0))), 84.2),
          bar=K((0, 0), (82.8, 60, 1.2), (84.2, 100, 1.0)),
          cols=[('Buscas', 'alternativas', 87.3), ('Abiertas', 'o más baratas', 88.9), ('Para', 'tus proyectos', 89.8)],
          stops=[('Vale la pena', 'darle una revisada', 91.0)],
          thumbs=[('🔍', AMB, 91.0)])
escena('e04-mistral', S, 93.3, 'amb', fase(1, 0, A(80.8)) + fase(2, A(80.9)),
       f"""<div class="p1">{st([('<em>Mistral</em> anuncia<br>Voxtral 3', 68.4, 77.3), ('Aún sin<br><em>detalles</em>', 77.4, None)], S, 88)}{baraja(CYT, TK, A, 68.6, SIG[3])}{c1}</div>
<div class="p2">{st([('¿Buscas una<br><em>alternativa</em>?', 81.0, None)], S, 88)}{baraja(CYT, TK, A, 81.2, SIG[3])}{c2}</div>""",
LIB + "const MI=" + js(G.svgpath('mistralai')) + r""";
const mi=R.shape(MI,260,3,R.gloss('#ff7000',{emissive:'#ff8a1a',emissiveIntensity:.25,roughness:.16,metalness:.25}),.5);R.scene.add(mi);
return t=>{const a=R.eb(R.k(t,68.8,.9)),p=R.eio(R.k(t,74.3,1.0)),q=R.eio(R.k(t,80.6,.8));mi.scale.setScalar(Math.max(.001,a*(1-.15*q)));
 R.at(mi,540,1660+10*Math.sin(t*1.4),2);mi.rotation.set(.15+.05*Math.sin(t*1.1),(1-a)*3+.5*Math.sin(t*.8)+p*6.283+q*6.283,0)}""")

# ───────── 1:33 · #04 OpenAI: sus modelos ya manejan mejor COBOL para migrar bancos; sin cifras; COBOL sigue en la banca
S = 93.3; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'gris', 93.45, A, gl('openai'), 'OpenAI · COBOL', ring=('↗', K((0, 0), (97.1, 100, 1.0))),
          btn=('Siguiente', 101.2),
          mL=('Maneja mejor', '<b>COBOL</b>', 97.1), mR=('Para', '<b>bancos</b>', 98.9),
          bar=K((0, 0), (97.1, 50, .8), (99.8, 100, .8)),
          cols=[('Lenguaje', 'COBOL', 97.3), ('Ayuda a', 'migrar', 99.5), ('Programas', 'viejos', 100.7)],
          stops=[('Asegura', 'la empresa', 95.0), ('Migrar', 'sistemas viejos', 99.8)],
          thumbs=[('🏦', GRIS, 98.9), ('💾', GRIS, 100.7)])
c2 = tray(TX, CYT, TW, TK, 'gris', 101.7, A, em('📣'), 'Lo dice la empresa', ring=('?', K((0, 100), (104.5, 0, .8))),
          btn=('Siguiente', 108.3),
          mL=('Cifras', '<b>ninguna</b>', 104.5), mR=('COBOL', 'en la <b>banca</b>', 107.4),
          bar=K((0, 100), (104.5, 0, .8)), ac0='#ff4d5e',
          cols=[('Datos', 'sin cifras', 104.7), ('', '', None), ('Aún así', 'corazón de la banca', 107.5)])
escena('e05-cobol', S, 108.8, 'gris', fase(1, 0, A(101.4)) + fase(2, A(101.5)),
       f"""<div class="p1">{st([('<em>OpenAI</em> y el<br>COBOL', 93.4, 99.0), ('Migrar los<br><em>bancos</em>', 99.1, None)], S, 88)}{baraja(CYT, TK, A, 93.6, SIG[4])}{c1}</div>
<div class="p2">{st([('Ojo: <em>sin cifras</em>', 101.6, 105.6), ('COBOL sigue en<br>la <em>banca</em>', 105.7, None)], S, 88)}{c2}
 {below('📣 lo dice la propia empresa', 1420, 102.3, A, 'pill', '--r:-3deg;')}</div>""",
LIB + "const OA=" + js(G.svgpath('openai')) + r""";
const oa=R.shape(OA,250,3,R.metal('#e8ecf3',{roughness:.14}),.5);R.scene.add(oa);const bk=R.bank(250);R.scene.add(bk);
return t=>{const a=R.eb(R.k(t,93.8,.9)),o=R.eo(R.k(t,98.6,.4)),b=R.eb(R.k(t,98.9,.8));
 oa.visible=t<99.1;oa.scale.setScalar(Math.max(.001,a*(1-o)));R.at(oa,540,1660+10*Math.sin(t*1.4),2);oa.rotation.set(.15,(1-a)*3+.5*Math.sin(t*.8),-t*.3);
 bk.visible=t>98.8;bk.scale.setScalar(Math.max(.001,b));R.at(bk,540,1670+8*Math.sin(t*1.3),2);bk.rotation.set(.18+.04*Math.sin(t*1.1),(1-b)*3-.4+.35*Math.sin(t*.7),0)}""")

# ───────── 1:48 · #04 (parte 2): si la IA lo traduce bien cambia el trabajo y la demanda → ojo si te dedicas a sistemas heredados
S = 108.8; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'gris', 108.95, A, em('🤖'), 'Si la IA traduce bien', ring=(N(K((0, 0), (112.1, 1, .3), (115.6, 2, .3))) + '/2', K((0, 0), (112.1, 50, .5), (115.6, 100, .5))),
          btn=('Siguiente', 118.0),
          mL=('Cambia', 'la <b>modernización</b>', 112.1), mR=('Y la', '<b>demanda</b>', 115.6),
          bar=K((0, 0), (112.1, 50, .6), (115.6, 100, .6)),
          cols=[('COBOL', '→ código nuevo', 110.2), ('', '', None), ('Quienes', 'lo programan', 116.8)])
c2 = tray(TX, CYT, TW, TK, 'gris', 118.4, A, em('🧭'), 'Sistemas heredados', ring=('👀', K((0, 0), (121.0, 100, 1.0))),
          mL=('Si te', '<b>dedicas</b> a esto', 119.4), mR=('Ojo con', 'cómo <b>se mueve</b>', 121.2),
          bar=K((0, 0), (119.4, 50, .8), (121.2, 100, .8)),
          cols=[('Hoy', 'COBOL', 119.6), ('', '', None), ('Mañana', '¿IA?', 121.5)])
escena('e06-heredados', S, 123.0, 'gris', fase(1, 0, A(118.2)) + fase(2, A(118.3)),
       f"""<div class="p1">{st([('Si la IA lo<br><em>traduce bien</em>', 108.9, 114.6), ('Cambia la<br><em>demanda</em>', 114.7, None)], S, 88)}{baraja(CYT, TK, A, 109.1, SIG[4])}{c1}</div>
<div class="p2">{st([('¿Te dedicas a<br><em>sistemas viejos</em>?', 118.3, None)], S, 86)}{baraja(CYT, TK, A, 118.5, SIG[4])}{c2}</div>""",
LIB + r"""const pc=R.punch(300);R.scene.add(pc);const rb=R.robot(170);R.scene.add(rb);
return t=>{const a=R.eb(R.k(t,109.2,.9)),b=R.eb(R.k(t,110.2,.8)),m=R.eio(R.k(t,118.1,.8));
 pc.scale.setScalar(Math.max(.001,a));R.at(pc,R.mix(540,360,b),1680+8*Math.sin(t*1.4),1);pc.rotation.set(.2+.05*Math.sin(t*1.1),-.3+.25*Math.sin(t*.8),.05);
 rb.visible=t>110;rb.scale.setScalar(Math.max(.001,b));R.at(rb,R.mix(540,760,b),1630+8*Math.sin(t*1.6),2);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),-.5+.3*Math.sin(t*.9)+m*6.283,0);rb.userData.em.emissiveIntensity=1.4+.6*Math.sin(t*3)}""")

# ───────── 2:03 · cierre: ¿le darías chance a una IA de migrar tu sistema? (arriba entra «Sígueme»)
S = 123.0; A = G.at(S)
OPC = []
for i, (pal, ico, nm, l, r, fin, t0) in enumerate([(3, em('✅'), 'Sí, con revisión', ('Migra', '<b>la IA</b>'), ('Revisa', '<b>un humano</b>'), 62, 124.6),
                                                   (1, em('🙅'), 'Mejor no', ('Mi sistema', '<b>no se toca</b>'), ('Riesgo', '<b>alto</b>'), 38, 125.9)]):
    OPC.append(tray(TX, 640 + i * 400, TW, 1.75, pal, t0, A, ico, nm, ring=(f'<b data-n=\'{K((0, 0), (126.7, fin, 1.0))}\' data-f="p">0%</b>', K((0, 0), (126.7, fin, 1.0))),
                    mL=(l[0], l[1], None), mR=(r[0], r[1], None), bar=K((0, 0), (126.7, fin, 1.0))))
SEG_INI = 128.2
escena('e07-cierre', S, FIN, 0, fase(1, 0, A(128.0)),
       f"""<div class="p1">{st([('¿Dejarías que una<br>IA <em>migre</em> tu sistema?', 123.1, None)], S, 80)}{''.join(OPC)}</div>""",
LIB + r"""const bk=R.bank(140);R.scene.add(bk);
const tx=R.text('EL LOG',140,60,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,126.0,.85)),o=R.eo(R.k(t,127.8,.4));
 bk.visible=t>125.8&&t<128.3;bk.scale.setScalar(Math.max(.001,a*(1-o)));R.at(bk,540,1640,3);bk.rotation.set(.15,t*1.0,0);
 const c=R.eb(R.k(t,128.3,.8));tx.visible=t>128.2;tx.scale.setScalar(Math.max(.001,c));R.at(tx,540,1450+(1-c)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}""",
sigue=False)

# ───────── tarjeta «Sígueme» (misma de #06 con la pregunta de esta semana)
SEGUIR = M.SEGUIR.replace('🔑 ¿Le darías tu cartera a un agente?', '🏦 ¿Una IA migrando tu sistema?') \
                 .replace('--n:27;', '--n:26;').replace('Solo con permisos mínimos 🔒', 'Sí, pero con revisión 👀')
_d0, _d1 = round(M.FIN - M.SEG_INI, 2), round(FIN - SEG_INI, 2)
SEGUIR = SEGUIR.replace(f'R.D={_d0};', f'R.D={_d1};').replace(f'--out:{_d0 - 0.45:.2f}s', f'--out:{_d1 - 0.45:.2f}s')

_bank = LIB[LIB.index('R.bank='):LIB.index('R.punch=')]
assert 'const lk=R.lock(130);' in SEGUIR
SEGUIR = SEGUIR.replace('const lk=R.lock(130);', _bank + 'const lk=R.bank(120);')
PIEZAS.append(('seguir', SEG_INI, FIN, SEGUIR))
PIEZAS.append(('cinta', 0.0, FIN, D.cinta()))  # al final: queda encima de todo
PRE = 'ell7-'
OUT, WORK, CAP = M.OUT, M.WORK, M.CAP

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
        rel = os.environ.get('REL', 'noticias/7/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
