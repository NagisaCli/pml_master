import os

authoritative_mapping = {}

# 1. Read all output pmls first (highest priority)
output_dir = r'c:\Users\A\Desktop\Projects\e3d_agent'
for root, dirs, files in os.walk(output_dir):
    for f in files:
        if f.endswith('.pml'):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                    cur_nozz = None
                    for line in fh:
                        line_s = line.strip()
                        if line_s.startswith('NEW NOZZLE '):
                            cur_nozz = line_s.split('NEW NOZZLE ')[1]
                        elif line_s.startswith('OLD NOZZLE '):
                            cur_nozz = line_s.split('OLD NOZZLE ')[1]
                        elif line_s.startswith('CATR ') and cur_nozz:
                            authoritative_mapping[cur_nozz] = line_s.split('CATR ')[1]
            except Exception:
                pass

# 2. Read imports if not in pml
for root, dirs, files in os.walk(output_dir):
    for f in files:
        if 'imports' in root and f.endswith('.txt'):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                    cur_nozz = None
                    for line in fh:
                        line_s = line.strip()
                        if line_s.startswith('NEW NOZZLE '):
                            cur_nozz = line_s.split('NEW NOZZLE ')[1]
                        elif line_s.startswith('OLD NOZZLE '):
                            cur_nozz = line_s.split('OLD NOZZLE ')[1]
                        elif line_s.startswith('CATR ') and cur_nozz:
                            if cur_nozz not in authoritative_mapping:
                                authoritative_mapping[cur_nozz] = line_s.split('CATR ')[1]
            except Exception:
                pass

# Let's inspect yes_detec.txt nozzles
with open(r'C:\Users\A\Desktop\yes_detec.txt', 'r', encoding='utf-8', errors='ignore') as f:
    yes_lines = f.readlines()

yes_nozzles = []
for line in yes_lines:
    ls = line.strip()
    if ls.startswith('NEW NOZZLE '):
        nozz = ls.split('NEW NOZZLE ')[1]
        yes_nozzles.append(nozz)

# Build pure PML1 fix macro
pml1_lines = [
    '-- ====================================================================',
    '-- AVEVA E3D PURE PML1 BATCH REPAIR NOZZLE CATR MACRO',
    '-- Scope: 235 nozzles in Site /SEAL/EQUIP',
    '-- Instructions: In E3D Command window type: $M "C:\\Users\\A\\Desktop\\fix_site_nozzles.mac"',
    '-- ====================================================================',
    '',
    '$S-  -- Synonym translation OFF',
    ''
]

for nozz in yes_nozzles:
    catr = authoritative_mapping.get(nozz, 'SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY')
    pml1_lines.append(f'{nozz}')
    pml1_lines.append(f'CATR {catr}')
    pml1_lines.append('')

pml1_lines.append('$S+  -- Synonym translation ON')
pml1_lines.append('-- ====================================================================')
pml1_lines.append(f'-- Finished batch repair for {len(yes_nozzles)} nozzles.')
pml1_lines.append('-- ====================================================================')

content = '\n'.join(pml1_lines)

for ext in ['mac', 'pml', 'txt']:
    p = rf'C:\Users\A\Desktop\fix_site_nozzles.{ext}'
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

print(f'Successfully wrote {len(yes_nozzles)} nozzle repairs to Desktop files.')
