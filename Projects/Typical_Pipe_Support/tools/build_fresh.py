"""Create a complete R2 namespace with no reliance on partial R1 state."""
import hashlib
import json
import re
from pathlib import Path
from build_review import SOURCE, EXPECTED_HASH, PROJECT, build, verify, validate_pml, parse_primitives

OUT=PROJECT/"output/Typical_Pipe_Support_R2.pml"
DEPLOY=Path(r"C:\e3d_models\SINGLE_TYPICAL_PIPE_SUPPORT_R2.pml")

def fresh_script(source):
    base=build(source)
    script=base.replace("/TPS_R1_","/TPS_R2_").replace("/ZONE_TYPICAL_SUPPORT_R1","/ZONE_TYPICAL_SUPPORT_R2")
    script=script.replace("Support R1: independent review candidate.","Support R2: complete fresh load; no R1 state required.")
    script=script.replace("-- Source identification is provisional; see the review report.",
                          "-- Source path uses underscores; escaped chat underscores are not directories.")
    return script

def verify_fresh(script,source):
    assert not validate_pml(script), validate_pml(script)
    assert not re.search(r"/TPS_R1_|/ZONE_TYPICAL_SUPPORT_R1",script)
    assert not re.search(r"(?im)^\s*(DELETE|SAVEWORK|SAVE WORK|\$M)\b",script)
    # Every explicit model selection must refer to an element created earlier
    # in this file. Catalogue SPRE attributes are separate external references.
    created=set()
    commands=[]
    for line in script.splitlines():
        if not line or line.startswith("--"): continue
        commands.append(line)
        m=re.match(r"NEW (\w+) (/\S+)$",line)
        if m:
            assert m[2] not in created
            created.add(m[2])
        elif line.startswith("/"):
            assert line in created, f"Uncreated model dependency: {line}"
    assert commands[0]=="NEW ZONE /ZONE_TYPICAL_SUPPORT_R2"
    assert "NEW STRU /TPS_R2_STRUCTURE" in commands
    assert "NEW FRMW /TPS_R2_FRAME" in commands
    assert commands.index("NEW FRMW /TPS_R2_FRAME") < commands.index("NEW SCTN /TPS_R2_BEAM")
    normalized=script.replace("/TPS_R2_","/TPS_R1_").replace("/ZONE_TYPICAL_SUPPORT_R2","/ZONE_TYPICAL_SUPPORT_R1")
    checks=verify(normalized,source)
    # Only comments and names may differ from the corrected complete R1.
    active=lambda s:[x for x in s.splitlines() if x and not x.startswith("--")]
    assert active(normalized)==active(build(source))
    assert len(parse_primitives(script,"TPS_R2_HARDWARE"))==174
    checks.update(revision="R2",requires_existing_R1=False,model_selections_created_before_use=True,
                  geometry_unchanged_from_corrected_R1=True)
    checks["limits"][0]="Source path decoded from chat underscore escapes"
    return checks

def main():
    raw=SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_HASH
    source=raw.decode("utf-8-sig").replace("\r\n","\n")
    script=fresh_script(source)
    checks=verify_fresh(script,source)
    for path in (OUT,DEPLOY):
        if path.exists():
            assert path.read_text(encoding="ascii")==script, f"Unexpected existing candidate: {path}"
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(script,encoding="ascii")
        verify_fresh(path.read_text(encoding="ascii"),source)
    assert OUT.read_bytes()==DEPLOY.read_bytes()
    checks["sha256"]=hashlib.sha256(DEPLOY.read_bytes()).hexdigest()
    (OUT.parent/"Typical_Pipe_Support_R2_checks.json").write_text(json.dumps(checks,indent=2)+"\n",encoding="ascii")
    print(json.dumps({"file":str(DEPLOY),**checks},indent=2))

if __name__=="__main__": main()
