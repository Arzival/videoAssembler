"""El Log #08 · diseño «Trayecto» con la cinta de noticiero arriba. Semana de una sola noticia (PHP2Shell) partida en capítulos.
Reutiliza los ayudantes de ellog-06-trayecto.py (tray, baraja, escena, contadores) y solo cambia guion y tiempos.
Tiempos = voz recortada de noticias/8 (voz/voz-norm.wav, 97.46 s). Necesita internet al capturar.
Uso: SALIDA=noticias/8/animaciones REL=noticias/8/animaciones python3 ejemplos/ellog-08-trayecto.py [ids…]   (SOLO_HTML=1 para revisar)
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
PHPV = '#7a86e0'

FIN = 97.46
M.PIEZAS = []
PIEZAS = M.PIEZAS
D.FIN = FIN
D.NOTICIAS = [(0.0, 1, '01', 'PHP: dos fallos críticos en alerta'),
              (17.0, 0, '02', 'Parche de seguridad: 9.2 de 10'),
              (32.85, 1, '03', 'PHP2Shell: ejecución remota de código'),
              (45.4, 'amb', '04', 'Millones de sitios en alerta'),
              (63.5, 2, '05', 'La IA ya encuentra estos fallos'),
              (76.6, 'fin', '06', 'Corre php -v y actualiza'),
              (91.1, 0, '✓', '¿Cada cuánto actualizas tu servidor?')]
D.CORRIDO = ['PHP 8.5.12, 8.4.27, 8.3.36 y 8.2.35 corrigen los dos fallos', 'CVE-2026-109618 y CVE-2026-109619: 9.2 de 10 en CVSS v4',
             'Permiten ejecutar código en el servidor sin iniciar sesión', 'Parche de emergencia: salió un día antes por una filtración',
             'Los encontraron investigadores de Calif, Wiz y OpenAI', 'Wiz: los modelos de IA bajaron la barrera para armar el ataque',
             'Hacker News: lo de Países Bajos aún no está confirmado', 'Revisa tu versión: php -v']

LIB = M.LIB + r"""
R.keyb=(w)=>{const G=R.group();G.add(R.rbox(w,w*.4,w*.06,w*.03,R.gloss('#1b1e26',{roughness:.3})));const km=R.gloss('#e8ecf3',{roughness:.35}),ks=[];
 for(let r=0;r<4;r++)for(let c=0;c<11;c++){const k=R.rbox(w*.07,w*.07,w*.03,w*.012,km);k.position.set(R.u(-w*.4+c*w*.08+(r%2)*w*.02),R.u(w*.12-r*w*.08),R.u(w*.04));G.add(k);ks.push(k)}
 const sp=R.rbox(w*.5,w*.07,w*.03,w*.012,km);sp.position.set(0,R.u(-w*.2+w*.03),R.u(w*.04));G.add(sp);G.userData.ks=ks;G.userData.km=km;return G};
R.globe=(w)=>{const G=R.group();G.add(new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.42),48,32),R.gloss('#2a1806',{emissive:'#ffb340',emissiveIntensity:.15,roughness:.25})));
 const wf=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.43),18,12),R.metal('#ffcf7a',{wireframe:true}));G.add(wf);
 const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(w*.58),R.u(w*.02),16,80),R.metal('#ffe6c2'));ring.rotation.x=Math.PI/2.3;G.add(ring);G.userData.wf=wf;return G};
"""

SIG = {
    1: [('🛡️', 'El parche', '0:17', 0), ('💻', 'PHP2Shell', '0:33', 1)],
    2: [('💻', 'PHP2Shell', '0:33', 1), ('🌐', 'Sitios en alerta', '0:45', 'amb')],
    3: [('🌐', 'Sitios en alerta', '0:45', 'amb'), ('🤖', 'La IA', '1:03', 2)],
    4: [('🤖', 'La IA', '1:03', 2), ('🖥️', 'Tu versión', '1:16', 'fin')],
    5: [('🖥️', 'Tu versión', '1:16', 'fin'), ('💬', 'Tu opinión', '1:31', 0)],
    6: [('💬', 'Tu opinión', '1:31', 0)],
}

# ───────── 0:00 · «Dicen que PHP está muerto», dos fallos críticos; si tienes Laravel/WordPress/PHP te toca actualizar
S = 0.0; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 1, 0.2, A, gl('php'), 'PHP · alerta', ring=(N(K((0, 0), (1.8, 2, .5))), K((0, 0), (1.8, 100, .8))),
          btn=('Siguiente', 4.7),
          mL=('Fallos', N(K((0, 0), (1.8, 2, .5))) + ' <b>críticos</b>', 2.0), mR=('Internet', 'en <b>alerta</b>', 4.2),
          bar=K((0, 0), (1.8, 100, 1.0)), ac0='#ff4d5e',
          cols=[('Dicen que', 'está muerto', 0.9), ('', '', None), ('Hoy', 'en alerta', 4.2)])
c2 = tray(TX, CYT, TW, TK, 1, 5.2, A, em('📦'), 'Si tienes un proyecto en…', ring=('!', K((0, 0), (9.8, 100, .8))),
          btn=('Siguiente', 10.5),
          mL=('Te toca', '<b>actualizar</b>', 9.8), mR=('Cuándo', '<b>ahorita</b>', 9.2),
          bar=K((0, 0), (6.6, 33, .5), (7.2, 66, .5), (8.8, 100, .5)),
          cols=[('Framework', 'Laravel', 6.6), ('CMS', 'WordPress', 7.2), ('O cualquier', 'cosa en PHP', 8.8)])
escena('e00-alerta', S, 10.9, 1, fase(1, 0, A(5.0)) + fase(2, A(5.1)),
       f"""<div class="p1">{st([('Dicen que PHP<br>está <em>muerto</em>…', 0.3, 1.7), ('Dos fallos<br><em>críticos</em>', 1.8, None)], S, 88)}{baraja(CYT, TK, A, 0.6, SIG[1])}{c1}</div>
<div class="p2">{st([('¿Laravel, WordPress<br>o <em>PHP</em>?', 5.2, 9.1), ('Te toca<br><em>actualizar</em>', 9.2, None)], S, 86)}{baraja(CYT, TK, A, 5.3, SIG[1])}{c2}</div>""",
LIB + "const PH=" + js(G.svgpath('php')) + ",LV=" + js(G.svgpath('laravel')) + ",WP=" + js(G.svgpath('wordpress')) + r""";
const ph=R.shape(PH,300,3,R.gloss('#7a86e0',{emissive:'#ff2a3a',emissiveIntensity:0,roughness:.16,metalness:.25}),.5);R.scene.add(ph);
const lv=R.shape(LV,190,3,R.gloss('#ff2d20',{emissive:'#ff2d20',emissiveIntensity:.2,roughness:.16}),.5);R.scene.add(lv);
const wp=R.shape(WP,190,3,R.metal('#e8ecf3',{roughness:.16}),.5);R.scene.add(wp);
return t=>{const a=R.eb(R.k(t,.5,.9)),al=R.k(t,1.8,.3),m=R.eio(R.k(t,6.3,.8)),l=R.eb(R.k(t,6.6,.7)),w=R.eb(R.k(t,7.2,.7));
 ph.scale.setScalar(Math.max(.001,a*(1-.35*m)));R.at(ph,540+(al>0&&al<1?Math.sin(t*40)*10:0),1650+10*Math.sin(t*1.4)-m*60,2);ph.rotation.set(.15+.05*Math.sin(t*1.1),(1-a)*3+.45*Math.sin(t*.8),0);
 ph.material.emissiveIntensity=t>1.8?.25+.2*Math.abs(Math.sin(t*3)):0;
 lv.visible=t>6.5;lv.scale.setScalar(Math.max(.001,l));R.at(lv,320,1720+8*Math.sin(t*1.5),2);lv.rotation.set(.15,(1-l)*3+.4*Math.sin(t*.9),0);
 wp.visible=t>7.1;wp.scale.setScalar(Math.max(.001,w));R.at(wp,760,1720+8*Math.sin(t*1.3),2);wp.rotation.set(.15,(1-w)*3-.4*Math.sin(t*.9),0)}""")

# ───────── 0:11 · uno de los fallos se llama PHP2Shell y lo encontraron con ayuda de IA
S = 10.9; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 1, 11.05, A, em('🐚'), 'Uno de los fallos', ring=('🤖', K((0, 0), (15.6, 100, .9))),
          btn=('Siguiente', 16.6),
          mL=('Se llama', '<b>PHP2Shell</b>', 13.6), mR=('Lo encontraron', 'con <b>IA</b>', 15.8),
          bar=K((0, 0), (13.6, 50, .6), (15.8, 100, .6)),
          cols=[('Nombre', 'PHP2Shell', 14.1), ('', '', None), ('Ayudó', 'la IA', 16.3)])
escena('e01-php2shell', S, 17.0, 1, '',
       f"""<div class="p1">{st([('Lo llamaron<br><em>PHP2Shell</em>', 11.0, 14.6), ('Lo encontraron<br>con <em>IA</em>', 14.7, None)], S, 86)}{baraja(CYT, TK, A, 11.2, SIG[1])}{c1}</div>""",
LIB + r"""const rb=R.robot(190);R.scene.add(rb);
return t=>{const a=R.eb(R.k(t,11.3,.9)),s=R.eio(R.k(t,15.6,1.0));rb.scale.setScalar(Math.max(.001,a));R.at(rb,540,1640+10*Math.sin(t*1.5),2);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),(1-a)*3-.3+.3*Math.sin(t*.9)+s*6.283,0);rb.userData.em.emissiveIntensity=1.4+.6*Math.sin(t*3)}""")

# ───────── 0:17 · el equipo de PHP sacó hoy una versión de seguridad: 2 fallos con 9.2; la escala va de 0 a 10 → casi lo máximo
S = 17.0; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 0, 17.15, A, gl('php'), 'Versión de seguridad', ring=('9.2', K((0, 0), (24.1, 92, 1.0))),
          btn=('Siguiente', 25.0),
          mL=('Sacada', '<b>hoy</b>', 18.8), mR=('Corrige', N(K((0, 0), (21.7, 2, .4))) + ' <b>fallos</b>', 21.7),
          bar=K((0, 0), (19.3, 40, .8), (24.1, 92, 1.0)),
          cols=[('Quién', 'equipo de PHP', 18.2), ('Qué', 'parche', 20.1), ('Calificación', '9.2', 24.1)])
c2 = tray(TX, CYT, TW, TK, 0, 25.5, A, em('🌡️'), '¿Qué tan grave?', ring=('9.2', K((0, 0), (29.2, 92, 1.0))),
          btn=('Siguiente', 32.4),
          mL=('La escala va', 'del <b>0 al 10</b>', 26.8), mR=('Estos fallos', '<b>9.2</b>', 29.2),
          bar=K((0, 0), (26.8, 10, .4), (27.1, 100, .6), (29.2, 92, .8)), ac0='#ff4d5e',
          cols=[('0', 'nada grave', 26.8), ('', '', None), ('10', 'lo máximo', 27.1)])
escena('e02-parche', S, 32.85, 0, fase(1, 0, A(25.2)) + fase(2, A(25.3)),
       f"""<div class="p1">{st([('PHP saca un<br><em>parche</em> hoy', 17.1, 21.6), ('Dos fallos<br>de <em>9.2</em>', 21.7, None)], S, 88)}{baraja(CYT, TK, A, 17.3, SIG[2])}{c1}</div>
<div class="p2">{st([('Del <em>0 al 10</em>…', 25.4, 30.0), ('Casi lo<br><em>máximo</em>', 30.1, None)], S, 88)}{c2}
 {below('🔥 casi lo máximo', 1420, 31.6, A, 'pill bad', '--r:-3deg;')}</div>""",
LIB + "const SH=" + js(D.SHIELD) + r""";
const sh=R.shape(SH,250,5,R.gloss('#7a86e0',{emissive:'#7a86e0',emissiveIntensity:.15,roughness:.16,metalness:.3}));R.scene.add(sh);
return t=>{const a=R.eb(R.k(t,17.5,.9)),p=R.eio(R.k(t,24.1,1.0)),h=R.k(t,29.2,1.2);sh.scale.setScalar(Math.max(.001,a*(1+.08*Math.sin(Math.PI*h))));
 R.at(sh,540,1660+10*Math.sin(t*1.4),2);sh.rotation.set(.15+.05*Math.sin(t*1.1),(1-a)*3+.45*Math.sin(t*.8)+p*6.283,0);
 sh.material.color.set(t>29.2?'#ff8a8a':'#7a86e0');sh.material.emissive.set(t>29.2?'#ff2a3a':'#7a86e0');sh.material.emissiveIntensity=t>29.2?.2+.3*h:.15}""")

# ───────── 0:33 · PHP2Shell = ejecución remota de código: alguien de afuera corre comandos en tu servidor → tu teclado a un desconocido
S = 32.85; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 1, 33.0, A, em('💻'), 'PHP2Shell', ring=('⚠', K((0, 0), (36.6, 100, .9))),
          btn=('Siguiente', 42.3),
          mL=('Ejecución', '<b>remota</b>', 36.0), mR=('De', '<b>código</b>', 36.6),
          bar=K((0, 0), (36.0, 40, .6), (40.9, 100, .8)), ac0='#ff4d5e',
          cols=[('Desde', 'afuera', 38.8), ('Corre', 'sus comandos', 40.9), ('En', 'tu servidor', 41.6)],
          stops=[('Alguien', 'de afuera', 38.0), ('Entra a', 'tu servidor', 41.6)],
          thumbs=[('🕵️', CORAL, 38.8), ('🖥️', CORAL, 41.6)])
c2 = tray(TX, CYT, TW, TK, 1, 42.8, A, em('⌨️'), 'Es como…', ring=('🫣', K((0, 0), (44.2, 100, .8))),
          mL=('Dejarle tu', '<b>teclado</b>', 43.5), mR=('A un', '<b>desconocido</b>', 44.2),
          bar=K((0, 0), (43.5, 50, .5), (44.2, 100, .5)), ac0='#ff4d5e',
          cols=[('Tu', 'teclado', 43.5), ('', '', None), ('Sus', 'manos', 44.2)])
escena('e03-remoto', S, 45.4, 1, fase(1, 0, A(42.5)) + fase(2, A(42.6)),
       f"""<div class="p1">{st([('Ejecución<br><em>remota</em> de código', 32.95, 37.9), ('Corre <em>comandos</em><br>en tu servidor', 38.0, None)], S, 84)}{baraja(CYT, TK, A, 33.2, SIG[3])}{c1}</div>
<div class="p2">{st([('Tu teclado a un<br><em>desconocido</em>', 42.7, None)], S, 86)}{c2}</div>""",
LIB + r"""const kb=R.keyb(380);R.scene.add(kb);const KS=kb.userData.ks;
return t=>{const a=R.eb(R.k(t,33.3,.9)),d=R.k(t,42.7,.6);kb.scale.setScalar(Math.max(.001,a));R.at(kb,540+(d>0&&d<1?Math.sin(t*40)*10:0),1650+10*Math.sin(t*1.4),2);
 kb.rotation.set(.45+.05*Math.sin(t*1.1),(1-a)*3+.35*Math.sin(t*.8),0);
 for(let i=0;i<KS.length;i++){const on=t>38&&Math.sin(t*9+i*1.7)>.82;KS[i].position.z=R.u(380*(on?.015:.04))}
 kb.userData.km.color.set(t>42.7?'#ffb3b3':'#e8ecf3')}""")

# ───────── 0:45 · no es cualquier cosa: PHP mueve millones de sitios; medios hablan de sitios en alerta; HN: Países Bajos (sin confirmar)
S = 45.4; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'amb', 45.55, A, gl('php'), 'PHP en la web', ring=('🌐', K((0, 0), (48.0, 100, 1.0))),
          btn=('Siguiente', 52.6),
          mL=('Mueve', '<b>millones</b>', 48.0), mR=('De', '<b>sitios</b>', 48.8),
          bar=K((0, 0), (48.0, 100, 1.2)),
          cols=[('No es', 'cualquier cosa', 46.5), ('', '', None), ('Medios', 'sitios en alerta', 51.5)])
c2 = tray(TX, CYT, TW, TK, 'amb', 53.0, A, gl('ycombinator'), 'Hacker News', ring=('?', K((0, 0), (57.1, 100, .9))),
          btn=('Siguiente', 63.0),
          mL=('Centro de', '<b>ciberseguridad</b>', 55.6), mR=('De', '<b>Países Bajos</b>', 57.1),
          bar=K((0, 0), (55.6, 50, .6), (58.3, 100, .6)),
          cols=[('Dicen que', 'fuera de línea', 58.3), ('', '', None), ('Por', 'usar PHP', 59.1)])
escena('e04-sitios', S, 63.5, 'amb', fase(1, 0, A(52.8)) + fase(2, A(52.9)),
       f"""<div class="p1">{st([('No es cualquier<br><em>cosa</em>', 45.5, 46.9), ('Millones de<br><em>sitios</em>', 47.0, 49.8), ('Sitios en<br><em>alerta</em>', 49.9, None)], S, 88)}{baraja(CYT, TK, A, 45.7, SIG[4])}{c1}</div>
<div class="p2">{st([('Lo que dicen en<br><em>Hacker News</em>', 53.0, 59.9), ('Ojo: aún <em>sin<br>confirmar</em>', 60.0, None)], S, 86)}{c2}
 {below('⚠️ sin confirmar', 1420, 60.2, A, 'pill bad', '--r:-3deg;')}</div>""",
LIB + "const YC=" + js(G.svgpath('ycombinator')) + r""";
const gb=R.globe(330);R.scene.add(gb);const yc=R.shape(YC,220,4,R.gloss('#ff6600',{emissive:'#ff6600',emissiveIntensity:.2,roughness:.16}),.6);R.scene.add(yc);
return t=>{const a=R.eb(R.k(t,45.8,.9)),o=R.eo(R.k(t,52.5,.4)),b=R.eb(R.k(t,53.3,.8)),q=R.k(t,60.0,.8);
 gb.visible=t<53;gb.scale.setScalar(Math.max(.001,a*(1-o)));R.at(gb,540,1650+10*Math.sin(t*1.4),2);gb.rotation.set(.2,t*.6,0);gb.userData.wf.material.color.set(t>49.9&&Math.sin(t*6)>0?'#ff6a5a':'#ffcf7a');
 yc.visible=t>53.2;yc.scale.setScalar(Math.max(.001,b));R.at(yc,540,1660+10*Math.sin(t*1.5),2);yc.rotation.set(.15,(1-b)*3+.45*Math.sin(t*.9)+(q>0&&q<1?Math.sin(t*30)*.15:0),0)}""")

# ───────── 1:03 · PHP no es malo, pero la IA ya ayuda a encontrar fallos → van a salir más seguido; actualizar ya no se deja para después
S = 63.5; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 2, 63.65, A, gl('php'), 'Que quede claro', ring=('✓', K((0, 0), (66.8, 100, .8))),
          btn=('Siguiente', 72.9),
          mL=('PHP', '<b>no es malo</b>', 66.5), mR=('La IA', '<b>encuentra fallos</b>', 69.2),
          bar=K((0, 0), (66.5, 50, .6), (69.2, 100, .6)),
          cols=[('Lenguaje', 'sigue bien', 66.8), ('Pero', 'la IA busca', 68.2), ('Y halla', 'fallos', 70.1)],
          stops=[('Van a salir', 'más seguido', 72.3)],
          thumbs=[('🔍', AZUL, 69.2), ('📈', AZUL, 72.3)])
c2 = tray(TX, CYT, TW, TK, 'gris', 73.3, A, em('⏰'), 'Actualizar', ring=('⏱', K((0, 0), (75.3, 100, .8))),
          mL=('Ya no se', 'puede <b>dejar</b>', 74.6), mR=('Para', '<b>después</b>', 75.9),
          bar=K((0, 0), (74.6, 50, .5), (75.9, 100, .5)))
escena('e05-ia', S, 76.6, 2, fase(1, 0, A(73.1)) + fase(2, A(73.2)),
       f"""<div class="p1">{st([('PHP no es<br><em>malo</em>', 63.6, 67.3), ('La <em>IA</em> ya<br>encuentra fallos', 67.4, 71.0), ('Saldrán más<br><em>seguido</em>', 71.1, None)], S, 86)}{baraja(CYT, TK, A, 63.8, SIG[5])}{c1}</div>
<div class="p2">{st([('No lo dejes para<br><em>después</em>', 73.3, None)], S, 86)}{c2}</div>""",
LIB + r"""const rb=R.robot(180);R.scene.add(rb);const mg=R.mag?R.mag(150):null;if(mg)R.scene.add(mg);
return t=>{const a=R.eb(R.k(t,64.0,.9)),b=R.eb(R.k(t,67.6,.8)),s=R.eio(R.k(t,73.2,1.0));
 rb.scale.setScalar(Math.max(.001,a));R.at(rb,R.mix(540,420,b),1640+10*Math.sin(t*1.5),2);rb.rotation.set(.1+.05*Math.sin(t*1.3),(1-a)*3-.3+.3*Math.sin(t*.9)+s*6.283,0);rb.userData.em.emissiveIntensity=1.4+.6*Math.sin(t*3);
 if(mg){mg.visible=t>67.5;mg.scale.setScalar(Math.max(.001,b));R.at(mg,720+30*Math.sin(t*1.2),1620+20*Math.sin(t*1.7),3);mg.rotation.set(.2,-.4+.3*Math.sin(t*1.1),.2*Math.sin(t*.9))}}""")

# ───────── 1:17 · si no sabes qué versión tienes: php -v y compárala con la última de tu rama (8.2.35) → PHP sigue vivo
S = 76.6; A = G.at(S)
c1 = tray(TX, CYT, TW, TK, 'fin', 76.75, A, em('🖥️'), 'En tu terminal', ring=('✓', K((0, 0), (82.3, 100, .9))),
          btn=('Siguiente', 85.8),
          mL=('Corre', '<b>php -v</b>', 80.0), mR=('Compárala con', 'la <b>última</b>', 81.8),
          bar=K((0, 0), (80.0, 50, .6), (82.3, 100, .6)),
          cols=[('Rama 8.5', '8.5.12', 83.2), ('Rama 8.4', '8.4.27', 83.5), ('Rama 8.3', '8.3.36', 83.8)],
          stops=[('Rama 8.2', '8.2.35', 84.1)],
          thumbs=[('🛡️', VERDE, 84.1)])
c2 = tray(TX, CYT, TW, TK, 0, 86.3, A, gl('php'), 'PHP sigue vivo', ring=('♥', K((0, 0), (87.2, 100, .8))),
          btn=('Siguiente', 90.6),
          mL=('No está', '<b>muerto</b>', 87.2), mR=('Hoy todos', 'lo <b>actualizan</b>', 89.8),
          bar=K((0, 0), (87.2, 50, .6), (89.8, 100, .6)))
escena('e06-version', S, 91.1, 'fin', fase(1, 0, A(86.0)) + fase(2, A(86.1)),
       f"""<div class="p1">{st([('¿Qué versión<br><em>tienes</em>?', 76.7, 79.5), ('Corre<br><em>php -v</em>', 79.6, 83.1), ('Ya con el<br><em>parche</em>', 83.2, None)], S, 88)}{baraja(CYT, TK, A, 76.9, SIG[6])}{c1}</div>
<div class="p2">{st([('PHP no está<br><em>muerto</em>', 86.2, 88.2), ('Tan vivo que hoy<br>lo <em>actualizamos</em>', 88.3, None)], S, 84)}{c2}</div>""",
LIB + "const PH=" + js(G.svgpath('php')) + r""";
const ph=R.shape(PH,300,3,R.gloss('#7a86e0',{emissive:'#7a86e0',emissiveIntensity:.15,roughness:.16,metalness:.25}),.5);R.scene.add(ph);
return t=>{const a=R.eb(R.k(t,77.0,.9)),p=R.eio(R.k(t,84.1,1.0)),v=R.k(t,87.2,1.2);ph.scale.setScalar(Math.max(.001,a*(1+.1*Math.sin(Math.PI*v))));
 R.at(ph,540,1660+10*Math.sin(t*1.4),2);ph.rotation.set(.15+.05*Math.sin(t*1.1),(1-a)*3+.45*Math.sin(t*.8)+p*6.283,0);
 ph.material.color.set(t>84.1&&t<86.2?'#7fe8b0':'#7a86e0')}""")

# ───────── 1:31 · cierre: ¿cada cuánto actualizas el servidor en tu trabajo? (arriba entra «Sígueme»)
S = 91.1; A = G.at(S)
OPC = []
for i, (pal, ico, nm, l, r, t0) in enumerate([('fin', em('📅'), 'Siempre al día', ('Reviso', '<b>cada semana</b>'), ('Parches', '<b>al salir</b>'), 92.1),
                                              (1, em('🔥'), 'Cuando algo truena', ('Actualizo', '<b>tarde</b>'), ('Riesgo', '<b>alto</b>'), 92.9)]):
    OPC.append(tray(TX, 640 + i * 400, TW, 1.75, pal, t0, A, ico, nm, ring=('?', K((0, 0), (t0 + .3, 100, 1.0))),
                    mL=(l[0], l[1], None), mR=(r[0], r[1], None), bar=K((0, 0), (t0 + .3, 100, 1.0))))
SEG_INI = 93.9
escena('e07-cierre', S, FIN, 0, fase(1, 0, A(93.7)),
       f"""<div class="p1">{st([('¿Cada cuánto actualizas<br>tu <em>servidor</em>?', 91.2, None)], S, 78)}{''.join(OPC)}</div>""",
LIB + "const PH=" + js(G.svgpath('php')) + r""";
const ph=R.shape(PH,150,3,R.gloss('#7a86e0',{emissive:'#7a86e0',emissiveIntensity:.15,roughness:.16}),.5);R.scene.add(ph);
const tx=R.text('EL LOG',140,60,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,92.0,.85)),o=R.eo(R.k(t,93.6,.4));
 ph.visible=t>91.9&&t<94.1;ph.scale.setScalar(Math.max(.001,a*(1-o)));R.at(ph,540,1640,3);ph.rotation.set(.15,t*1.0,0);
 const c=R.eb(R.k(t,94.0,.8));tx.visible=t>93.9;tx.scale.setScalar(Math.max(.001,c));R.at(tx,540,1450+(1-c)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}""",
sigue=False)

# ───────── tarjeta «Sígueme» (misma de #06 con la pregunta de esta semana; el candado queda: es de seguridad)
_txt = 'Cada semana, ya aprendí 😅'
SEGUIR = M.SEGUIR.replace('🔑 ¿Le darías tu cartera a un agente?', '🛠️ ¿Cada cuánto actualizas?') \
                 .replace('--n:27;', f'--n:{len(_txt) + 1};').replace('Solo con permisos mínimos 🔒', _txt)
_d0, _d1 = round(M.FIN - M.SEG_INI, 2), round(FIN - SEG_INI, 2)
SEGUIR = SEGUIR.replace(f'R.D={_d0};', f'R.D={_d1};').replace(f'--out:{_d0 - 0.45:.2f}s', f'--out:{_d1 - 0.45:.2f}s')
PIEZAS.append(('seguir', SEG_INI, FIN, SEGUIR))

# ───────── «breaking news»: cinta en rojo que parpadea + capa de alerta (bordes rojos que laten, destello inicial y cinta de precaución abajo)
CINTA = D.cinta()
for a, b in [('background:linear-gradient(160deg,#e9e0ff,#a78bfa);box-shadow:inset 0 2px 0 rgba(255,255,255,.6),12px 0 40px rgba(167,139,250,.35)}',
              'background:linear-gradient(160deg,#ff8a8a,#e0192f);color:#fff;box-shadow:inset 0 2px 0 rgba(255,255,255,.5),12px 0 40px rgba(255,45,72,.5);animation:lgB 1s steps(1) infinite}'
              '@keyframes lgB{50%{background:linear-gradient(160deg,#ffffff,#ffd0d0);color:#c4102a}}'),
             ('background:#ff2d48;box-shadow:0 0 0 0 rgba(255,45,72,.7)', 'background:#fff;box-shadow:0 0 0 0 rgba(255,255,255,.8)'),
             ('box-shadow:inset 0 1.5px 0 rgba(255,255,255,.22),0 26px 60px rgba(0,0,0,.55)}',
              'box-shadow:inset 0 1.5px 0 rgba(255,255,255,.22),0 26px 60px rgba(0,0,0,.55),0 0 0 3px rgba(255,45,72,.9);animation:bandA 1.2s ease-in-out infinite}'
              '@keyframes bandA{50%{box-shadow:inset 0 1.5px 0 rgba(255,255,255,.22),0 26px 60px rgba(0,0,0,.55),0 0 0 3px rgba(255,45,72,.25),0 0 50px rgba(255,45,72,.6)}}'),
             ('background:linear-gradient(90deg,rgba(167,139,250,.92),rgba(124,92,230,.92))', 'background:linear-gradient(90deg,rgba(255,92,108,.95),rgba(214,22,48,.95))'),
             ('color:#fff;background:#160b33}', 'color:#fff;background:#2a0508;white-space:nowrap}'),
             ('font-size:25px;font-weight:700;color:#160b33;', 'font-size:25px;font-weight:700;color:#fff;'),
             ('<span class="tag">ÚLTIMO</span>', '<span class="tag">⚠ ÚLTIMA HORA</span>')]:
    assert a in CINTA, a[:40]
    CINTA = CINTA.replace(a, b)

_TAPE = ['⚠ ALERTA DE SEGURIDAD', '⚠ ACTUALIZA PHP'] * 12
ALERTA = f"""<!doctype html><html><head><meta charset="utf-8">{G.FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:{G.SANS}}}
.vg{{position:absolute;inset:0;box-shadow:inset 0 0 140px 26px rgba(255,30,50,.7);opacity:.35;animation:vg 1.6s ease-in-out infinite,fin .6s ease 91.1s forwards}}
@keyframes vg{{50%{{opacity:.9}}}}
.fl{{position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,rgba(255,60,70,.0),rgba(255,30,50,.55));opacity:0;animation:fl .9s ease-out .05s,fl .9s ease-out 1.85s}}
@keyframes fl{{10%{{opacity:1}}to{{opacity:0}}}}
.tp{{position:absolute;left:-60px;right:-60px;top:1838px;height:62px;transform:rotate(-2.5deg);overflow:hidden;display:flex;align-items:center;
  background:repeating-linear-gradient(-45deg,#ffd43b 0 34px,#16130a 34px 68px);box-shadow:0 14px 40px rgba(0,0,0,.5);
  animation:tpIn .5s cubic-bezier(.22,1.2,.36,1) .2s both,fin .5s ease 91.1s forwards}}
.tp .mv{{display:flex;white-space:nowrap;font-size:27px;font-weight:800;letter-spacing:.06em;color:#16130a;animation:mv 40s linear infinite}}
.tp .mv span{{background:#ffd43b;padding:6px 18px;margin-right:30px;border-radius:6px}}
@keyframes mv{{to{{transform:translateX(-50%)}}}}
@keyframes tpIn{{from{{transform:translateX(-110%) rotate(-2.5deg)}}to{{transform:rotate(-2.5deg)}}}}
@keyframes fin{{to{{opacity:0}}}}
</style><script>window.__listo=Promise.resolve();</script></head><body>
<div class="vg"></div><div class="fl"></div>
<div class="tp"><div class="mv">{''.join(f'<span>{x}</span>' for x in _TAPE) * 2}</div></div>
</body></html>"""
PIEZAS.append(('alerta', 0.0, FIN, ALERTA))
PIEZAS.append(('cinta', 0.0, FIN, CINTA))  # al final: queda encima de todo
PRE = 'ell8-'
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
        rel = os.environ.get('REL', 'noticias/8/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
