# -*- coding: utf-8 -*-
import os, re
from transform_mc_pumps import transform_054_equipment

def export_individual_pumps():
    in_054_path = 'Projects/JK_Pump_Build/imports/2026-08-24_205_PU_054_native_updated.txt'
    with open(in_054_path, 'r', encoding='utf-8') as f:
        text_054 = f.read()

    pos_054 = text_054.find('NEW EQUIPMENT /205_PU_054')
    end_054 = text_054.find('OLD NOZZLE', pos_054)
    if end_054 == -1: end_054 = text_054.find('INPUT END', pos_054)
    block_054 = text_054[pos_054:end_054].strip()

    targets = {
        '/205_PU_054': {
            'tag': '205_PU_054',
            'desc': 'D1 STAGE MC PUMP',
            'block': block_054
        },
        '/203_PU_020': {
            'tag': '203_PU_020',
            'desc': '025024',
            'block': transform_054_equipment(block_054, '/203_PU_020', '025024', (17095.0, 5685.0, 0.0), 'CCW')
        },
        '/204_PU_028': {
            'tag': '204_PU_028',
            'desc': 'POST OXYGEN WASHER DISCHARGE MC PUMP',
            'block': transform_054_equipment(block_054, '/204_PU_028', 'POST OXYGEN WASHER DISCHARGE MC PUMP', (22370.0, 6986.0, 0.0), 'CW')
        },
        '/205_PU_018': {
            'tag': '205_PU_018',
            'desc': 'D0 STAGE MC PUMP',
            'block': transform_054_equipment(block_054, '/205_PU_018', 'D0 STAGE MC PUMP', (35727.6, 5019.0, 0.0), 'CCW')
        },
        '/205_PU_038': {
            'tag': '205_PU_038',
            'desc': 'EOP STAGE MC PUMP',
            'block': transform_054_equipment(block_054, '/205_PU_038', 'EOP STAGE MC PUMP', (43112.9, 5016.0, 0.0), 'CCW')
        }
    }

    out_dir = 'Projects/JK_Pump_Build/output/2026-08-23_pumps_mc_replaced'
    os.makedirs(out_dir, exist_ok=True)

    header_template = """$S-  -- Synonym translation OFF
-- ----------------------------------------------------------------
-- Equipment Listing    Tag: {eq_tag}

ONERROR GOLABEL /ERROR3

INPUT BEGIN
{eq_block}

OLD NOZZLE 1 of SUBEQUIPMENT /{eq_tag}_AID_MOTOR_2
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0WW

OLD NOZZLE /{eq_tag}_SUCTION_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR

OLD NOZZLE 2 of SUBEQUIPMENT /{eq_tag}_SUCTION
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR

OLD NOZZLE /{eq_tag}_DISCHARGE_NOZZLE
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0RR

INPUT END  EQUIPMENT /{eq_tag}
INPUT FINISH
-- Switch synonyms back on if an error occurs.
LABEL /ERROR3
handle ANY
$S+
RETURN ERROR
endhandle

$S+  -- Synonym translation ON
-- ----------------------------------------------------------------
"""

    for full_tag, cfg in targets.items():
        tag_clean = cfg['tag']
        file_content = header_template.format(
            eq_tag=tag_clean,
            eq_block=cfg['block']
        )
        file_path = os.path.join(out_dir, f'{tag_clean}.pml')
        with open(file_path, 'w', encoding='utf-8') as out_f:
            out_f.write(file_content)
        print(f'Wrote individual equipment file: {file_path}')

if __name__ == '__main__':
    export_individual_pumps()
