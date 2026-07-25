"""
E3D Agent — AVEVA E3D modeling automation for pulp & paper plants
=================================================================

Generates PML1 macro scripts for AVEVA E3D (Everything3D Mk3.1) from project
data, drawings, or natural language.

Two entry points:

``wsb``
    Project delivery for the Pulp Mill Washing, Screening & Bleaching area.
    Models the 22 tank-type equipment items from the JK-Project equipment list,
    each positioned by its bottom centre point, with an engineering report
    covering modeling parameters, reference values and outstanding issues::

        python -m wsb

``agent``
    General pipeline: parse a description or drawing, retrieve knowledge, emit
    PML, optionally execute in E3D::

        python -m e3d_agent.agent "a 4800mm fourdrinier paper machine"

Modules
-------
``wsb``             WSB tank dataset, geometry builder, validator, report
``drawing_parser``  SVG / PDF / DXF and natural language parsing
``pml_knowledge``   Equipment specifications and PML syntax reference
``pml_generator``   DesignIntent to PML1 code generation
``e3d_interface``   E3D execution: file mode and command line
``memory``          Error tracking and pattern learning
``examples``        Standalone reference plant model generators
"""

__version__ = "1.0.0"
