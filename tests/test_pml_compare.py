from __future__ import annotations

from wsb.pml_compare import compare_elements, parse_pml, render_markdown


BASELINE = """\
-- accepted model
NEW EQUI /TANK_1
POS E 0 N 0 U 0
NEW SUBE /TANK_1_SHELL
NEW CYLI
DIAM 3000
HEIG 5000
ORI Z IS U AND Y IS N
POS E 1000 N 2000 U 2500
NEW NOZZLE /TANK_1_N1_NOZZ
CATR SPCOMPONENT /150lb_Ansi_Flanged/AAZFBB0GG
POS E 2500 N 2000 U 3000
ORI P1 IS E
HEIG 350
"""


def test_native_compare_finds_named_attribute_change_and_added_child():
    modified = BASELINE.replace("HEIG 350", "HEIG 425") + """\
NEW SUBE /TANK_1_USER_DETAIL
NEW BOX
XLEN 100
YLEN 200
ZLEN 25
POS E 1000 N 2000 U 5100
"""
    result = compare_elements(parse_pml(BASELINE), parse_pml(modified))

    assert result["summary"] == {
        "baseline_elements": 4,
        "modified_elements": 6,
        "added": 2,
        "removed": 0,
        "changed": 1,
    }
    assert result["added"] == [
        "/TANK_1/TANK_1_USER_DETAIL > BOX #1",
        "SUBE /TANK_1_USER_DETAIL",
    ]
    assert result["changed"][0]["element"] == "NOZZLE /TANK_1_N1_NOZZ"
    assert result["changed"][0]["attributes"] == [
        {"attribute": "HEIG", "before": "350", "after": "425"}
    ]


def test_native_compare_ignores_comments_whitespace_and_numeric_formatting():
    reformatted = (
        BASELINE.replace("-- accepted model\n", "-- native export\n\n")
        .replace("DIAM 3000", "  DIAM    3000.000 ")
        .replace("POS E 1000 N 2000 U 2500", "POS E 1000.0 N 2000.00 U 2500")
    )
    result = compare_elements(parse_pml(BASELINE), parse_pml(reformatted))
    assert result["summary"]["added"] == 0
    assert result["summary"]["removed"] == 0
    assert result["summary"]["changed"] == 0


def test_native_compare_aligns_unnamed_primitive_after_insertion():
    baseline = """\
NEW EQUI /V1
NEW SUBE /V1_SHELL
NEW CYLI
DIAM 1000
HEIG 2000
POS E 0 N 0 U 1000
NEW CYLI
DIAM 800
HEIG 1000
POS E 0 N 0 U 2500
"""
    modified = baseline.replace(
        "NEW CYLI\nDIAM 800",
        "NEW BOX\nXLEN 50\nYLEN 50\nZLEN 50\nPOS E 0 N 0 U 2050\n"
        "NEW CYLI\nDIAM 800",
    )
    result = compare_elements(parse_pml(baseline), parse_pml(modified))
    assert result["summary"]["added"] == 1
    assert result["summary"]["removed"] == 0
    assert result["summary"]["changed"] == 0
    assert result["added"] == ["/V1/V1_SHELL > BOX #1"]


def test_markdown_report_exposes_before_and_after_values():
    modified = BASELINE.replace("ORI P1 IS E", "ORI P1 IS N")
    result = compare_elements(parse_pml(BASELINE), parse_pml(modified))
    report = render_markdown(result)
    assert "ORI" in report
    assert "P1 IS E" in report
    assert "P1 IS N" in report
