"""Archivo #01 · Knight Capital (2012) · edición «Pixel 16-bit» (videojuego retro). Video 100 % animado sobre la voz.
Cinco escenas a pantalla completa contiguas (0 → 74.81) que se encadenan con el mosaico del SNES, más la capa de subtítulos
en caja de diálogo. Tiempos = video final (archivo/1/voz/voz-editada.wav); cada idea entra con su palabra (palabras.json).
Uso: SALIDA=~/Documents/Videos/archivo/1/animaciones REL=archivo/1/animaciones python3 ejemplos/archivo01-pixel.py [ids…]
     SOLO_HTML=1 → solo escribe los .html (sin ids escribe además overlays-pixel.json y lote-pixel.json). Prefijo «ap1-».
"""
import json, os, re, subprocess, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import pixel as X

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, '..', 'capturar.ts')
OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/archivo/1/animaciones')))
REL = os.environ.get('REL', 'archivo/1/animaciones')
VOZ = os.path.join(OUT, '..', 'voz')
WORK = os.path.join(OUT, '_html-pixel'); os.makedirs(WORK, exist_ok=True)
PRE, FIN = 'ap1-', 74.81

_n = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())
PAL = [(_n(w['word']), w['start']) for w in json.load(open(os.path.join(VOZ, 'palabras.json')))['words']]


def W(palabra, desde=0.0):
    """Inicio (video final) de la primera aparición de `palabra` a partir de `desde`."""
    for w, t in PAL:
        if t >= desde - 1e-6 and w == _n(palabra):
            return t
    raise KeyError(palabra)


def tiempos(js, S0, **marcas):
    """Sustituye @marca@ por el tiempo local (marca en segundos del video final)."""
    for k, v in marcas.items():
        js = js.replace(f'@{k}@', f'{v - S0:.2f}')
    if '@' in js:
        raise ValueError('marca sin tiempo: ' + re.search(r'@\w+@', js).group(0))
    return js


ESCENAS = []


def escena(pid, S, E, js, mosaico=(True, True), fondo='k', **marcas):
    ESCENAS.append((pid, S, E, X.page(tiempos(js, S, **marcas), round(E - S, 3), mosaico=mosaico, fondo=fondo)))


# ───────────── 1 · gancho, la razón y Knight Capital (0 → 15.45)
escena('p1-gancho', 0.0, 15.45, r"""
if(t<@pasa@){
 if(t<@razon0@){
  // Wall Street de noche: la bolsa escupe monedas mientras se vacía el dinero
  CIELO(['k','n','N','P'],0,330);ESTRELLAS(t,50,150);SKYLINE(300,'n',3,90);SKYLINE(318,'P',7,50);
  BOLSA(75,228,t);PISO(316,'G','k');
  const d=P(t,@perdio@,5.0),din=1-d*.97;HUD(din,String(Math.floor(d*45)).padStart(2,'0')+':00',{rc:t>@m45@?'y':'w'});SERIE();
  for(let i=0;i<26;i++){const t0=@perdio@+i*.16;if(t<t0)continue;const u=t-t0,a=-1.6+(hs(i)-.5)*2.2,v=90+hs(i+7)*70;
   const x=135+Math.cos(a)*v*u,y=300+Math.sin(a)*v*u+120*u*u;if(y<470)MONEDA(x,y,t,i)}
  if(t>=@n470@){const k=E.back(P(t,@n470@,@n470@+.35));TX('-$470',128,lerp(36,70,k),{z:32,c:'r',a:'c',sh:'k'})}
  if(t>=@millones@){const k=E.bote(P(t,@millones@,@millones@+.4));TX('MILLONES',128,lerp(60,110,k),{z:16,c:'w',a:'c'})}
  if(t>=@dolares@)TX(TY('DE DÓLARES',t,@dolares@,24),128,134,{c:'s',a:'c'});
  if(t>=@m45@){const k=E.back(P(t,@m45@,@m45@+.3));R(40,154,176,26,'k');R(42,156,172,22,'R');TX('EN 45 MIN',128,lerp(150,161,k),{z:16,c:'y',a:'c'})}
 }else{
  // ¿la razón? un servidor que nadie actualizó
  CORTE(t,@razon0@);R(0,0,W,330,'k');for(let j=0;j<330;j+=12)for(let i=(j/12%2)*12;i<W;i+=24)R(i,j,12,12,'n');
  PISO(300,'G','k');SERIE();
  VENTANA(30,50,196,34,null);TX(TY('¿LA RAZÓN?',t,@razon0@,20),128,62,{z:16,c:'w',a:'c'});
  if(t>=@un@){const k=P(t,@un@,@un@+.25);g.fillStyle='rgba(255,243,160,.18)';g.beginPath();g.moveTo(118,90);g.lineTo(138,90);g.lineTo(178,320);g.lineTo(78,320);g.fill();
   ESC(104,lerp(80,150,E.bote(k)),3,()=>SERVIDOR(0,0,'viejo',t,3));
   for(let i=0;i<12;i++){const y=(hs(i)*230+t*8*(1+hs(i+2)))%230+90;R(90+hs(i+4)*80,y,1,1,'s')}}
  if(t>=@nadie@){const k=E.bote(P(t,@nadie@,@nadie@+.4));ALERTA(150,lerp(100,146,k))}
  if(t>=@actualizo@){VENTANA(36,262,184,40,'v1.0',{tc:'r'});TX('ACTUALIZAR',46,272,{c:'w'});BAR(46,286,120,6,blink(t,3)?.02:0,'l');TX('0%',172,284,{c:'r'})}
 }
}else if(t<@knight@){
 // pantalla de «mundo» como en los juegos
 CORTE(t,@pasa@);R(0,0,W,H,'k');ESTRELLAS(t,30,480);SERIE();
 TX('MUNDO',128,130,{z:16,c:'w',a:'c'});if(t>=@a2012@){const k=E.back(P(t,@a2012@,@a2012@+.35));TX('2012',128,lerp(140,160,k),{z:32,c:'y',a:'c',sh:'R'})}
 S('vida',96,220,{s:2});TX('x 1',118,224,{c:'w'});TX(TY('NUEVA YORK',t,@pasa@+.2,20),128,260,{c:'s',a:'c'});
}else{
 // Knight Capital: rascacielos, corredores y flechas de acciones
 CORTE(t,@knight@);CIELO(['b','c','C'],0,320);SKYLINE(300,'s',5,70);
 EDIFICIO(72,96,112,224,'g',2,t,'C');R(70,78,116,20,'k');R(72,80,112,16,'r');
 R(62,78,132,20,'k');R(64,80,128,16,'r');TX(t>=@capital@?'KNIGHT CAPITAL':'KNIGHT',128,84,{c:'w',a:'c',sh:'R'});
 PISO(316,'s','g');SERIE();
 for(let i=0;i<6;i++){const x=((i*53+t*(18+i*4))%(W+20))-10,fl=i%2===1;S(Math.floor(t*6+i)%2?'trader':'trader2',fl?W-x:x,296,{f:fl,s:1})}
 if(t>=@acciones@){for(let i=0;i<14;i++){const t0=@acciones@+i*.18;if(t<t0)continue;const u=(t-t0)%1.6,x=80+hs(i)*96,y=300-u*170,up=hs(i+4)>.35;
  if(y>60){R(x,y,7,7,'k');if(up){R(x+3,y+1,1,5,'l');R(x+2,y+2,3,1,'l');R(x+1,y+3,5,1,'l')}else{R(x+3,y+1,1,5,'r');R(x+2,y+4,3,1,'r');R(x+1,y+3,5,1,'r')}}}}
 if(t>=@empresas@){const k=E.back(P(t,@empresas@,@empresas@+.3));VENTANA(26,lerp(-40,46,k),204,30,'RÉCORD',{tc:'y'});TX('TOP EN ACCIONES',128,lerp(-26,58,k),{c:'y',a:'c'})}
 if(t>=@eeuu@){const k=E.bote(P(t,@eeuu@,@eeuu@+.4));BANDERA(114,lerp(20,40,k)-2,t);}
}
""", mosaico=(False, True), razon0=W('la', 5) - .05, un=W('un', 6), nadie=W('nadie'), actualizo=W('actualizo'),
       perdio=W('perdio'), n470=W('470'), millones=W('millones'), dolares=W('dolares'), m45=W('45'), pasa=W('paso') - .05,
       a2012=W('2012'), knight=W('knight') - .05, capital=W('capital'), empresas=W('empresas'), acciones=W('acciones'),
       eeuu=W('estados'))

# ───────────── 2 · sistema nuevo, el interruptor y el programa viejo (15.45 → 31.5)
escena('p2-interruptor', 15.45, 31.5, r"""
if(t<@problema@){
 // sala de control: estreno del sistema nuevo y el interruptor que ya existía en el código
 R(0,0,W,330,'n');for(let i=0;i<5;i++)EDIFICIO(i*56-4,60,52,40,'G',i*9,t,'c');PISO(300,'G','k');SERIE();
 if(t>=@sistema@){const k=E.back(P(t,@sistema@,@sistema@+.35));VENTANA(34,lerp(-60,112,k),188,84,'NUEVO',{tc:'l'});
  const y=lerp(-60,112,k);for(let i=0;i<4;i++)R(48,y+12+i*14,lerp(60,150,hs(i+2)),6,['l','c','y','m'][i]);
  TX('SISTEMA',128,y+66,{z:8,c:'w',a:'c'});CONFETI(t,@nuevo@,128,y+20,40);
  if(t>=@nuevo@&&t<@prender@){const s=1+Math.floor(t*6)%2;R(196,y-8,26,12,'y');TX('NEW!',198,y-6,{c:'r',sh:null})}}
 if(t>=@prender@&&t<@interruptor@){VENTANA(26,232,204,40,null);TX(TY('¿Y CÓMO LO PRENDEMOS?',t,@prender@,30),36,246,{c:'w'})}
 if(t>=@interruptor@){
  CORTE(t,@interruptor@);R(0,46,W,284,'k');VENTANA(16,58,224,252,'CÓDIGO',{f:['k']});CODIGO(28,72,200,30,t,1);
  // la línea del interruptor resaltada
  R(26,94,206,15,'y');R(28,96,202,11,'k');TX('if (FLAG) prender()',34,98,{c:'y',sh:null});
  const k=E.bote(P(t,@interruptor@,@interruptor@+.45)),Y=lerp(-110,124,k);R(64,Y-4,128,104,'k');R(66,Y-2,124,100,'G');ESC(104,Y+52,2,()=>PALANCA(0,0,0));
  TX('INTERRUPTOR',128,Y+2,{c:'w',a:'c'});
  if(t>=@existia@){R(48,276,160,26,'k');R(50,278,156,22,'P');TX(TY('YA EXISTÍA',t,@existia@,20),128,284,{z:8,c:'Y',a:'c'})}
 }
}else if(t<@otro@){
 // «el problema»: recuerdo en sepia (marco ondulado) hacia años antes
 CORTE(t,@problema@);
 if(t<@anos@){R(0,0,W,H,'R');for(let i=0;i<10;i++)R(0,i*48+((t*60)%48),W,24,'r');SERIE();
  const k=E.back(P(t,@problema@,@problema@+.35));R(18,120,220,70,'k');R(20,122,216,66,'w');TX('EL',128,lerp(110,132,k),{z:16,c:'k',a:'c',sh:null});
  TX('PROBLEMA',128,lerp(150,156,k),{z:24,c:'r',a:'c',sh:'k'});const [sx,sy]=SAC(t,@problema@,@problema@+.6,3);g.translate(sx,sy);
  ESC(104,240,2,()=>PALANCA(0,0,0));g.setTransform(1,0,0,1,0,0);
 }else{
  R(0,0,W,H,'u');D(0,0,W,H,'u','T');for(let i=0;i<W;i+=8){const o=Math.round(Math.sin(t*5+i*.2)*2);R(i,6+o,6,3,'q');R(i,318+o,6,3,'q')}SERIE();
  TX(TY('AÑOS ANTES...',t,@anos@,16),128,60,{z:16,c:'Y',a:'c',sh:'k'});
  R(30,136,70,112,'Q');R(32,138,66,108,'T');ESC(41,196,2,()=>PALANCA(0,0,lerp(0,1,P(t,@prendia@,@prendia@+.25))));TX('2003',65,256,{z:16,c:'Y',a:'c'});
  if(t>=@prendia@){const k=P(t,@prendia@,@prendia@+.8);for(let i=0;i<Math.floor(k*30);i++)R(100+i*5,190+Math.round(Math.sin(i*.6)*3),3,2,blink(t,4)&&i%3==0?'y':'q')}
 }
}else{
 // el programa viejo, dormido; nadie lo borró
 if(t<@viejo@+.1)CORTE(t,@otro@);
 R(0,0,W,H,'u');D(0,0,W,330,'u','T');PISO(300,'Q','u');SERIE();
 const k=E.bote(P(t,@otro@,@otro@+.5));S('dormido',48,lerp(40,150,k),{s:8});
 for(let i=0;i<3;i++){const u=((t-@otro@)*.8+i/3)%1;if(t>@otro@+.3)TX('z',210+u*20,140-u*60-i*2,{z:8+8*(i%2),c:'w'})}
 if(t>=@viejo@){VENTANA(30,58,196,30,'PROGRAMA',{tc:'o'});TX('VIEJO',128,70,{z:16,c:'o',a:'c'})}
 if(t>=@apagado@){R(150,262,80,14,'k');R(151,263,78,12,'g');TX('APAGADO',190,266,{c:'w',a:'c'})}
 if(t>=@a2003@){const k2=E.back(P(t,@a2003@,@a2003@+.3));R(22,lerp(300,262,k2),100,30,'k');R(24,lerp(300,264,k2),96,26,'y');TX('DESDE',72,lerp(300,267,k2),{c:'k',a:'c',sh:null});TX('2003',72,lerp(300,276,k2),{z:8,c:'R',a:'c',sh:null})}
 if(t>=@nunca@){CORTE(t,@nunca@);VENTANA(46,100,164,96,'¿BORRAR?',{tc:'r'});TX('SÍ',100,128,{z:16,c:'w'});TX('NO',100,160,{z:16,c:t>=@borraron@?'y':'w'});
  const cy=t>=@borraron@?160:128;if(blink(t,3)||t<@borraron@)TX('>',78,cy,{z:16,c:'y'});
  if(t>=@borraron@){R(56,206,144,26,'k');R(58,208,140,22,'r');TX(TY('NUNCA LO BORRARON',t,@borraron@,30),128,215,{c:'w',a:'c'})}}
}
""", problema=W('problema') - .05, anos=W('anos'), prendia=W('prendia'), otro=W('otro', 25), viejo=W('viejo', 26),
       sistema=W('sistema', 15), nuevo=W('nuevo', 15), prender=W('prenderlo'), interruptor=W('interruptor', 18),
       existia=W('existia'), apagado=W('apagado', 26), a2003=W('2003'), nunca=W('nunca'), borraron=W('borraron'))

# ───────────── 3 · ocho servidores, uno olvidado y el despertar (31.5 → 44.9)
escena('p3-despierta', 31.5, 44.9, r"""
const XS=[18,70,122,174];
if(t<@abre@){
 // centro de datos: la versión nueva entra a 7 de 8 servidores
 R(0,0,W,330,'n');for(let i=0;i<W;i+=30)R(i,46,2,260,'N');PISO(300,'G','k');SERIE();
 const upd=i=>@sube@+.35+i*.34;
 for(let i=0;i<8;i++){const x=XS[i%4],y=i<4?84:180;let st=i===7?'viejo':(t>=upd(i)?'ok':'off');ESC(x,y,2,()=>SERVIDOR(0,0,st,t,i));
  if(i<7&&t>=upd(i)){R(x+22,y-8,13,10,'k');R(x+23,y-7,11,8,'e');L(x+25,y-3,x+27,y-1,'w');L(x+27,y-1,x+31,y-5,'w')}}
 // el cartucho «v2» que va saltando de servidor en servidor
 if(t>=@sube@&&t<upd(7)+.3){const f=(t-@sube@)/.34,i=Math.min(7,Math.floor(f)),u=f-Math.floor(f),x=XS[i%4]+8,y=(i<4?84:180)-18-Math.sin(u*Math.PI)*24;
  R(x,y,16,14,'k');R(x+1,y+1,14,12,'p');R(x+3,y+3,10,5,'w');TX('v2',x+4,y+3,{c:'k',sh:null})}
 if(t>=@version@){VENTANA(18,264,220,28,null);TX(TY('VERSIÓN NUEVA >',t,@version@,26),30,274,{c:'l'})}
 if(t>=@n8@){const k=E.back(P(t,@n8@,@n8@+.3));R(160,lerp(-30,50,k),82,24,'k');R(162,lerp(-30,52,k),78,20,'y');
  TX(t>=@n7@?'7/8':'8/8',201,lerp(-26,55,k),{z:16,c:t>=@n7@?'r':'k',a:'c',sh:null})}
 if(t>=@bueno@&&t<@n7@){R(20,48,96,16,'k');TX('BUENO...',24,52,{c:'w'})}
 if(t>=@uno@){const k=E.bote(P(t,@uno@,@uno@+.4));ALERTA(XS[3]+16,lerp(130,176,k));O(XS[3]-3,177,38,62,blink(t,4)?'r':'k',2)}
 if(t>=@paso@){R(124,244,118,14,'k');R(125,245,116,12,'r');TX('SE LES PASÓ',183,248,{c:'w',a:'c'})}
}else if(t<@servidor@){
 // abre la bolsa: campana, cinta de cotizaciones y el interruptor en ON
 CORTE(t,@abre@);R(0,0,W,330,'P');D(0,250,W,80,'P','n');PISO(300,'g','G');SERIE();
 ESC(128,56,2,()=>CAMPANA(0,0,t,t<@prende@?1:.3));TX('9:30',128,112,{z:16,c:'y',a:'c'});TX(TY('ABRE LA BOLSA',t,@abre@,24),128,134,{c:'w',a:'c'});
 R(0,154,W,14,'k');const tk='KCG +10.33  NYSE -2.1  IBM +0.4  BOLSA ABIERTA  ';const ox=-((t*60)%TW(tk));TX(tk+tk,ox,157,{c:'l',sh:null});
 const v=P(t,@prende@,@prende@+.3);ESC(104,250,2,()=>PALANCA(0,0,v));if(t>=@prende@){CONFETI(t,@prende@,128,214,26);
  R(70,180,116,18,'k');R(72,182,112,14,v>.5?'l':'G');TX('INTERRUPTOR: ON',128,185,{c:'k',a:'c',sh:null})}
}else{
 // el servidor olvidado despierta al programa viejo (jefe final)
 CORTE(t,@servidor@);R(0,0,W,330,'k');PISO(300,'G','k');
 const des=t>=@despierta@,[sx,sy]=SAC(t,@despierta@,@despierta@+1.2,4);g.translate(sx,sy);
 if(!des){ESC(104,130,3,()=>SERVIDOR(0,0,'viejo',t,9));for(let i=0;i<40;i++)R(i*7,240+Math.round(Math.sin(i+t*8)*2),4,2,blink(t,6)?'y':'o');
  if(t>=@olvidado@){R(10,150,82,14,'k');R(11,151,80,12,'g');TX('OLVIDADO',51,154,{c:'w',a:'c'})}}
 else{const k=E.back(P(t,@despierta@,@despierta@+.6));for(let i=0;i<24;i++){const a=hs(i)*6.28,d=(t-@despierta@)*90;R(128+Math.cos(a)*d,200+Math.sin(a)*d,3,3,['g','s','Q'][i%3])}
  if(blink(t,5))R(0,46,W,284,'R');S('viejo',128-60*k,lerp(220,120,k),{s:Math.max(1,Math.round(6*k))});
  VENTANA(14,54,228,30,null);TX('PROGRAMA VIEJO',22,60,{c:'w'});TX('LV 2003',236,60,{c:'y',a:'r'});BAR(22,72,212,6,1,'r')}
 g.setTransform(1,0,0,1,0,0);SERIE();
 if(t>=@programa@){R(36,262,184,28,'k');R(38,264,180,24,'r');TX('¡DESPERTÓ!',128,268,{z:16,c:'y',a:'c'})}
}
""", sube=W('subieron'), version=W('version'), n8=W('8', 31), bueno=W('bueno'), n7=W('7', 34), uno=W('uno', 36),
       paso=W('paso', 36), abre=W('abre') - .05, prende=W('prende'), servidor=W('servidor', 40) - .05,
       olvidado=W('olvidado'), despierta=W('despierta'), programa=W('programa', 43))

# ───────────── 4 · compra caro / vende barato, 97 correos y nadie los leyó (44.9 → 59.2)
escena('p4-correos', 44.9, 59.2, r"""
if(t<@peor@){
 // el jefe aprieta los botones sin parar: el dinero se vacía
 R(0,0,W,330,'k');for(let i=0;i<W;i+=18)R(i,46,1,284,'n');PISO(300,'G','k');
 const d=P(t,@comprar@,@peor@),[sx,sy]=SAC(t,@sin@,@peor@,2);g.translate(sx,sy);
 S('viejo',88,62,{s:4});
 const lado=Math.floor(t*6)%2;
 // botones
 const bt=(x,c,cc,tit,sub,on)=>{R(x,170,104,72,'k');R(x+2,on?176:172,100,64,on?cc:c);TX(tit,x+52,(on?184:180),{c:'w',a:'c',sh:'k'});TX(sub,x+52,(on?206:202),{z:16,c:'y',a:'c',sh:'k'});R(x+2,240,100,4,'k')};
 if(t>=@comprar@)bt(18,'e','E','COMPRAR',t>=@caro@?'CARO':'',t>=@comprar@&&lado===0);
 if(t>=@vender@)bt(134,'r','R','VENDER',t>=@barato@?'BARATO':'',lado===1);
 for(let i=0;i<20;i++){const t0=@comprar@+i*.2;if(t<t0)continue;const u=t-t0,x=(i%2?186:70)+(hs(i)-.5)*40*u,y=240+u*120;if(y<330)MONEDA(x,y,t,i)}
 g.setTransform(1,0,0,1,0,0);HUD(1-d*.9,'-$'+Math.floor(d*470)+'M',{rc:'r'});SERIE();
 if(t>=@sin@){const k=E.back(P(t,@sin@,@sin@+.3));R(30,lerp(330,258,k),196,30,'k');R(32,lerp(330,260,k),192,26,'y');TX('SIN PARAR  x'+Math.floor((t-@sin@)*900+99),128,lerp(330,268,k),{c:'k',a:'c',sh:null})}
}else if(t<@nadie@){
 // bandeja de entrada: 97 correos de alerta antes de abrir
 CORTE(t,@peor@);R(0,0,W,330,'n');PISO(300,'G','k');SERIE();
 if(t<@sistema@){VENTANA(26,120,204,60,null);TX(TY('Y LO PEOR...',t,@peor@,18),128,140,{z:16,c:'w',a:'c'})}
 if(t>=@antes@){const h=Math.floor(lerp(8,9,P(t,@antes@,@m97@))),m=Math.floor(lerp(0,29,P(t,@antes@,@m97@)))%60;
  R(20,22,232,20,'k');TX('ANTES DE ABRIR',24,28,{c:'s'});TX(String(h)+':'+String(m).padStart(2,'0'),248,28,{c:'y',a:'r'})}
 if(t>=@sistema@){const k=E.back(P(t,@sistema@,@sistema@+.3));const y0=lerp(330,58,k);VENTANA(14,y0,228,232,'CORREOS',{f:['N']});
  const n=Math.min(97,Math.floor(lerp(0,97,P(t,@mando@,@correos@+.3))));
  for(let i=0;i<100;i++){const x=24+(i%10)*21,y=y0+14+Math.floor(i/10)*20;R(x,y,18,16,'k');R(x+1,y+1,16,14,'n');if(i<n)SOBRE(x+4,y+5,i===96&&t>=@avisando@?'y':'w')}
  if(t>=@m97@){const k2=E.back(P(t,@m97@,@m97@+.3));R(140,lerp(y0-30,y0-20,k2),98,24,'k');R(142,lerp(y0-28,y0-18,k2),94,20,'r');TX('x97',189,lerp(y0-24,y0-14,k2),{z:16,c:'w',a:'c'})}}
 if(t>=@avisando@){const k=E.bote(P(t,@avisando@,@avisando@+.4));VENTANA(34,lerp(330,150,k),188,70,'ALERTA',{tc:'r',f:['w'],b2:'r'});
  const y=lerp(330,150,k);ALERTA(60,y+40);TX(TY('ALGO ANDA',t,@algo@,24),74,y+22,{c:'k',sh:null});TX(TY('MAL',t,@mal@,12),74,y+40,{z:16,c:'r',sh:null})}
}else{
 // nadie los leyó
 CORTE(t,@nadie@);R(0,0,W,H,'k');SERIE();
 for(let i=0;i<97;i++){const x=10+(i%12)*21,y=200+Math.floor(i/12)*13;SOBRE(x,y+Math.round(Math.sin(t*3+i)*1),'G')}
 TX('NADIE',128,70,{z:24,c:'w',a:'c'});if(t>=@leyo@)TX('LOS LEYÓ.',128,106,{z:24,c:'r',a:'c'});
 R(56,150,144,18,'k');TX('LEÍDOS: 0/97',128,155,{c:'y',a:'c'});
 const tw=(t*40)%(W+40)-20;R(tw,312,8,8,'Q');R(tw+2,310,4,2,'Q');R(0,320,W,2,'g');
}
""", comprar=W('comprar'), caro=W('caro'), vender=W('vender'), barato=W('barato'), sin=W('sin', 48),
       peor=W('lo', 49) - .1, antes=W('antes', 50), sistema=W('sistema', 51), mando=W('mando'), m97=W('97'),
       correos=W('correos'), avisando=W('avisando'), algo=W('algo'), mal=W('mal', 55), nadie=W('nadie', 57) - .05,
       leyo=W('leyo'))

# ───────────── 5 · game over, la lección y la pantalla de título (59.2 → 74.81)
escena('p5-cierre', 59.2, FIN, r"""
if(t<@empresa@){
 // lo apagaron, el jefe explota… GAME OVER
 R(0,0,W,H,'k');
 if(t<@perdido@){PISO(300,'G','k');const v=1-P(t,@apagaron@,@apagaron@+.3);ESC(104,250,2,()=>PALANCA(0,0,v));
  const k=P(t,@apagaron@+.3,@apagaron@+.9);if(k<1){if(k===0)S('viejo',68,80,{s:6});else for(let i=0;i<60;i++){const a=hs(i)*6.28,d=k*160;R(128+Math.cos(a)*d,128+Math.sin(a)*d,4,4,['q','Q','r','k'][i%4])}}
  TX('OFF',128,190,{z:16,c:'w',a:'c'})}
 else{if(blink(t,1.2)||t>@perdido@+1)TX('GAME OVER',128,110,{z:24,c:'r',a:'c',sh:'R'});
  if(t>=@todo@){R(40,160,176,46,'k');R(42,162,172,42,'n');TX('PERDIDO:',128,168,{c:'s',a:'c'});TX('-$470M',128,182,{z:16,c:'y',a:'c'})}
  if(t>=@dinero@){TX('CONTINUE?',128,240,{c:'w',a:'c'});TX(String(Math.max(0,9-Math.floor((t-@dinero@)*3))),128,256,{z:16,c:'y',a:'c'})}}
 HUD(0,'45:00',{rc:'r'});SERIE();
}else if(t<@asi@){
 // la empresa terminó vendida
 CORTE(t,@empresa@);CIELO(['G','g','s'],0,320);SKYLINE(300,'G',5,70);EDIFICIO(72,96,112,224,'g',2,0,'k');
 R(70,78,116,20,'k');R(72,80,112,16,'G');TX('KNIGHT CAPITAL',128,84,{c:'s',a:'c',sh:'k'});PISO(316,'s','g');SERIE();
 if(t>=@termino@){const k=E.bote(P(t,@termino@,@termino@+.5));R(56,lerp(-60,150,k),144,52,'T');R(60,lerp(-56,154,k),136,44,'w');
  TX(t>=@vendida@?'VENDIDA':'SE VENDE',128,lerp(-48,166,k),{z:16,c:'r',a:'c',sh:null});R(126,lerp(-80,130,k),4,24,'T')}
}else if(t<@yasi@){
 // consejo del archivo: bórralo
 CORTE(t,@asi@);R(0,0,W,330,'n');PISO(300,'G','k');SERIE();
 VENTANA(20,52,216,28,'TIP DEL ARCHIVO',{tc:'l'});TX(TY('CÓDIGO VIEJO APAGADO',t,@codigo@,30),128,63,{c:'w',a:'c'});
 const del=t>=@borralo@,k=E.io(P(t,@borralo@,@borralo@+.5));
 if(k<1){const x=lerp(30,178,k),y=lerp(110,230,k),s=1-k*.8;R(x,y,130*s,90*s,'k');R(x+2,y+2,126*s-4,86*s-4,'G');if(s>.5){CODIGO(x+8,y+8,110,10,0,4,['g','s']);
  R(x+70,y+64,56,14,'k');TX('APAGADO',x+98,y+67,{c:'s',a:'c'})}}
 S('basura',194,214,{s:3});if(del&&t<@borralo@+.8)R(194,206-Math.round(Math.sin(P(t,@borralo@+.4,@borralo@+.8)*Math.PI)*8),30,4,'g');
 if(t>=@acaso@&&!del)TX('POR SI ACASO...',30,214,{c:'y'});
 if(del){VENTANA(26,214,140,40,'¿BORRAR?',{tc:'r'});TX('> SÍ',40,230,{z:16,c:'y'});if(t>@borralo@+.5)TX('+100',202,190-((t-@borralo@-.5)*20),{c:'l'})}
}else if(t<@titulo@){
 // a mano → automatizado: 8 servidores (2 filas) que antes se actualizaban uno por uno
 CORTE(t,@yasi@);CIELO(t>=@hoy@?['c','C','Y']:['n','N','b'],0,320);PISO(300,'e','E');
 if(t>=@hoy@){const k=E.o(P(t,@hoy@,@hoy@+.6));S('sol',214,lerp(130,100,k),{s:4})}
 SERIE();
 const XS=[18,70,122,174],auto=t>=@automatizar@;
 for(let i=0;i<8;i++){const x=XS[i%4],y=i<4?112:190,on=auto&&t>=@automatizar@+.1+i*.05;ESC(x,y,2,()=>SERVIDOR(0,0,on?'ok':'off',t,i));
  if(on){R(x+22,y-8,13,10,'k');R(x+23,y-7,11,8,'e');L(x+25,y-3,x+27,y-1,'w');L(x+27,y-1,x+31,y-5,'w')}}
 if(!auto){const x=lerp(4,214,((t-@yasi@)*.45)%1);ESC(x,256,2,()=>{S(Math.floor(t*6)%2?'trader':'trader2',0,0);R(1,-6,9,7,'p');R(3,-4,5,2,'w')});
  if(blink(t,3)&&t>=@cambios@)R(x+22,254,2,4,'C');
  VENTANA(20,52,216,40,null);if(t<@buen@){TX(TY('¿TODAVÍA SUBES',t,@yasi@+.25,24),128,62,{c:'w',a:'c'});TX(TY('CAMBIOS A MANO?',t,@cambios@,24),128,76,{c:'y',a:'c'})}
  else{TX('HOY ES UN',128,61,{c:'w',a:'c'});TX('BUEN DÍA',128,73,{z:16,c:'y',a:'c'})}}
 else{ESC(lerp(-40,112,E.o(P(t,@automatizar@,@automatizar@+.3))),252,2,()=>S('robot',0,0));
  VENTANA(20,52,216,40,null);TX('AUTOMATIZAR',128,66,{z:16,c:'l',a:'c'});if(t>=@automatizar@+.45){R(160,256,80,16,'k');TX('DEPLOY 8/8',200,260,{c:'l',a:'c'})}}
}else{
 // pantalla de título de la serie
 CORTE(t,@titulo@);R(0,0,W,H,'k');CIELO(['k','n','P'],0,330);ESTRELLAS(t,60,330);SKYLINE(330,'k',9,60);
 const k=E.back(P(t,@titulo@,@titulo@+.45));
 TX('ARCHIVO',128,lerp(-40,92,k),{z:32,c:'y',a:'c',sh:'r'});R(92,lerp(-10,134,k),72,16,'r');TX('#01',128,lerp(-6,138,k),{z:8,c:'w',a:'c',sh:'R'});
 TX('KNIGHT CAPITAL - 2012',128,164,{c:'s',a:'c'});
 if(blink(t,1.5))TX('PRESS START',128,206,{z:16,c:'w',a:'c'});
 R(30,252,196,40,'k');R(32,254,192,36,'r');TX('SÍGUEME PARA MÁS',128,262,{c:'w',a:'c',sh:'R'});TX('HISTORIAS',128,276,{c:'y',a:'c',sh:'R'});
}
""", mosaico=(True, False), apagaron=W('aunque'), perdido=W('perdido'), todo=W('todo', 61), dinero=W('dinero', 61),
       empresa=W('empresa', 62) - .05, termino=W('termino'), vendida=W('vendida'), asi=W('asi', 64) - .05,
       codigo=W('codigo', 65), acaso=W('acaso'), borralo=W('borralo'), yasi=W('si', 68.5) - .2, cambios=W('cambios'),
       hoy=W('hoy'), buen=W('buen'), automatizar=W('automatizarlo'), titulo=73.3)

# ───────────── subtítulos (caja de diálogo); se ocultan cuando la escena ya dice la frase en grande
G = json.load(open(os.path.join(VOZ, 'grupos.json')))
OCULTAR = [[round(W('nadie', 57) - .05, 2), round(W('aunque'), 2)], [73.3, FIN]]
SUB = ('sub', 0.0, FIN, X.subtitulos(G, FIN, ocultar=OCULTAR))

PIEZAS = ESCENAS + [SUB]


def main():
    ids = sys.argv[1:]
    lote = []
    for pid, S, E, html in PIEZAS:
        if ids and pid not in ids:
            continue
        f = os.path.join(WORK, pid + '.html')
        open(f, 'w').write(html)
        lote.append(dict(html=f, dur=round(E - S, 3), out=os.path.join(OUT, PRE + pid + '.webm')))
        print(f'{pid:16} {S:6.2f} → {E:6.2f}')
    if not ids:
        ov = [dict(file=f'{REL}/{PRE}{pid}.webm', html=f'{REL}/_html-pixel/{pid}.html', start=round(S, 2), end=round(E, 2),
                   trimIn=0, scale=1, position='center') for pid, S, E, _ in PIEZAS]
        json.dump(ov, open(os.path.join(OUT, 'overlays-pixel.json'), 'w'), indent=1, ensure_ascii=False)
        json.dump(lote, open(os.path.join(OUT, 'lote-pixel.json'), 'w'), indent=1, ensure_ascii=False)
    if not os.environ.get('SOLO_HTML'):
        subprocess.run(['node', CAP, '--lote', os.path.join(OUT, 'lote-pixel.json')], check=True)


if __name__ == '__main__':
    main()
