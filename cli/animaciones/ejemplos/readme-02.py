"""El Readme #02 · RAG — estilo «Pista», propuesta «ficha» (full): la ficha Catálogo grande con el 3D dentro de su imagen.
Reutiliza todo el sistema de readme-01.py (piel, fondo de tecnología, ficha, escena, pestaña) y solo cambia guion y tiempos.
Tiempos = readme/2/voz/voz-norm.wav (132.34 s).
Uso: SALIDA=~/Documents/Videos/readme/2/pista-full python3 ejemplos/readme-02.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import importlib.util, json, os, subprocess, sys

os.environ['ESTILO'] = 'pista'
os.environ['VAR'] = 'full'
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('readme01', os.path.join(HERE, 'readme-01.py'))
M = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(M)
G, C, ic, ficha, paso, escena, fase, N, K, z = M.G, M.C, M.ic, M.ficha, M.paso, M.escena, M.fase, M.N, M.K, M.z
IMX, IMY, SC = M.IMX, M.IMY, M.SC

FIN = 132.34
M.FIN = FIN
M.PIEZAS = []
PIEZAS = M.PIEZAS
M.CODE_LN = ['## Paso 1 · prepara', 'chunks: 1 284', 'embed(chunk) → [0.12, -0.8, …]', 'top_k = 4', '$ rag index ./docs', '› busca por idea',
             'similarity: 0.91', 'git log --oneline', 'context = top_k(query)', '- [x] redes sociales', 'claude.ask(q, ctx)', '> ⚠️ ojo',
             'README.md · #02', 'tokens: 4 %', 'return answer', '$ cat chunks/017.md']
M.LIB += r"""
R.mag=r=>{const G=R.group();const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(r),R.u(r*.16),24,72),R.metal('#e8ecf3',{roughness:.12}));G.add(ring);
 const lens=new THREE.Mesh(new THREE.CircleGeometry(R.u(r),64),R.glass('#ffd2bd',{opacity:.35}));G.add(lens);
 const hd=new THREE.Mesh(new THREE.CylinderGeometry(R.u(r*.17),R.u(r*.2),R.u(r*1.3),32),MAT(C1));hd.position.set(R.u(r*1.2),R.u(-r*1.2),0);hd.rotation.z=Math.PI/4;G.add(hd);return G};
R.server=(w)=>{const G=R.group();const bm=R.gloss('#2c2b2e',{roughness:.3});const lm=R.gloss('#3ee08a',{emissive:'#3ee08a',emissiveIntensity:1});const L=[];
 for(let i=0;i<3;i++){const u=R.rbox(w,w*.3,w*.8,w*.06,bm);u.position.y=R.u((i-1)*w*.34);G.add(u);
  for(let j=0;j<3;j++){const l=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.03),16,12),lm.clone());l.position.set(R.u(-w*.36+j*w*.09),u.position.y,R.u(w*.41));G.add(l);L.push(l)}
  const s=R.rbox(w*.42,w*.05,4,2,MAT(C1));s.position.set(R.u(w*.18),u.position.y,R.u(w*.4));G.add(s)}
 G.userData.leds=L;return G};
R.book=(w)=>{const G=R.group();const cv=MAT(C1);const h=w*1.3,d=w*.32;
 const back=R.rbox(w,h,w*.05,w*.03,cv);back.position.z=R.u(-d/2);G.add(back);const front=R.rbox(w,h,w*.05,w*.03,cv);front.position.z=R.u(d/2);G.add(front);
 const sp=R.rbox(w*.08,h,d+w*.05,w*.03,cv);sp.position.x=R.u(-w/2);G.add(sp);
 const pg=R.rbox(w*.94,h*.95,d*.92,w*.02,R.gloss(C3,{roughness:.5}));pg.position.x=R.u(w*.02);G.add(pg);
 const lb=R.rbox(w*.6,w*.14,w*.02,w*.03,R.gloss(C2,{emissive:C2,emissiveIntensity:.25}));lb.position.set(R.u(w*.04),R.u(h*.22),R.u(d/2+w*.03));G.add(lb);return G};
R.chunks=(w,n=6)=>{const G=R.group(),P=[];for(let i=0;i<n;i++){const c=R.rbox(w,w*.62,w*.18,w*.08,i%3==0?MAT(C2):R.gloss(C3,{roughness:.35}));
  const ln=R.rbox(w*.6,w*.08,w*.04,w*.03,R.gloss(i%3==0?C3:C1));ln.position.set(0,R.u(w*.1),R.u(w*.1));c.add(ln);
  const l2=R.rbox(w*.42,w*.08,w*.04,w*.03,R.gloss(i%3==0?C3:'#a9a4a6'));l2.position.set(R.u(-w*.09),R.u(-w*.1),R.u(w*.1));c.add(l2);G.add(c);P.push(c)}
 G.userData.P=P;return G};
"""
M.SECC = [(0.0, '# RAG'), (4.6, '## ¿Qué es?'), (21.85, '## Paso 1 · Prepara'), (34.2, '## Paso 2 · Busca'), (39.25, '## Paso 3 · Contesta'),
          (47.0, '## Libro vs página'), (60.3, '## Mi ejemplo'), (77.3, '&gt; ⚠️ Ojo'), (99.4, '## ¿Y el contexto largo?'), (115.5, '## Funciona hoy'),
          (124.7, '## Tu turno'), (128.75, '✓ guardado')]

# ───────────────────────── 0:00 · gancho: tu IA contesta sin conocer tus datos → 3 pasos
S = 0.0; A = G.at(S)
f1 = ficha(0.15, A, 'ia-sin-tus-datos', [('bot', 'tu IA'), ('clock', 'sin contexto')], 'Te contesta sin conocer tus datos: rellena con lo que se imagina.',
           [('v', '¿tus docs?', 1.2), ('v', '¿tus notas?', 1.5), ('rd', 'inventado', 1.9), ('gr', '3 pasos', 2.6)],
           [(ic('term'), 'Chat', [(0.3, None)])],
           [('<i>›</i> ¿qué dice <em>mi contrato</em>?', [(0.3, 1.1)]), ('<i>🤖</i> <em>probablemente…</em> <i>(no lo leyó)</i>', [(1.15, 2.5)]),
            ('<i>arreglo:</i> <em>3 pasos</em>', [(2.55, None)])], dd=0.8,
           hi_in=C.chip('🤖 sin tus datos', z(30), z(30), 0.4, A))
escena('s0-gancho', S, 4.6, '', [f1], f"""const rb=R.bot({z(250)});R.scene.add(rb);
return t=>{{const a=R.eb(R.k(t,.3,.8)),sh=R.k(t,1.6,.8);rb.scale.setScalar(Math.max(.001,a));
 R.at(rb,{IMX}+(sh>0&&sh<1?Math.sin(t*40)*10:0),{IMY}+10*Math.sin(t*1.6),3);
 rb.rotation.set(.1,-.4+.3*Math.sin(t*.9)+(sh>0&&sh<1?.5*Math.sin(t*22):0),0);rb.userData.em.emissiveIntensity=sh>0&&sh<1?3.2:1.4}}""")

# ───────────────────────── 0:04 · RAG: contesta con tus datos → en vez de todos tus documentos, buscas solo lo que sirve
S = 4.6; A = G.at(S)
f1 = ficha(4.65, A, 'rag', [('file', 'Retrieval-Augmented Generation')], 'Que la IA conteste con tus datos y no con lo que se imagina.',
           [('v', 'tus datos', 8.86), ('rd', 'no imagina', 10.5)],
           [('📘', 'Concepto', [(4.8, None)])], [('<i>RAG =</i> <em>buscar</em> <i>→</i> <em>contestar</em>', [(5.9, None)])], dd=6.2)
f2 = ficha(11.1, A, 'solo-lo-que-sirve', [('folder', 'tus documentos'), ('check', 'una pregunta')],
           'En lugar de pasarle todos tus documentos, primero buscas solo lo que sirve para esa pregunta.',
           [('rd', 'todos los docs', 12.9), ('v', 'busca primero', 14.8), ('gr', 'solo eso', 19.95)],
           [('📚', 'Todo', [(11.3, 14.2)]), ('🔍', 'Buscar', [(14.3, None)])],
           [('<i>contexto:</i> <s>docs/*</s> <i>(todo)</i>', [(11.3, 14.2)]), ('<i>$</i> rag search <em>"tu pregunta"</em>', [(14.3, 19.8)]),
            ('<i>contexto:</i> <em>3 pedazos</em> <i>· nada más</i>', [(19.9, None)])], copy=(16.0, 19.0), dd=11.6,
           hi_in=paso([('📚 todos tus docs', 11.3, 14.2), ('🔍 solo lo que sirve', 14.3, None)], A))
escena('s1-rag', S, 21.85, fase(1, 0, A(10.9)) + fase(2, A(11.0)), [f1, f2],
       f"""const tx=R.tx('RAG',{z(150)},{z(60)});R.scene.add(tx);const ss=[];for(let i=0;i<5;i++){{const s=R.sheet(i==2?C2:i%2?C1:'#a9b4bf');R.scene.add(s);ss.push(s)}}
const mg=R.mag({z(70)});R.scene.add(mg);
return t=>{{const a=R.eb(R.k(t,4.9,.9)),o=R.eo(R.k(t,10.7,.4));tx.visible=t<11.2;tx.scale.setScalar(Math.max(.001,a*(1-o)));R.at(tx,{IMX},{IMY}+10*Math.sin(t*1.5),2);
 tx.rotation.set(.15+.05*Math.sin(t*1.2),(1-a)*2+.3*Math.sin(t*.9),0);
 const pk=R.eio(R.k(t,19.9,.8));
 ss.forEach((s,i)=>{{const b=R.eb(R.k(t,11.3+i*.12,.7)),out=i!=2?R.eo(R.k(t,19.9,.6)):0;s.visible=t>11.2&&out<.99;
  s.scale.setScalar(Math.max(.001,b*(1-out)*{1.5 * SC:.2f}*(i==2?1+.3*pk:1)));R.at(s,{IMX - z(170)}+i*{z(85)},{IMY + z(20)}-(i==2?pk*{z(40)}:0),2+i*.3+(i==2?pk*2:0));
  s.rotation.set(.2+.05*Math.sin(t+i),-.3+.15*Math.sin(t*.8+i)+(i==2?pk*.3:0),.1-i*.05)}});
 mg.visible=t>14.3;mg.scale.setScalar(Math.max(.001,R.eb(R.k(t,14.4,.7))));
 R.at(mg,{IMX - z(170)}+{z(85)}*R.mix(4*R.k(t,14.4,4.5),2,pk),{IMY - z(40)},6);mg.rotation.set(.2,-.3+.2*Math.sin(t),0)}}""")

# ───────────────────────── 0:21 · 3 pasos: prepara (pedazos con significado) → busca los que más se parecen → contesta solo con eso
S = 21.85; A = G.at(S)
PAS = [(21.9, 34.2), (34.26, 39.25), (39.28, None)]
f1 = ficha(21.95, A, '## 3 pasos', [('file', 'prepara · busca · contesta'), ('clock', 'en la práctica')],
           'Partes tus datos en pedazos con significado, buscas los que más se parecen a la pregunta y la IA contesta solo con eso.',
           [('v', 'pedazos pequeños', 26.47), ('gr', 'con significado', 29.14), ('cy', 'por idea', 31.42), ('rd', 'no palabra exacta', 32.94),
            ('v', 'los que más se parecen', 38.31), ('gr', 'pregunta + pedazos', 42.43), ('rd', 'solo eso', 45.76)],
           [(f'{i + 1}', n, [w]) for i, (n, w) in enumerate(zip(['Prepara', 'Busca', 'Contesta'], PAS))],
           [('<i>docs/ →</i> <em>pedazos</em>', [(22.0, 27.55)]), ('<i>pedazo 017 ›</i> <em>conserva su significado</em>', [(27.6, 29.9)]),
            ('<i>buscar:</i> <em>«cancelar plan»</em> <i>≈ «dar de baja»</i>', [(29.95, 34.2)]),
            ('<i>$</i> rag search <em>"pregunta"</em> <i>→ top 3</i>', [(34.26, 39.25)]),
            ('<i>ia(</i><em>pregunta</em><i>,</i> <em>pedazos</em><i>)</i>', [(39.28, 43.6)]), ('<i>›</i> contesta <em>usando solo eso</em> <i>✓</i>', [(43.65, None)])],
           copy=(36.0, 39.0), ih=540, dd=22.6,
           hi_in=paso([('## Paso 1 · Prepara', 22.0, 34.2), ('## Paso 2 · Busca', 34.26, 39.25), ('## Paso 3 · Contesta', 39.28, None)], A))
escena('s2-pasos', S, 47.0, '.chip.st{font-family:"JetBrains Mono",monospace}', [f1],
       f"""const sh=R.sheet(C1);R.scene.add(sh);const ch=R.chunks({z(110)},6);R.scene.add(ch);const P=ch.userData.P;const mg=R.mag({z(62)});R.scene.add(mg);
const rb=R.bot({z(150)});R.scene.add(rb);
return t=>{{const a=R.eb(R.k(t,22.3,.8)),sp=R.eio(R.k(t,25.8,1.0)),s2=R.k(t,34.3,.8),s3=R.eio(R.k(t,39.4,1.0));
 sh.visible=sp<.99;sh.scale.setScalar(Math.max(.001,a*(1-sp)*{2.2 * SC:.2f}));R.at(sh,{IMX},{IMY - z(20)}+10*Math.sin(t*1.4),3);sh.rotation.set(.2,-.3+.2*Math.sin(t*.8),.05);
 const sel=[1,3,4];
 P.forEach((p,i)=>{{const c=i%3,r=Math.floor(i/3),hit=sel.includes(i),dim=R.k(t,37.0,.6)*(hit?0:1),gx={IMX}+(c-1)*{z(150)},gy={IMY - z(50)}+(r-.5)*{z(110)};
  const tx={IMX - z(120)}+sel.indexOf(i)*{z(120)},ty={IMY + z(75)};
  const px=hit?R.mix(gx,tx,s3):gx,py=hit?R.mix(gy,ty,s3):gy;p.visible=sp>0&&!(s3>.6&&!hit);
  p.scale.setScalar(Math.max(.001,R.eb(Math.min(1,sp*1.1))*(1-dim*.35)*(1-(!hit?R.eo(R.k(t,39.3,.5)):0))));
  p.position.set((px-540)/R.PX,(960-py)/R.PX,(2+(hit&&s2>0?Math.sin(Math.PI*Math.min(1,s2))*1.2:0)));
  p.rotation.set(.15*Math.sin(t*1.1+i),.25*Math.sin(t*.9+i),.06*Math.sin(t+i))}});
 const ms=R.eb(R.k(t,34.3,.6))*(1-R.eo(R.k(t,39.2,.4)));mg.visible=t>34.2&&t<39.7;mg.scale.setScalar(Math.max(.001,ms));
 const sw=R.k(t,34.6,3.0),ci=[0,1,2,3,4,5][Math.min(5,Math.floor(sw*6))];R.at(mg,{IMX}+(ci%3-1)*{z(150)},{IMY - z(50)}+(Math.floor(ci/3)-.5)*{z(110)},6);mg.rotation.set(.2,-.3,0);
 rb.visible=t>39.5;rb.scale.setScalar(Math.max(.001,R.eb(R.k(t,39.6,.8))));R.at(rb,{IMX},{IMY - z(115)}+8*Math.sin(t*1.6),1);
 rb.rotation.set(.1,-.3+.25*Math.sin(t*.9),0);rb.userData.em.color.set(t>43.7?'#3ee08a':C2);rb.userData.em.emissive.set(t>43.7?'#3ee08a':C2)}}""")

# ───────────────────────── 0:47 · libro entero vs la página que ocupa
S = 47.0; A = G.at(S)
f1 = ficha(47.05, A, 'libro-vs-pagina', [('file', 'contexto'), ('check', 'la diferencia')],
           'Darle todo el contexto es darle un libro entero. Con RAG le das solo la página que va a ocupar.',
           [('rd', 'libro entero', 50.81), ('rd', 'que la encuentre', 52.28), ('gr', 'esa página', 56.69), ('v', 'tu pregunta', 59.36)],
           [('📕', 'Todo', [(47.2, 54.85)]), ('📄', 'RAG', [(54.9, None)])],
           [('<i>contexto:</i> <em>' + N(K((0, 1), (48.8, 412, 1.4)), '1') + '</em> <i>páginas</i>', [(47.2, 54.85)]),
            ('<i>contexto:</i> <em>1</em> <i>página · la que ocupas ✓</i>', [(54.9, None)])], dd=47.7,
           hi_in=paso([('📕 todo el libro', 47.2, 54.85), ('📄 solo esa página', 54.9, None)], A))
escena('s3-libro', S, 60.3, '', [f1], f"""const bk=R.book({z(230)});R.scene.add(bk);const pg=R.sheet(C2);R.scene.add(pg);
return t=>{{const a=R.eb(R.k(t,47.3,.9)),sh=R.k(t,51.7,2.0),o=R.eo(R.k(t,54.9,.5)),b=R.eb(R.k(t,55.2,.8));
 bk.visible=o<.99;bk.scale.setScalar(Math.max(.001,a*(1-o)));R.at(bk,{IMX}+(sh>0&&sh<1?Math.sin(t*30)*6:0),{IMY}+10*Math.sin(t*1.4),3);
 bk.rotation.set(.18,(1-a)*3-.5+.3*Math.sin(t*.8),.04);
 pg.visible=t>55.1;pg.scale.setScalar(Math.max(.001,b*{2.4 * SC:.2f}));R.at(pg,{IMX},{IMY}+10*Math.sin(t*1.5),4);pg.rotation.set(.12+.05*Math.sin(t),(1-b)*3-.25+.25*Math.sin(t*.9),.05)}}""")

# ───────────────────────── 1:00 · mi ejemplo: el homelab recaba redes y proyectos → Claude contesta solo con eso (medio RAG)
S = 60.3; A = G.at(S)
f1 = ficha(60.35, A, 'homelab/', [('cpu', 'mi servidor'), ('check', 'medio RAG')],
           'Mi homelab va recabando información de mis redes sociales y proyectos; Claude solo contesta con lo que se guardó.',
           [('v', 'medio RAG', 63.79), ('gr', 'redes sociales', 66.77), ('gr', 'proyectos', 67.51), ('cy', 'Claude', 70.11), ('rd', 'solo esos datos', 72.46)],
           [('🖥️', 'Recaba', [(60.5, 68.0)]), ('💬', 'Pregunta', [(68.05, None)])],
           [('<i>recabados:</i> <em>' + N(K((0, 0), (64.6, 1284, 3.0)), '0') + '</em> <i>registros</i>', [(60.5, 68.0)]),
            ('<i>›</i> claude: <em>¿cómo van mis redes?</em>', [(68.05, 70.4)]), ('<i>contexto =</i> <em>datos guardados</em> <i>· nada más</i>', [(70.45, None)])],
           dd=61.0,
           hi_in=paso([('🖥️ mi homelab', 60.5, 63.7), ('📥 recaba redes + proyectos', 63.75, 68.0), ('💬 Claude contesta', 68.05, None)], A))
escena('s4-ejemplo', S, 77.3, '', [f1], f"""const sv=R.server({z(220)});R.scene.add(sv);const ss=[];for(let i=0;i<4;i++){{const s=R.sheet(i%2?C1:C2);R.scene.add(s);ss.push(s)}}
return t=>{{const a=R.eb(R.k(t,60.6,.9));sv.scale.setScalar(Math.max(.001,a));R.at(sv,{IMX},{IMY}+8*Math.sin(t*1.3),2);sv.rotation.set(.25,-.5+.25*Math.sin(t*.7),0);
 sv.userData.leds.forEach((l,i)=>{{l.material.emissiveIntensity=t>64.5?.4+.9*Math.abs(Math.sin(t*4+i*1.3)):.3}});
 ss.forEach((s,i)=>{{const p=((t-64.6)/1.6+i*.25)%1,on=t>64.6&&t<68.0;s.visible=on;
  s.scale.setScalar(Math.max(.001,on?Math.sin(Math.PI*p)*{.9 * SC:.2f}:0));R.at(s,{IMX}+(i%2?1:-1)*{z(300)}*(1-p),{IMY - z(80)}+(i-1.5)*{z(40)},4);s.rotation.set(.2,.4*(i%2?-1:1),0)}})}}""")

# ───────────────────────── 1:17 · > ⚠️ Ojo: pedazos mal cortados · datos viejos · búsqueda equivocada → revisa qué encontró
S = 77.3; A = G.at(S)
f1 = ficha(77.35, A, '&gt; ⚠️ ojo', [('lock', 'cuidados'), ('check', '3')], 'Tres cuidados para que tu RAG no te conteste mal.',
           [('rd', 'pedazos mal cortados', 80.52), ('rd', 'a medias', 83.51), ('rd', 'desactualizados', 85.13), ('rd', 'ya no es cierto', 89.62),
            ('rd', 'lo que no es', 92.34), ('gr', 'revisa qué encontró', 97.61)],
           [('1', 'Cortes', [(79.5, 83.9)]), ('2', 'Al día', [(83.94, 90.7)]), ('3', 'Búsqueda', [(90.72, 96.35)]), ('✓', 'Revisa', [(96.4, None)])],
           [('<i>pedazo:</i> <em>«el plan cuesta…»</em> <i>✂ a medias</i>', [(79.5, 83.9)]), ('<i>datos:</i> <em>2024</em> <i>≠ hoy</i>', [(83.94, 90.7)]),
            ('<i>busca</i> <em>«baja»</em> <i>→ trae</i> <s>«bajar precio»</s>', [(90.72, 96.35)]), ('<i>$</i> rag search <em>--show-sources</em>', [(96.4, None)])],
           copy=(97.8, None), dd=77.9,
           hi_in=paso([('⚠️ cuidados', 77.4, 79.45), ('⚠️ 1/3 · mal cortado', 79.5, 83.9), ('⚠️ 2/3 · desactualizado', 83.94, 90.7),
                       ('⚠️ 3/3 · búsqueda errada', 90.72, 96.35), ('✓ revisa las fuentes', 96.4, None)], A))
escena('s5-ojo', S, 99.4, '', [f1], f"""const w=R.warn({z(240)});R.scene.add(w);const mg=R.mag({z(80)});R.scene.add(mg);
return t=>{{const a=R.eb(R.k(t,77.5,.9)),o=R.eo(R.k(t,96.3,.4)),b=[79.5,83.94,90.72].reduce((s,x)=>s+Math.sin(Math.PI*R.k(t,x,.5)),0);
 w.visible=o<.99;w.scale.setScalar(Math.max(.001,a*(1-o)*(1+.15*b)));R.at(w,{IMX},{IMY}+10*Math.sin(t*1.5),3);w.rotation.set(.12+.05*Math.sin(t*1.2),(1-a)*3+.4*Math.sin(t*.9),0);
 w.userData.t.material.emissiveIntensity=.15+.25*b;
 const m=R.eb(R.k(t,96.5,.8));mg.visible=t>96.4;mg.scale.setScalar(Math.max(.001,m));R.at(mg,{IMX}+{z(60)}*Math.sin(t*1.4),{IMY}+{z(30)}*Math.cos(t*1.1),5);mg.rotation.set(.2,-.3+.3*Math.sin(t),0)}}""")

# ───────────────────────── 1:39 · ¿y el contexto largo? pocos docs: pásalos todos · miles: tokens, tiempo, se pierde a la mitad
S = 99.4; A = G.at(S)
f1 = ficha(99.45, A, 'contexto-largo', [('cpu', 'modelos de hoy'), ('check', 'es cierto')],
           'Los modelos ya aguantan muchísimo contexto. Con pocos documentos, pásale todos; con miles, no.',
           [('gr', 'pocos → todos', 107.34), ('rd', 'miles', 109.12), ('rd', '+ tokens', 110.87), ('rd', '+ tiempo', 112.29), ('rd', 'se pierde a la mitad', 114.23)],
           [('📄', 'Pocos', [(99.6, 108.2)]), ('📚', 'Miles', [(108.26, None)])],
           [('<i>contexto:</i> <em>muchísimo</em> <i>· es cierto ✓</i>', [(99.6, 104.9)]), ('<i>docs:</i> <em>5</em> <i>→ pásale todos ✓</i>', [(104.96, 108.2)]),
            ('<i>docs:</i> <em>' + N(K((0, 5), (108.3, 3000, 1.2)), '5') + '</em> <i>· tokens:</i> <em>' + N(K((0, 4), (109.7, 96, 1.4)), '4', ' %') + '</em>', [(108.26, None)])],
           dd=100.2,
           hi_in=paso([('💬 «ya aguantan mucho contexto»', 99.6, 104.9), ('📄 pocos docs', 104.96, 108.2), ('📚 miles de docs', 108.26, None)], A))
escena('s6-contexto', S, 115.5, '', [f1], f"""const ss=[];for(let i=0;i<12;i++){{const s=R.sheet(i%3==0?C2:i%2?C1:'#a9b4bf');R.scene.add(s);ss.push(s)}}
return t=>{{const many=R.eio(R.k(t,108.3,1.2)),hot=R.k(t,112.6,1.2);
 ss.forEach((s,i)=>{{const few=i<4,a=R.eb(R.k(t,few?99.8+i*.15:108.3+(i-4)*.08,.7));s.visible=few?t>99.7:t>108.2;
  const col=i%4,row=Math.floor(i/4),x=few?{IMX - z(150)}+i*{z(100)}:{IMX - z(240)}+col*{z(160)},y=few?{IMY}:{IMY - z(110)}+row*{z(110)};
  const fx=few?R.mix({IMX - z(150)}+i*{z(100)},{IMX - z(240)}+col*{z(160)},many):x,fy=few?R.mix({IMY},{IMY - z(110)}+row*{z(110)},many):y;
  s.scale.setScalar(Math.max(.001,a*{1.25 * SC:.2f}*(1-.3*many)));R.at(s,fx+(hot>.3?Math.sin(t*30+i)*5:0),fy+6*Math.sin(t*1.4+i),2+i*.15);
  s.rotation.set(.2+.05*Math.sin(t+i),-.3+.15*Math.sin(t*.8+i),.1-(i%5)*.05)}})}}""")

# ───────────────────────── 1:55 · funciona hoy → si tus datos ya no caben, ponlo a buscar antes de contestar
S = 115.5; A = G.at(S)
f1 = ficha(115.55, A, 'busca-antes', [('cpu', 'modelos de hoy'), ('clock', '2026')],
           'Funciona hoy con los modelos que tenemos. Si tus datos ya no caben en una conversación, ponlo a buscar antes de contestar.',
           [('gr', 'hoy ✓', 117.92), ('rd', 'no caben', 121.25), ('v', 'busca primero', 122.93), ('gr', 'luego contesta', 123.72)],
           [('✅', 'Hoy', [(115.6, 119.8)]), ('🔍', 'Busca', [(119.82, None)])],
           [('<i>estado:</i> <em>funciona hoy</em>', [(115.6, 119.8)]), ('<i>si</i> <em>datos &gt; chat</em> <i>→</i> <em>busca → contesta</em>', [(119.82, None)])],
           copy=(122.6, None), dd=116.2,
           hi_in=paso([('✅ hoy', 115.6, 119.8), ('🔍 busca antes', 119.82, None)], A))
escena('s7-hoy', S, 124.7, '', [f1], f"""const rb=R.bot({z(220)});R.scene.add(rb);const mg=R.mag({z(70)});R.scene.add(mg);
return t=>{{const a=R.eb(R.k(t,115.8,.9)),m=R.eb(R.k(t,122.5,.7));rb.scale.setScalar(Math.max(.001,a));R.at(rb,{IMX}-m*{z(90)},{IMY}+10*Math.sin(t*1.6),3);
 rb.rotation.set(.1+.05*Math.sin(t*1.3),-.4+.3*Math.sin(t*.9),0);rb.userData.em.emissiveIntensity=1.4;
 mg.visible=t>122.4;mg.scale.setScalar(Math.max(.001,m));R.at(mg,{IMX + z(150)},{IMY + z(40)}+8*Math.sin(t*2),5);mg.rotation.set(.2,-.4+.3*Math.sin(t*1.2),0)}}""")

# ───────────────────────── 2:04 · resumen para guardar + pregunta
S = 124.7; A = G.at(S)
SUM = '<div class="sum">' + ''.join(f'<div style="animation-delay:{A(125.1 + i * .25)}"><b>{i + 1}</b> {n}</div>' for i, n in enumerate(['Prepara', 'Busca', 'Contesta'])) + \
      f'<div style="animation-delay:{A(126.0)}"><b>&gt;</b> ⚠️ Revisa</div></div>'
f1 = ficha(124.75, A, '# readme · rag', [('check', 'guárdalo'), ('chat', 'tu turno')], '¿Tú le pasas todo a tu IA o ya la pones a buscar primero?',
           [('v', '1 prepara', 125.1), ('v', '2 busca', 125.35), ('v', '3 contesta', 125.6), ('rd', 'revisa fuentes', 126.0)],
           [('🔖', 'Guardar', [(124.9, 125.8)]), ('💬', 'Tu turno', [(125.85, None)])],
           [('<i>¿</i><em>todo</em> <i>o</i> <em>busca primero</em><i>?</i>', [(124.9, None)])], dd=125.2, lo_in=SUM,
           hi_in=paso([('💬 cuéntame', 124.9, None)], A))
escena('s8-pregunta', S, 128.75, '.chip.st{left:auto!important;right:calc(var(--k)*12px)}', [f1], f"""const mg=R.mag({z(90)});R.scene.add(mg);
return t=>{{const a=R.eb(R.k(t,124.9,.9));mg.scale.setScalar(Math.max(.001,a));R.at(mg,{IMX + z(190)},{IMY}+10*Math.sin(t*1.4),4);mg.rotation.set(.2,-.5+.3*Math.sin(t*.9),.06)}}""")

# ───────────────────────── 2:08 · cierre: «nos vemos cuando toque la actualización de este README»
S = 128.75; A = G.at(S)
f1 = ficha(128.8, A, 'README.md', [('check', 'guardado'), ('clock', 'hasta la próxima')], 'Nos vemos cuando toque actualizar este README.',
           [('gr', '✓ guardado', 130.0)], [('💾', 'Guardar', [(128.9, None)])], [('<i>⌘S</i> <em>README.md</em>', [(129.0, None)])], copy=(129.9, None), dd=129.1)
escena('s9-cierre', S, FIN, '', [f1], f"""const tx=R.tx('README',{z(120)},{z(48)});R.scene.add(tx);
return t=>{{const c=R.eb(R.k(t,129.1,.8));tx.scale.setScalar(Math.max(.001,c));R.at(tx,{IMX},{IMY}+(1-c)*120,2);tx.rotation.set(.18+.05*Math.sin(t*2),(1-c)*1.8+.22*Math.sin(t*1.5),0)}}""",
       sigue=False)

PIEZAS.append(('pestana', 0.0, FIN, M.pestana().replace('#01 · SDD', '#02 · RAG')))
PRE = 'rm2-pista-full-'
OUT, WORK = M.OUT, M.WORK

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path, f'{b - a:.2f}'); continue
        r = subprocess.run(['node', M.CAP, path, f'{b - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'readme/2/pista-full')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
