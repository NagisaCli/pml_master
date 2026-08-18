import os
import re

def build_nozzle_fix_macro(source_file, workspace_dir, output_macro):
    mapping = {}
    
    # 1. Scan workspace for all known NOZZLE -> CATR mappings
    for root, dirs, files in os.walk(workspace_dir):
        for f in files:
            if f.endswith('.txt') or f.endswith('.pml'):
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
                                mapping[cur_nozz] = line_s.split('CATR ')[1]
                except Exception:
                    pass

    # 2. Extract all nozzles from the target Data Listing file
    with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
        source_lines = f.readlines()

    target_nozzles = []
    for line in source_lines:
        ls = line.strip()
        if ls.startswith('NEW NOZZLE '):
            nozz = ls.split('NEW NOZZLE ')[1]
            target_nozzles.append(nozz)

    # 3. Generate PML repair script
    pml_lines = [
        '-- ====================================================================',
        '-- AVEVA E3D BATCH REPAIR NOZZLE CATR MACRO',
        f'-- Source: {source_file}',
        f'-- Total Nozzles: {len(target_nozzles)}',
        '-- Usage in E3D Command Line:',
        f'--   $M "{output_macro}"',
        '-- ====================================================================',
        '',
        '$S-  -- Synonym translation OFF',
        ''
    ]

    for nozz in target_nozzles:
        catr = mapping.get(nozz, 'SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0YY')
        pml_lines.append(f'-- Repair {nozz}')
        pml_lines.append('handle ANY')
        pml_lines.append(f'{nozz}')
        pml_lines.append(f'CATR {catr}')
        pml_lines.append('endhandle')
        pml_lines.append('')

    pml_lines.append('$S+  -- Synonym translation ON')
    pml_lines.append('-- ====================================================================')
    pml_lines.append(f'-- Finished batch repair for {len(target_nozzles)} nozzles.')
    pml_lines.append('-- ====================================================================')

    with open(output_macro, 'w', encoding='utf-8') as f:
        f.write('\n'.join(pml_lines))
        
    print(f'Successfully generated {output_macro} with {len(target_nozzles)} nozzles.')

if __name__ == '__main__':
    source_file = r'C:\Users\A\Desktop\yes_detec.txt'
    workspace_dir = r'c:\Users\A\Desktop\Projects\e3d_agent'
    output_macro = r'C:\Users\A\Desktop\fix_site_nozzles.pml'
    build_nozzle_fix_macro(source_file, workspace_dir, output_macro)
