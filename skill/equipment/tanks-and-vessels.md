# Tank-Type Equipment

Vertical cylindrical vessels: tanks, chests, towers, reactors, receivers. The
dominant equipment class in a pulp mill and the most-modelled type in this skill.

**User-supplied parameters always override this file.**

---

## Anatomy

```
            ┌─────────┐   ← roof: flat / conical / dished
            │         │   ← top-mounted accessories
            │  shell  │   ← stiffening rings (external, on tall thin shells)
            │         │   ← nozzles: neck + flange
            │         │   ← manway (access, ~DN600, at grade or platform level)
            └─────────┘   ← bottom: flat / conical / dished
             ║       ║    ← support: skirt / legs / ground
        ─────╨───────╨────← foundation bearing plane = BOTTOM CENTRE POINT
```

The **bottom centre point** is the setting-out datum (IR-6): the centre of the
foundation bearing plane at the bottom of the support, not the bottom of the
shell. Nothing is modelled below it.

---

## Configuration by duty — VERIFIED in production (JK-Project, 22 tanks)

Configuration follows the equipment's process duty. This table drove 22 delivered
models:

| Equipment class | Roof | Bottom | Support | Notes |
|-----------------|------|--------|---------|-------|
| Filtrate / dilution tank | Conical | Flat | Ground | Atmospheric, often agitated |
| Feed tank | Dished | Dished | Skirt | Elevated above an MC pump |
| Oxygen / EOP reactor | Dished | Conical | Skirt | Upflow, pressurised, platforms |
| Bleaching tower (D0/D1) | Flat | Conical | Skirt | Flat roof carries top equipment |
| Blow tank | Conical | Conical | Skirt | Large vapour relief to cyclone |
| Storage tower | Conical | Dished | Ground | Double shell, bottom scraper |
| Washer dropleg | Flat | Conical | Legs | Barometric leg, >10 m for vacuum seal |
| Vent scrubber | Conical | Conical | Skirt | Packed column inside an outer shell |
| Air receiver | Dished | Dished | Legs | Pressure vessel, relief valve |

### Why the configuration follows the duty

- **Pressurised** → dished heads. Flat heads cannot carry internal pressure at
  these diameters.
- **Solids or pulp to be drained completely** → conical bottom.
- **Elevated for pump suction (NPSH)** → skirt.
- **Atmospheric, sits on a slab** → flat bottom, ground bearing.
- **Carries equipment on top** → flat roof.
- **Vapour to be collected centrally** → conical roof.

Reasoning from duty is more reliable than memorising the table; the table is the
worked result of it.

---

## Process logic — the most common engineering error

- **Upflow** (reactor, bleaching tower): fed at the **bottom** cone, discharges
  at the **top**.
- **Downflow / storage**: fed **high** on the shell, drawn from the **bottom**.

Nozzle elevations must follow the flow direction. Getting this backwards produces
a model that is geometrically perfect and process-nonsense.

Additionally: vents at the **high** point, drains at the **low** point, overflow
below the roof.

---

## Nozzles

**Never place nozzles arbitrarily.** Where reference drawings dimension them,
follow the drawings. Otherwise provide the minimum process-logical set — feed,
discharge, overflow, vent, drain, manway — sized to the duty, spread across
distinct bearings so future piping does not collide, and flagged as Reference
Values.

Modelled as `CYLI` neck + `CYLI` flange, each nozzle in its **own SUBE** (IR-8),
so a piping designer can attach to one connection without disturbing its
neighbours.

Production constants (`wsb/tank_builder.py`) — RECOMMENDED:

| Feature | Value |
|---------|-------|
| Flange oversize on DN | +120 mm |
| Flange thickness | 40 mm |
| Manway | ~DN600, reachable from grade or a platform |

**Spread the bearings.** Nozzles stacked on one bearing are unusable downstream —
the pipes cannot all be routed. Distribute them around the shell.

---

## Support

**Skirt** — cylindrical shell from the bearing plane to the vessel bottom. Datum
is the skirt base. Used where the vessel is pressurised, elevated, or has a
conical bottom needing clearance.

**Legs** — typically 4, equally spaced. Datum is the base of the legs.

**Ground** — bottom bears directly on the slab. Datum is the bottom of the shell.

---

## Structural detail — RECOMMENDED

| Feature | Value | When |
|---------|-------|------|
| Stiffening ring projection | 120 mm | Tall thin shells, external |
| Stiffening ring depth | 200 mm | — |
| Platform width | 1200 mm | Where drawings show access |
| Platform thickness | 60 mm | — |
| Insulation thickness | 100 mm | Hot service, where modelled |
| Conical roof rise | 0.15 × diameter | No stated head height |
| Dished head rise | 0.25 × diameter | No stated head height |

Dished head rise of D/4 corresponds to a 2:1 elliptical head, the standard
pressure-vessel form. For a `DISH` primitive, `RADIUS ≈ DIAM` approximates it
(IR-9).

Do not add ladders, platforms or accessories that no drawing shows (IR-10).

---

## Special cases

**Double-shell vessels.** Where the equipment list gives an outer and an inner
diameter ("Outside 9.9, inside 6.47"), model both: the inner shell is the process
boundary, the outer is the insulation or containment envelope that clash
detection must see.

**Droplegs.** A barometric leg holds the vacuum seal for a drum washer and must
exceed roughly 10 m — this is a physical requirement (the height of a water
column the atmosphere can support), not a convention. Model as a tall small-bore
standpipe on legs with an offset conical bottom to a seal pot.

---

## Sanity checks before modelling

- π/4 · D² · H ≈ stated volume? A ~10× discrepancy means **height and diameter
  are transposed** in the source data — a defect confirmed twice in JK-Project.
- Height understood as tangent-to-tangent or overall? See
  [README](README.md#know-which-part-each-parameter-describes).
- Does the support type match the bottom type? A conical bottom on ground
  bearing, with no skirt, is usually an error.
