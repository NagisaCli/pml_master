"""
pumpcad - JSON-driven precision pump reconstruction.
====================================================

Rebuilds each pump from the CAD linework exported alongside its
``Pump_details.xlsx`` row, instead of from a generic pump template.

Pipeline (each stage is a separate module so it can be tested alone)::

    JSON                -> source.py      (RawCadEntity, PumpRecord)
    ValidatedGeometry   -> geometry.py    (Segment, dedup, validation)
    ContourGroups       -> contours.py    (chaining, closure, circle recovery)
    PumpSemanticModel   -> semantic.py    (component classification)
    world placement     -> transform.py   (CAD -> local -> world)
    E3D objects         -> emit.py        (PML, reusing wsb conventions)
    audit               -> audit.py       (per-pump validation record)

The installation/reference architecture (baseplate datum, orientation,
nozzle sizing, naming, OWNER logic) is inherited from JK_Pump_Build; the
pump body geometry comes from the CAD evidence.
"""

from __future__ import annotations

__all__ = ["__version__"]

__version__ = "1.0.0"
