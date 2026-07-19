# MagnetFlux Studio — User Guide

MagnetFlux Studio predicts the magnetic field and sputter-erosion "race track"
of permanent-magnet magnetron cathodes.

## Typical workflow

1. **Import geometry** — *File ▸ Import CAD…* (STEP, IGES or STL). Each solid
   appears in the **Model Tree**. Geometry is scaled to metres on import
   (CAD files are assumed to be in millimetres).

2. **Assign materials** — select a body in the Model Tree and use the
   **Properties** panel to pick a material:
   - Permanent magnets: NdFeB **N35 / N42 / N52** or **ceramic ferrite**.
   - Soft-magnetic pole plates / yokes: **low-carbon steel** (nonlinear B‑H).
   For magnets, set the **magnetisation** mode (uniform, axial, radial or
   diametric) and the operating **temperature** (applies the Br(T) correction).

3. **Solve the field** — *Solve ▸ Solve Field*. The solver builds an air domain,
   assembles the magnetostatic problem (analytic charge model, or the
   scikit-fem vector-potential FEM backend) and computes **B** on a grid.

4. **Visualise** — choose a field quantity (|B|, Bx/By/Bz, |H|, energy) in the
   toolbar, then *Display ▸ Slice / Contours / Vector Glyphs / Streamlines*.
   Export with *Display ▸ Export PNG / CSV / VTK*.

5. **Predict the race track** — *Analyze ▸ Predict Race Track…* computes the
   erosion-intensity heatmap on a target plane above the magnets. The bright
   closed loop is the predicted groove; the cyan contour marks where the field
   is parallel to the target (B_n = 0).

6. **Report** — *Analyze ▸ PDF Report…* writes a one-page summary with the
   heatmap and key metrics (peak |B_t|, uniformity, eroded-area fraction).

## Optimisation

For parametric planar-magnetron layouts (central magnet + outer ring), the
optimizer searches for the **ring spacing** and **magnet count** that maximise
the target-utilisation estimate (a wide, uniform race track). See
`magnetflux.optimization` — `optimize_spacing` and `optimize_pole_arrangement`.

## Field quantities & units

All results are SI internally (metres, tesla, A/m). The UI displays lengths in
millimetres and flux density in millitesla.

## Projects

*File ▸ Save Project* writes a versioned `.mfx` archive containing the geometry,
material assignments and settings; *Open Project* restores them.
