"""Built-in magnet grade and soft-magnetic material library (Milestone 2).

Values are representative catalogue figures for engineering use (room
temperature, 20 degC). NdFeB grades follow the standard N-series remanence
bands; the ceramic ferrite entry is a typical hard ferrite (Y30-class). The
soft-iron B-H curve is a representative low-carbon steel used as the default
pole-plate / yoke material.
"""

from __future__ import annotations

import numpy as np

from magnetflux.materials.material import BHCurve, Material, MaterialType

# Representative low-carbon (1010-class) steel B-H curve.
_STEEL_B = np.array(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
)
_STEEL_H = np.array(
    [0.0, 100, 150, 200, 280, 400, 500, 700, 1000, 1600, 3000, 6000, 12000, 30000, 70000],
    dtype=float,
)


def _builtin_materials() -> dict[str, Material]:
    mats: dict[str, Material] = {}

    def add(m: Material) -> None:
        mats[m.id] = m

    add(Material("AIR", "Air", MaterialType.AIR, mu_r=1.0, density=1.2))

    # NdFeB sintered magnets (recoil mu_r ~ 1.05, temp coeff of Br ~ -0.12 %/K).
    add(Material("N35", "NdFeB N35", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.05, remanence_br=1.18, coercivity_hc=868e3,
                 temp_coeff_br=-0.12, density=7500,
                 description="Sintered NdFeB, (BH)max ~ 279 kJ/m^3"))
    add(Material("N42", "NdFeB N42", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.05, remanence_br=1.30, coercivity_hc=955e3,
                 temp_coeff_br=-0.12, density=7500,
                 description="Sintered NdFeB, (BH)max ~ 334 kJ/m^3"))
    add(Material("N52", "NdFeB N52", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.05, remanence_br=1.44, coercivity_hc=923e3,
                 temp_coeff_br=-0.12, density=7500,
                 description="Sintered NdFeB, (BH)max ~ 414 kJ/m^3"))

    # Hard ferrite (ceramic), Y30-class.
    add(Material("FERRITE", "Ceramic Ferrite (Y30)", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.1, remanence_br=0.40, coercivity_hc=240e3,
                 temp_coeff_br=-0.20, density=4900,
                 description="Hard ferrite, low cost, high temp stability"))

    # Soft-magnetic pole/yoke steel with nonlinear B-H.
    add(Material("STEEL_1010", "Low-carbon steel (1010)", MaterialType.SOFT_MAGNETIC,
                 bh_curve=BHCurve(_STEEL_H, _STEEL_B), density=7870,
                 description="Representative soft-iron pole plate / yoke"))

    # Common non-magnetic structural materials.
    add(Material("COPPER", "Copper", MaterialType.NON_MAGNETIC, mu_r=1.0, density=8960))
    add(Material("SS304", "Stainless 304", MaterialType.NON_MAGNETIC, mu_r=1.0, density=8000))

    return mats


#: The immutable built-in material library, keyed by material id.
BUILTIN_MATERIALS: dict[str, Material] = _builtin_materials()

#: Convenience list of the magnet grades required by the spec.
MAGNET_GRADES = ["N35", "N42", "N52", "FERRITE"]
