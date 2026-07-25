"""
Standalone model generators
===========================
Self-contained scripts that emit complete PML1 macros for reference plant
models. They demonstrate the modeling patterns in ``AGENTS.md`` at full scale
and do not depend on the agent pipeline.

Run them as modules from the repository's parent directory::

    python -m e3d_agent.examples.paper_machine_model
    python -m e3d_agent.examples.paper_mill_plant_master
    python -m e3d_agent.examples.paper_mill_mega_100k_plant

Macros are written to ``output/`` at the package root.
"""
