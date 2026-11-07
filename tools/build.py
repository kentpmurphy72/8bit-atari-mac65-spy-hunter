"""Two-pass MAC/65 subset assembler; py65 supplies official NMOS opcodes."""
import sys, re, json, struct
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools/vendor'))
from py65.devices.mpu6502 import MPU
from py65.assembler import Assembler
symbols = {}
lines = (ROOT/'src/game.asm').read_text().splitlines()
def value(s, loose=False):
    s=s.strip().upper()
    low=s.startswith('<'); high=s.startswith('>')
    if low or high: s=s[1:]
    s=re.sub(r'\$([0-9A-F]+)',r'0x\1',s)
    s=re.sub(r'\b[A-Z_][A-Z_0-9]*\b',lambda m:str(symbols.get(m[0],0)) if loose else str(symbols[m[0]]),s)
    n=eval(s,{'__builtins__':{}},{})
    return n&255 if low else (n>>8)&255 if high else n
asm=Assembler(MPU())
for stage in range(6):
    pc=0; memory={}
    for number,line in enumerate(lines,1):
        try:
            line=line.split(';')[0].rstrip()
            if not line.strip(): continue
            if '=' in line and not line.lstrip().startswith('*'):
                name,expr=line.split('=',1); symbols[name.strip().upper()]=value(expr,stage<5); continue
            if line.lstrip().startswith('*='):
                pc=value(line.split('=',1)[1]); continue
            if not line.startswith(' '):
                parts=line.split(None,1); symbols[parts[0].upper()]=pc
                line=parts[1] if len(parts)>1 else ''
            if not line: continue
            parts=line.strip().upper().split(None,1); op=parts[0]; arg=parts[1] if len(parts)>1 else ''
            if op in ('.BYTE','.WORD'):
                data=[]
                for item in arg.split(','):
                    n=value(item,stage<5); data.extend([n&255] if op=='.BYTE' else [n&255,n>>8])
            else:
                operand=arg
                if arg and arg!='A':
                    immediate=arg.startswith('#')
                    suffix=',X' if arg.endswith(',X') else ',Y' if arg.endswith(',Y') else ''
                    expr=arg[1:] if immediate else arg
                    if suffix: expr=expr[:-2]
                    n=value(expr,stage<5)
                    # Force absolute addressing except immediate and relative.
                    operand=('#$%02X'%n if immediate else '$%04X'%n)+suffix
                if op.startswith('B') and op not in ('BIT','BRK'):
                    if stage==5 and not -128 <= value(arg)-(pc+2) <=127: raise ValueError('branch out of range')
                    operand='$%04X'%(pc+2) if stage<5 else operand
                data=asm.assemble(op+' '+operand,pc)
            for byte in data:
                if pc in memory: raise ValueError('overlapping segment')
                memory[pc]=byte; pc+=1
        except Exception as e: raise RuntimeError(f'line {number}: {line}: {e}') from e
out=bytearray(b'\xff\xff'); addresses=sorted(memory); i=0
while i<len(addresses):
    start=addresses[i]; end=start
    while i+1<len(addresses) and addresses[i+1]==end+1: i+=1; end+=1
    out+=struct.pack('<HH',start,end)+bytes(memory[a] for a in range(start,end+1)); i+=1
(ROOT/'dist/road-agent.xex').write_bytes(out)
(ROOT/'dist/symbols.json').write_text(json.dumps(symbols,indent=2)+'\n')
print(f'Built {len(out)} bytes')

(ROOT/"dist/game.mac").write_bytes(bytes([155]).join((str((i+1)*10)+" "+line).encode("ascii") for i,line in enumerate(lines))+bytes([155]))
