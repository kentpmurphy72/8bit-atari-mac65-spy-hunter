"""Regenerate the original multicolor tile artwork embedded in game.asm."""
from pathlib import Path
from interceptor import INTERCEPTOR
p=Path(__file__).resolve().parents[1]/'src/game.asm'
tiles=[[0]*8 for _ in range(64)]
tiles[0]=[85,85,85,85,85,85,85,85] # green verge
tiles[1]=[106,106,106,106,127,127,127,127] # rumble strip
tiles[2]=[10]*8;tiles[3]=[0]*8
tiles[4]=[34,34,34,34,0,0,0,0] # twin machine guns
tiles[5]=[12,12,12,12,0,0,0,0]
tiles[6]=[85,85,69,65,65,69,85,85] # verge texture
enemy_base=['00022000','00222200','00222200','02222220','02222220','02222220','00222200','00200200','00200200','00200200','03222230','03222230','00222200','00222200','00222200','00222200','03222230','03222230','00222200','00200200','00222200','00222200','00222200','00000000']
red=[r.replace('2','3') for r in enemy_base]
armored=['00333300','03333330','03333330','03333330','03333330','00322300','00322300','03333330']+red[8:]
truck=['00222200','02222220','02200220','02200220','02222220','03333330','03333330','00333300']+['03222230','03233230','03233230','03233230']*3+['03222230','03300330','03300330','00000000']
oil=['00000000','00033000','00333300','03333330','03333330','00333300','00033000','00000000']*3
smoke=['00222000','02222200','22222220','02222222','22222220','02222200','00222220','00022000']*3
explosion=['00030000','02030020','00333000','23323332','00333000','03020300','30000030','00000000']*3
def sprite(code,rows):
 assert len(rows)==24
 for by in range(3):
  for bx in range(2):
   tiles[code-64+by*2+bx]=[sum(int(rows[by*8+y][bx*4+x])<<(6-2*x) for x in range(4)) for y in range(8)]
for code,rows in [(86,red),(92,armored),(98,truck),(104,oil),(110,smoke),(116,explosion)]:sprite(code,rows)
# Player occupies fifteen consecutive characters, 71-85 (3 columns x 5 rows).
for by in range(5):
 for bx in range(3):
  tiles[71-64+by*3+bx]=[sum(int(INTERCEPTOR[by*8+y][bx*4+x])<<(6-2*x) for x in range(4)) for y in range(8)]
s=p.read_text();a=s.index('\nART\n')+5;b=s.index('\nDLIST\n',a)
s=s[:a]+'; Original 4-color tiles, glyphs 64-127.\n'+''.join(' .BYTE '+','.join(map(str,t))+'\n' for t in tiles)+s[b:];p.write_text(s)
