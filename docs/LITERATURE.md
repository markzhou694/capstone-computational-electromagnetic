# Literature map

The four references below come from the supplied proposal, in its order.
They cover different parts of the project; none alone supplies a complete,
validated implementation of the proposed pipeline. Access checked 2026-11-04.

1. **A. Becker and V. Hansen (2003).** “A hybrid method combining the FDTD
   and a time domain boundary-integral equation marching-on-in-time
   algorithm.” *Advances in Radio Science*, **1**, 99–104.
   [DOI and publisher article](https://doi.org/10.5194/ars-1-99-2003).
   Most directly relevant to the coupling extension: the abstract describes
   equivalent electric/magnetic currents and transfer with a Yee/FIT region.
   **Checked:** publisher metadata and abstract. Full PDF retrieval timed
   out during setup; the detailed discretization and stability assumptions
   have not yet been audited. Read those before implementing a coupling.

2. **J.-P. Berenger (1994).** “A perfectly matched layer for the absorption
   of electromagnetic waves.” *Journal of Computational Physics*, **114**(2),
   185–200. [DOI](https://doi.org/10.1006/jcph.1994.1159).
   Establishes the PML background for artificial boundaries. **Checked:**
   publisher-indexed bibliographic metadata/abstract; direct full text was
   unavailable. This reference is about PML; it does not by itself document
   the particular convolutional PML recurrence in the unpublished local prototype.

3. **M. W. Scroggs, T. Betcke, E. Burman, W. Śmigaj, and E. van 't Wout
   (2017).** “Software frameworks for integral equations in electromagnetic
   scattering based on Calderón identities.” *Computers & Mathematics with
   Applications*, **74**, 2897–2914.
   [DOI](https://doi.org/10.1016/j.camwa.2017.07.049) ·
   [Author-hosted paper](https://www.mscroggs.co.uk/papers/2017-softwareframeworks.pdf).
   Useful for Maxwell trace spaces, boundary operators, and the existing
   harmonic BEM study. **Checked:** title, authors, journal details, and
   introductory formulation in the paper. This is time-harmonic work; do not
   cite it as proof that a retarded time-domain scheme is stable.

4. **K. S. Yee (1966).** “Numerical solution of initial boundary value
   problems involving Maxwell's equations in isotropic media.” *IEEE
   Transactions on Antennas and Propagation*, **14**(3), 302–307.
   [DOI / IEEE record](https://doi.org/10.1109/TAP.1966.1138693).
   Foundational reference for the staggered FDTD scheme. Bibliography agrees
   with the supplied proposal and existing README. **Access limit:** IEEE
   returned a JavaScript verification page; full-text verification was not
   completed in this setup.

## Implementation-specific supplement

**J. A. Roden and S. D. Gedney (2000).** “Convolution PML (CPML): An efficient
FDTD implementation of the CFS-PML for arbitrary media.” *Microwave and
Optical Technology Letters*, **27**(5), 334–339.
[Publisher link](https://onlinelibrary.wiley.com/doi/abs/10.1002/1098-2760%2820001205%2927%3A5%3C334%3A%3AAID-MOP14%3E3.0.CO%3B2-A).
Carried forward from the earlier local prototype README as the CPML-specific reference;
full text has not been independently reviewed in this setup.

For each implementation, add a short note with the equation/page actually
used, conventions translated into code, assumptions, and validation case.
Keep “available”, “read”, and “implemented and tested” distinct. Link papers
rather than uploading publisher PDFs without checking redistribution rights.
