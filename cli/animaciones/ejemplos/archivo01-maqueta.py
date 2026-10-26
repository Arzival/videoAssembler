"""Archivo #01 · Knight Capital (45 minutos, 470 millones) · edición «Maqueta» (diorama isométrico).
Video 100 % animado sobre la voz (74.81 s). Un solo diorama continuo que la cámara recorre:
plaza del dinero → bolsa y torre de Knight → oficina con el interruptor → sótano con el programa viejo (Power Peg)
→ cuarto de servidores (8 racks, uno olvidado) → cinta de compra/venta → buzón con 97 correos → final y consejos.
Tiempos = video final (archivo/1/voz/palabras.json). Las páginas cortan el mismo recorrido en tramos ≤ 13 s.
Uso: SALIDA=~/Documents/Videos/archivo/1/animaciones REL=archivo/1/animaciones python3 ejemplos/archivo01-maqueta.py [ids…]
     (SOLO_HTML=1 solo escribe los HTML; escribe overlays-maqueta.json y lote-maqueta.json). Los webm salen con prefijo «am1-».
"""
import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import maqueta as Q
from maqueta import placa, pin, et, N

OUT = os.path.abspath(os.environ.get('SALIDA', os.path.expanduser('~/Documents/Videos/archivo/1/animaciones')))
WORK = os.path.join(OUT, '_html-maqueta'); os.makedirs(WORK, exist_ok=True)
VOZ = os.path.join(OUT, '..', 'voz')
PRE = 'am1-'
FIN = 74.81
COLA = .1

_norm = lambda s: unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode().strip('.,;:¿?¡!«»"')
PAL = [(_norm(w['word']), w['start'], w['end']) for w in json.load(open(os.path.join(VOZ, 'palabras.json')))['words']]
GRUPOS = json.load(open(os.path.join(VOZ, 'grupos.json')))


def W(palabra, desde=0.0, fin=False):
    """Inicio (o fin) de la primera palabra que coincide a partir de `desde`."""
    for w, a, b in PAL:
        if a >= desde - .01 and w == _norm(palabra):
            return round(b if fin else a, 2)
    raise KeyError(palabra)


# momentos clave (segundos del video final)
T = dict(
    empresa=W('empresa'), perdio=W('perdio'), m470=W('470'), minutos=W('minutos'), m45=W('45'),
    razon=W('razon'), servidor=W('servidor'), nadie=W('nadie'), actualizo=W('actualizo'),
    paso=W('paso'), y2012=W('2012'), knight=W('knight'), una=W('una', 11), acciones=W('acciones'), unidos=W('unidos'),
    estrenar=W('estrenar'), sistema=W('sistema'), prenderlo=W('prenderlo'), interruptor=W('interruptor'), existia=W('existia'),
    problema=W('problema'), anos=W('anos'), prendia=W('prendia'), programa=W('programa'),
    viejo=W('viejo', 26), apagado=W('apagado', 27), d2003=W('2003'), borraron=W('borraron'),
    subieron=W('subieron'), ocho=W('8'), bueno=W('bueno'), siete=W('7'), uno=W('uno', 36), paso2=W('paso', 37),
    abre=W('abre'), prende=W('prende'), interruptor2=W('interruptor', 39), olvidado=W('olvidado'), despierta=W('despierta'),
    comprar=W('comprar'), vender=W('vender'), sin=W('sin', 48), peor=W('peor'), antes=W('antes', 50), mando=W('mando'),
    d97=W('97'), correos=W('correos'), avisando=W('avisando'), mal=W('mal', 55), nadie2=W('nadie', 57), leyo=W('leyo'),
    apagaron=W('apagaron'), perdido=W('perdido'), dinero=W('dinero'), vendida=W('vendida'),
    asi=W('asi', 64), codigo=W('codigo', 65), acaso=W('acaso'), borralo=W('borralo'),
    mano=W('mano'), hoy=W('hoy'), automatizarlo=W('automatizarlo'), FIN=FIN,
)

# ------------------------------------------------------------------ el diorama (JS, tiempo global t)
MUNDO = r"""
const {caja,cil,cono,bola,grupo,letrero,pintura,persona,arbol,camion,rack,led,cuarto,reloj,cable,avanza,sobre,crece,hunde,vive,brota,cae,oscila,k,eo,eio,eb,h,mat,brillo,sombra}=M;
const T=__T__;
const add=(...os)=>{for(const o of os)M.scene.add(sombra(o));return os[0]};
const C={tabla:'#e3ddd0',canto:'#b8ae9e',calle:'#a39c90',raya:'#f2eee6',muro:'#ece7dd',piso:'#d6cfc2',tinta:'#22252b',rojo:'#d9483b',verde:'#3f8f5a',
 ocre:'#d9a441',pizarra:'#4b6a88',billete:'#7ba277',hueso:'#f6f3ec',gris:'#8e939b',fondo:'#5a5f68'};

// ---------- base de la maqueta (con el hueco del sótano en x[-1,5] z[3,9]) ----------
const HX0=-1,HX1=5,HZ0=3,HZ1=9,BAJO=-2.8;
const tabla=(x0,x1,z0,z1)=>add(caja(x1-x0,3.2,z1-z0,C.tabla,(x0+x1)/2,-3.2,(z0+z1)/2));
tabla(-22,HX0,-22,22);tabla(HX1,22,-22,22);tabla(HX0,HX1,HZ1,22);tabla(HX0,HX1,-22,HZ0);
// canto inferior más oscuro (se nota al alejarse)
add(caja(44.4,.5,44.4,C.canto,0,-3.7,0));
// sótano: piso y muros interiores de concreto
add(caja(HX1-HX0,.2,HZ1-HZ0,'#8f877b',(HX0+HX1)/2,BAJO-.2,(HZ0+HZ1)/2));
add(caja(.12,2.8,HZ1-HZ0,'#a79e90',HX0+.06,BAJO,(HZ0+HZ1)/2));add(caja(HX1-HX0,2.8,.12,'#9d9486',(HX0+HX1)/2,BAJO,HZ0+.06));
// calles
add(caja(44,.04,2.4,C.calle,0,0,0));add(caja(2.4,.04,44,C.calle,-4.2,0,0));
for(let i=-20;i<=20;i+=2.2){if(Math.abs(i+4.2)>1.5)add(caja(1.1,.05,.12,C.raya,i,0,0));if(Math.abs(i)>1.5)add(caja(.12,.05,1.1,C.raya,-4.2,0,i))}
// árboles y gente de relleno (fijos)
const ARB=[[-19,5],[-18,8],[-19,17],[-7,17],[-6,9],[7,15],[9,18],[18,14],[19,11],[19,-2],[18,-12],[8,-14],[-1,-14],[-17,-13],[-19,-8],[6,1.8],[-1.5,1.8],[11,1.9],[16,1.9],[-16,1.8],[-9,1.9]];
for(const [x,z] of ARB)add(arbol(x,z,h(x*3+z)<.5?'#8fa98b':'#a3b48c',.9+h(x+z)*.5));

// ---------- A · plaza del dinero (centro -12, 12) ----------
const AX=-12,AZ=12;
add(caja(9,.08,8,'#d9d1c1',AX,0,AZ));
const fajos=[];
for(let i=0;i<5;i++)for(let j=0;j<4;j++){const n=2+Math.floor(h(i*7+j*3)*5);const g=grupo(AX-3+i*1.5,0,AZ-2.4+j*1.6);
 for(let q=0;q<n;q++){const f=grupo(0,q*.2,0,caja(1.0,.19,.48,q%2?'#86ad80':'#7ba277'),caja(.2,.2,.5,C.hueso,0,0,0));f.rotation.y=(h(i*31+j*7+q)-.5)*.35;g.add(f)}
 g.userData.t0=T.perdio+.3+(i*4+j)*.16+h(i+j*9)*.4;fajos.push(add(g))}
const gentA=[[-16,8.5],[-15.6,9.2],[-8,15.5],[-8.6,16.1],[-16.2,15]].map(([x,z],i)=>add(persona(['#e8e2d6','#c9d3dc','#e3cfc0'][i%3],x,z)));
// torre del reloj
const torre=add(grupo(AX-1.6,0,AZ-4.6,caja(1.1,4.2,1.1,'#c8bfaf'),caja(1.4,.3,1.4,'#b4aa98',0,4.2,0),cono(.95,1,'#9e8f78',0,4.5,0,4)));
torre.rotation.y=Math.PI/4;
const rl=reloj(.48);rl.g.position.set(0,3.4,.6);torre.add(rl.g);
// el servidor del gancho (aparece en la plaza vacía)
const rk0=rack(AX,AZ,2.4);add(rk0.g);rk0.g.userData.s=1;
const polvo0=[];for(let i=0;i<10;i++){const b=caja(.16+h(i)*.12,.025,.12+h(i+2)*.1,'#d9d3c8',AX-.33+h(i)*.66,2.4,AZ-.33+h(i+4)*.66);b.rotation.y=h(i)*3;polvo0.push(add(b))}

// ---------- B · bolsa de NY y torre de Knight ----------
const nyse=grupo(-14,0,-3.5);
nyse.add(caja(6.4,.5,4.2,'#e9e4da'),caja(6,3,3.2,'#ddd6c9',0,.5,-.4),caja(6.6,.4,4.4,'#e9e4da',0,3.5,0));
for(let i=0;i<6;i++)nyse.add(cil(.2,3,'#f2eee6',-2.5+i,.5,1.6,8));
const fronton=new M.THREE.Mesh(new M.THREE.CylinderGeometry(1.4,1.4,6.4,3,1).rotateZ(Math.PI/2).rotateX(-Math.PI/2),mat('#e9e4da'));
fronton.scale.set(1,.5,1.3);fronton.position.set(0,3.9,.3);nyse.add(fronton);
const lNY=letrero('BOLSA DE NUEVA YORK',{w:4.6,h:.5,bg:'#e9e4da',fg:'#4a4d53',grosor:.06});lNY.position.set(0,3.5,2.25);nyse.add(lNY);
const asta=grupo(2.6,4.3,1.6,cil(.04,2,'#6b6f76'),caja(.9,.55,.04,'#c94a3d',.47,1.4,0));nyse.add(asta);
const campana=grupo(-1.6,4.3,-1.2,cil(.05,1.1,'#6b6f76'),caja(.9,.12,.12,'#6b6f76',0,1.1,0));
// la campana cuelga del travesaño (punta arriba, boca abajo)
const bellP=grupo(0,1.05,0,cono(.42,.62,'#d9a441',0,-.62,0,10),bola(.11,'#b3832c',0,-.7,0,0));campana.add(bellP);
nyse.add(campana);add(nyse);
const ondas=[0,1,2].map(i=>{const r=new M.THREE.Mesh(new M.THREE.TorusGeometry(1,.05,6,32),brillo('#e8b84a',1.2));r.rotation.x=Math.PI/2;r.position.set(-15.6,5,-4.7);M.scene.add(r);return r});
const knight=grupo(-7.6,0,-7.2);
knight.add(caja(3.4,8.4,3.4,'#cbc4b7'),caja(3.6,.3,3.6,'#b9b1a2',0,8.4,0));
const vOn=brillo('#f3dc9a',.35),vOff=mat('#7d776d');
const vent=[];for(let f=0;f<9;f++)for(const [w,d,x,z] of [[3.42,.14,0,1.7],[.14,3.42,1.7,0]]){const v=new M.THREE.Mesh(new M.THREE.BoxGeometry(w*.86,.32,d*.86).translate(0,.16,0),vOn);
 v.position.set(x,.7+f*.85,z);knight.add(v);vent.push(v)}
const sK=letrero('KNIGHT CAPITAL',{w:3.6,h:.8,bg:'#22252b',fg:'#f6f3ec',grosor:.16});sK.position.set(0,8.7,.9);knight.add(sK);
const sV=letrero('VENDIDA',{w:3.6,h:.9,bg:'#d9483b',fg:'#f6f3ec',grosor:.16});sV.position.set(0,8.7,.9);knight.add(sV);
add(knight);
const camiones=[0,1,2].map(i=>add(camion(['#4b6a88','#d9a441','#3f8f5a'][i])));
const cajasC=camiones.map(c=>{const b=caja(.9,.42,.6,'#c9a77a',-.3,.88,0);c.add(b);return b});
const mud=add(camion('#d9483b'));mud.scale.setScalar(1.25);mud.userData.s=1.25;
const cajasM=[0,1,2].map(i=>{const b=caja(.36,.3,.36,'#c9a77a',-1+i*.42,1.1,0);mud.add(b);return b});

// ---------- C · oficina de Knight (centro 2,-6) ----------
const OX=2,OZ=-6;
const ofi=add(cuarto(OX,OZ,7.4,6,2.6,C.muro,C.piso));
const escritorio=(x,z,c='#c9bfae')=>grupo(x,0,z,caja(1.3,.08,.7,c,0,.72,0),caja(.08,.72,.6,c,-.58,0,0),caja(.08,.72,.6,c,.58,0,0),caja(.5,.36,.06,'#2f3237',0,.8,-.18));
const PUESTOS=[[-2.1,.1],[-2.1,1.8],[2.4,2.0]];
const escs=PUESTOS.map(([x,z])=>add(escritorio(OX+x,OZ+z)));
const gente=PUESTOS.map(([x,z],i)=>add(persona(['#c9d3dc','#e3cfc0','#e8e2d6'][i],OX+x,OZ+z+.6)));
// sistema nuevo con moño
const nuevo=grupo(OX+2.4,0,OZ-.5,caja(1.3,1.7,1,'#9cc3d5'),caja(1.1,.5,.04,'#22252b',0,1,.5),caja(1.34,.16,1.04,'#d9483b',0,.9,0),caja(.16,1.74,1.04,'#d9483b',0,0,0),
 bola(.2,'#d9483b',-.18,1.85,0,0),bola(.2,'#d9483b',.18,1.85,0,0));
const scr=new M.THREE.Mesh(new M.THREE.BoxGeometry(.9,.36,.03).translate(0,.18,0),brillo('#7fe0a0',.0));scr.position.set(0,1.07,.52);nuevo.add(scr);
add(nuevo);
const tagN=letrero('NUEVO',{w:1.2,h:.42,bg:'#f6f3ec',fg:'#d9483b',grosor:.05});tagN.position.set(OX+2.4,1.95,OZ+.02);add(tagN);
// el interruptor: panel en el muro del fondo + palanca
const panel=grupo(OX-.6,.9,OZ-2.72,caja(1.2,1.3,.16,'#5a5f68'),caja(1,1.1,.04,'#6c727b',0,.1,.09));
const piv=grupo(0,.65,.16);const palanca=grupo(0,0,0,cil(.06,.6,'#c9ccd1',0,0,0,8),bola(.13,'#d9483b',0,.62,0,1));piv.add(palanca);panel.add(piv);
const lamp=new M.THREE.Mesh(new M.THREE.BoxGeometry(.2,.2,.05),brillo('#555',.2));lamp.position.set(.38,1.08,.12);panel.add(lamp);
const lP=letrero('INTERRUPTOR',{w:1.5,h:.3,bg:'#22252b',fg:'#f6f3ec',grosor:.05});lP.position.set(0,1.42,.06);panel.add(lP);
add(panel);
// cable del interruptor al sótano (y su chispa)
const ruta=[[OX-.6,1.1,OZ-2.7],[OX-.6,.12,OZ-2.55],[OX-.3,.12,OZ-.5],[OX,.12,OZ+2.6],[OX+.2,.06,0],[OX-.4,.06,HZ0-.6],[OX-.6,-.4,HZ0+.08],[OX-.7,-2.0,HZ0+.1],[OX-1.1,BAJO+.12,HZ0+.9]];
const cab=cable(ruta,.07,'#2f3237');add(cab);
const cabOn=cable(ruta,.095,'#ffb23a');cabOn.material=brillo('#ffb23a',1.1);M.scene.add(cabOn);
const chispa=bola(.3,'#ffe08a',0,0,0,1,{emissive:'#ffcf5a',emissiveIntensity:2.6});M.scene.add(chispa);

// ---------- C' · sótano con el programa viejo (robot Power Peg) ----------
const RX=.9,RZ=4.6;
const robot=grupo(RX,BAJO,RZ);
const piernas=grupo(0,0,0,caja(.28,.7,.3,'#7a6650',-.24,0,0),caja(.28,.7,.3,'#7a6650',.24,0,0));
const torso=grupo(0,.7,0,caja(1,1,.7,'#c08a4a'),caja(.5,.3,.05,'#2f3237',0,.55,.36));
const cabeza=grupo(0,1,0,caja(.72,.55,.6,'#b07d43'),cil(.03,.35,'#6b6f76',0,.55,0,6));
const ant=bola(.08,'#d9483b',0,.92,0,0);const antOn=brillo('#ff3b2b',2),antOff=mat('#d9483b');cabeza.add(ant);
const ojos=[-.16,.16].map(x=>{const o=new M.THREE.Mesh(new M.THREE.BoxGeometry(.15,.1,.04),brillo('#333',.1));o.position.set(x,.3,.31);cabeza.add(o);return o});
torso.add(cabeza);
const brazos=[-.6,.6].map(x=>{const b=grupo(x,.9,0,caja(.2,.75,.22,'#a87a45',0,-.75,0));torso.add(b);return b});
robot.add(piernas,torso);add(robot);
const polvo=[];for(let i=0;i<14;i++){const b=caja(.14+h(i)*.1,.025,.1+h(i+3)*.08,'#d9d3c8',RX-.32+h(i*3)*.64,BAJO+1.75+h(i)*.2,RZ-.25+h(i+9)*.5);b.rotation.y=h(i)*3;polvo.push(add(b))}
const cal=letrero('2003',{w:.9,h:.6,bg:'#f6f3ec',fg:'#22252b',grosor:.04,marco:'#d9483b'});cal.position.set(HX0+1.6+1.6,BAJO+1.4,HZ0+.14);add(cal);
const cajasS=[[3.6,4],[4.2,4.1],[3.9,4.1,.6]].map(([x,z,y=0])=>add(caja(.6,.6,.6,'#b89a72',x,BAJO+y,z)));
// basurero «BORRAR» y gancho de grúa
const BX=-2.4,BZ=6.6;
const bote=grupo(BX,0,BZ,caja(1.8,1.5,1.4,'#4b6a88'),caja(1.9,.1,1.5,'#3a556e',0,1.5,0));
const tapa=grupo(0,1.6,-.75,caja(1.9,.1,1.5,'#3a556e',0,0,.75));bote.add(tapa);
const lB=letrero('BORRAR',{w:1.5,h:.45,bg:'#f6f3ec',fg:'#d9483b',grosor:.04});lB.position.set(0,.5,.71);bote.add(lB);add(bote);
const gancho=grupo(0,0,0);const soga=caja(.05,12,.05,'#3b3f45',0,0,0);gancho.add(soga,caja(.6,.12,.3,'#d9a441',0,0,0),caja(.08,.4,.26,'#d9a441',-.26,-.4,0),caja(.08,.4,.26,'#d9a441',.26,-.4,0));
add(gancho);

// ---------- D · cuarto de servidores (centro 13, 6) ----------
const DX=13,DZ=6;
add(cuarto(DX,DZ,9.4,6,2.8,C.muro,'#cfd4d6'));
const racks=[];for(let i=0;i<8;i++){const r=rack(16.6-i*1.0,DZ-2.1,2.2,.78);add(r.g);racks.push(r)}
const etq=racks.map((r,i)=>{const l=letrero(String(i+1),{w:.5,h:.34,bg:i===7?'#d9483b':'#f6f3ec',fg:i===7?'#f6f3ec':'#22252b',grosor:.04});l.position.set(r.g.position.x,2.32,r.g.position.z+.4);add(l);return l});
const carrito=grupo(DX+1.6,0,DZ+1.6,caja(1.3,.5,.8,'#9aa0a8',0,.2,0),cil(.08,.4,'#22252b',-.5,0,.4),cil(.08,.4,'#22252b',.5,0,.4));
const chips=[];for(let i=0;i<8;i++){const c=caja(.32,.16,.24,'#59b46e',0,0,0);M.scene.add(sombra(c));chips.push(c)}
add(carrito);
const anillo=new M.THREE.Mesh(new M.THREE.TorusGeometry(.75,.06,6,32),brillo('#d9483b',1.4));anillo.rotation.x=Math.PI/2;anillo.position.set(racks[7].g.position.x,.12,racks[7].g.position.z);M.scene.add(anillo);
const ruta2=[[racks[7].g.position.x-.2,.1,DZ-2.4],[8.7,.06,DZ-2.4],[7,.06,DZ-2.2],[HX1+.4,.06,RZ+.5],[HX1-.2,-.5,RZ+.5],[HX1-.3,-2.2,RZ+.3],[RX+.6,BAJO+.1,RZ+.2]];const cab2=cable(ruta2,.06,'#2f3237');add(cab2);const cab2On=cable(ruta2,.085,'#ff5a3a');cab2On.material=brillo('#ff5a3a',1.1);M.scene.add(cab2On);
const trab=add(persona('#e3cfc0',DX+3,DZ+2.2));
const riel=grupo(DX+.1,2.7,DZ-1.6,caja(7.9,.18,.3,'#d9a441'));add(riel);
const lA=letrero('AUTO ✓',{w:1.7,h:.55,bg:'#3f8f5a',fg:'#f6f3ec',grosor:.06});lA.position.set(DX-2.6,2.22,DZ-2.84);add(lA);

// ---------- E · cinta de compra/venta y pizarra (alrededor del sótano) ----------
const cinta1=add(grupo(.4,0,12.2,caja(.9,.35,6.6,'#5a5f68')));
const cinta2=add(grupo(3.6,0,12.2,caja(.9,.35,6.6,'#5a5f68')));
const tex=(txt,bg,fg)=>letrero(txt,{w:.62,h:.3,bg,fg,grosor:.03});
const compra=[],venta=[];
for(let i=0;i<6;i++){const g=grupo(0,0,0,caja(.6,.5,.5,'#59b46e'));const l=tex('$$$','#f6f3ec','#3f8f5a');l.position.set(0,.12,.26);g.add(l);compra.push(add(g))}
for(let i=0;i<6;i++){const g=grupo(0,0,0,caja(.6,.5,.5,'#d9483b'));const l=tex('$','#f6f3ec','#d9483b');l.position.set(0,.12,.26);g.add(l);venta.push(add(g))}
const piz=grupo(-2.0,0,6.9,caja(2.6,2.6,.3,'#22252b',0,0,0));piz.rotation.y=Math.PI/4;
const flechas=[0,1,2].map(i=>{const f=cono(.28,.45,'#d9483b',-.8+i*.8,0,.2,4);f.rotation.x=Math.PI;f.position.y=2.1;piz.add(f);return f});
const lPz=letrero('KNIGHT  ▼ ▼ ▼',{w:2.3,h:.5,bg:'#22252b',fg:'#ff7a6b',grosor:.04});lPz.position.set(0,.8,.16);piz.add(lPz);add(piz);

// ---------- F · buzón de guardia (centro 13, -6) ----------
const FX=13,FZ=-6;
add(cuarto(FX,FZ,6.4,5.4,2.6,'#e6e1d6',C.piso));
const mesa=add(grupo(FX+.4,0,FZ-.4,caja(2.2,.08,1,'#c9bfae',0,.74,0),caja(.08,.74,.9,'#c9bfae',-1,0,0),caja(.08,.74,.9,'#c9bfae',1,0,0),caja(.6,.4,.06,'#2f3237',-.6,.82,-.3)));
const silla=add(grupo(FX+.3,0,FZ+.6,caja(.6,.08,.6,'#4b6a88',0,.45,0),caja(.6,.6,.08,'#4b6a88',0,.5,.28),cil(.05,.45,'#22252b',0,0,0,6)));
const charola=add(caja(.9,.12,.6,'#9aa0a8',FX+.8,.82,FZ-.4));
const tubo=add(cable([[FX+.8,2.6,FZ-2.6],[FX+.8,2.6,FZ-1.3],[FX+.8,2.0,FZ-.5]],.16,'#9aa0a8'));
const rF=reloj(.42);rF.g.position.set(FX-2.98,1.8,FZ-.6);rF.g.rotation.y=Math.PI/2;add(rF.g);
const taza=add(cil(.1,.18,'#f6f3ec',FX-.3,.82,FZ-.2,10));
const sobres=[];for(let i=0;i<42;i++){const s=sobre(h(i)<.85?'#f4f1ea':'#e9e3d3');M.scene.add(s);sobres.push(s)}

// ---------- placa de la serie (frente de la maqueta) ----------
const placaS=grupo(12.6,0,15.4,caja(8.4,.5,1.6,'#22252b'));placaS.rotation.y=Math.PI/4;
const lS=letrero('ARCHIVO #01\nKNIGHT CAPITAL · 2012',{w:8,h:2.4,bg:'#22252b',fg:'#f6f3ec',grosor:.12,marco:'#d9a441'});lS.rotation.x=-Math.PI/4;lS.position.set(0,.3,-.3);placaS.add(lS);add(placaS);placaS.visible=false;

// ---------- cámara (global) ----------
M.camara([
 [0,{x:-12,y:1,z:12,Z:7.4,az:40,el:31,oy:-.1}],
 [.15,{Z:6.6,az:46},5.2],
 [5.45,{y:1.4,Z:5.8,az:50},3.0],
 [8.9,{x:-10.4,y:2.6,z:-4.4,Z:8.6,az:42,el:30},1.3],
 [11.4,{az:50,Z:9.4},3.9],
 [15.4,{x:2.2,y:1,z:-6,Z:6.4,az:46,el:33},1.25],
 [18.3,{x:1.3,y:1.3,z:-7.4,Z:4.4},1.0],
 [21.7,{Z:3.9,az:42},2.6],
 [24.7,{x:1.8,y:-1.1,z:5.3,Z:5.6,el:40,az:46},1.55],
 [26.4,{Z:4.6},4.8],
 [31.45,{x:13,y:.9,z:5.6,Z:6.3,el:32,az:44},1.15],
 [36.15,{x:9.9,y:1.3,z:4.4,Z:4.3},1.0],
 [37.6,{x:-4.6,y:1.2,z:-3.6,Z:16,az:45,el:33},0.95],
 [40.3,{x:9.8,y:1.3,z:4.3,Z:4.6},1.0],
 [41.55,{x:1.3,y:-1.3,z:5.4,Z:4.4,el:41},0.9],
 [44.85,{x:1.6,y:-.4,z:8.4,Z:8.4,el:36},1.0],
 [49.4,{x:13.5,y:1.1,z:-6.2,Z:5.0,el:32,az:44},1.2],
 [54.5,{x:13.6,y:1.1,z:-6.4,Z:4.2},1.5],
 [57.15,{x:13,y:.8,z:-5.6,Z:3.3,az:50},1.0],
 [59.2,{x:-3,y:0,z:0,Z:20,az:45,el:35},1.4],
 [62.3,{x:-7.6,y:6,z:-6.6,Z:6.6},1.0],
 [64.85,{x:-.6,y:0,z:6.4,Z:7.0,el:36},1.1],
 [68.45,{x:13,y:2.9,z:5.4,Z:6.8,el:32},1.1],
 [72.7,{x:7.5,y:0,z:9.5,Z:17,el:38,az:45},1.7],
]);

// ---------- update(t) ----------
const P0=new M.THREE.Vector3();
return t=>{
 // luz: día; atenuada durante el apagón final; «antes de abrir» un poco más fría
 M.luz(1-.42*k(t,T.apagaron,.6)*(1-k(t,T.asi,.8)));
 // A · dinero que se va
 for(const f of fajos){if(t<T.empresa){f.visible=false;continue}crece(f,t,T.empresa+(f.position.x-AX+3)*.03,.5);if(t>=f.userData.t0)hunde(f,t,f.userData.t0,.45)}
 for(const [i,g] of gentA.entries())vive(g,t,T.empresa+.2+i*.1);
 vive(torre,t,0,1e9,.01);
 const mins=45*eio(k(t,T.perdio,T.minutos+.4-T.perdio));rl.hora(9,30+mins);
 // gancho: el servidor que nadie actualizó
 vive(rk0.g,t,T.servidor-.05,T.paso);
 for(const l of rk0.leds)led(l,'#8a9099',.15);
 led(rk0.leds[2],(Math.floor(t*3)%2)?'#d9483b':'#5a2a26',(Math.floor(t*3)%2)?2:.3);
 for(const [i,p] of polvo0.entries()){p.visible=t>=T.servidor+.35&&t<T.paso;p.scale.setScalar(Math.max(.001,eb(k(t,T.servidor+.35+i*.04,.3))))}
 // B · bolsa y Knight
 vive(nyse,t,T.paso-.2);vive(knight,t,T.knight-.1);
 sK.visible=t<T.vendida;if(t>=T.vendida-.05)hunde(sK,t,T.vendida-.05,.3);
 sV.visible=t>=T.vendida+.15;if(sV.visible)brota(sV,t,T.vendida+.15,.5);
 for(const v of vent)v.material=t>=T.apagaron&&t<T.asi?vOff:vOn;
 oscila(bellP,t,T.abre,.55,2.4,2.2);
 for(const [i,r] of ondas.entries()){const p=k(t,T.abre+i*.25,.9);r.visible=p>0&&p<1;r.scale.setScalar(.4+p*2.6)}
 for(const [i,c] of camiones.entries()){const on=t>=T.una;c.visible=on;if(!on)continue;
  const L=12,u=((t-T.una)*2.0+i*L/3)%L,ida=u<L/2,x=ida?-12.5+u*1.15:-12.5+(L-u)*1.15;
  c.position.set(x,0,ida?-.62:.62);c.rotation.y=ida?0:Math.PI;cajasC[i].visible=ida;brota(c,t,T.una+i*.15,.4)}
 // camión de mudanza tras «vendida»
 {const t0=T.vendida+.3;mud.visible=t>=t0-.6&&t<T.asi;const p=k(t,t0,1.8);mud.position.set(-7.6+(-12)*eio(p),0,-3.6+2.6*eo(k(t,t0-.6,.5)));mud.rotation.y=Math.PI;
  if(t<t0)brota(mud,t,t0-.6,.4);for(const [i,b] of cajasM.entries())b.visible=t>=t0-.4+i*.1}
 // C · oficina
 for(const e of escs)vive(e,t,T.estrenar-.4);for(const [i,g] of gente.entries())vive(g,t,T.estrenar-.3+i*.08);
 vive(nuevo,t,T.sistema,T.asi);brota(tagN,t,T.sistema+.35);tagN.visible=t>=T.sistema+.35&&t<T.prenderlo+1.2;
 scr.material.emissiveIntensity=t>T.sistema+.6?1.2:0;
 vive(panel,t,T.interruptor-.25);
 const on=t>=T.prende&&t<T.apagaron;
 {const pa=k(t,T.prende,.25),pb=k(t,T.apagaron,.25);piv.rotation.z=.7-1.4*eio(pa)+1.4*eio(pb)}
 led(lamp,on?'#3fd46e':'#55585e',on?2.2:.2);
 // la chispa recorre el cable: primero la «historia» (años antes) y luego de verdad al abrir la bolsa
 const curva=cab.userData.curva;
 const viaje=(a,d)=>{const p=k(t,a,d);return p>0&&p<1?p:null};
 let pc=viaje(T.prendia,1.7);if(pc==null)pc=viaje(T.prende+.1,1.2);
 chispa.visible=pc!=null;if(pc!=null){curva.getPointAt(pc,P0);chispa.position.copy(P0);chispa.scale.setScalar(.8+.3*Math.sin(t*30))}
 {const a=k(t,T.prendia,1.7),b=k(t,T.prende+.1,1.2);avanza(cabOn,t<T.viejo+1.4?a:(t>=T.prende+.1&&t<T.apagaron?b:0))}
 vive(cab,t,T.interruptor-.2,1e9,.01);
 // C' · robot: dormido → despierta → trabaja → apagado → a la basura
 vive(robot,t,T.viejo-.15,1e9,.6);
 const desp=k(t,T.despierta,.7),apg=k(t,T.apagaron,.6);
 const vivo=desp*(1-apg);
 for(const o of ojos)led(o,vivo>.5?'#ff3b2b':'#33302c',vivo>.5?2.6:.1);
 cabeza.rotation.x=.45*(1-vivo);cabeza.rotation.y=vivo>.5&&t<T.comprar?Math.sin((t-T.despierta)*5)*.4:0;
 torso.position.y=.7-.25*(1-vivo);ant.material=vivo>.5&&Math.floor(t*6)%2?antOn:antOff;
 for(const [i,b] of brazos.entries())b.rotation.x=t>=T.comprar&&t<T.apagaron?Math.sin(t*14+i*Math.PI)*.9:(vivo>.5?-.3:.15);
 for(const [i,p] of polvo.entries()){const sal=k(t,T.despierta+h(i)*.3,.6);p.visible=t>=T.viejo+.3&&sal<1;
  p.position.y=BAJO+1.75+h(i)*.2+sal*1.4;p.scale.setScalar(Math.max(.001,eb(k(t,T.viejo+.3+i*.02,.3))))}
 brota(cal,t,T.d2003-.1);cal.visible=t>=T.d2003-.1;
 for(const c of cajasS)vive(c,t,T.viejo+.1);
 // grúa: baja, agarra al robot y lo tira en «BORRAR»
 {const g0=T.codigo,ag=T.acaso-.2,su=ag+.35,mv=T.borralo-.35,dr=T.borralo;
  const top=9,yAg=BAJO+2.55;let gx=RX,gz=RZ,gy=top;
  if(t>=g0&&t<ag)gy=top+(yAg-top)*eio(k(t,g0,ag-g0));
  else if(t>=ag&&t<su)gy=yAg;
  else if(t>=su&&t<mv)gy=yAg+(3.6-yAg)*eio(k(t,su,mv-su));
  else if(t>=mv&&t<dr+.6){const p=eio(k(t,mv,.45));gx=RX+(BX-RX)*p;gz=RZ+(BZ-RZ)*p;gy=3.6}
  else if(t>=dr+.6){const p=eio(k(t,dr+.6,.6));gx=BX;gz=BZ;gy=3.6+(top-3.6)*p}
  gancho.visible=t>=g0&&t<dr+1.3;gancho.position.set(gx,gy,gz);soga.position.y=0;soga.scale.y=1;soga.position.y=0;
  soga.geometry.boundingSphere=null;
  if(t>=su&&t<dr+.1){robot.position.set(gx,gy-2.4,gz)}
  else if(t>=dr+.1){const p=k(t,dr+.1,.35);robot.position.set(BX,3.6-2.4-(3.6-2.4-.2)*p*p,BZ);robot.visible=p<1}
  else robot.position.set(RX,BAJO,RZ);
  tapa.rotation.x=t>=g0&&t<dr+.45?-1.2*eo(k(t,g0,.4)):-1.2*(1-eb(k(t,dr+.45,.4)));
  vive(bote,t,T.codigo-.4);
  bote.rotation.z=t>dr+.5?Math.sin((t-dr)*30)*.04*(1-k(t,dr+.5,.8)):0}
 // D · servidores
 for(const [i,r] of racks.entries())vive(r.g,t,T.subieron+i*.07);
 for(const [i,l] of etq.entries()){l.visible=t>=T.ocho-.1;brota(l,t,T.ocho-.1+i*.05,.35)}
 vive(carrito,t,T.subieron+.2,T.hoy);
 if(t>=T.asi+3.4&&t<T.hoy){carrito.position.x=DX+1.6-.9*k(t,T.asi+3.6,T.hoy-T.asi-3.6)}else carrito.position.x=DX+1.6;
 const cx=carrito.position.x;
 for(const [i,c] of chips.entries()){
  const r=racks[i].g.position,a=i<7?T.bueno-.6+i*.17:1e9,auto=T.hoy+.2+i*.05;
  const x0=cx-.4+(i%4)*.27,z0=DZ+1.45+Math.floor(i/4)*.3,y0=.72;
  if(t>=auto){const p=k(t,auto,.5);c.position.set(r.x,2.9-1.5*eio(p),r.z+.2);c.visible=p<1}
  else if(t>=a){const p=k(t,a,.45);c.position.set(x0+(r.x-x0)*p,y0+Math.sin(p*Math.PI)*1.6+.6*p,z0+(r.z+.3-z0)*p);c.visible=p<1}
  else{c.position.set(x0,y0,z0);c.visible=t>=T.subieron+.5&&t<T.hoy}}
 for(const [i,r] of racks.entries()){
  const ok=(i<7&&t>=T.bueno-.6+i*.17+.45)||t>=T.hoy+.7+i*.05;
  const rojo=i===7&&t>=T.olvidado-.3&&t<T.apagaron;
  const off=t>=T.apagaron&&t<T.hoy+.7;
  r.leds.forEach((l,j)=>{if(rojo)led(l,(Math.floor(t*8)+j)%2?'#ff3b2b':'#5a2a26',(Math.floor(t*8)+j)%2?2.4:.3);
   else if(off)led(l,'#4d5157',.1);else if(ok)led(l,'#3fd46e',1.6);else led(l,'#8a9099',.2)})}
 anillo.visible=t>=T.uno-.1&&t<T.abre;anillo.scale.setScalar(Math.max(.001,eb(k(t,T.uno-.1,.4))));
 vive(cab2,t,T.olvidado-.2,1e9,.01);avanza(cab2On,t<T.apagaron?k(t,T.olvidado,1.0):0);
 // trabajador con carrito «a mano» y luego el riel automático
 trab.visible=t>=T.asi+3.5&&t<T.hoy+.3;if(trab.visible){const p=k(t,T.asi+3.6,T.hoy-T.asi-3.6);trab.position.set(DX+3-.9*p,0,DZ+2.2);trab.rotation.z=Math.sin(t*9)*.06}
 vive(riel,t,T.hoy-.1);brota(lA,t,T.automatizarlo+.2);lA.visible=t>=T.automatizarlo+.2;
 // E · compra cara / venta barata
 vive(cinta1,t,T.comprar-.6,T.apagaron);vive(cinta2,t,T.comprar-.5,T.apagaron);
 const vel=1+2.2*k(t,T.sin,1.2);
 for(const [i,b] of compra.entries()){const s0=T.comprar-.25+i*.06;const u=((t-T.comprar)*1.7*vel+i*1.1)%6.6;
  b.visible=t>=s0&&t<T.apagaron;b.position.set(.4,.35,15.4-u);if(u>6.2)b.position.y=.35-(u-6.2)*7;if(t<s0+.4)brota(b,t,s0,.35);else b.scale.setScalar(1)}
 for(const [i,b] of venta.entries()){const s0=T.vender-.25+i*.06;const u=((t-T.vender)*1.7*vel+i*1.1)%6.6;
  b.visible=t>=s0&&t<T.apagaron;b.position.set(3.6,.35,9.0+u);if(t<s0+.4)brota(b,t,s0,.35);else b.scale.setScalar(1)}
 vive(piz,t,T.comprar+.2,T.apagaron+.4);for(const [i,f] of flechas.entries())f.position.y=2.6+Math.sin(t*9+i)*.12;
 vive(placaS,t,72.5,1e9,.6);
 // F · 97 correos que nadie leyó
 for(const o of [mesa,silla,charola,taza,tubo])vive(o,t,T.peor-.2);
 vive(rF.g,t,T.peor-.2,1e9,.01);
 {const p=k(t,T.antes,1.0);const m=(9*60+30)-(89)*eio(p);rF.hora(Math.floor(m/60),m%60)}
 silla.rotation.y=t>T.nadie2?Math.sin((t-T.nadie2)*1.2)*.5:0;
 for(const [i,s] of sobres.entries()){const t0=T.mando+.05+i*.06;if(t<t0){s.visible=false;continue}s.visible=true;
  const p=k(t,t0,.35);const fx=FX+.8+(h(i)-.5)*.62,fz=FZ-.4+(h(i+7)-.5)*.42,fy=.9+Math.min(i,32)*.022+(i>32?(h(i)*.15):0);
  const sx=FX+.8,sy=2.0,sz=FZ-.4;s.position.set(sx+(fx-sx)*p,sy+(fy-sy)*p*p,sz+(fz-sz)*p);
  s.rotation.y=h(i*3)*2.4;s.rotation.z=i>30?(h(i)-.5)*.6:0;
  const rojo=s.children[1];rojo.visible=t>=T.avisando-.1+i*.01}
};
"""


# ------------------------------------------------------------------ capas de texto (placas y etiquetas)
def capas():
    t = T
    c = []
    # b01–b02 gancho
    c += [placa(t['m470'] - .15, 5.3, 60, 170, 700, et('Una empresa perdió') + f'<div class="gr">${N([[t["m470"], 0], [t["m470"], 470, .9]])}<span class="md" style="font-size:64px"> millones</span></div>'),
          placa(t['m45'] - .1, 5.3, 60, 520, 520, et('en') + f'<div class="gr">{N([[t["m45"], 0], [t["m45"], 45, .7]])} <span class="md" style="font-size:60px">minutos</span></div>', ac=Q.OCRE),
          placa(t['razon'] - .1, 8.9, 60, 190, 560, '<div class="md">¿La razón?</div>', cls='osc'),
          pin(t['servidor'] + .25, 8.9, [-12, 2.4, 12], '<small>un servidor</small>que nadie actualizó', dx=150, dy=-260, ac=Q.ROJO)]
    # b03 2012 · Knight
    c += [placa(t['paso'], 15.3, 60, 170, 470, et('Nueva York') + '<div class="gr">2012</div>', ac=Q.PIZARRA),
          pin(t['knight'] + .2, 15.3, [-7.6, 8.9, -6.2], '<small>la empresa</small>Knight Capital', dx=-60, dy=-150),
          pin(t['una'] + .1, 15.3, [-9.5, .9, -.5], '<small>una de las que más</small>acciones movía en EE.&nbsp;UU.', dx=60, dy=330, ac=Q.VERDE)]
    # b04 sistema nuevo + interruptor
    c += [placa(t['estrenar'] - .05, 21.55, 60, 170, 560, et('Iban a estrenar') + '<div class="md">un sistema nuevo</div>', ac=Q.PIZARRA),
          pin(t['interruptor'], 21.55, [1.4, 2.2, -8.8], '<small>para prenderlo</small>un interruptor', dx=110, dy=-210, ac=Q.ROJO),
          placa(t['existia'], 21.55, 60, 1020, 640, et('ya existía en su código') + '<div class="cod">if (interruptor) {<br>&nbsp;&nbsp;arranca(…)<br>}</div>', ac=Q.OCRE)]
    # b05 el problema
    c += [placa(t['problema'] - .1, 26.1, 60, 170, 620, et('El problema') + '<div class="md">ese interruptor, años antes…</div>'),
          placa(t['prendia'] - .05, 26.1, 60, 470, 620, '<div class="md">prendía <span class="ac" style="color:#ffb23a">otro programa</span></div>', cls='osc')]
    # b06 el programa viejo
    c += [pin(t['viejo'] + .3, 31.4, [.9, -.6, 4.6], '<small>programa viejo</small>Power Peg', dx=120, dy=-300, ac=Q.OCRE),
          placa(t['apagado'], 31.4, 60, 170, 540, et('apagado desde') + '<div class="gr">2003</div>', ac=Q.OCRE),
          placa(t['borraron'] - .2, 31.4, 60, 1100, 640, '<div class="md">…y nunca lo borraron</div>', cls='osc')]
    # b07 8 servidores, a 7
    c += [placa(t['subieron'], 37.5, 60, 170, 600, et('Subieron la versión nueva') + f'<div class="gr">{N([[t["ocho"], 8], [t["siete"], 7, .35]])}<span class="md" style="font-size:60px"> de 8 servidores</span></div>', ac=Q.VERDE),
          pin(t['uno'], 37.5, [9.6, 2.3, 4.0], '<small>servidor 8</small>a este se les pasó', dx=-380, dy=430, ac=Q.ROJO)]
    # b08 abre la bolsa → despierta
    c += [placa(t['abre'] - .05, 40.2, 420, 170, 500, et('9:30 a. m.') + '<div class="md">abre la bolsa</div>', ac=Q.OCRE),
          pin(t['prende'], 40.2, [1.4, 2.0, -8.7], '<small>interruptor</small>ON', dx=90, dy=-200, ac=Q.VERDE),
          pin(t['olvidado'] - .3, 41.5, [9.6, 2.3, 4.0], '<small>el servidor olvidado</small>prende el programa viejo', dx=60, dy=330, ac=Q.ROJO),
          pin(t['despierta'] + .2, 44.8, [.9, -.3, 4.6], '<small>Power Peg</small>¡despierta!', dx=120, dy=-300, ac=Q.ROJO)]
    # b09 compra caro / vende barato (contador de pérdida)
    loss = [[t['comprar'], 0], [t['comprar'], 160, t['sin'] + 1 - t['comprar']]]
    c += [placa(t['comprar'] - .1, 49.3, 60, 170, 420, et('compra caro') + '<div class="md" style="color:#3f8f5a">▲ $$$</div>', ac=Q.VERDE),
          placa(t['vender'] - .1, 49.3, 500, 170, 420, et('vende barato') + '<div class="md" style="color:#d9483b">▼ $</div>'),
          placa(t['sin'] - .1, 49.3, 60, 420, 380, et('pérdida') + f'<div class="md">−${N(loss)}M</div>', cls='osc')]
    # b10–b11 97 correos
    c += [placa(t['antes'] - .1, 57.1, 60, 170, 560, et('antes de abrir') + '<div class="md">8:01 a. m.</div>', ac=Q.PIZARRA),
          placa(t['d97'] - .1, 57.1, 60, 450, 560, et('mandó') + f'<div class="gr">{N([[t["d97"], 0], [t["d97"], 97, 1.6]])}<span class="md" style="font-size:60px"> correos</span></div>'),
          pin(t['avisando'], 57.1, [13.8, 1.3, -6.4], '<small>asunto</small>Power Peg disabled', dx=-330, dy=380, ac=Q.ROJO),
          placa(t['nadie2'] - .05, 59.1, 60, 230, 780, '<div class="gr" style="font-size:92px">Nadie los leyó.</div><div class="ch">leídos: 0 de 97</div>', cls='osc')]
    # b12 final
    c += [placa(t['apagaron'] - .05, 64.8, 60, 170, 700, et('aunque lo apagaron') + f'<div class="gr">−${N([[t["perdido"], 160], [t["perdido"], 470, t["dinero"] + .4 - t["perdido"]]])}<span class="md" style="font-size:60px"> millones</span></div>'),
          pin(t['vendida'] + .3, 64.8, [-7.6, 9.6, -6.2], '<small>Knight Capital</small>terminó vendida', dx=-40, dy=-170, ac=Q.ROJO)]
    # b13 bórralo
    c += [placa(t['asi'], 68.4, 60, 170, 640, et('consejo 1') + '<div class="md">¿código viejo apagado «por si acaso»?</div>', ac=Q.OCRE),
          placa(t['borralo'] - .05, 68.4, 60, 520, 440, '<div class="gr">Bórralo.</div>', cls='osc')]
    # b14 automatiza + cierre
    c += [placa(t['mano'] - 1.9, 72.6, 60, 170, 600, et('consejo 2') + '<div class="md">¿subes cambios a mano?</div>', ac=Q.PIZARRA),
          placa(t['hoy'], 72.6, 60, 470, 600, '<div class="md">Hoy es buen día para <span style="color:#7fe0a0">automatizarlo</span>.</div>', cls='osc'),
          placa(72.75, FIN + 1, 60, 170, 860, et('ARCHIVO · #01') + '<div class="md">Historias raras, graciosas y trágicas del mundo tech</div><div class="ch" style="font-weight:800">Sígueme para la siguiente →</div>')]
    return c


# ------------------------------------------------------------------ páginas (tramos del mismo recorrido)
TRAMOS = [('p1-gancho', 0.0, 8.95), ('p2-knight', 8.95, 21.65), ('p3-viejo', 21.65, 31.5), ('p4-despierta', 31.5, 44.9),
          ('p5-correos', 44.9, 57.2), ('p6-borralo', 57.2, 68.5), ('p7-cierre', 68.5, FIN)]
MJS = MUNDO.replace('__T__', json.dumps(T))
CAPAS = capas()
PIEZAS = []
for pid, a, b in TRAMOS:
    fin = b if b >= FIN else round(b + COLA, 2)
    PIEZAS.append((pid, a, fin, Q.page(MJS, CAPAS, a, round(fin - a, 2))))
OCULTAR = [[T['nadie2'] - .1, 59.2], [72.7, FIN + 1]]
PIEZAS.append(('sub', 0.0, FIN, Q.subtitulos(GRUPOS, FIN, OCULTAR)))

if __name__ == '__main__':
    solo = set(sys.argv[1:])
    lote = []
    for pid, a, b, html in PIEZAS:
        if solo and pid not in solo:
            continue
        path = f'{WORK}/{pid}.html'
        open(path, 'w').write(html)
        print('html', pid, f'{a:6.2f}–{b:6.2f}')
        lote.append(dict(html=path, dur=round(b - a, 2), out=f'{OUT}/{PRE}{pid}.webm'))
    json.dump(lote, open(f'{OUT}/lote-maqueta.json', 'w'), indent=1)
    if not solo:
        rel = os.environ.get('REL', 'archivo/1/animaciones')
        ovs = [{'file': f'{rel}/{PRE}{pid}.webm', 'html': f'{rel}/_html-maqueta/{pid}.html', 'start': a, 'end': round(min(b, FIN), 2), 'trimIn': 0,
                'scale': 1, 'position': 'center'} for pid, a, b, _ in PIEZAS]
        json.dump(ovs, open(f'{OUT}/overlays-maqueta.json', 'w'), indent=2, ensure_ascii=False)
        print('overlays-maqueta.json · lote-maqueta.json')
