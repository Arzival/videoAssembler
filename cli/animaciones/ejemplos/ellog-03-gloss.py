"""El Log #03 · estilo «gloss 2». Sin intro hablada: arriba va una cinta de noticiero fija («EL LOG» + titular de la
noticia en curso + texto corrido) durante todo el video; las escenas dejan libre la franja superior (títulos en top 410).
Tiempos = voz recortada de noticias/3 (voz/voz-norm.wav, 100.86 s). Necesita internet al capturar (three.js y fuentes por CDN).
Uso: SALIDA=noticias/3/animaciones REL=noticias/3/animaciones python3 ejemplos/ellog-03-gloss.py [ids…]   (SOLO_HTML=1 para revisar)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import ellog_gloss as G
from ellog_gloss import js

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.getcwd()))
WORK = os.path.join(OUT, '_html'); os.makedirs(WORK, exist_ok=True)
FIN = 100.86
TOP = 410  # títulos de las escenas (debajo de la cinta)

# titulares de la cinta: (inicio, paleta, número, texto)
NOTICIAS = [(0.0, 4, '01', '🇫🇷 Hackers «descongelan» súpers en Francia'),
            (27.9, 2, '02', 'Meta lanza Muse Wonder, «de frontera»'),
            (59.4, 1, '03', 'Anthropic deja Git: nace Scion'),
            (83.0, 0, '✓', 'Antes de conectar un agente…')]
CORRIDO = ['250–350 tiendas afectadas en Francia', 'refrigeradores hasta 50 °C', 'ciclo de descongelado de 1 h a 8 h',
           'Meta presenta Muse Wonder y Wonder Full', 'DeepSWE 1.1: 78.8 % según Meta', 'Anthropic: de 2,500 a 30,000 merges al día',
           'Scion no se publicará', 'Hacker News debate el fin de Git en Anthropic']

SHIELD = 'M12 1.5 3.5 4.8v6.1c0 5.3 3.6 10 8.5 11.6 4.9-1.6 8.5-6.3 8.5-11.6V4.8z'
TICKET = """-webkit-mask:radial-gradient(circle 30px at 0 var(--ny,72%),#0000 97%,#000) left/51% 100% no-repeat,
  radial-gradient(circle 30px at 100% var(--ny,72%),#0000 97%,#000) right/51% 100% no-repeat"""

# piezas 3D: refrigerador (panel que pasa de hielo a rojo), cabeza de robot
LIB = r"""const {THREE}=R;
R.fridge=(w)=>{const G=R.group(),h=w*1.75;const body=R.gloss('#e9eef5',{roughness:.2});
 G.add(R.rbox(w,h,w*.8,w*.08,body));
 const panel=R.gloss('#9fe8ff',{emissive:'#4fd2ff',emissiveIntensity:.9,roughness:.1,transparent:true,opacity:.92});
 const top=R.rbox(w*.84,h*.3,8,w*.04,panel);top.position.set(0,R.u(h*.31),R.u(w*.41));G.add(top);
 const bot=R.rbox(w*.84,h*.56,8,w*.04,panel);bot.position.set(0,R.u(-h*.15),R.u(w*.41));G.add(bot);
 const hm=R.metal('#c9d2de',{roughness:.15});for(const [y,l] of [[h*.31,h*.18],[-h*.05,h*.3]]){const hd=R.rbox(w*.06,l,w*.08,w*.03,hm);hd.position.set(R.u(w*.33),R.u(y),R.u(w*.47));G.add(hd)}
 const sm=R.gloss('#ffffff',{emissive:'#ffffff',emissiveIntensity:.25,transparent:true,opacity:.5});
 for(let i=0;i<3;i++){const s=R.rbox(w*.7,8,6,3,sm);s.position.set(0,R.u(-h*.32+i*h*.15),R.u(w*.43));G.add(s)}
 G.userData={panel};return G};
R.robot=(w)=>{const G=R.group();G.add(R.rbox(w,w*.86,w*.8,w*.16,R.metal('#5b6270',{roughness:.22})));
 const visor=R.rbox(w*.8,w*.26,10,w*.12,R.gloss('#0b0c10',{roughness:.08}));visor.position.set(0,R.u(w*.08),R.u(w*.41));G.add(visor);
 const em=R.gloss('#ff3030',{emissive:'#ff1010',emissiveIntensity:1.6});
 for(const x of[-1,1]){const e=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.07),24,16),em);e.position.set(R.u(x*w*.2),R.u(w*.08),R.u(w*.45));G.add(e)}
 const ant=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.025),R.u(w*.025),R.u(w*.3),16),R.metal('#c9d2de'));ant.position.y=R.u(w*.56);G.add(ant);
 const tip=new THREE.Mesh(new THREE.SphereGeometry(R.u(w*.06),24,16),em);tip.position.y=R.u(w*.72);G.add(tip);
 for(const x of[-1,1]){const ear=new THREE.Mesh(new THREE.CylinderGeometry(R.u(w*.12),R.u(w*.12),R.u(w*.1),32),R.metal('#3a404c'));ear.rotation.z=Math.PI/2;ear.position.x=R.u(x*w*.53);G.add(ear)}
 return G};
"""

PIEZAS = []


def escena(pid, start, end, n, css, body, js3d=None, script='', sigue=True):
    if sigue:
        end += 0.45
    PIEZAS.append((pid, start, end, G.page(css, body, end - start, script, n=n, js3d=js3d, salida=not sigue, t0=start)))


def st(items, S, size=88):
    return G.steps(items, S, top=TOP, size=size)


# ───────── 0:00 · #01 hackers descongelan los refrigeradores de supermercados en Francia
S = 0.0; A = G.at(S)
escena('e00-hackers', S, 14.0, 4, f"""
.p1{{animation:gone .4s ease {A(4.3)} forwards}}
.temp{{position:absolute;left:0;right:0;top:1390px;text-align:center;z-index:9}}
.temp .num{{font-size:230px;color:#bff0ff;text-shadow:0 0 60px rgba(79,210,255,.6)}}
.temp .lbl{{font-size:30px;margin-top:4px}}
.where{{position:absolute;left:0;right:0;top:1680px;display:flex;justify-content:center;gap:16px;z-index:9}}.where .pill{{font-size:32px}}
.p2{{opacity:0;animation:fade .35s ease {A(4.45)} forwards,gone .4s ease {A(9.7)} forwards}}
.vs{{position:absolute;left:80px;right:80px;top:1080px;padding:34px 36px;display:grid;gap:18px;z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(4.5)} both}}
.vs .r{{display:flex;align-items:center;gap:22px;padding:22px 28px;border-radius:999px;font-size:36px;font-weight:800;background:rgba(255,255,255,.07)}}
.vs .r .e{{font-size:44px}}.vs .r b{{margin-left:auto;font-size:30px;padding:10px 22px;border-radius:999px}}
.vs .no{{position:relative}}.vs .no:after{{content:'';position:absolute;left:24px;right:24px;top:50%;height:7px;border-radius:4px;background:#ff4d5e;transform:scaleX(0);transform-origin:left;animation:strike .35s ease {A(5.1)} forwards}}
@keyframes strike{{to{{transform:scaleX(1)}}}}
.vs .no b{{background:rgba(255,255,255,.12);color:rgba(255,255,255,.7)}}
.vs .si{{opacity:0;animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(6.4)} forwards}}.vs .si b{{background:linear-gradient(180deg,#ffb0b9,#ff4d5e);color:#2a0308}}
.cyc{{position:absolute;left:80px;right:80px;top:1440px;padding:30px 40px;z-index:9;opacity:0;animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(7.2)} forwards}}
.cyc .lbl{{font-size:24px}}.cyc .trk{{position:relative;height:40px;border-radius:20px;background:rgba(255,255,255,.08);margin-top:18px;overflow:hidden}}
.cyc .trk i{{position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:20px;background:linear-gradient(90deg,#4fd2ff,#ffb340,#ff4d5e);transform-origin:left;transform:scaleX(.125);
  animation:grow8 1.6s cubic-bezier(.45,0,.2,1) {A(7.7)} forwards;box-shadow:0 0 30px rgba(255,120,80,.6)}}@keyframes grow8{{to{{transform:scaleX(1)}}}}
.cyc .ax{{display:flex;justify-content:space-between;margin-top:12px;font-size:28px;font-weight:800}}
.p3{{opacity:0;animation:fade .35s ease {A(9.85)} forwards}}
.kps{{position:absolute;left:70px;right:70px;top:1110px;display:grid;grid-template-columns:1fr 1fr;gap:20px;z-index:9}}
.kp{{padding:36px 34px;animation:pop .55s cubic-bezier(.22,1.35,.36,1) both}}.kp .e{{font-size:64px}}.kp b{{display:block;font-size:44px;margin-top:14px}}
.kp .lbl{{font-size:26px;margin-top:6px}}.kp.bad b{{color:#ff8a95}}
.trash{{position:absolute;left:0;right:0;top:1480px;text-align:center;z-index:9;animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(12.3)} both}}.trash .pill{{font-size:32px}}
""", f"""{st([('Hackers <em>«descongelaron»</em><br>súpers en Francia', 0.15, 4.3), ('No robaron <em class="red">datos</em>', 4.4, 9.7), ('Y afectó <em>envíos</em><br>y <em class="red">precios</em>', 9.8, None)], S, 92)}
<div class="p1">
 <div class="temp fade" style="animation-delay:{A(0.9)}"><div class="num" id="tc">−18°</div><div class="lbl">temperatura dentro del refrigerador</div></div>
 <div class="where"><span class="pill pop" style="animation-delay:{A(3.3)}">🇫🇷 Francia</span><span class="pill on pop" style="animation-delay:{A(3.6)}">🏪 250–350 tiendas</span></div>
</div>
<div class="p2">
 <div class="vs glass"><div class="r no"><span class="e">💾</span>Robar datos<b>✕ no</b></div>
  <div class="r si"><span class="e">❄️</span>Descongelado forzado<b>✓ sí</b></div></div>
 <div class="cyc glass"><div class="lbl">Ciclo de descongelado · lo alargaron para que no sonaran alarmas</div><div class="trk"><i></i></div>
  <div class="ax"><span class="g">1 h</span><span class="red">8 h</span></div></div>
</div>
<div class="p3">
 <div class="kps"><div class="kp glass" style="animation-delay:{A(10.6)}"><div class="e">🚚</div><b>Envíos</b><div class="lbl">retrasados</div></div>
  <div class="kp glass bad" style="animation-delay:{A(12.0)}"><div class="e">🏷️</div><b>Precios ↑</b><div class="lbl">en la tienda</div></div></div>
 <div class="trash"><span class="pill bad">🗑️ comida echada a perder</span></div>
</div>""",
LIB + r"""const F=R.fridge(300);R.scene.add(F);const P=F.userData.panel;
const ice=new THREE.Color('#9fe8ff'),iceE=new THREE.Color('#4fd2ff'),hot=new THREE.Color('#ff8a6b'),hotE=new THREE.Color('#ff3a1a');
const drops=[];for(let i=0;i<10;i++){const d=new THREE.Mesh(new THREE.SphereGeometry(R.u(14),20,14),R.glass('#bff0ff',{opacity:.7}));d.userData={x:(i*53)%260-130,t:2.2+i*.37};R.scene.add(d);drops.push(d)}
return t=>{
 const a=R.eb(R.k(t,.2,.85)),h=R.eio(R.k(t,1.0,2.8)),m=R.eio(R.k(t,4.3,.7));
 const y=R.mix(990,840,m),s=a*R.mix(1,.78,m);F.scale.setScalar(Math.max(.001,s));
 const shk=h>0&&h<1?Math.sin(t*40)*.02:0;R.at(F,540,y);F.rotation.set(.12+.05*Math.sin(t*.9),-.5+.25*Math.sin(t*.7)+(1-a)*2.4,shk);
 P.color.copy(ice).lerp(hot,h);P.emissive.copy(iceE).lerp(hotE,h);P.emissiveIntensity=.9+.6*h;
 for(const d of drops){const u=d.userData,p=R.k(t,u.t,1.1);d.visible=p>0&&p<1&&t<9.7;R.at(d,540+u.x*s,y+260*s+p*260,3);d.scale.setScalar(Math.max(.001,Math.sin(p*Math.PI)*s))}
}""",
"""window.__cnt=t=>{const p=Math.min(1,Math.max(0,(t-1.0)/2.8)),e=p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2,v=Math.round(-18+68*e),el=document.getElementById('tc');
el.textContent=(v<0?'−'+(-v):v)+'°'+(p>=1?'C':'');const c=v>20?'#ffb0a0':v>0?'#ffe1b0':'#bff0ff';el.style.color=c;el.style.textShadow='0 0 60px '+(v>20?'rgba(255,90,60,.7)':'rgba(79,210,255,.6)')}""")

# ───────── 0:14 · #01 (parte 2): «no se va a parecer a Terminator» + protege lo que tengas expuesto
S = 14.0; A = G.at(S)
q1 = ''.join(f'<span class="w" style="animation-delay:{A(14.5 + k * .22)}">{w} </span>' for k, w in enumerate('El riesgo no se va a parecer a'.split()))
escena('e01-riesgo', S, 27.9, 1, f"""
.p1{{animation:gone .4s ease {A(19.4)} forwards}}
.qt{{position:absolute;left:70px;right:70px;top:560px;padding:70px 60px 64px;z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(14.15)} both}}
.qt .mk{{font-size:150px;line-height:.6;font-weight:800;color:var(--ink);opacity:.35}}
.qt .tx{{font-size:72px;font-weight:800;letter-spacing:-.035em;line-height:1.08;color:var(--ink);margin-top:10px}}.qt .w{{opacity:0;animation:fade .25s ease forwards}}
.qt .tm{{display:inline-block;position:relative;opacity:0;animation:fade .3s ease {A(16.4)} forwards}}
.qt .tm:after{{content:'';position:absolute;left:-6px;right:-6px;top:52%;height:10px;border-radius:5px;background:#2a0c05;transform:scaleX(0);transform-origin:left;animation:strike .35s ease {A(17.3)} forwards}}
@keyframes strike{{to{{transform:scaleX(1)}}}}
.qt .es{{display:block;margin-top:16px;opacity:0;animation:stamp .45s cubic-bezier(.22,1.6,.36,1) {A(17.6)} forwards;--r:-2deg}}
.qt .es span{{background:#fff;color:#2a0c05;padding:2px 22px;border-radius:24px;box-shadow:0 16px 40px rgba(0,0,0,.3)}}
.lk{{position:absolute;left:0;right:0;top:1330px;text-align:center;z-index:9;animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(18.3)} both}}.lk .pill{{font-size:34px}}
.p2{{opacity:0;animation:fade .35s ease {A(19.55)} forwards}}
.dev{{position:absolute;left:70px;right:70px;top:640px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;z-index:9}}
.dev,.net{{animation:gone .4s ease {A(25.0)} forwards}}
.dv{{padding:30px 10px;text-align:center;font-size:28px;font-weight:800;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both,dvOff .4s ease {A(24.4)} forwards}}
.dv .e{{font-size:64px;display:block;margin-bottom:10px}}
@keyframes dvOff{{to{{box-shadow:inset 0 1.5px 0 rgba(255,255,255,.3),0 0 0 4px rgba(255,77,94,.75),0 0 60px rgba(255,77,94,.4)}}}}
.net{{position:absolute;left:0;right:0;top:1100px;text-align:center;z-index:9}}.net .pill{{font-size:44px;padding:22px 44px;--r:-4deg;animation-delay:{A(24.3)}}}
.fix{{position:absolute;left:90px;right:90px;top:1290px;display:grid;gap:18px;z-index:9}}
.fx{{display:flex;align-items:center;gap:22px;padding:24px 32px;border-radius:999px;font-size:36px;font-weight:800;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}}
.fx .e{{font-size:44px}}.fx .ck{{margin-left:auto;width:62px;height:62px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;
  background:linear-gradient(160deg,var(--ac2),var(--ac));color:var(--ink);box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 26px rgba(var(--acr),.6)}}
""", f"""<div class="p1">
 <div class="qt hero"><div class="mk">“</div><div class="tx">{q1}<span class="tm">Terminator…</span><span class="es"><span>se va a parecer a esto.</span></span></div></div>
 <div class="lk"><span class="pill">🧊 → 🔥 un refrigerador conectado a internet</span></div>
</div>
<div class="p2">
 {st([('¿Tienes cosas <em>conectadas</em>?', 19.6, 25.0), ('Ponles más <em>protección</em>', 25.1, None)], S, 86)}
 <div class="dev"><div class="dv glass" style="animation-delay:{A(20.4)}"><span class="e">📷</span>Cámaras</div>
  <div class="dv glass" style="animation-delay:{A(21.7)}"><span class="e">🏠</span>Tu casa</div>
  <div class="dv glass" style="animation-delay:{A(22.5)}"><span class="e">🖥️</span>Homelab</div></div>
 <div class="net"><span class="pill bad stamp">🌐 abiertos a internet</span></div>
 <div class="fix"><div class="fx glass" style="animation-delay:{A(25.7)}"><span class="e">🔑</span>Contraseñas fuertes<span class="ck">✓</span></div>
  <div class="fx glass" style="animation-delay:{A(26.2)}"><span class="e">🚪</span>Cierra puertos<span class="ck">✓</span></div>
  <div class="fx glass" style="animation-delay:{A(26.7)}"><span class="e">🛡️</span>Entra por VPN<span class="ck">✓</span></div></div>
</div>""",
LIB + "const SH=" + js(SHIELD) + r""";
const rb=R.robot(260);R.scene.add(rb);const F=R.fridge(150);R.scene.add(F);F.userData.panel.color.set('#ff8a6b');F.userData.panel.emissive.set('#ff3a1a');
const sh=R.shape(SH,300,5,R.gloss('#ff8a6b',{emissive:'#ff5a3a',emissiveIntensity:.2,roughness:.16}));R.scene.add(sh);
return t=>{
 const a=R.eb(R.k(t,14.4,.8)),x=R.eo(R.k(t,17.3,.45)),f=R.eb(R.k(t,17.6,.7)),o=R.eo(R.k(t,19.3,.4));
 rb.visible=t<17.8;rb.scale.setScalar(Math.max(.001,a*(1-x)));R.at(rb,860,560+x*120,4);rb.rotation.set(.1+.06*Math.sin(t*1.3),-.45+.3*Math.sin(t*.9),.06*Math.sin(t*2));
 F.visible=t>17.55&&t<19.75;F.scale.setScalar(Math.max(.001,f*(1-o)));R.at(F,860,540,4);F.rotation.set(.15,-.5+.3*Math.sin(t),Math.sin(t*30)*.03);
 const s=R.eb(R.k(t,25.15,.75));sh.visible=t>25.1;sh.scale.setScalar(Math.max(.001,s));R.at(sh,540,880,3);sh.rotation.set(.15+.06*Math.sin(t),(1-s)*3+.5*Math.sin(t*1.1),0);
 sh.material.emissiveIntensity=.2+.4*R.k(t,26.7,.5);
}""")

# ───────── 0:28 · #02 Meta Muse Wonder
S = 27.9; A = G.at(S)
bars = [('Muse Wonder', 78.8, 'on', 37.0), ('Claude Opus 5.5', 74.2, '', 37.3), ('GPT-6 Astra', 74.1, '', 37.6)]
filas = ''.join(f'<div class="br" style="animation-delay:{A(t0)}"><span class="nm">{n}</span><div class="tk"><i class="{c}" style="width:{(v - 60) / 20 * 100:.0f}%;animation-delay:{A(t0 + .1)}"></i></div><b class="{c}">{v}<span class="d">%</span></b></div>'
                for n, v, c, t0 in bars)
escena('e02-meta', S, 47.05, 2, f"""
.p1{{animation:gone .4s ease {A(36.1)} forwards}}
.tg{{position:absolute;left:0;right:0;top:1250px;display:flex;justify-content:center;gap:16px;z-index:9;animation:gone .4s ease {A(32.8)} forwards}}.tg .pill{{font-size:32px}}
.cmp{{position:absolute;left:80px;right:80px;top:1050px;display:grid;grid-template-columns:1fr 1.25fr;gap:20px;align-items:end;z-index:9}}
.cm{{padding:34px 34px;opacity:0;animation:pop .5s cubic-bezier(.22,1.35,.36,1) forwards}}.cm .lbl{{font-size:24px}}.cm b{{display:block;font-size:44px;margin-top:10px}}
.cm.hero b,.cm.hero .lbl{{color:var(--ink)}}.cm.hero{{padding:50px 40px}}.cm.hero b{{font-size:56px}}
.p2{{opacity:0;animation:fade .35s ease {A(36.25)} forwards,gone .4s ease {A(40.5)} forwards}}
.ch{{position:absolute;left:70px;right:70px;top:880px;padding:40px 44px;z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(36.4)} both}}
.ch .lbl{{font-size:26px;margin-bottom:26px}}
.br{{display:grid;grid-template-columns:250px 1fr 150px;align-items:center;gap:18px;margin-top:22px;opacity:0;animation:fade .3s ease forwards}}
.br .nm{{font-size:28px;font-weight:700}}.br .tk{{height:44px;border-radius:22px;background:rgba(255,255,255,.08);overflow:hidden}}
.br i{{display:block;height:100%;border-radius:22px;background:linear-gradient(90deg,rgba(255,255,255,.35),rgba(255,255,255,.6));transform-origin:left;animation:up 1s cubic-bezier(.22,1.1,.36,1) both}}
.br i.on{{background:linear-gradient(90deg,var(--ac),var(--ac2));box-shadow:0 0 30px rgba(var(--acr),.6)}}@keyframes up{{from{{transform:scaleX(0)}}}}
.br b{{font-size:44px;font-weight:800;text-align:right;letter-spacing:-.04em}}.br b.on{{color:var(--ac2)}}.br .d{{opacity:.4;font-size:30px}}
.src{{position:absolute;left:0;right:0;top:1360px;text-align:center;z-index:9;animation:pop .5s ease {A(38.6)} both}}.src .pill{{font-size:28px}}
.p3{{opacity:0;animation:fade .35s ease {A(40.65)} forwards}}
.ft{{position:absolute;left:80px;right:80px;top:880px;display:grid;gap:20px;z-index:9}}
.f{{display:flex;align-items:center;gap:26px;padding:30px 36px;animation:pop .55s cubic-bezier(.22,1.35,.36,1) both}}
.f .e{{width:96px;height:96px;flex-shrink:0;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:48px;background:linear-gradient(160deg,var(--ac2),var(--ac));box-shadow:inset 0 2px 0 #fff,0 0 30px rgba(var(--acr),.5)}}
.f b{{display:block;font-size:40px}}.f span{{font-size:26px;color:rgba(255,255,255,.6);font-weight:600}}
""", f"""{st([('Meta <em>Muse Wonder</em>', 28.1, 32.8), ('Más grande que<br><em>Muse Spark</em>', 32.9, 36.1), ('Mejor para <em>programar</em>', 36.2, 40.5),
           ('Memoria y enfoque<br><em>activos</em>', 40.6, None)], S, 90)}
<div class="p1">
 <div class="tg"><span class="pill pop" style="animation-delay:{A(29.3)}">📅 12 de octubre</span><span class="pill on pop" style="animation-delay:{A(31.6)}">🚀 «de frontera»</span></div>
 <div class="cmp"><div class="cm glass" style="animation-delay:{A(33.4)}"><div class="lbl">abril</div><b>Muse Spark</b></div>
  <div class="cm hero" style="animation-delay:{A(34.0)}"><div class="lbl">octubre</div><b>Muse Wonder</b><div class="lbl" style="margin-top:8px">+ Wonder Full</div></div></div>
</div>
<div class="p2">
 <div class="ch glass"><div class="lbl">DeepSWE 1.1 · programación de largo aliento</div>{filas}</div>
 <div class="src"><span class="pill">📊 cifras publicadas por Meta</span></div>
</div>
<div class="p3"><div class="ft">
 <div class="f glass" style="animation-delay:{A(41.0)}"><div class="e">🧠</div><div><b>Memoria activa</b><span>recuerda contexto por días y meses</span></div></div>
 <div class="f glass" style="animation-delay:{A(41.9)}"><div class="e">🎯</div><div><b>Enfoque activo</b><span>no suelta la tarea a la primera traba</span></div></div>
 <div class="f glass" style="animation-delay:{A(44.6)}"><div class="e">🛑</div><div><b>Agentes bajo control</b><span>para que no se salgan de control</span></div></div>
</div></div>""",
"const {THREE}=R;const META=" + js(G.svgpath('meta')) + r""";
const lg=R.shape(META,520,2.6,R.gloss('#2f7bff',{emissive:'#1a5cff',emissiveIntensity:.25,roughness:.14}),.35);R.scene.add(lg);
const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(330),R.u(8),16,200),R.iri('#cfe0ff',{opacity:1,transparent:false}));R.scene.add(ring);
return t=>{
 const a=R.eb(R.k(t,28.2,.85)),m=R.eio(R.k(t,32.7,.7)),x=R.eo(R.k(t,36.0,.45)),b=R.eb(R.k(t,40.7,.7));
 const sc=a*R.mix(1,.7,m)*(1-x)+b*.5*(t>40.6?1:0);const y=t>40.6?680:R.mix(800,820,m);
 lg.scale.setScalar(Math.max(.001,sc));R.at(lg,t>40.6?840:540,y,3);lg.rotation.set(.18+.06*Math.sin(t*1.1),(1-a)*2.6+.45*Math.sin(t*.8),0);
 ring.visible=t<36.5;ring.scale.setScalar(Math.max(.001,a*(1-x)*R.mix(1,.7,m)));R.at(ring,540,y,-2);ring.rotation.set(1.2,.2,t*.4);
}""")

# ───────── 0:47 · #02 (parte 2): «lo de la frontera lo dice Meta» → una opción más
S = 47.05; A = G.at(S)
opts = [('claude', '#ffb38f', 'Claude', 55.2), ('openai', '#fff', 'ChatGPT', 55.5), ('googlegemini', '#8ab4ff', 'Gemini', 55.8)]
op = ''.join(f'<div class="op glass" style="animation-delay:{A(t0)}">{G.logo(n, c, 64)}<b>{nm}</b></div>' for n, c, nm, t0 in opts)
escena('e03-meta-ojo', S, 59.4, 2, f"""
.p1{{animation:gone .4s ease {A(51.0)} forwards}}
.fr{{position:absolute;left:90px;right:90px;top:640px;height:520px;padding:56px 54px;z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(47.2)} both}}
.fr .lbl{{font-size:28px;color:rgba(6,18,46,.7);font-weight:700}}
.fr .big{{font-size:110px;font-weight:800;letter-spacing:-.05em;line-height:1;color:var(--ink);margin-top:30px}}
.fr .big sup{{font-size:80px;color:#ff4d5e}}
.fr .ft{{position:absolute;left:54px;bottom:50px;font-size:30px;font-weight:700;color:var(--ink);opacity:.75}}
.dice{{position:absolute;left:0;right:0;top:1230px;text-align:center;z-index:9}}.dice .pill{{font-size:44px;padding:22px 44px;--r:-5deg;animation-delay:{A(49.9)}}}.dice svg{{width:44px;height:44px}}
.p2{{opacity:0;animation:fade .35s ease {A(51.15)} forwards}}
.ops{{position:absolute;left:70px;right:70px;top:760px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px;z-index:9}}
.op{{padding:34px 8px 28px;text-align:center;animation:pop .5s cubic-bezier(.22,1.35,.36,1) both}}.op svg{{display:block;margin:0 auto 16px}}.op b{{font-size:26px}}
.op.nw{{background:linear-gradient(160deg,var(--ac2) -30%,var(--ac) 30%,rgba(var(--acr),.4));color:var(--ink);box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 60px rgba(var(--acr),.55)}}
.op.nw svg path{{fill:var(--ink)}}
.plus{{position:absolute;left:0;right:0;top:1080px;text-align:center;z-index:9;animation:stamp .45s cubic-bezier(.22,1.6,.36,1) {A(56.6)} both}}.plus .pill{{font-size:36px;--r:-3deg}}
.pr{{position:absolute;left:110px;right:110px;top:1240px;padding:34px 40px 38px;border-radius:40px;background:#f6f2ee;color:#151318;--ny:56%;{TICKET};
  box-shadow:0 40px 90px rgba(0,0,0,.5);z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(57.4)} both}}
.pr h4{{font-size:28px;font-weight:800}}.pr .sep{{border-top:3px dashed #d8d1c9;margin:20px 0}}
.pr .r{{display:flex;justify-content:space-between;font-size:30px;font-weight:700;margin-top:8px}}.pr .r b{{color:#1a5cff}}
""", f"""<div class="p1">
 {st([('¿«De <em>frontera</em>»?', 47.2, None)], S, 96)}
 <div class="fr hero"><div class="lbl">Muse Wonder · clasificación</div><div class="big">Frontier class<sup>*</sup></div><div class="ft">* lo afirma la propia empresa</div></div>
 <div class="dice"><span class="pill bad stamp">{G.logo('meta', '#2a0308')} lo dice Meta 🤷</span></div>
</div>
<div class="p2">
 {st([('¿Programas con <em>IA</em>?', 51.2, 53.9), ('Una <em>opción más</em>', 54.0, None)], S, 92)}
 <div class="ops">{op}<div class="op nw" style="animation-delay:{A(56.3)}">{G.logo('meta', '#06122e', 64)}<b>Muse Wonder</b></div></div>
 <div class="plus"><span class="pill on">+ código y agentes 🤖</span></div>
 <div class="pr"><h4>🧾 Muse Wonder · API de Meta</h4><div class="sep"></div>
  <div class="r"><span>Entrada</span><b>$4 / millón de tokens</b></div><div class="r"><span>Salida</span><b>$20 / millón de tokens</b></div></div>
</div>""",
r"""const {THREE}=R;
const mg=R.group();const ring=new THREE.Mesh(new THREE.TorusGeometry(R.u(120),R.u(20),24,72),R.metal('#e8ecf3',{roughness:.12}));mg.add(ring);
const lens=new THREE.Mesh(new THREE.CircleGeometry(R.u(120),64),R.glass('#cfe9ff',{opacity:.35}));mg.add(lens);
const hd=new THREE.Mesh(new THREE.CylinderGeometry(R.u(22),R.u(26),R.u(170),32),R.gloss('#1b1e26',{roughness:.25}));hd.position.set(R.u(145),R.u(-145),0);hd.rotation.z=Math.PI/4;mg.add(hd);R.scene.add(mg);
return t=>{const a=R.eb(R.k(t,47.6,.8)),o=R.eo(R.k(t,50.9,.4));mg.visible=t<51.4;mg.scale.setScalar(Math.max(.001,a*(1-o)));
 R.at(mg,850+30*Math.sin(t*1.4),720+25*Math.cos(t*1.1),5);mg.rotation.set(.2,-.4+.3*Math.sin(t),.1)}""")

# ───────── 0:59 · #03 Anthropic deja Git → Scion
S = 59.4; A = G.at(S)
escena('e04-scion', S, 73.3, 1, f"""
.p1{{animation:gone .4s ease {A(65.5)} forwards}}
.who{{position:absolute;left:0;right:0;top:1230px;display:flex;justify-content:center;gap:16px;z-index:9}}.who .pill{{font-size:32px}}
.nw{{position:absolute;left:0;right:0;top:1380px;text-align:center;z-index:9;animation:pop .5s cubic-bezier(.22,1.35,.36,1) {A(62.9)} both}}.nw .pill{{font-size:36px;padding:20px 40px}}
.p2{{opacity:0;animation:fade .35s ease {A(65.65)} forwards}}
.art{{position:absolute;left:90px;right:90px;top:640px;padding:44px 48px 48px;border-radius:44px;background:#f6f2ee;color:#151318;--ny:34%;{TICKET};
  box-shadow:0 40px 90px rgba(0,0,0,.5);z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(65.8)} both}}
.art .h{{display:flex;align-items:center;gap:16px;font-size:26px;font-weight:700;color:#6b6460}}.art .h svg{{width:40px;height:40px}}
.art h3{{font-size:58px;font-weight:800;letter-spacing:-.035em;line-height:1.05;margin-top:22px}}
.art .sep{{border-top:3px dashed #d8d1c9;margin:34px 0 18px}}
.art .ln{{display:flex;align-items:center;gap:18px;padding:16px 0;font-size:34px;font-weight:700;opacity:0;animation:pop .5s cubic-bezier(.22,1.35,.36,1) forwards}}
.art .ln b{{width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;color:#2a0c05;background:linear-gradient(160deg,#ffd9cc,#ff8a6b)}}
.bye{{position:absolute;left:0;right:0;top:1400px;text-align:center;z-index:9}}.bye .pill{{font-size:40px;padding:20px 42px;--r:-6deg;animation-delay:{A(72.2)}}}.bye svg{{width:40px;height:40px}}
""", f"""{st([('Anthropic deja <em>Git</em>', 59.6, 65.5), ('Y explicó <em>por qué</em>', 65.6, None)], S, 92)}
<div class="p1">
 <div class="who"><span class="pill pop" style="animation-delay:{A(60.3)}">{G.logo('anthropic')} Anthropic</span><span class="pill pop" style="animation-delay:{A(62.3)}">🧩 control de versiones propio</span></div>
 <div class="nw"><span class="pill on">🌱 se llama Scion</span></div>
</div>
<div class="p2">
 <div class="art"><div class="h">{G.logo('anthropic', '#151318')} Engineering at Anthropic · 13 oct 2026</div><h3>Redesigning source control</h3><div class="sep"></div>
  <div class="ln" style="animation-delay:{A(68.4)}"><b>?</b>Por qué dejaron Git</div><div class="ln" style="animation-delay:{A(69.2)}"><b>⚙</b>Cómo armaron su alternativa</div></div>
 <div class="bye"><span class="pill bad stamp">{G.logo('git', '#2a0308')} adiós, Git</span></div>
</div>""",
"const {THREE}=R;const GIT=" + js(G.svgpath('git')) + r""";
const gt=R.shape(GIT,380,4,R.gloss('#f05032',{emissive:'#c03010',emissiveIntensity:.25,roughness:.16}));R.scene.add(gt);
const sc=R.text('SCION',150,60,R.iri('#ffd9cc',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(sc);
const grey=new THREE.Color('#5a5560'),org=new THREE.Color('#f05032');
return t=>{
 const a=R.eb(R.k(t,59.7,.85)),g=R.eio(R.k(t,61.8,.6)),f=R.k(t,62.4,.9),s=R.eb(R.k(t,62.9,.8)),o=R.eo(R.k(t,65.4,.45));
 gt.visible=f<1;gt.scale.setScalar(Math.max(.001,a*(1-f*.4)));R.at(gt,540-g*230,820+f*f*700,2);gt.rotation.set(.2+f*1.6,(1-a)*2.6+.4*Math.sin(t*.9),f*1.2);
 gt.material.color.copy(org).lerp(grey,g);gt.material.emissiveIntensity=.25*(1-g);
 sc.visible=t>62.85&&t<65.9;sc.scale.setScalar(Math.max(.001,s*(1-o)));R.at(sc,R.mix(540,560,s),R.mix(900,820,s),3);sc.rotation.set(.16+.05*Math.sin(t*2),(1-s)*1.8+.22*Math.sin(t*1.4),0);
}""")

# ───────── 1:13 · #03 (parte 2): la razón (merges/día) y el debate en Hacker News
S = 73.3; A = G.at(S)
coms = [('dev_42', 'Si Anthropic no aguanta con Git, ¿quién sí? 🤯'), ('hn_reader', '30,000 merges al día… son puros agentes'),
        ('oldtimer', 'Git se diseñó para trabajo offline, no para esto')]
cm = ''.join(f'<div class="c" style="animation-delay:{A(79.6 + k * .9)}"><b>{u}</b> · hace {k + 2} h<div>{t}</div></div>' for k, (u, t) in enumerate(coms))
escena('e05-ritmo', S, 83.0, 1, f"""
.p1{{animation:gone .4s ease {A(78.1)} forwards}}
.hc{{position:absolute;left:70px;right:70px;top:620px;height:560px;padding:56px;z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(73.5)} both}}
.hc .lbl{{color:rgba(42,12,5,.7);font-size:30px;font-weight:700}}
.hc .num{{font-size:220px;color:#2a0c05;margin-top:30px}}
.hc .bt{{position:absolute;left:56px;right:56px;bottom:50px;display:flex;justify-content:space-between;font-size:32px;font-weight:800;color:#2a0c05}}
.x12{{position:absolute;right:90px;top:560px;z-index:10}}.x12 .pill{{font-size:56px;padding:20px 40px;--r:8deg;animation-delay:{A(76.9)}}}
.tm{{position:absolute;left:0;right:0;top:1270px;display:flex;justify-content:center;gap:16px;z-index:9}}.tm .pill{{font-size:32px}}
.p2{{opacity:0;animation:fade .35s ease {A(78.25)} forwards}}
.hn{{position:absolute;left:70px;right:70px;top:620px;border-radius:44px;overflow:hidden;z-index:9;animation:rise .7s cubic-bezier(.22,1.1,.36,1) {A(78.4)} both;
  background:#f6f6ef;color:#1a1a1a;box-shadow:0 40px 90px rgba(0,0,0,.5)}}
.hn .bar{{display:flex;align-items:center;gap:18px;padding:22px 32px;background:#ff6600;color:#111;font-size:30px;font-weight:800}}
.hn .bar .y{{width:48px;height:48px;border:3px solid #fff;color:#fff;display:flex;align-items:center;justify-content:center;font-size:30px}}
.hn .tt{{padding:30px 34px 10px;font-size:38px;font-weight:800;letter-spacing:-.02em;line-height:1.15}}
.hn .mt{{padding:0 34px 24px;font-size:26px;color:#828282;font-weight:600}}.hn .mt b{{color:#ff6600}}
.hn .c{{margin:0 24px 18px;padding:20px 24px;border-radius:24px;background:#ececE4;font-size:27px;font-weight:600;opacity:0;animation:pop .45s cubic-bezier(.22,1.35,.36,1) forwards}}
.hn .c b{{color:#ff6600}}.hn .c div{{margin-top:6px;color:#222;font-weight:600}}
""", f"""{st([('Demasiados <em>cambios</em>', 73.4, 78.1), ('Debate en <em>Hacker News</em>', 78.2, None)], S, 92)}
<div class="p1">
 <div class="hc hero"><div class="lbl">Merges al día en su repositorio</div><div class="num" id="mg">2,500</div><div class="bt"><span>mayo</span><span>→</span><span>septiembre</span></div></div>
 <div class="x12"><span class="pill light stamp">12×</span></div>
 <div class="tm"><span class="pill pop" style="animation-delay:{A(77.2)}">🤖 la mayoría los hace Claude</span></div>
</div>
<div class="p2">
 <div class="hn"><div class="bar"><span class="y">Y</span>Hacker News</div>
  <div class="tt">Anthropic: Redesigning source control (anthropic.com)</div>
  <div class="mt"><b id="pts">0</b> puntos · <b id="cms">0</b> comentarios</div>{cm}</div>
</div>""",
r"""const {THREE}=R;const P=[];const cm=R.gloss('#ff8a6b',{emissive:'#ff5a3a',emissiveIntensity:.4,roughness:.2});
for(let i=0;i<26;i++){const b=R.rbox(54,54,54,12,i%3?cm:R.gloss('#ffd9cc',{roughness:.2}));b.userData={x:120+((i*137)%840),t:74.6+i*.08,s:.7+((i*29)%10)/20};R.scene.add(b);P.push(b)}
return t=>{const o=R.eo(R.k(t,78.0,.5));for(const b of P){const u=b.userData,p=R.k(t,u.t,2.2);b.visible=p>0&&t<78.6;
 R.at(b,u.x,620+p*1300*u.s,6-u.s*4);b.rotation.set(t*2*u.s,t*1.5,0);b.scale.setScalar(Math.max(.001,u.s*(1-o)))}}""",
f"""window.__cnt=t=>{{t+={S};const e=(s,d)=>1-Math.pow(1-Math.min(1,Math.max(0,(t-s)/d)),3);
document.getElementById('mg').textContent=Math.round(2500+27500*e(74.5,2.3)).toLocaleString('en-US');
document.getElementById('pts').textContent=Math.round(1240*e(78.8,2.5)).toLocaleString('en-US');document.getElementById('cms').textContent=Math.round(687*e(78.8,2.8))}}""")

# ───────── 1:23 · cierre: permisos y datos de tu agente → ¿dejarías que actúe por ti? (arriba entra «Sígueme»)
S = 83.0; A = G.at(S)
COLS = [G.PALETAS[k][2] for k in (4, 2, 1)]
rec = ''.join(f'<div class="rw glass pop" style="animation-delay:{A(94.2 + k * .2)}"><span class="ck" style="background:{c};box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 24px {c}">✓</span>{t}</div>'
              for k, (t, c) in enumerate(zip(['Refris hackeados en Francia', 'Meta · Muse Wonder', 'Anthropic · Scion'], COLS)))
escena('e06-cierre', S, FIN, 0, f"""
.p1{{animation:gone .4s ease {A(89.4)} forwards}}
.chk{{position:absolute;left:90px;right:90px;top:1080px;display:grid;gap:22px;z-index:9}}
.it{{display:flex;align-items:center;gap:26px;padding:30px 36px;border-radius:999px;font-size:44px;font-weight:800;animation:pop .55s cubic-bezier(.22,1.35,.36,1) both}}
.it .e{{font-size:54px}}.it .ck{{margin-left:auto;width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:900;
  background:rgba(255,255,255,.1);color:transparent;animation:ckOn .4s cubic-bezier(.22,1.6,.36,1) both}}
@keyframes ckOn{{from{{transform:scale(.5)}}to{{background:linear-gradient(160deg,var(--ac2),var(--ac));color:var(--ink);box-shadow:inset 0 2px 0 rgba(255,255,255,.6),0 0 30px rgba(var(--acr),.6);transform:none}}}}
.p2{{opacity:0;animation:fade .35s ease {A(89.55)} forwards,gone .4s ease {A(93.6)} forwards}}
.rv{{position:absolute;left:0;right:0;top:1180px;text-align:center;z-index:9}}.rv .pill{{font-size:38px;padding:22px 42px}}
.p3{{opacity:0;animation:fade .35s ease {A(93.8)} forwards}}
.rec{{position:absolute;left:100px;right:100px;top:1090px;display:grid;gap:16px;z-index:9}}
.rw{{display:flex;align-items:center;gap:22px;padding:22px 30px;border-radius:999px;font-size:32px;font-weight:700}}
.rw .ck{{width:52px;height:52px;border-radius:50%;color:#111;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800;flex-shrink:0}}
""", f"""<div class="p1">
 {st([('Antes de conectar<br>un <em>agente</em>', 83.1, None)], S, 90)}
 <div class="chk"><div class="it glass" style="animation-delay:{A(86.0)}"><span class="e">🔑</span>¿Qué permisos?<span class="ck" style="animation-delay:{A(86.9)}">✓</span></div>
  <div class="it glass" style="animation-delay:{A(87.4)}"><span class="e">📂</span>¿Qué datos?<span class="ck" style="animation-delay:{A(88.1)}">✓</span></div></div>
</div>
<div class="p2">
 {st([('Revísalo <em>tú</em><br>antes de que actúe', 89.6, None)], S, 90)}
 <div class="rv"><span class="pill on pop" style="animation-delay:{A(91.4)}">✋ aprobación humana primero</span></div>
</div>
<div class="p3"><div class="rec">{rec}</div></div>""",
LIB + r"""const rb=R.robot(240);R.scene.add(rb);
const tx=R.text('EL LOG',140,60,R.iri('#b9a2ff',{metalness:.85,roughness:.14,opacity:1,transparent:false,iridescence:1}));R.scene.add(tx);
return t=>{const a=R.eb(R.k(t,83.4,.8)),o=R.eo(R.k(t,93.4,.4)),stop=R.eo(R.k(t,91.2,.4));
 rb.visible=t<93.9;rb.scale.setScalar(Math.max(.001,a*(1-o)));R.at(rb,540,t<89.5?820:R.mix(820,860,stop));
 rb.rotation.set(.1+.05*Math.sin(t*1.3),-.4+.35*Math.sin(t*.9)*(1-stop),.05*Math.sin(t*2)*(1-stop));
 const b=R.eb(R.k(t,94.0,.8));tx.visible=t>93.9;tx.scale.setScalar(Math.max(.001,b));R.at(tx,540,1560+(1-b)*150);tx.rotation.set(.18+.05*Math.sin(t*2),(1-b)*1.8+.22*Math.sin(t*1.5),0)}""",
sigue=False)

# ───────── tarjeta «Sígueme» (entra al final, debajo de la cinta)
SEG_INI = 93.8
SEGUIR = G.tarjeta("""
.tt{display:flex;align-items:center;gap:24px;padding-right:170px}
.av{width:120px;height:120px;border-radius:50%;background:linear-gradient(160deg,#e9e0ff,#a78bfa);display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:800;color:#160b33;
  box-shadow:inset 0 3px 0 rgba(255,255,255,.6),0 0 0 6px rgba(255,255,255,.12),0 0 40px rgba(167,139,250,.45)}
.nm{font-size:44px;font-weight:800;letter-spacing:-.03em}
.btn{position:relative;margin-top:30px;height:96px}
.btn span{position:absolute;inset:0;border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800}
.b1{background:linear-gradient(180deg,#e9e0ff,#a78bfa);color:#160b33;box-shadow:inset 0 2px 0 #fff,0 20px 50px rgba(167,139,250,.4);animation:tap .22s ease 1.0s,off .2s ease 1.17s forwards}
.b2{background:linear-gradient(180deg,rgba(255,255,255,.18),rgba(255,255,255,.07));opacity:0;animation:fade .25s ease 1.17s forwards}
@keyframes tap{50%{transform:scale(.92)}}
.q{margin-top:22px;text-align:center}.q .pill{font-size:28px}
.cm{display:flex;gap:18px;align-items:center;margin-top:20px;padding:20px 26px;border-radius:36px;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));animation:pop .45s cubic-bezier(.22,1.3,.36,1) 3.0s both}
.cm .mini{background:linear-gradient(160deg,#e9e0ff,#a78bfa)}.cm .t{font-size:28px;font-weight:600}
""", """<div class="tt"><div class="av">A</div><div><div class="nm">Armando</div><div class="sub">El Log · cada semana</div></div></div>
<div class="btn"><span class="b1">Seguir</span><span class="b2">Siguiendo ✓</span></div>
<div class="q pop" style="animation-delay:.5s"><span class="pill on">🤖 ¿Dejarías que un agente actúe por ti?</span></div>
<div class="cm"><div class="mini">💬</div><div><div class="sub" style="font-size:21px">Tú · ahora</div><div class="t"><span class="type" style="--td:1.5s;--n:26;animation-delay:3.3s">Solo si me pide permiso 😅</span></div></div></div>""",
round(FIN - SEG_INI, 2), pal='ia', top=380,
js3d=LIB + r"""const rb=R.robot(170);R.scene.add(rb);
return t=>{const a=R.IN(t),o=R.OUT(t),n=Math.sin(Math.PI*R.k(t,3.3,.5));rb.scale.setScalar(Math.max(.001,a*(1-o)));R.at(rb,870,450-o*80,4);
 rb.rotation.set(.15+.25*n,-.45+.3*Math.sin(t*1.2),.05*Math.sin(t*2))}""")


# ───────── cinta de noticiero (todo el video, encima de las escenas)
def cinta():
    heads = []
    for k, (t0, pal, num, txt) in enumerate(NOTICIAS):
        t1 = NOTICIAS[k + 1][0] if k + 1 < len(NOTICIAS) else None
        ac, ac2, ink = G.PALETAS[pal][2], G.PALETAS[pal][3], G.PALETAS[pal][5]
        anim = f'hIn .5s cubic-bezier(.22,1.2,.36,1) {t0 + (.35 if k == 0 else 0):.2f}s both' + (f',hOut .35s ease {t1 - .05:.2f}s forwards' if t1 else '')
        heads.append(f'<div class="hl" style="animation:{anim}"><span class="nn" style="background:linear-gradient(160deg,{ac2},{ac});color:{ink}">{num}</span><span class="tx">{txt}</span></div>')
    crawl = ''.join(f'<span>{c}</span><i>◆</i>' for c in CORRIDO)
    css = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:{G.SANS};color:#fff;-webkit-font-smoothing:antialiased}}
.cin{{position:absolute;left:36px;right:36px;top:170px;animation:cIn .6s cubic-bezier(.22,1.2,.36,1) .05s both}}
@keyframes cIn{{from{{opacity:0;transform:translateY(-60px)}}to{{opacity:1;transform:none}}}}
.band{{position:relative;height:112px;border-radius:30px 30px 10px 10px;display:flex;align-items:center;overflow:hidden;
  background:linear-gradient(180deg,rgba(30,27,42,.94),rgba(14,13,20,.96));box-shadow:inset 0 1.5px 0 rgba(255,255,255,.22),0 26px 60px rgba(0,0,0,.55)}}
.lg{{height:100%;display:flex;align-items:center;gap:14px;padding:0 30px 0 28px;flex-shrink:0;font-size:38px;font-weight:800;letter-spacing:-.02em;color:#160b33;
  background:linear-gradient(160deg,#e9e0ff,#a78bfa);box-shadow:inset 0 2px 0 rgba(255,255,255,.6),12px 0 40px rgba(167,139,250,.35)}}
.lg i{{width:18px;height:18px;border-radius:50%;background:#ff2d48;box-shadow:0 0 0 0 rgba(255,45,72,.7);animation:rec 1.2s ease-in-out infinite}}
@keyframes rec{{50%{{box-shadow:0 0 0 9px rgba(255,45,72,0);opacity:.55}}}}
.hs{{position:relative;flex:1;height:100%}}
.hl{{position:absolute;inset:0;display:flex;align-items:center;gap:18px;padding:0 26px;opacity:0}}
.hl .nn{{min-width:62px;height:62px;padding:0 10px;border-radius:31px;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800;flex-shrink:0;box-shadow:inset 0 2px 0 rgba(255,255,255,.6)}}
.hl .tx{{font-size:31px;font-weight:700;letter-spacing:-.01em;line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
@keyframes hIn{{from{{opacity:0;transform:translateY(60px)}}to{{opacity:1;transform:none}}}}
@keyframes hOut{{to{{opacity:0;transform:translateY(-60px)}}}}
.crawl{{position:relative;margin-top:6px;height:54px;border-radius:10px 10px 24px 24px;overflow:hidden;display:flex;align-items:center;
  background:linear-gradient(90deg,rgba(167,139,250,.92),rgba(124,92,230,.92));box-shadow:0 18px 40px rgba(0,0,0,.4)}}
.crawl .tag{{position:relative;z-index:2;height:100%;display:flex;align-items:center;padding:0 22px;font-size:22px;font-weight:800;letter-spacing:.08em;color:#fff;background:#160b33}}
.mv{{display:flex;align-items:center;white-space:nowrap;gap:22px;padding-left:22px;font-size:25px;font-weight:700;color:#160b33;animation:mv {FIN:.2f}s linear both}}
.mv i{{font-style:normal;font-size:16px;opacity:.6}}
@keyframes mv{{from{{transform:translateX(0)}}to{{transform:translateX(-{len(CORRIDO) * 2 * 520}px)}}}}
"""
    body = f"""<div class="cin"><div class="band"><div class="lg"><i></i>EL LOG</div><div class="hs">{''.join(heads)}</div></div>
<div class="crawl"><span class="tag">ÚLTIMO</span><div class="mv">{crawl}{crawl}{crawl}</div></div></div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8">{G.FONTS}<style>{css}</style>
<script>window.__listo=Promise.resolve();</script></head><body>{body}</body></html>"""


PIEZAS.append(('seguir', SEG_INI, FIN, SEGUIR))
PIEZAS.append(('cinta', 0.0, FIN, cinta()))  # al final: queda encima de todo
PRE = 'gloss-'

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        if os.environ.get('SOLO_HTML'):
            print('html', path); continue
        r = subprocess.run(['node', CAP, path, f'{b - a:.2f}', f'{OUT}/{PRE}{pid}.webm'], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr[-600:], flush=True)
    if not solo:
        rel = os.environ.get('REL', 'noticias/3/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0, 'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays.json')
