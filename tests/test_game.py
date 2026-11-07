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
run('INPUT');assert get('BULY')==19 and get('BULX')==20
put('TICK',2);put('EY',18);put('EX',20);put('KIND',0)
run('UPDATE');assert get('EY')==0 and get('SCORE')==2
put('EY',20);put('EX',20);run('UPDATE');assert get('LIVES')==2
run('UPDATE');assert get('LIVES')==2
put('IMMUNE',0);put('KIND',3);put('OIL',0);run('UPDATE');assert get('OIL')==3
put('IMMUNE',0);put('LIVES',1);put('EY',20);put('KIND',0)
run('UPDATE');assert get('DEAD')==1
run('RESET');put('EY',17);m.memory[0xd01f]=5;run('INPUT');assert get('OIL')==2 and get('EY')==0
run('INPUT');assert get('OIL')==2
run('RESET');put('TICK',2);put('SHOTY',19);put('SHOTX',20);run('UPDATE');assert get('LIVES')==2
run('RESET');random.seed(800);maxcycles=0
for i in range(2000):
 put('TICK',(i*2)&255);m.memory[0xd20a]=random.randrange(256)
 m.memory[0x278]=random.choice([15,11,7,14]);m.memory[0x284]=random.randrange(2);m.memory[0xd01f]=7
 start=m.processorCycles
 run('INPUT');run('UPDATE');run('DRAW')
 maxcycles=max(maxcycles,m.processorCycles-start)
 assert 10<=get('PX')<=29
 assert all(0<=m.memory[s['EY']+j]<=23 for j in range(6))
 if get('DEAD'):run('RESET')
print('PASS: XEX entry, steering, shooting, collision, invulnerability, supplies, oil, enemy fire, game over, 2000-frame soak')
print('Maximum simulated update/draw cycles:',maxcycles,'(excludes Atari DMA and OS interrupts)')
