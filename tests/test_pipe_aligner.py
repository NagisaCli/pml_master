import re
import pytest

def test_pipe_aligner_syntax_and_callbacks():
    with open(r'C:\Users\A\Desktop\PIPE_Aligin\pipe_action.mac', 'r', encoding='ascii') as f:
        action_content = f.read()

    with open(r'C:\Users\A\Desktop\PIPE_Aligin\pipe_aligner.pmlfrm', 'r', encoding='ascii') as f:
        form_content = f.read()

    # Verify illegal commands and syntax traps are NOT present
    assert 'DIR P3' not in action_content, 'DIR P3 found in macro!'
    assert 'DIR LEAV' not in action_content, 'DIR LEAV found in macro!'
    assert 'DIR ^^' not in action_content, 'DIR ^^ found in macro!'
    assert 'var !picked' not in action_content, 'Invalid pick syntax found!'
    assert 'ID ELEMENT' not in action_content, 'Invalid ID ELEMENT found!'
    assert '.abs(' not in action_content, 'Method .abs() found in macro!'

    # Verify callbacks in form match actions in macro
    callbacks = re.findall(r'pipe_action\.mac"\s+([a-zA-Z0-9]+)', form_content)
    assert len(callbacks) >= 6
    for cb in callbacks:
        assert f"!action.eq('{cb}')" in action_content, f'Action {cb} missing in macro!'

    # Verify autoAll calls all 5 sub-steps:
    auto_match = re.search(r"elseif \(!action\.eq\('autoAll'\)\) then(.*?)(\$S\+|endif)", action_content, re.DOTALL)
    assert auto_match, 'autoAll block not found!'
    auto_body = auto_match.group(1)
    for step in ['calcInter', 'alignU', 'solveMove', 'alignDir', 'connectTail']:
        assert step in auto_body, f'{step} not invoked in autoAll!'

    # Verify syntax pairs
    assert action_content.count('$S-') == action_content.count('$S+'), 'Synonym balance mismatch!'
    assert action_content.count('handle ANY') == action_content.count('endhandle'), 'Handle balance mismatch!'


def test_geometric_ray_intersection():
    # Exact coordinates from user project
    main_hpos = {'E': 66365.47, 'N': 62250.0, 'U': 11058.5}
    main_tpos = {'E': 66365.47, 'N': 73812.12, 'U': 1051.33}
    elb_pos = {'E': 66876.0, 'N': 70800.0, 'U': 11158.5}
    elb_dir = {'E': -0.70710678, 'N': 0.70710678, 'U': 0.0}

    # Solver
    rawDeltaE = main_tpos['E'] - main_hpos['E']
    deltaE = -rawDeltaE if rawDeltaE < 0 else rawDeltaE

    rawDeltaN = main_tpos['N'] - main_hpos['N']
    deltaN = -rawDeltaN if rawDeltaN < 0 else rawDeltaN

    assert deltaN >= deltaE  # North-South pipe

    tE = main_hpos['E']
    tU = main_hpos['U']
    s = (tE - elb_pos['E']) / elb_dir['E']
    tN = elb_pos['N'] + s * elb_dir['N']

    assert abs(tE - 66365.47) < 0.001
    assert abs(tN - 71310.53) < 0.01
    assert abs(tU - 11058.50) < 0.001
    assert abs((elb_pos['U'] - tU) - 100.0) < 0.001
