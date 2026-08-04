# Workflow: Equipment Nozzles to Piping

Use this workflow when the user supplies equipment carrying native NOZZLE
elements and asks for the corresponding pipework.

## 1. Inventory before routing

For every equipment item and nozzle, recover:

- owner equipment tag and nozzle mark;
- service and process role;
- nominal bore and connection type;
- catalogue component path;
- flange-face position in world coordinates;
- outward P1 direction;
- whether the connection is already referenced;
- source evidence and any missing value.

Do not infer service from position alone. A high nozzle may be an inlet,
overflow, vent or instrument connection; a low nozzle may be an outlet, drain
or recirculation connection.

## 2. Publish the connection logic

Before generating geometry, produce a connection schedule:

| From | To | Flow direction | DN/spec | Required fittings | Route constraint | Evidence |
|---|---|---|---|---|---|---|

Apply process logic:

- vents leave the highest practical point;
- drains fall toward a valid low point;
- pump suction routes avoid unnecessary high points and excessive fittings;
- reducers follow the stated equipment/pump bore transition;
- slope is used only when required by process or project data;
- nozzle P1 direction controls the initial departure, not a global-axis guess.

Unknown service, destination, specification or flow direction is reported
explicitly. Never connect two nozzles merely because they are close.

## 3. Select syntax by intent

Syntax weighting is evidence-based:

- connectable process route → native `PIPE` / `BRANCH`;
- equipment tie-in → catalogue-backed `NOZZLE`;
- direction change → catalogue `ELBOW` with component-specific P-points;
- bore transition → catalogue `REDUCER` with native-proven local axes;
- unsupported connection/component → isolated experiment before production;
- primitive solids → visual-only representation when no native connectable
  form is justified.

Do not force equal counts. Do not let one familiar syntax replace semantically
different E3D elements.

## 4. Modeling order

1. Confirm the receiving piping ZONE, specification and catalogue paths.
2. Create one PIPE per line/service, not one PIPE for the whole plant.
3. Create BRANCH head/tail geometry from the connection schedule.
4. Depart each nozzle along its outward P1 direction before the first turn.
5. Add required slope, then direction changes, then bore transitions and inline
   items in process order.
6. Create all referenced elements before applying cyclic `HREF` / `TREF` /
   `CREF` relationships in a later pass.
7. Keep unverified reference forms isolated until their E3D trial passes.

## 5. Verification

Check both geometry and database semantics:

- every route is solid, not green dashed/ill-defined;
- pipe legs meet component arrive/leave P-points;
- reducers are coaxial and bores match the branch ends;
- no route doubles back through its equipment or another nozzle;
- slope and flow direction agree;
- queried `HREF`, `TREF`, `CREF`, `SLOREF`, `ADIR`, `LDIR`, `ABORE` and
  `LBORE` match the connection schedule;
- every assumption remains labelled.

The user’s E3D view and queries are authoritative. A locally valid macro is not
reported as fully connected until these properties have been observed.
