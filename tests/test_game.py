"""Execute the shipped XEX on an NMOS 6502 simulator (not an Atari emulator)."""
import sys,json,struct,random
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools/vendor'))
from py65.devices.mpu6502 import MPU
s=json.loads((R/'dist/symbols.json').read_text()); m=MPU(); b=(R/'dist/road-agent.xex').read_bytes(); p=2
while p<len(b):
 a,z=struct.unpack_from('<HH',b,p); p+=4;m.memory[a:z+1]=b[p:p+z-a+1];p+=z-a+1
assert m.memory[0x2e0]+256*m.memory[0x2e1]==s['START']
def get(k):return m.memory[s[k]]
def put(k,v):m.memory[s[k]]=v
def run(label):
 m.pc=s[label];m.sp=0xff;m.stPushWord(0x17ff);n=0
 while m.pc!=0x1800:
  m.step();n+=1
  assert n<100000,(label,hex(m.pc))
 return n
run('RESET');assert get('LIVES')==3 and get('PX')==20
m.memory[0x278]=11;m.memory[0x284]=1;m.memory[0xd01f]=7
run('INPUT');assert get('PX')==19
m.memory[0x278]=7;run('INPUT');assert get('PX')==20
m.memory[0x278]=15;m.memory[0x284]=0
run('INPUT');assert get('BULY')==16 and get('BULX')==21
put('TICK',2);put('EY',15);put('EX',20);put('KIND',0)
run('UPDATE');assert get('EY')==0 and get('SCORE')==2
put('EY',20);put('EX',20);run('UPDATE');assert get('LIVES')==2
run('UPDATE');assert get('LIVES')==2
put('IMMUNE',0);put('KIND',3);put('OIL',0);put('SMOKE',0);put('SPEED',1)
for _ in range(12):run('UPDATE')
assert get('OIL')==3 and get('SMOKE')==3 and get('EY')==0
put('IMMUNE',0);put('LIVES',1);put('EY',20);put('KIND',0)
run('UPDATE');assert get('DEAD')==1
run('RESET');put('EY',19);put('EX',20);m.memory[0xd01f]=5;run('INPUT');assert get('OIL')==2 and get('HAZARD')==60
run('UPDATE');assert get('EY')==0
run('INPUT');assert get('OIL')==2
run('RESET');put('TICK',2);put('SHOTY',19);put('SHOTX',20);run('UPDATE');assert get('LIVES')==2
# Smoke persists, uses a separate inventory, and does not repeat while held.
run('RESET');m.memory[0xd01f]=3;run('INPUT')
assert get('SMOKE')==2 and get('HAZTYPE')==3
run('INPUT');assert get('SMOKE')==2
# Armored enemies and supply trucks resist machine guns.
for kind in (2,3):
 run('RESET');put('TICK',2);put('EY',10);put('EX',20);put('KIND',kind);put('BULY',11);put('BULX',20)
 run('UPDATE');assert get('EY')==10 and get('BULY')==0
# Bends propagate down the road and off-road driving costs a life.
run('RESET')
for _ in range(100):run('WORLD')
assert len(set(m.memory[s['LEFTS']+2:s['LEFTS']+24]))>1
run('RESET');put('PX',2);run('WORLD');assert get('LIVES')==2 and get('SPEED')==1
# Screen geometry and 2x3 player tiles; clipping never touches the font.
run('RESET');run('DRAW')
assert m.memory[0x6000+17*40+20:0x6000+17*40+23]==[71,72,73]
assert m.memory[0x6000+21*40+20:0x6000+21*40+23]==[83,84,85]
assert m.memory[0x6000+23]==19 and m.memory[0x6000+30]==19 and m.memory[0x6000+39]==19
m.memory[0x63c0:0x6400]=[0xA5]*64
put('ROW',23);put('COL',36);m.a=98;run('CAR')
assert m.memory[0x63c0:0x6400]==[0xA5]*64
run('RESET');random.seed(800);maxcycles=0
for i in range(2000):
 put('TICK',(i*2)&255);m.memory[0xd20a]=random.randrange(256)
 m.memory[0x278]=random.choice([15,11,7,14,13]);m.memory[0x284]=random.randrange(2);m.memory[0xd01f]=7
 start=m.processorCycles
 run('INPUT');run('UPDATE');run('DRAW')
 maxcycles=max(maxcycles,m.processorCycles-start)
 assert 2<=get('PX')<=36
 assert all(0<=m.memory[s['EY']+j]<=23 for j in range(6))
 if get('DEAD'):run('RESET')
print('PASS: XEX entry, steering, shooting, collision, invulnerability, truck docking, oil/smoke, armor, bends, rendering bounds, enemy fire, game over, 2000-update soak')
print('Maximum simulated update/draw cycles:',maxcycles,'(excludes Atari DMA and OS interrupts)')
# Title startup integration: advance the OS clock and use real entry point.
def boot_until(target,limit=200000):
 for i in range(limit):
  if m.pc==s[target]:return
  if i%100==0:m.memory[0x14]=(m.memory[0x14]+1)&255
  m.step()
 raise AssertionError(('Did not reach',target,hex(m.pc)))
for trigger in ('fire','start'):
 m.pc=s['START'];m.sp=255;m.memory[0x284]=1;m.memory[0xd01f]=7
 boot_until('TITLEWAIT')
 assert m.memory[0x230]+256*m.memory[0x231]==s['TITLEDL']
 before=(get('SCORE'),get('LIVES'),get('TICK'))
 for i in range(100000):
  if i%100==0:m.memory[0x14]=(m.memory[0x14]+1)&255
  m.step()
  assert m.pc!=s['MAIN']
 assert before==(get('SCORE'),get('LIVES'),get('TICK'))
 if trigger=='fire':m.memory[0x284]=0
 else:m.memory[0xd01f]=6
 boot_until('TITLERELEASE')
 m.memory[0x284]=1;m.memory[0xd01f]=7
 boot_until('MAIN')
 assert get('LIVES')==3 and get('SCORE')==0 and get('BULY')==0
 assert m.memory[0x230]+256*m.memory[0x231]==s['DLIST']
m.memory[0x14]=32;run('TITLEBLINK');assert not any(m.memory[0x9600:0x9800])
m.memory[0x14]=0;run('TITLEBLINK');assert bytes(m.memory[0x9600:0x9800])==bytes(m.memory[s['TITLEPROMPT']:s['TITLEPROMPT']+512])
# Every bitmap scanline has an LMS and the final JVB targets the title list.
for y in range(192):
 a=s['TITLEDL']+3+3*y
 assert m.memory[a]==0x4e
 assert m.memory[a+1]+256*m.memory[a+2]==0x7000+64*y
print('PASS: title idle, blink, FIRE/START release-gated launch, bitmap display list')

# Shared artwork must decode identically in the title bitmap and gameplay tiles.
sys.path.insert(0,str(R/'tools'))
from interceptor import INTERCEPTOR
for y,row in enumerate(INTERCEPTOR):
 for x,c in enumerate(row):
  glyph=71+(y//8)*3+x//4
  packed=m.memory[s['ART']+(glyph-64)*8+y%8]
  assert (packed>>(6-2*(x%4)))&3==int(c)
  packed=m.memory[0x7000+(84+y)*64+(74+x)//4]
  assert (packed>>(6-2*((74+x)%4)))&3==int(c)
# Visible front and right edge of the enlarged player participate in collisions.
for ex,ey in [(22,15),(19,21)]:
 run('RESET');put('TICK',2);put('EX',ex);put('EY',ey);put('KIND',0)
 run('UPDATE');assert get('LIVES')==2
run('RESET');put('TICK',2);put('SHOTY',16);put('SHOTX',22)
run('UPDATE');assert get('LIVES')==2
print('PASS: identical title/driving car pixels, enlarged collision and projectile alignment')
