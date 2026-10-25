"""Terror demo («El Leviatán», 4:12) en estilo Sombras. Tiempos en segundos del video final (voz-final.wav).

    SALIDA=… REL=… PRE=td- python3 cli/animaciones/ejemplos/terror-demo-sombras.py [ids…]
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import sombras as S

FIN = 252.2
TIEMPOS = []


def E(pid, ini, fin, js, q=.5):
    # T = tiempo del video final; t = local
    S.escena(pid, ini, fin, f'const T=t+{ini};' + js, q)


# 0 · «Si estás escuchando esto, ya es demasiado tarde. El Leviatán ya te vio.» + señal perdida
E('s01-transmision', 0, 12.0, r'''
const ac=E(R(5.6,8.4,T)), cam={s:L(1,1.9,ac)*L(1,1.04,R(0,6,T)),x:L(0,-330,ac),y:L(0,700,ac)};
X.save();camara(cam);
cabina(t,{ojo:[300,560,190],vista:fondo('estrellas',t,{A:[0,0,3,0]}),alarma:1,consolaY:1600});
const p=seq([[0,'habla'],[3.2,{t:9,h:14,bi:10,ci:80,bd:22,cd:150}],[5.6,{t:4,h:-2,bi:10,ci:80,bd:24,cd:150}]],T);
p.h+=ruido(T*1.3)*3;
const ab=E(R(6.3,7.6,T))*(1-R(9.5,10,T));
figura({tipo:'astro',x:560,y:1480,s:2.15,dir:1,pose:p,luz:[-.9,-.4],rim:`rgba(255,${70+60*(.5+.5*Math.sin(t*5.2))|0},50,.95)`,
  enVisor:(c,s,dir)=>{ if(ab>0) ojo2d(dir*34*s,8*s,26*s,ab,.15+.2*R(7,8,T)); }});
X.restore();
const k=R(8.3,8.6,T)*(1-R(11.7,12,T));
post(t,{grano:.18,lineas:.08,ruido:Math.max(corte(T,0,.4),k*(.45+.35*Math.abs(ruido(T*6))),T>10.1&&T<10.3?1:0),parpadeo:.15});
if(T>10.1&&T<10.25){pintaFondo('ojo',t,{A:[0,0,.9,0],B:[1,.1,0,0]});interferencia(t,.6)}
// HUD de la grabación
if(Math.floor(T*1.6)%2===0)texto('●',80,110,34,'#ff3b30',{al:'left',glow:14});
texto('REC  TRANSMISIÓN 0417',120,110,34,'rgba(255,220,200,.85)',{al:'left'});
texto('KRAKEN-1  →  EUROPA-2',80,160,28,'rgba(255,200,170,.55)',{al:'left',esp:2});
const sen=Math.max(0,3-Math.floor(R(7.8,9,T)*3));
for(let i=0;i<4;i++){X.fillStyle=i<sen?'rgba(255,220,200,.8)':'rgba(255,220,200,.15)';X.fillRect(860+i*34,140-i*14,22,24+i*14)}
if(k>0)texto('SEÑAL PERDIDA',W/2,H/2,64,`rgba(255,230,220,${.55+.45*(Math.floor(T*8)%2)})`,{esp:8,glow:20});
''')

# 12 · «No sé cuánto tiempo me queda. La señal está cayendo. Y mi oxígeno también. Pero si alguien recibe esto, por favor…»
E('s02-consola', 12.0, 21.0, r'''
X.save();camara({s:L(1.04,1.12,R(12,21,T))});
cabina(t,{alarma:.8,consolaY:1700});
const sig=Math.round(L(62,9,E(R(12.4,15,T)))), o2=L(34,11,E(R(15.3,17.8,T)));
pantalla(90,330,900,470,t,(w,h)=>{
  texto('SEÑAL',40,50,40,'rgba(255,200,170,.8)',{al:'left',esp:6});texto(sig+'%',w-40,50,56,sig<20?'#ff4a3a':'rgba(255,220,190,.95)',{al:'right',glow:12});
  X.strokeStyle=sig<20?'#ff4a3a':'rgba(255,190,140,.9)';X.lineWidth=4;X.beginPath();
  for(let i=0;i<=200;i++){const x=40+i/200*(w-80);const a=sig/62;const y=h*.62+Math.sin(i*.35+T*9)*70*a*(.6+.4*ruido(i*.2+T*3))+(hash(i+Math.floor(T*20))-.5)*30*(1-a);i?X.lineTo(x,y):X.moveTo(x,y)}X.stroke();
  for(let i=0;i<10;i++){X.fillStyle=i<sig/10?'rgba(255,200,150,.85)':'rgba(255,200,150,.12)';X.fillRect(40+i*((w-80)/10),h-60,(w-80)/10-10,26)}
});
pantalla(90,880,900,560,t,(w,h)=>{
  texto('O₂',40,50,44,'rgba(255,200,170,.8)',{al:'left',esp:6});
  const cx=w/2,cy=h*.78,r=300,a0=Math.PI*1.1,a1=Math.PI*1.9;
  X.lineWidth=34;X.strokeStyle='rgba(255,200,150,.12)';X.beginPath();X.arc(cx,cy,r,a0,a1);X.stroke();
  X.strokeStyle=o2<15?'#ff4030':'rgba(255,190,130,.9)';X.beginPath();X.arc(cx,cy,r,a0,L(a0,a1,o2/40));X.stroke();
  const an=L(a0,a1,o2/40);X.strokeStyle='#ffe2cc';X.lineWidth=8;X.beginPath();X.moveTo(cx,cy);X.lineTo(cx+Math.cos(an)*(r-50),cy+Math.sin(an)*(r-50));X.stroke();
  texto(o2.toFixed(0)+'%',cx,cy-90,90,o2<15?'#ff4a3a':'rgba(255,225,200,.95)',{glow:16});
  if(T>16.6&&Math.floor(T*4)%2===0)texto('OXÍGENO BAJO',cx,cy+10,40,'#ff4a3a',{esp:6,glow:14});
});
// botón de transmitir
const tr=R(18.5,18.8,T);
X.fillStyle=tr>0?'#ff3b30':'#3a1010';X.shadowColor='#ff3b30';X.shadowBlur=tr>0?40:0;X.beginPath();X.arc(820,1610,70,0,7);X.fill();X.shadowBlur=0;
texto('TX',820,1612,40,tr>0?'#fff':'rgba(255,190,170,.5)');
if(tr>0)texto('TRANSMITIENDO · TODAS LAS FRECUENCIAS',W/2,1500,30,'rgba(255,230,210,.9)',{esp:3});
// la mano: toca la pantalla de señal y luego aprieta TX
const m1=E(R(12.9,13.6,T))*(1-E(R(14.6,15.3,T))), m2=E(R(17.9,18.5,T));
if(m1>0)guante([-300,1500],[L(-160,300,m1),L(1300,700,m1)],1.15,{senala:1,dir:-1});
if(m2>0)guante([1300,2200],[L(1250,860,m2),L(2100,1720,m2)],1.15,{dir:1});
X.restore();
post(t,{ruido:corte(T,12)+Math.max(0,ruido(T*3)-.75)*.6,grano:.16,parpadeo:.12,lineas:.06});
''')

# 21 · «…no se acerquen a Júpiter.»
E('s03-jupiter', 21.0, 24.7, r'''
cabina(t,{consola:false});
const vx=60,vy=220,vw=960,vh=1250;
X.save();X.beginPath();X.roundRect(vx,vy,vw,vh,140);X.clip();
const z=L(.9,1.05,E(R(21,24.7,T)));
X.drawImage(fondo('planeta',t+60,{A:[.02,-.02,.36*z,0]}),0,0,W,H);
X.restore();
X.strokeStyle='#160b0b';X.lineWidth=40;X.beginPath();X.roundRect(vx,vy,vw,vh,140);X.stroke();
X.strokeStyle='rgba(255,170,110,.25)';X.lineWidth=3;X.beginPath();X.roundRect(vx+18,vy+18,vw-36,vh-36,124);X.stroke();
const g=X.createRadialGradient(W/2,800,100,W/2,800,1300);g.addColorStop(0,'rgba(255,150,80,.18)');g.addColorStop(1,'rgba(0,0,0,0)');X.fillStyle=g;X.fillRect(0,0,W,H);
const p=seq([[21,'mira'],[21.5,'vidrio',.8]],T);
figura({tipo:'astro',x:L(520,560,R(21,24,T)),suelo:2020,s:1.9,dir:1,pose:p,luz:[0,-1],borde:5,rim:'rgba(255,175,110,.95)',glow:26});
post(t,{ruido:corte(T,21),grano:.15});
''', q=.6)

# 24.7 · «Éramos cinco. Una misión científica sencilla,»
E('s04-cinco', 24.7, 28.2, r'''
cabina(t,{consola:false,ojo:[540,520,300],vista:fondo('estrellas',t,{A:[.3,0,2.2,0]})});
X.fillStyle='#070304';X.fillRect(-50,1560,W+100,500);X.fillStyle='rgba(255,150,100,.15)';X.fillRect(-50,1560,W+100,4);
// parche de la misión en la ventanilla
const pa=E(R(26,26.8,T));
if(pa>0){X.save();X.globalAlpha=pa;X.strokeStyle='rgba(255,200,160,.85)';X.lineWidth=6;X.beginPath();X.arc(540,520,250,0,7);X.stroke();
 X.lineWidth=2;X.beginPath();X.arc(540,520,200,0,7);X.stroke();
 const txt='MISIÓN CIENTÍFICA · KRAKEN-1 · EUROPA-2 · ';X.font='30px "Share Tech Mono"';X.fillStyle='rgba(255,210,180,.9)';X.textAlign='center';
 for(let i=0;i<txt.length;i++){const a=-Math.PI/2+(i/txt.length)*Math.PI*2+T*.05;X.save();X.translate(540+Math.cos(a)*226,520+Math.sin(a)*226);X.rotate(a+Math.PI/2);X.fillText(txt[i],0,0);X.restore()}
 X.restore()}
// los cinco entran y se forman
for(let i=0;i<5;i++){
  const ti=24.85+i*.22, x=L(-260,150+i*195,EO(R(ti,ti+.9,T)));
  const p=T<ti+.9?caminar(T+i*.3,1.1,1):seq([[0,'pie'],[ti+.9,'firme',.4],[26.1+i*.12,{t:0,h:i%2?-10:8,bi:-4,ci:8,bd:4,cd:8,pi:2,ri:0,pd:-2,rd:0}]],T);
  figura({tipo:'astro',x,suelo:1600,s:1.1,dir:1,pose:p,luz:[0,-1],rim:'rgba(255,180,120,.9)',coleta:i===3?T:0,sinCasco:false});
}
post(t,{ruido:corte(T,24.7),grano:.15});
''')

# 28.2 · «…enviada desde la estación orbital de Europa 2.»
E('s05-estacion', 28.2, 31.5, r'''
pintaFondo('planeta',t+20,{A:[-.12,-.36,.5,0]});
europa(L(760,700,R(28.2,31.5,T)),1550,420,t);
estacion(L(470,540,E(R(28.2,31.5,T))),900,.85,T*.15,{t:T,letrero:T>28.9?'EUROPA-2':''});
post(t,{ruido:corte(T,28.2),grano:.14});
''', q=.6)

# 31.5 · «El objetivo simple, descender a la gran mancha roja»
E('s06-mancha', 31.5, 35.5, r'''
const p=E(R(31.6,35.5,T));const rad=L(.26,1.0,p);const sp=[.26,.36];
const cen=[L(0,-sp[0]*rad,p),L(0,-sp[1]*rad,p)];
pintaFondo('planeta',t+40,{A:[cen[0],cen[1],rad,0],B:[0,0,0,0]});
// mira de objetivo sobre la mancha
const m=R(33.1,33.6,T);
if(m>0){const x=W/2+(cen[0]+sp[0]*rad)*H,y=H/2+(cen[1]+sp[1]*rad)*H,r=L(260,180,m)*(1+p);X.strokeStyle='rgba(255,230,210,.8)';X.lineWidth=3;
 X.beginPath();X.arc(x,y,r,0,7);X.stroke();for(const a of [0,1,2,3]){const c=Math.cos(a*Math.PI/2),s=Math.sin(a*Math.PI/2);X.beginPath();X.moveTo(x+c*(r-30),y+s*(r-30));X.lineTo(x+c*(r+30),y+s*(r+30));X.stroke()}
 texto('OBJETIVO · GRAN MANCHA ROJA',x,y-r-50,32,'rgba(255,230,210,.9)',{esp:3})}
post(t,{ruido:corte(T,31.5),grano:.14});
''', q=.6)

# 35.5 · «…con un módulo experimental, el Kraken 1, el cual estaba diseñado para soportar la atmósfera del planeta.»
E('s07-kraken', 35.5, 44.6, r'''
if(T<40.3){
  pintaFondo('planeta',t+80,{A:[0,.62,.75,0]});
  const su=E(R(36.6,39.5,T));
  estacion(540,L(80,-120,su),.9,T*.1,{t:T});
  kraken(540+ruido(T*.5)*10,L(420,860,su),1.15,ruido(T*.4)*4,{t:T,letrero:true,luz:[0,1],rim:'rgba(255,170,110,.9)',fuego:T>37.3?.35+.1*Math.sin(T*30):0});
  if(T<36.8){X.strokeStyle='#060405';X.lineWidth=14;for(const s of [-1,1]){X.beginPath();X.moveTo(540+s*60,200);X.lineTo(540+s*60,240);X.stroke()}}
}else{
  const d=T-40.3;
  pintaFondo('nubes',t,{A:[d*1.4,R(40.3,44.6,T)*.3,0,0]},{x:ruido(T*14)*14,y:ruido(T*13+5)*14});
  kraken(540+ruido(T*9)*12,880,1.2,ruido(T*7)*5,{t:T,letrero:true,plasma:1,fuego:.9,luz:[0,1],rim:'rgba(255,200,140,.95)'});
}
post(t,{ruido:corte(T,35.5)+corte(T,40.3),grano:.15});
''', q=.55)

# 44.6 · «Buscábamos estructuras anómalas, que fueron detectadas por unas sondas que se habían enviado,»
E('s08-sondas', 44.6, 51.0, r'''
pintaFondo('nubes',t,{A:[t*.25,.25,.6,0]});
// estructuras: aparecen cuando las barre un pulso
const est=[[300,1300,1],[760,1500,2],[540,1150,3]];
for(const [x,y,s] of est){const ap=R(45.2+s*.4,46+s*.4,T);if(ap<=0)continue;X.save();X.globalAlpha=ap*(.45+.25*Math.sin(T*3+s));X.strokeStyle='rgba(255,230,200,.9)';X.lineWidth=3;X.shadowColor='#ffd0a0';X.shadowBlur=12;
 X.translate(x,y);X.rotate(T*.1*s);X.strokeRect(-60*s*.6,-60*s*.6,120*s*.6,120*s*.6);X.rotate(.785);X.strokeRect(-40*s*.6,-40*s*.6,80*s*.6,80*s*.6);X.beginPath();X.arc(0,0,20*s,0,7);X.stroke();X.restore()}
// sondas que caen
const so=[[260,.0,46.5],[560,.4,46.9],[840,.7,47.3]];
for(const [x,f,t0] of so){const y=L(-200,L(500,900,f),E(R(t0-1.5,t0+2.5,T)));sonda(x,y,1,T,{fase:f});if(T>t0)pings(x,y+40,T-t0,{max:900,per:1.6,n:3,arco:[.2,Math.PI-.2]})}
post(t,{ruido:corte(T,44.6),grano:.15});
if(T>45.1)etiqueta(T,'ESTRUCTURAS ANÓMALAS',80,140,45.1,{px:38});
if(T>47.3)etiqueta(T,'SONDAS 1 · 2 · 3',80,200,47.3,{px:30,col:'rgba(255,200,170,.7)'});
''')

# 51 · «ya que algo, algo no debía de estar ahí.»
E('s09-radar', 51.0, 55.2, r'''
cabina(t,{consola:false});
pantalla(60,330,960,1260,t,(w,h)=>{
  const cx=w/2,cy=h/2,r=440;
  X.strokeStyle='rgba(255,140,90,.25)';X.lineWidth=2;for(let i=1;i<=4;i++){X.beginPath();X.arc(cx,cy,r*i/4,0,7);X.stroke()}
  X.beginPath();X.moveTo(cx-r,cy);X.lineTo(cx+r,cy);X.moveTo(cx,cy-r);X.lineTo(cx,cy+r);X.stroke();
  const a=T*2.2;const g=X.createConicGradient?X.createConicGradient(a-.9,cx,cy):null;
  if(g){g.addColorStop(0,'rgba(255,120,60,0)');g.addColorStop(.14,'rgba(255,120,60,.45)');g.addColorStop(.145,'rgba(255,120,60,0)');X.fillStyle=g;X.beginPath();X.arc(cx,cy,r,0,7);X.fill()}
  X.strokeStyle='rgba(255,180,120,.9)';X.lineWidth=4;X.beginPath();X.moveTo(cx,cy);X.lineTo(cx+Math.cos(a)*r,cy+Math.sin(a)*r);X.stroke();
  for(let i=0;i<9;i++){const bx=cx+(hash(i)-.5)*600,by=cy+(hash(i+20)-.5)*600;X.fillStyle=`rgba(255,200,150,${.3+.4*hash(i+Math.floor(T*2))})`;X.beginPath();X.arc(bx,by,6,0,7);X.fill()}
  // la cosa que no debía estar ahí
  const b=E(R(53.3,54.4,T));
  if(b>0){X.save();X.globalAlpha=b*(.7+.3*Math.sin(T*12));X.fillStyle='rgba(255,60,40,.55)';X.shadowColor='#ff3020';X.shadowBlur=40;
   X.beginPath();X.ellipse(cx+40,cy+120,r*.75*b,r*.32*b,-.4,0,7);X.fill();X.restore();
   texto('ANOMALÍA · TAMAÑO DESCONOCIDO',cx,h-90,38,`rgba(255,80,60,${Math.floor(T*4)%2?1:.4})`,{esp:4,glow:14})}
  texto('RADAR PROFUNDO',60,60,34,'rgba(255,200,170,.7)',{al:'left',esp:4});
},{brillo:.5});
post(t,{ruido:corte(T,51),grano:.16,parpadeo:.1});
''')

# 55.2 · «Y lo encontramos. Al principio solo era una lectura de densidad. Algo enorme moviéndose dentro de la tormenta.»
E('s10-lectura', 55.2, 65.9, r'''
cabina(t,{consola:false,alarma:.25});
pantalla(110,260,860,700,t,(w,h)=>{
  if(T<61.6){
    texto('DENSIDAD',40,50,36,'rgba(255,200,170,.8)',{al:'left',esp:6});
    X.strokeStyle='rgba(255,190,130,.95)';X.lineWidth=5;X.beginPath();
    for(let i=0;i<=240;i++){const x=30+i/240*(w-60);const tt=i/240*10;const sp=E(R(59.4,60.9,T))*Math.exp(-Math.pow((tt-7.5)/.6,2))*380;const y=h-110-20*ruido(tt*3+T)-sp;i?X.lineTo(x,y):X.moveTo(x,y)}X.stroke();
    if(T>60.2)texto('▲ '+Math.round(L(1,9400,E(R(60.2,61.3,T))))+' kg/m³',w*.75,120,40,'#ff6a4a',{glow:12});
  }else{
    texto('MAPA DE DENSIDAD',40,50,36,'rgba(255,200,170,.8)',{al:'left',esp:6});
    const bx=L(-200,w+200,R(61.7,66,T)),by=h*.58+Math.sin(T*1.3)*40;
    for(let gx=0;gx<w;gx+=28)for(let gy=90;gy<h;gy+=28){const d=Math.hypot((gx-bx)/380,(gy-by)/150);const v=Math.max(0,1-d)+.08*hash(gx*3+gy+Math.floor(T*6));
     X.fillStyle=`rgba(255,${Math.round(200-150*v)},${Math.round(120-100*v)},${.1+v*.85})`;X.fillRect(gx,gy,24,24)}
  }
},{brillo:.9});
// la tripulación de espaldas, mirando la pantalla
const lean=E(R(61.7,63,T));
const xs=[[220,1.25,-1],[540,1.35,1],[860,1.25,1]];
for(const [x,s,d] of xs){const p=seq([[0,{t:4,h:-10,bi:-4,ci:10,bd:4,cd:12}],[61.7,{t:14,h:-18,bi:10,ci:30,bd:14,cd:30}]],T);p.h+=ruido(T*.7+x)*3;
 figura({tipo:'astro',x,suelo:2050,s,dir:d,pose:p,luz:[0,-1],rim:'rgba(255,180,110,.95)',glow:24,visor:false})}
post(t,{ruido:corte(T,55.2),grano:.15});
''')

# 65.9 · «Como si estuviera nadando entre las nubes de gas y los cristales de amoníaco. Pensamos que era una aberración climática. Una especie de tormenta.»
E('s11-nadando', 65.9, 76.0, r'''
const sx=L(-1.1,1.2,R(65.9,76,T)),sy=.18+Math.sin(T*.6)*.05;
pintaFondo('nubes',t,{A:[t*.06,.15,1,0],B:[sx*.5,sy,.65,.17]});
// lomo colosal entre las nubes
X.save();X.filter='blur(9px)';X.globalAlpha=.85*(1-R(71.5,74.5,T)*.55);X.fillStyle='#0d0302';
const bx=W/2+sx*H*.5,by=H/2+sy*H;X.beginPath();
for(let i=0;i<=40;i++){const u=i/40,x=bx-700+u*1400,y=by-120*Math.sin(u*Math.PI)*(1+.2*Math.sin(T+u*6))-30*Math.sin(u*9+T*2);i?X.lineTo(x,y):X.moveTo(x,y)}
for(let i=40;i>=0;i--){const u=i/40,x=bx-700+u*1400,y=by+60+80*Math.sin(u*Math.PI);X.lineTo(x,y)}
X.fill();
// aletas y cola
for(let i=0;i<5;i++){const u=.25+i*.12,x=bx-700+u*1400,y=by-120*Math.sin(u*Math.PI)-30*Math.sin(u*9+T*2);X.beginPath();X.moveTo(x-50,y+10);X.quadraticCurveTo(x-10,y-140-30*Math.sin(T*2+i),x+70,y-40-20*Math.sin(T*2+i));X.lineTo(x+40,y+10);X.fill()}
X.lineWidth=60;X.lineCap='round';X.strokeStyle='#0d0302';X.beginPath();X.moveTo(bx-690,by+20);X.quadraticCurveTo(bx-950,by+120+Math.sin(T*1.4)*90,bx-1250,by+40+Math.sin(T*1.4+1)*160);X.stroke();
X.restore();
// niebla encima para que se vea entre nubes
X.save();X.globalAlpha=.35;X.drawImage(fondo('nubes',t+9,{A:[t*.06+3,.1,0,0]}),0,0,W,H);X.restore();
kraken(540+ruido(T*.3)*30,330,.35,ruido(T*.5)*8,{t:T,luz:[0,1]});
post(t,{ruido:corte(T,65.9),grano:.15});
if(T>68.4)etiqueta(T,'CRISTALES DE AMONÍACO',80,1780,68.4,{px:30,col:'rgba(255,230,210,.7)'});
''', q=.55)

# 76 · «Pero cuando descendimos lo suficiente, lo vimos. No tengo palabras para describirlo. Y aún así, lo voy a intentar.»
E('s12-vimos', 76.0, 87.0, r'''
if(T<78.8){
  pintaFondo('nubes',t,{A:[t*.5,R(76,78.8,T)*.9,0,0]});
  kraken(540,L(400,1100,E(R(76,78.8,T))),.8,ruido(T)*4,{t:T,luz:[0,1],fuego:.3});
}else{
  cabina(t,{consola:false});
  const vx=40,vy=180,vw=1000,vh=1300,fl=1-R(78.8,79.6,T);
  X.save();X.beginPath();X.roundRect(vx,vy,vw,vh,160);X.clip();
  X.drawImage(fondo('ojo',t,{A:[0,.6,1.8,0],B:[0,0,0,0]}),0,0,W,H);
  X.fillStyle=`rgba(255,230,200,${fl*.8})`;X.fillRect(0,0,W,H);X.restore();
  X.strokeStyle='#160b0b';X.lineWidth=40;X.beginPath();X.roundRect(vx,vy,vw,vh,160);X.stroke();
  const g=X.createRadialGradient(W/2,900,100,W/2,900,1400);g.addColorStop(0,'rgba(255,140,60,.25)');g.addColorStop(1,'rgba(0,0,0,0)');X.fillStyle=g;X.fillRect(0,0,W,H);
  const p=seq([[78.8,'vidrio'],[81.2,{t:2,h:-14,bi:15,ci:30,bd:40,cd:30},1.2],[83.3,{t:-4,h:-6,bi:5,ci:20,bd:20,cd:40},1.2]],T);
  p.h+=Math.sin(T*1.7)*2;
  figura({tipo:'astro',x:L(560,480,E(R(81.2,84,T))),suelo:2000,s:2,dir:1,pose:p,luz:[0,-1],borde:6,glow:30,rim:'rgba(255,170,90,1)'});
}
post(t,{ruido:corte(T,76)+corte(T,78.8,.3),grano:.15});
''', q=.6)

# 87 · «Era un ojo. Solo eso. Un ojo del tamaño de una ciudad que se abrió lentamente frente a nosotros. Entre esos remolinos anaranjados. Como si nos hubiera estado esperando.»
E('s13-ojo', 87.0, 105.0, r'''
const ab=Math.max(.04*R(87.2,88.2,T),E(R(93.4,98.5,T)));
const pup=L(.12,.55,E(R(101,104,T)));
const z=L(1.25,.95,E(R(87,105,T)));
pintaFondo('ojo',t,{A:[0,-.02,z,0],B:[ab,pup,0,0],D:[0,L(0,.18,E(R(100.9,104,T))),0,0]},{s:1+.05*R(87,105,T)});
const ci=E(R(91.2,92.6,T))*(1-E(R(97.4,98.6,T)));
if(ci>0){X.save();X.globalAlpha=ci;ciudad(H-140+(1-ci)*300,1.3,1,5);X.restore()}
const ky=L(1500,1350,R(87,105,T)),kx=W/2+ruido(T*.4)*30;
kraken(kx,ky,.28,ruido(T*.3)*6,{t:T,ventanas:1,luz:[0,-1]});
post(t,{ruido:corte(T,87),grano:.15,vig:.85});
''', q=.66)

# 105 · «Un susurro cruzó la nave. Pero no provenía del radio.»
E('s14-susurro', 105.0, 109.6, r'''
const tc=tmpCanvas(),tx=tc.getContext('2d');
if(T<107){
  cabina(t,{alarma:.2,consolaY:1700});
  for(const [x,s,d,ph] of [[250,1.3,1,0],[560,1.4,-1,1],[860,1.25,-1,2]]){
    const gira=E(R(105.6+ph*.15,106.3+ph*.15,T));
    figura({tipo:'astro',x,suelo:1760,s,dir:d*(gira>.5?-1:1),pose:{...POSES.pie,h:L(0,-20,gira)},luz:[0,-1],rim:'rgba(255,170,110,.9)'});
  }
  // onda que atraviesa la nave (distorsión)
  const wx=L(W+300,-400,R(105.3,106.9,T));
  tx.clearRect(0,0,W,H);tx.drawImage(cv,0,0);
  for(let y=0;y<H;y+=8){const dx=Math.sin(y*.012+T*9)*16*Math.exp(-Math.pow((wx-W/2)/520,2));X.drawImage(tc,0,y,W,8,dx,y,W,8)}
  X.strokeStyle='rgba(255,160,120,.35)';X.lineWidth=6;for(let i=0;i<3;i++){X.beginPath();X.arc(wx+i*90,H/2,900+i*40,Math.PI*.7,Math.PI*1.3);X.stroke()}
}else{
  cabina(t,{consola:false});
  pantalla(90,520,900,640,t,(w,h)=>{
    texto('RADIO · 121.5 MHz',40,50,36,'rgba(255,200,170,.8)',{al:'left',esp:4});
    X.strokeStyle='rgba(255,190,130,.9)';X.lineWidth=4;X.beginPath();X.moveTo(30,h/2);for(let i=0;i<=100;i++)X.lineTo(30+i/100*(w-60),h/2+(hash(i+Math.floor(T*15))-.5)*4);X.stroke();
    texto('SIN SEÑAL',w/2,h-80,52,'#ff5a4a',{esp:8,glow:14});
  },{brillo:.5});
  // bocina de la radio, quieta
  X.fillStyle='#0d0707';X.beginPath();X.roundRect(340,1260,400,260,30);X.fill();X.fillStyle='rgba(255,160,120,.15)';
  for(let i=0;i<6;i++)for(let j=0;j<4;j++){X.beginPath();X.arc(390+i*60,1310+j*55,12,0,7);X.fill()}
}
post(t,{ruido:corte(T,105)+corte(T,107,.3),grano:.16});
''')

# 109.6 · «Era algo mental.»
E('s15-mental', 109.6, 113.9, r'''
cabina(t,{consola:false,alarma:.15});
const p={...POSES.pie,h:-6+ruido(T)*3};
X.save();camara({s:L(1.6,1.75,R(109.6,113.9,T)),y:450});
const k=figura({tipo:'astro',x:540,y:1480,s:2.6,dir:1,pose:p,luz:[-1,0],rim:'rgba(255,140,90,.95)',visor:true});
X.restore();
// ondas que entran a la cabeza
const cx=540,cy=640;
for(let i=0;i<5;i++){const ph=((T-110)*.7+i/5)%1;if(T<110.2)continue;const r=L(900,40,E(ph));X.strokeStyle=`rgba(255,120,90,${ph*.7})`;X.lineWidth=5;X.beginPath();X.arc(cx,cy,r,0,7);X.stroke()}
const g=X.createRadialGradient(cx,cy,10,cx,cy,260);g.addColorStop(0,`rgba(255,200,140,${.6*R(110.4,111.4,T)})`);g.addColorStop(1,'rgba(255,100,60,0)');X.fillStyle=g;X.fillRect(0,0,W,H);
post(t,{ruido:corte(T,109.6),grano:.16});
''')

# 113.9 · «Era algo raro. Era un idioma que no conocía. Pero que en lo más profundo de mi ser, lo conocía. Lo lograba entender.»
E('s16-idioma', 113.9, 125.0, r'''
X.fillStyle='#070304';X.fillRect(0,0,W,H);
const neb=fondo('niebla',t,{});X.save();X.globalAlpha=.35;X.drawImage(neb,0,0,W,H);X.restore();
// cabeza de perfil enorme
const k=figura({tipo:'astro',x:420,y:2100,s:3.4,dir:1,pose:{...POSES.pie,h:-4+ruido(T*.5)*2},luz:[1,-.2],rim:'rgba(255,150,100,.9)',glow:30,visor:false});
const ord=E(R(120.3,123.6,T)),deep=R(117.6,119.8,T);
// glifos que fluyen hacia la cabeza
for(let i=0;i<70;i++){
  const sd=i*7.3,vel=.12+hash(sd)*.1,ph=((T-114)*vel+hash(sd+1))%1;if(T<114.6)continue;
  const sx=W+100,sy=200+hash(sd+2)*1500,tx=k.cab[0]+40,ty=k.cab[1];
  let x=L(sx,tx,ph),y=L(sy,ty,ph)+Math.sin(ph*8+sd)*60*(1-ph);
  // ordenados en renglones cuando «lo entiende»
  const rx=140+(i%9)*100,ry=320+Math.floor(i/9)*95;x=L(x,rx,ord);y=L(y,ry,ord);
  const c=ord>.5?`rgba(255,235,200,${.9})`:`rgba(255,${120+100*deep|0},90,${.85*(1-ph*.6*(1-ord))})`;
  glifo(x,y,L(46,58,ord),sd,c,{glow:ord>.3?16:6,rot:(1-ord)*ph*3});
}
// brillo en lo más profundo
if(deep>0){const g=X.createRadialGradient(k.cab[0],k.cab[1],10,k.cab[0],k.cab[1],420);g.addColorStop(0,`rgba(255,210,150,${.75*deep})`);g.addColorStop(1,'rgba(255,90,40,0)');X.fillStyle=g;X.fillRect(0,0,W,H)}
post(t,{ruido:corte(T,113.9),grano:.16});
''')

# 125 · «Como si mis células estuvieran temblando al oírlo.»
E('s17-celulas', 125.0, 129.2, r'''
X.fillStyle='#080304';X.fillRect(0,0,W,H);
const tb=R(125.2,126.6,T);const sh=()=>[(hash(Math.floor(T*30))-.5)*14*tb,(hash(Math.floor(T*30)+3)-.5)*14*tb];
const [dx,dy]=sh();
// mano abierta enorme que tiembla, con células por dentro
guante([540+dx,2500],[540+dx,1250+dy],2.6,{abierta:1,dir:1,rim:'rgba(255,120,80,.95)',dentro:()=>{const c=X;
  c.fillStyle='#120504';c.fillRect(0,0,W,H);
  for(let i=0;i<170;i++){const cx=180+hash(i)*720+dx+Math.sin(T*40+i)*6*tb,cy=520+hash(i+40)*1400+dy+Math.cos(T*37+i)*6*tb,r=16+hash(i+80)*26;
   c.strokeStyle=`rgba(255,${110+hash(i)*80|0},80,${.35+.45*tb})`;c.lineWidth=3;c.beginPath();c.arc(cx,cy,r*(1+.15*Math.sin(T*25+i)*tb),0,7);c.stroke();c.fillStyle='rgba(255,140,100,.4)';c.beginPath();c.arc(cx+r*.2,cy,r*.25,0,7);c.fill()}}});
post(t,{ruido:corte(T,125)+tb*.15*Math.abs(ruido(T*20)),grano:.17});
''')

# 129.2 · «Los demás comenzaron a murmurar cosas que no tenían sentido. Ramírez. Él arrancó su propio visor mientras gritaba que el cielo se metía bajo la piel.»
E('s18-ramirez', 129.2, 139.6, r'''
if(T<133.8){
  cabina(t,{alarma:.4,consolaY:1700});
  for(const [x,s,d,i] of [[180,1.15,1,0],[420,1.25,-1,1],[680,1.2,1,2],[900,1.1,-1,3]]){
    const p={...POSES.pie,t:Math.sin(T*1.3+i)*6,h:Math.sin(T*1.7+i*2)*14,bi:-6+Math.sin(T+i)*8,bd:8+Math.sin(T*1.2+i)*10};
    const k=figura({tipo:'astro',x,suelo:1760,s,dir:d,pose:p,luz:[0,-1],rim:'rgba(255,160,100,.9)'});
    for(let j=0;j<5;j++){const ph=((T-129.4)*.5+j/5+i*.13)%1;if(T<129.5)continue;glifo(k.cab[0]+d*60+ph*d*120,k.cab[1]-40-ph*260,26,i*20+j+Math.floor((T-129.4)*.5+j/5),`rgba(255,200,170,${(1-ph)*.8})`,{rot:ph*2})}
  }
}else{
  cabina(t,{alarma:1,consolaY:1700});
  const ar=R(134.8,135.6,T),gr=R(136,136.6,T);
  const p=seq([[133.8,'pie'],[134.6,'arranca',.5],[135.8,'grita',.6]],T);
  p.t+=Math.sin(T*18)*3*gr;p.h+=Math.sin(T*21)*5*gr;
  const sin=T>135.5;
  const k=figura({tipo:'astro',sinCasco:sin,x:560,suelo:1800,s:2.1,dir:1,pose:p,luz:[-1,-.3],rim:'rgba(255,60,40,.95)',glow:26});
  // el casco sale volando
  if(sin){const u=R(135.5,137,T);X.fillStyle='#050304';X.beginPath();X.arc(L(k.cab[0],1100,EO(u)),L(k.cab[1],300,EO(u))+u*u*700,126,0,7);X.fill()}
  // el cielo bajo la piel: venas rojas que crecen
  if(gr>0){X.save();X.strokeStyle='rgba(255,70,40,.9)';X.shadowColor='#ff3a20';X.shadowBlur=16;X.lineWidth=4;
   const pts=puntosCuerpo(k,60,9);for(let i=0;i<pts.length;i++){const [x,y,r]=pts[i];if(r>R(136,138.6,T))continue;X.beginPath();X.moveTo(x,y);let cx=x,cy=y;for(let j=0;j<5;j++){cx+=(hash(i*7+j)-.5)*60;cy+=(hash(i*9+j)-.5)*60;X.lineTo(cx,cy)}X.stroke()}X.restore()}
  if(T>133.9)etiqueta(T,'RAMÍREZ',80,150,133.9,{px:52});
}
post(t,{ruido:corte(T,129.2)+corte(T,133.8),grano:.16,parpadeo:.2});
''')

# 139.6 · «Lina. Ella se arrodilló frente a la pantalla y comenzó a llorar. Dijo que veía a su madre muerta detrás del ojo.»
E('s19-lina', 139.6, 148.7, r'''
cabina(t,{alarma:.35,consolaY:1700});
const br=.7+.3*Math.sin(t*3.1)*Math.sin(t*1.7);
pantalla(470,300,560,860,t,(w,h)=>{
  const c=fondo('ojo',t,{A:[0,0,.75,0],B:[.9,L(.2,.5,R(145.3,147,T)),0,0]});
  X.drawImage(c,-(h*W/H-w)/2,0,h*W/H,h);
  const m=E(R(145.4,146.6,T));
  if(m>0){X.save();X.globalAlpha=m*(.75+.25*Math.sin(T*23));X.translate(w/2,h/2+90);
    figura({tipo:'mujer',x:0,suelo:0,s:.42,dir:-1,pose:{...POSES.firme,h:6+3*Math.sin(T*.7)},color:'#eadcd0',borde:0});X.restore()}
},{brillo:br});
const p=T<141.4?caminar(T,.8,.8):seq([[141.4,'pie'],[141.45,'rodillas',.7],[143.2,'llora',.6]],T);
const llora=R(143.2,143.8,T);p.t+=Math.sin(T*14)*2.5*llora;p.h+=Math.sin(T*14+1)*3*llora;
const x=L(120,300,E(R(139.6,141.6,T)));
figura({tipo:'astro',sinCasco:true,coleta:T,x,suelo:1760,s:1.9,dir:1,pose:p,luz:[1,-.2],rim:'rgba(255,160,80,.95)',glow:24});
if(T>139.8)etiqueta(T,'LINA',80,150,139.8,{px:52});
post(t,{ruido:corte(T,139.6),grano:.16,parpadeo:.1});
''')

# 148.7 · «Yo. Yo intenté detenerlos. Lo juro. Pero el leviatán ya estaba adentro. Y no de la nave. De nosotros.»
E('s20-adentro', 148.7, 160.2, r'''
const ap=R(156.4,157.2,T);
cabina(t,{alarma:1-ap,consolaY:1700});
if(ap>0){X.fillStyle=`rgba(0,0,0,${ap*.85})`;X.fillRect(0,0,W,H)}
const llega=E(R(150.1,151.6,T));
const pY=T<150.1?{...POSES.pie}:T<151.6?caminar(T,1.4,1.2):seq([[151.6,'jala',.3]],T);
const pR={...POSES.grita,t:-10+Math.sin(T*9)*3,h:-30};
const fy={tipo:'astro',x:L(120,520,llega),suelo:1760,s:1.6,dir:1,pose:pY,luz:[0,-1],rim:'rgba(255,170,110,.9)'};
const fr={tipo:'astro',sinCasco:true,x:790,suelo:1760,s:1.6,dir:-1,pose:pR,luz:[0,-1],rim:'rgba(255,60,40,.9)'};
const llena=E(R(153.3,155.2,T));
figura(fr);figura(fy);
if(llena>0){const img=fondo(T<158.1?'nubes':'ojo',t,T<158.1?{A:[t*.2,0,0,0]}:{A:[0,0,.55,0],B:[E(R(158.1,159,T)),.15,0,0]});
  figuraRelleno({...fr,alfa:llena},img);figuraRelleno({...fy,alfa:llena},img)}
if(T>149.3)etiqueta(T,'YO',80,150,149.3,{px:52});
post(t,{ruido:corte(T,148.7)+corte(T,158.1,.3),grano:.16,parpadeo:.15*(1-ap)});
''', q=.5)

# 160.2 · «Porque eso era. No una criatura. No como la conocemos. Era una presencia antigua. Anterior a la materia. Al tiempo. Al universo mismo.»
E('s21-antigua', 160.2, 172.5, r'''
if(T<164.6){
  pintaFondo('niebla',t,{});
  // la «criatura» se deshace: no es eso
  const des=R(161.7,164,T);
  X.save();X.globalAlpha=1-des;X.fillStyle='#050203';X.beginPath();X.ellipse(540,900,330,420,0,0,7);X.fill();
  X.lineCap='round';for(let i=0;i<8;i++){X.lineWidth=46-i*2;X.strokeStyle='#050203';X.beginPath();X.moveTo(540+(i-3.5)*70,1200);
   X.bezierCurveTo(540+(i-3.5)*120+Math.sin(T*1.5+i)*80,1500,540+(i-3.5)*60+Math.cos(T+i)*120,1700,540+(i-3.5)*140,1950);X.stroke()}
  ojo2d(540,860,140,.6+.1*Math.sin(T*2),.2);X.restore();
  if(des>0){for(let i=0;i<300;i++){const r=hash(i);const x=540+(hash(i+1)-.5)*700,y=900+(hash(i+2)-.5)*1000;const q=Math.max(0,des*1.5-r*.5);X.fillStyle=`rgba(255,120,90,${(1-q)*.8})`;X.fillRect(x+(hash(i+3)-.5)*q*900,y-q*600,4,4)}}
}else{
  const col=E(R(167.3,169.6,T)),fl=R(170.2,170.6,T)*(1-R(170.6,171.6,T));
  pintaFondo('cosmos',t,{A:[col,col*.6+fl,0,R(171.4,172.2,T)]});
  // la presencia: un ojo que abarca todo
  const pr=R(170.6,172,T);if(pr>0){X.save();X.globalAlpha=pr*.6;X.strokeStyle='rgba(255,60,40,.8)';X.lineWidth=6;X.shadowColor='#ff3020';X.shadowBlur=30;
   X.beginPath();X.moveTo(-100,960);X.quadraticCurveTo(540,960-1100*pr,1180,960);X.quadraticCurveTo(540,960+1100*pr,-100,960);X.stroke();X.restore()}
}
post(t,{ruido:corte(T,160.2)+corte(T,164.6,.3),grano:.15});
''', q=.55)

# 172.5 · «Había estado durmiendo bajo Júpiter desde que el sol existía. Y nos vio llegar.»
E('s22-dormia', 172.5, 179.4, r'''
const sol=E(R(174.7,176,T));
const ab=L(0,.32,E(R(177.4,178.6,T)));
pintaFondo('planeta',t+100,{A:[-.05,.08,.42,0],B:[Math.max(.02,ab),.1,0,0]});
// el sol se enciende al fondo
if(sol>0){const g=X.createRadialGradient(980,140,10,980,140,700);g.addColorStop(0,`rgba(255,250,230,${sol})`);g.addColorStop(.08,`rgba(255,220,160,${sol*.9})`);g.addColorStop(.3,`rgba(255,140,60,${sol*.3})`);g.addColorStop(1,'rgba(0,0,0,0)');
 X.save();X.globalCompositeOperation='lighter';X.fillStyle=g;X.fillRect(0,0,W,H);X.restore()}
// zzz: respiración de algo dormido (pulso tenue en la mancha)
const sx=W/2+(-.05+.26*.42)*H,sy=H/2+(.08+.36*.42)*H;
const pu=.5+.5*Math.sin(T*1.1);X.fillStyle=`rgba(255,80,40,${.12*pu*(1-ab)})`;X.beginPath();X.ellipse(sx,sy,140,80,0,0,7);X.fill();
// el módulo llega
if(T>176.6){const u=E(R(176.6,178.6,T));X.fillStyle='#fff3e0';X.shadowColor='#ffd0a0';X.shadowBlur=14;X.beginPath();X.arc(L(1150,sx+40,u),L(-50,sy-120,u),5,0,7);X.fill();X.shadowBlur=0}
post(t,{ruido:corte(T,172.5),grano:.14});
''', q=.6)

# 179.4 · «Uno por uno mis compañeros desaparecieron en la niebla roja. No gritaban. Eso era lo peor. Solo, solo se disolvieron. Como si nunca hubieran estado ahí.»
E('s23-disuelven', 179.4, 190.4, r'''
pintaFondo('niebla',t,{});
const F=[[190,1.35,180.4],[430,1.6,182.1],[680,1.5,186.9],[900,1.3,188.8]];
for(const [x,s,t0] of F){const f={tipo:'astro',x,suelo:1500+s*200,s,dir:x<540?1:-1,pose:{...POSES.pie,h:Math.sin(T*.4+x)*4},luz:[0,-1],rim:'rgba(255,90,70,.9)'};
 disuelve(f,R(t0,t0+1.8,T),{seed:x})}
// niebla delante
const n2=fondo('niebla',t+30,{});X.save();X.globalAlpha=.3;X.drawImage(n2,0,300,W,H);X.restore();
post(t,{ruido:corte(T,179.4),grano:.16,vig:.85});
''')

# 190.4 · «Y yo. Y yo. Aunque estoy aquí. Pero ya no soy el mismo. Siento el leviatán dentro de mí.»
E('s24-yo', 190.4, 199.9, r'''
cabina(t,{alarma:.15,consolaY:1700});
X.fillStyle='rgba(0,0,0,.45)';X.fillRect(0,0,W,H);
const p=seq([[190.4,'cabizbajo'],[192.9,{t:6,h:10,bi:10,ci:40,bd:12,cd:40}],[197.6,{t:-6,h:-20,bi:20,ci:60,bd:24,cd:60}]],T);
const f={tipo:'astro',sinCasco:true,x:540,suelo:1820,s:2.1,dir:1,pose:p,luz:[0,-1],rim:'rgba(255,150,100,.9)'};
// ya no es el mismo: copias desfasadas
const gl=R(195.1,195.8,T);
if(gl>0){for(const [c,dx] of [['rgba(255,40,40,.5)',-24],['rgba(80,200,255,.35)',22]]){X.save();X.translate(dx*gl*(1+ruido(T*5)),0);figura({...f,color:c,borde:0});X.restore()}}
const k=figura(f);
// el ojo se abre en el pecho
const oj=E(R(197.6,198.8,T));
if(oj>0){const cx=L(k.hip[0],k.cuello[0],.55),cy=L(k.hip[1],k.cuello[1],.55);const g=X.createRadialGradient(cx,cy,10,cx,cy,300);g.addColorStop(0,`rgba(255,150,60,${.5*oj})`);g.addColorStop(1,'rgba(255,60,20,0)');X.fillStyle=g;X.fillRect(0,0,W,H);ojo2d(cx,cy,70,oj,.15+.2*R(198.6,199.8,T))}
post(t,{ruido:corte(T,190.4)+gl*(1-R(195.8,196.4,T))*.6,grano:.16});
''')

# 199.9 · «Arrastrando mis recuerdos. Mezclando mi conciencia con otros. Con otras cosas que no deberían existir.»
E('s25-recuerdos', 199.9, 207.7, r'''
X.fillStyle='#090304';X.fillRect(0,0,W,H);
const nb=fondo('niebla',t,{});X.save();X.globalAlpha=.5;X.drawImage(nb,0,0,W,H);X.restore();
// remolino al centro
const cx=540,cy=980;for(let i=0;i<60;i++){const a=i*.4+T*1.5,r=20+i*12;X.strokeStyle=`rgba(255,90,60,${.25-i*.003})`;X.lineWidth=3;X.beginPath();X.arc(cx,cy,r,a,a+1.2);X.stroke()}
const marcos=[
 (w,h)=>{figura({tipo:'nina',x:w*.35,suelo:h*.92,s:.9,dir:1,pose:{...POSES.pie,bd:150,cd:10},borde:0,color:'#120807'});X.strokeStyle='#120807';X.lineWidth=2;X.beginPath();X.moveTo(w*.42,h*.3);X.lineTo(w*.8,h*.12);X.stroke();X.fillStyle='#120807';X.beginPath();X.moveTo(w*.8,h*.05);X.lineTo(w*.88,h*.13);X.lineTo(w*.8,h*.22);X.lineTo(w*.72,h*.13);X.fill()},
 (w,h)=>{X.fillStyle='#120807';X.beginPath();X.moveTo(w*.2,h*.55);X.lineTo(w*.5,h*.3);X.lineTo(w*.8,h*.55);X.lineTo(w*.8,h*.95);X.lineTo(w*.2,h*.95);X.fill();X.fillStyle='rgba(255,210,140,.9)';X.fillRect(w*.42,h*.62,w*.16,h*.12)},
 (w,h)=>{figura({tipo:'mujer',x:w*.5,suelo:h*.95,s:.75,dir:1,pose:{...POSES.pie,bd:160,cd:20},borde:0,color:'#120807'})},
 (w,h)=>{figura({tipo:'persona',x:w*.4,suelo:h*.95,s:.7,dir:1,pose:{...POSES.pie,bd:40,cd:30},borde:0,color:'#120807'});figura({tipo:'nina',x:w*.65,suelo:h*.95,s:.7,dir:-1,pose:{...POSES.pie,bd:40,cd:30},borde:0,color:'#120807'})},
];
const raro=(w,h,i)=>{X.fillStyle='#120807';X.beginPath();X.ellipse(w/2,h*.45,w*.25,h*.25,0,0,7);X.fill();X.lineCap='round';for(let j=0;j<5;j++){X.strokeStyle='#120807';X.lineWidth=10;X.beginPath();X.moveTo(w/2+(j-2)*20,h*.6);X.quadraticCurveTo(w/2+(j-2)*60+Math.sin(T*3+j)*30,h*.8,w/2+(j-2)*50,h*.98);X.stroke()}ojo2d(w/2,h*.43,w*.12,.8,.2)};
for(let i=0;i<8;i++){
  const base=i%4,t0=200+i*.55,tira=E(R(t0,t0+3.8,T));
  const a=i*.8+T*.6+tira*4,r=L(560+hash(i)*120,0,tira);
  const x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r*1.2,sc=L(1,.05,tira);if(sc<.06)continue;
  X.save();X.translate(x,y);X.rotate(a*.3+(hash(i)-.5));X.scale(sc,sc);
  X.fillStyle='#e9dccb';X.fillRect(-170,-210,340,420);X.save();X.translate(-150,-190);X.beginPath();X.rect(0,0,300,320);X.clip();X.fillStyle='#d8b893';X.fillRect(0,0,300,320);
  const mezcla=R(202.5+i*.2,203.5+i*.2,T);
  if(T>205.4&&i>=4)raro(300,320,i);else marcos[base](300,320);
  if(mezcla>0){X.globalAlpha=mezcla*.6;X.fillStyle='#7a1a0e';X.fillRect(0,0,300,320);X.globalAlpha=1}
  X.restore();X.restore();
}
post(t,{ruido:corte(T,199.9)+R(205.4,206,T)*(1-R(206,206.6,T))*.5,grano:.17});
''')

# 207.7 · «Sueño con mundos que giran alrededor de soles muertos. Con formas que no pueden ver sin perder la cordura.»
E('s26-soles', 207.7, 218.6, r'''
if(T<213.6){
  pintaFondo('estrellas',t,{A:[T*.01,0,1,0]});
  for(const [x,y,r,n] of [[540,820,170,4],[230,1520,90,2],[880,1420,70,3]]){
    // sol muerto: disco negro con corona apagada
    const g=X.createRadialGradient(x,y,r*.9,x,y,r*2.4);g.addColorStop(0,'rgba(140,30,20,.6)');g.addColorStop(.2,'rgba(90,15,10,.25)');g.addColorStop(1,'rgba(0,0,0,0)');X.fillStyle=g;X.fillRect(x-r*3,y-r*3,r*6,r*6);
    X.fillStyle='#000';X.beginPath();X.arc(x,y,r,0,7);X.fill();X.strokeStyle='rgba(255,90,60,.5)';X.lineWidth=2;X.beginPath();X.arc(x,y,r,0,7);X.stroke();
    for(let j=0;j<n;j++){const R1=r*(1.8+j*.9),a=T*(.6/(j+1))+j*2+x;X.strokeStyle='rgba(255,170,130,.12)';X.lineWidth=2;X.beginPath();X.ellipse(x,y,R1,R1*.35,-.2,0,7);X.stroke();
     const px=x+Math.cos(a)*R1,py=y+Math.sin(a)*R1*.35;X.fillStyle='#1a0d0a';X.beginPath();X.arc(px,py,r*.12+j*3,0,7);X.fill();X.strokeStyle='rgba(255,120,90,.5)';X.beginPath();X.arc(px,py,r*.12+j*3,Math.PI*.8,Math.PI*1.6);X.stroke()}
  }
}else{
  X.fillStyle='#060203';X.fillRect(0,0,W,H);
  const lo=R(213.6,217.5,T);
  tesseract(540,820,190,T*1.2,'rgba(255,120,90,.9)');
  // triángulo imposible
  X.save();X.translate(540,1450);X.rotate(T*.3);X.strokeStyle='rgba(255,200,170,.7)';X.lineWidth=26;X.lineJoin='miter';
  for(let i=0;i<3;i++){X.rotate(Math.PI*2/3);X.beginPath();X.moveTo(-160,92);X.lineTo(0,-185);X.lineTo(40,-115);X.stroke()}X.restore();
  for(let i=0;i<5;i++)tesseract(140+hash(i)*800,300+hash(i+5)*1400,30+hash(i+9)*40,T*(.5+hash(i)),`rgba(255,90,70,${.3*lo})`);
}
post(t,{ruido:corte(T,207.7)+corte(T,213.6,.3)+(T>213.6?R(214,217,T)*.35*Math.abs(ruido(T*4)):0),grano:.16});
''')

# 218.6 · «Ahora lo entiendo. La gran mancha roja no es una tormenta. Es un ojo. Un ojo entreabierto. Y no lo despertamos.»
E('s27-entreabierto', 218.6, 230.4, r'''
const p=E(R(218.6,230,T));const rad=L(.3,.95,p);const sp=[.26,.36];
const cen=[L(0,-sp[0]*rad,p),L(0,-sp[1]*rad,p)];
const ab=L(0,.45,E(R(223.8,225.6,T)));
pintaFondo('planeta',t+140,{A:[cen[0],cen[1],rad,0],B:[Math.max(.0,ab),.12+.1*R(228,230,T),0,0]});
post(t,{ruido:corte(T,218.6),grano:.14});
''', q=.66)

# 230.4 · «Lo llamamos. Por eso envío esto. No como advertencia. Sino como penitencia.»
E('s28-llamamos', 230.4, 239.4, r'''
if(T<233){
  pintaFondo('planeta',t+150,{A:[-.26*.95,-.36*.95+.1,.95,0],B:[.45,.2,0,0]});
  for(const [x,y,f] of [[200,300,0],[540,180,.3],[880,320,.6]]){sonda(x,y,.8,T,{fase:f});pings(x,y+40,T+f,{max:1000,per:1.1,n:4,col:'255,200,160',alfa:.6})}
}else{
  cabina(t,{alarma:.6,consolaY:1700});
  const pe=R(234.9,237.4,T);
  const p=seq([[233,'consola'],[234.9,'rodillas',1],[237,'penitencia',1]],T);
  figura({tipo:'astro',x:L(560,520,pe),suelo:1760,s:1.9,dir:1,pose:p,luz:[0,-1],rim:'rgba(255,90,60,.95)',glow:24});
  if(T<235)texto('TRANSMITIENDO',W/2,300,46,`rgba(255,230,210,${Math.floor(T*3)%2?.9:.4})`,{esp:8,glow:14});
}
post(t,{ruido:corte(T,230.4)+corte(T,233,.3),grano:.15,parpadeo:.1});
''', q=.6)

# 239.4 · «Porque el leviatán me dejará vivir solo hasta que otro lo escuche. Y tú. Tú ya me escuchaste.»
E('s29-escuchaste', 239.4, FIN, r'''
if(T<245.7){
  pintaFondo('estrellas',t,{A:[0,0,1,0]});
  X.drawImage(fondo('planeta',t+170,{A:[0,0,.18,0],B:[.4,.2,0,0]}),-260,-560,W,H);
  // la tierra, lejos
  X.fillStyle='#4a7ab8';X.shadowColor='#6aa0ff';X.shadowBlur=20;X.beginPath();X.arc(820,1500,26,0,7);X.fill();X.shadowBlur=0;
  const u=R(239.6,244,T);for(let i=0;i<6;i++){const ph=(u*1.6+i/6)%1;X.strokeStyle=`rgba(255,120,80,${(1-ph)*.7})`;X.lineWidth=4;X.beginPath();X.arc(280,400,ph*1600,.6,1.2);X.stroke()}
  if(T>243.6){const k=E(R(243.6,245.6,T));X.strokeStyle=`rgba(255,120,80,${.8*k})`;X.lineWidth=6;X.beginPath();X.arc(820,1500,40+k*80,0,7);X.stroke()}
}else{
  // tú: el ojo te mira desde la pantalla
  const ab=E(R(246.4,248.2,T)),pup=L(.1,.6,E(R(248.2,250,T)));
  pintaFondo('ojo',t,{A:[0,0,L(.9,.62,E(R(245.7,251,T))),0],B:[Math.max(.05,ab),pup,0,0]});
}
const fin=T>251.0;
post(t,{ruido:corte(T,239.4)+corte(T,245.7,.3)+(T>250.6&&T<251.0?.9:0),grano:.16,negro:fin?1:0});
''', q=.66)

if __name__ == '__main__':
    S.correr(sys.argv[1:])
