import re, os, shutil

SRC = r'C:\Users\A\Desktop\pump_edit.txt'
BAK = SRC + '.bak'

if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print('backup ->', BAK)

with open(SRC, encoding='utf-8') as f:
    text = f.read()
had_final_newline = text.endswith('\n')
lines = text.split('\n')

# ---------- 1) seat the 8 motor-pedestal hex nuts on the sole plate (U140..156) ----------
nut_pos_re = re.compile(r'^POS E (625|685|1245|1305)mm ([NS]) 220mm U 170mm$')
nut_count = 0
for i, ln in enumerate(lines):
    if nut_pos_re.match(ln.strip()):
        lines[i] = ln.replace('U 170mm', 'U 140mm')
        nut_count += 1
print('hex nuts reseated:', nut_count)
assert nut_count == 8

# ---------- 2) replace the two rounded-rect junction-box extrusions with BOX ----------
GEOM = {'EXTRUSION', 'CYLINDER', 'BOX'}
stack = []
blocks = []
for idx, raw in enumerate(lines):
    ln = raw.strip()
    if not ln:
        continue
    if re.match(r'^NEW\s+', ln, re.I):
        typ = ln.split()[1].upper()
        stack.append([typ if typ in GEOM else None, idx])
        continue
    if ln.upper() == 'END' and stack:
        t, s = stack.pop()
        if t:
            blocks.append((s, idx, t))
assert not stack

box_blocks = []
for s, e, t in blocks:
    if t != 'EXTRUSION':
        continue
    head = [lines[i].strip() for i in range(s, min(s+5, e+1))]
    if len(head) >= 2 and head[0] == 'NEW EXTRUSION' and re.match(r'^POS E (870|970)mm N 0mm U 665mm$', head[1]) and head[2] == 'HEIG 50mm':
        box_blocks.append((s, e, head[1]))
print('junction-box extrusion blocks found:', len(box_blocks))
assert len(box_blocks) == 2

remove_idx = set()
for s, e, _ in box_blocks:
    remove_idx.update(range(s, e+1))

def box_block(pos_line):
    m = re.match(r'^POS E (870|970)mm N 0mm U 665mm$', pos_line)
    cx = m.group(1)
    return [
        'NEW BOX',
        f'POS E {cx}mm N 0mm U 690mm',
        'XLEN 60mm',
        'YLEN 50mm',
        'ZLEN 50mm',
        '',
        'END',
    ]

# ---------- 3) top suction nozzle: plug the pipe into the volute dome ----------
# pipe U745..835 -> U678..835 (embedded ~20 mm into the dome, no rim gap)
top_ok = 0
for i, ln in enumerate(lines):
    if ln.strip() == 'POS E 0mm N 0mm U 745mm':
        lines[i] = 'POS E 0mm N 0mm U 678mm'
        top_ok += 1
    if ln.strip() == 'HEIG 90mm':
        # only the top-nozzle pipe has HEIG 90mm with DIAM 170mm; guard by neighbour
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        if j < len(lines) and lines[j].strip() == 'END':
            k = i - 1
            while k >= 0 and lines[k].strip() == '':
                k -= 1
            if lines[k].strip() == 'DIAM 170mm':
                lines[i] = 'HEIG 157mm'
print('top nozzle pipe repositioned:', top_ok)
assert top_ok == 1

# ---------- 4) discharge nozzle: extend pipe to the volute left face (X -150) ----------
dis_ok = 0
for i, ln in enumerate(lines):
    if ln.strip() == 'POS W 208mm N 0mm U 400mm':
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        k = j
        while k < len(lines) and lines[k].strip() not in ('HEIG',) and not lines[k].strip().startswith('HEIG'):
            k += 1
        # find DIAM 170mm then HEIG 40mm within the same block
        blk_end = None
        depth = 0
        for m in range(i, len(lines)):
            s = lines[m].strip()
            if re.match(r'^NEW\s+', s, re.I):
                depth += 1
            elif s == 'END':
                depth -= 1
                if depth == 0:
                    blk_end = m
                    break
        seg = lines[i:blk_end+1]
        if 'DIAM 170mm' in [x.strip() for x in seg] and 'HEIG 40mm' in [x.strip() for x in seg]:
            for m in range(i, blk_end+1):
                if lines[m].strip() == 'HEIG 40mm':
                    lines[m] = 'HEIG 58mm'
                    dis_ok += 1
print('discharge nozzle extended:', dis_ok)
assert dis_ok == 1

# ---------- assemble ----------
final = []
for i, ln in enumerate(lines):
    if i in remove_idx:
        continue
    final.append(ln)

# insert the two BOX blocks at the position of the first removed box
insert_at = min(s for s, e, _ in box_blocks)
out_lines = []
for i, ln in enumerate(final):
    if i == insert_at:
        out_lines.append('')
        out_lines.extend(box_block(box_blocks[0][2]))
        out_lines.append('')
        out_lines.extend(box_block(box_blocks[1][2]))
        out_lines.append('')
    out_lines.append(ln)

out_text = '\n'.join(out_lines)
if had_final_newline:
    out_text += '\n'
with open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write(out_text)
print('wrote', SRC, 'lines:', len(out_lines))
