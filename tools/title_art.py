"""Generate the hardware-sized title bitmap and embed MAC/65 data in game.asm."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
font={
'A':['01110','10001','10001','11111','10001','10001','10001'],
'C':['01111','10000','10000','10000','10000','10000','01111'],
'E':['11111','10000','10000','11110','10000','10000','11111'],
'F':['11111','10000','10000','11110','10000','10000','10000'],
'H':['10001','10001','10001','11111','10001','10001','10001'],
'I':['111','010','010','010','010','010','111'],
'J':['00111','00010','00010','00010','10010','10010','01100'],
'K':['10001','10010','10100','11000','10100','10010','10001'],
'L':['10000','10000','10000','10000','10000','10000','11111'],
'M':['10001','11011','10101','10101','10001','10001','10001'],
'N':['10001','11001','11001','10101','10011','10011','10001'],
'O':['01110','10001','10001','10001','10001','10001','01110'],
'P':['11110','10001','10001','11110','10000','10000','10000'],
'R':['11110','10001','10001','11110','10100','10010','10001'],
'S':['01111','10000','10000','01110','00001','00001','11110'],
'T':['11111','00100','00100','00100','00100','00100','00100'],
'U':['10001','10001','10001','10001','10001','10001','01110'],
'Y':['10001','10001','01010','00100','00100','00100','00100'],
' ':['000']*7, ':':['0','1','0','0','1','0','0']}
pix=[[0]*160 for _ in range(192)]
def rect(x,y,w,h,c):
 for yy in range(y,y+h):
  for xx in range(x,x+w):pix[yy][xx]=c

def text(t,y,sx=1,sy=1,c=2,dx=0):
 width=sum(len(font[ch][0])+1 for ch in t)-1;x=(160-width*sx)//2+dx
 for ch in t:
  for yy,line in enumerate(font[ch]):
   for xx,bit in enumerate(line):
    if bit=='1':rect(x+xx*sx,y+yy*sy,sx,sy,c)
  x+=(len(font[ch][0])+1)*sx
for t,y,sx,sy in [('SPY',7,5,3),('HUNTER',35,4,3)]:
 text(t,y+3,sx,sy,3,1);text(t,y,sx,sy)
for y in range(68,145):
 rect(0,y,27,1,1);rect(133,y,27,1,1)
 rect(27,y,3,1,2 if (y//6)%2 else 3);rect(130,y,3,1,2 if (y//6)%2 else 3)
 if (y%16)<9:
  rect(62,y,1,1,2);rect(98,y,1,1,2)
car=['00022000','00222200','00222200','02222220','02222220','02222220','00222200','00200200','00200200','00200200','00222200','00222200','00222200','00222200','00222200','00222200','00222200','00222200','00222200','00200200','00222200','00222200','00300300','00000000']
for y,row in enumerate(car):
 for x,c in enumerate(row):rect(72+x*2,82+y*2,2,2,int(c))
text('PRESS FIRE OR START',153)
text('JOYSTICK: STEER  FIRE: SHOOT',174)
text('SELECT: OIL  OPTION: SMOKE',184)
data=b''.join(bytes(sum(pix[y][x+k]<<(6-2*k) for k in range(4)) for x in range(0,160,4))+bytes(24) for y in range(192))
def emit(data):return ''.join(' .BYTE '+','.join(str(n) for n in data[i:i+16])+'\n' for i in range(0,len(data),16))
p=R/'src/game.asm';s=p.read_text().split('; BEGIN GENERATED TITLE')[0]
s+='; BEGIN GENERATED TITLE (tools/title_art.py)\nTITLEPROMPT\n'+emit(data[152*64:160*64])
s+=' *= $6C00\nTITLEDL\n .BYTE $70,$70,$70\n'
# Pad each scanline to 64 bytes: no 40-byte line straddles a 4 KB boundary.
for y in range(192):s+=' .BYTE $4E\n .WORD '+str(0x7000+64*y)+'\n'
s+=' .BYTE $41\n .WORD TITLEDL\n *= $7000\nTITLEBITMAP\n'+emit(data)
s+=' *= $02E0\n .WORD START\n';p.write_text(s)
# Optional exact-palette preview, never used by the game or required to build.
if __name__=='__main__':
 from PIL import Image
 im=Image.new('RGB',(160,192));palette=[(20,20,20),(0,130,35),(244,244,244),(181,76,14)]
 im.putdata([palette[c] for row in pix for c in row]);im.resize((640,384),Image.Resampling.NEAREST).save(R/'docs/title-screen.png')
