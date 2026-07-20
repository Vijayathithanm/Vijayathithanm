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
    # Representative catalogue Br [T] and max operating temperature [degC].
    ndfeb = [
        ("N35", 1.18, 868e3, 80), ("N38", 1.23, 899e3, 80),
        ("N40", 1.27, 923e3, 80), ("N42", 1.30, 955e3, 80),
        ("N45", 1.35, 963e3, 80), ("N48", 1.40, 995e3, 80),
        ("N50", 1.42, 907e3, 60), ("N52", 1.44, 923e3, 60),
    ]
    for gid, br, hc, tmax in ndfeb:
        add(Material(gid, f"NdFeB {gid}", MaterialType.PERMANENT_MAGNET,
                     mu_r=1.05, remanence_br=br, coercivity_hc=hc,
                     temp_coeff_br=-0.12, density=7500,
                     max_operating_temp=tmax, curie_temp=310,
                     description="Sintered NdFeB"))

    # Hard ferrite (ceramic).
    add(Material("FERRITE_Y30", "Ceramic Ferrite Y30", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.1, remanence_br=0.40, coercivity_hc=240e3,
                 temp_coeff_br=-0.20, density=4900, max_operating_temp=250,
                 curie_temp=450, description="Hard ferrite, low cost"))
    add(Material("FERRITE_Y35", "Ceramic Ferrite Y35", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.1, remanence_br=0.44, coercivity_hc=265e3,
                 temp_coeff_br=-0.20, density=4900, max_operating_temp=250,
                 curie_temp=450, description="Hard ferrite, higher Br"))

    # Samarium-cobalt: high temperature stability, low temp coefficient.
    add(Material("SMCO_28", "SmCo 2:17 (Sm2Co17-28)", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.05, remanence_br=1.05, coercivity_hc=760e3,
                 temp_coeff_br=-0.035, density=8300, max_operating_temp=300,
                 curie_temp=800, description="SmCo, high-temp, corrosion-resistant"))
    add(Material("SMCO_32", "SmCo 2:17 (Sm2Co17-32)", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.05, remanence_br=1.13, coercivity_hc=780e3,
                 temp_coeff_br=-0.035, density=8300, max_operating_temp=300,
                 curie_temp=800, description="SmCo, high-temp grade"))

    # Alnico: very high Curie temperature, low coercivity.
    add(Material("ALNICO_5", "Alnico 5", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.9, remanence_br=1.25, coercivity_hc=51e3,
                 temp_coeff_br=-0.02, density=7300, max_operating_temp=525,
                 curie_temp=860, description="Alnico, high temp, low Hc"))
    add(Material("ALNICO_8", "Alnico 8", MaterialType.PERMANENT_MAGNET,
                 mu_r=1.7, remanence_br=0.82, coercivity_hc=131e3,
                 temp_coeff_br=-0.02, density=7300, max_operating_temp=525,
                 curie_temp=860, description="Alnico, higher Hc"))

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

#: Convenience list of the built-in permanent-magnet grades.
MAGNET_GRADES = [
    "N35", "N38", "N40", "N42", "N45", "N48", "N50", "N52",
    "FERRITE_Y30", "FERRITE_Y35", "SMCO_28", "SMCO_32", "ALNICO_5", "ALNICO_8",
]
