from typing import List, Tuple, Union

import numpy as np
from scipy.constants import mu_0

from src.biot_savart_equation_solver import BiotSavartEquationSolver
from src.circuit import Circuit
from src.fields import ScalarField, VectorField
from src.laplace_equation_solver import LaplaceEquationSolver
from src.wire import Wire


class World:
    """
    A 2D world. We can place wires or electric circuits in the world and observe the resulting electromagnetic fields.
    """

    class EmptyWorldException(Exception):
        pass

    def __init__(self, shape: Tuple[int, int]):
        """
        Creates an empty voltage scalar field (self._wires_voltage) and an empty electric current vector field
        (self._wires_current) the size of the world. Also initializes the lists of wires and circuits contained in the
        world to empty lists.

        Parameters
        ----------
        shape : Tuple[int, int]
            Two-dimensional tuple defining the size (x, y) of the world.

        Attributes
        ----------
        self.wires : List[Wire]
            List of the wires in the world.
        self.circuits : List[Circuit]
            List of the circuits in the world.
        self._wires_voltage : ScalarField
            A scalar field V : ℝ² → ℝ ; (x, y) → V(x, y), where V(x, y) is the wires' voltage at a given point (x, y)
            in space.
        self._wires_current : VectorField
            A vector field I : ℝ² → ℝ³ ; (x, y) → (I_x(x, y), I_y(x, y), I_z(x, y)), where I_x(x, y), I_y(x, y) and
            I_z(x, y) are the 3 components of the wire current vector at a given point (x, y) in space. Note that
            I_z = 0 is always True in our 2D world.
        self._magnetic_field : VectorField
            A vector field B : ℝ² → ℝ³ ; (x, y) → (B_x(x, y), B_y(x, y), B_z(x, y)), where B_x(x, y), B_y(x, y) and
            B_z(x, y) are the 3 components of the magnetic vector at a given point (x, y) in space. Note that
            B_x = B_y = 0 is always True in our 2D world.
        self._potential : ScalarField
            A scalar field P : ℝ² → ℝ ; (x, y) → P(x, y), where P(x, y) is the electric potential at a given point
            (x, y) in space. The difference between P and V is that P gives the potential in the whole world, i.e in
            the wires and in the empty space between the wires, while the field V always gives V(x, y) = 0 if (x, y)
            is not a point belonging to an electric wire.
        self._electric_field : VectorField
            A vector field E : ℝ² → ℝ² ; (x, y) → (E_x(x, y), E_y(x, y)), where E_x(x, y) and E_y(x, y) are the 2
            components of the electric vector at a given point (x, y) in space. Note that the E_z component is missing
            because it is not possible to compute the gradient of the potential in the z axis in a 2D world.
        self._energy_flux : VectorField
            A vector field EF : ℝ² → ℝ³ ; (x, y) → (EF_x(x, y), EF_y(x, y), EF_z(x, y)), where EF_x(x, y), EF_y(x, y)
            and EF_z(x, y) are the 3 components of the energy flux vector at a given point (x, y) in space. Note that
            EF_z = 0 is always True in our 2D world.
        """
        if not isinstance(shape, tuple):
            raise ValueError(f"The world's shape should be a tuple. Received a {type(shape)}.")
        if len(shape) != 2:
            raise ValueError(f"The length of the world's shape should be 2. The given shape has length {len(shape)}.")

        self.wires: List[Wire] = []
        self.circuits: List[Circuit] = []

        self._wires_voltage = ScalarField(np.zeros(shape))
        self._wires_current = VectorField(np.zeros((shape[0], shape[1], 3)))
        self._magnetic_field = None
        self._potential = None
        self._electric_field = None
        self._energy_flux = None

    def _place_wire(self, wire: Wire):
        """
        Place a wire in the world and change the voltage and current fields accordingly.

        Parameters
        ----------
        wire : Wire
            A wire.
        """
        self._wires_current[wire.position] = wire.current
        self._wires_voltage[wire.position] = wire.voltage

        self.wires.append(wire)

    def _place_circuit(self, circuit: Circuit):
        """
        Place a circuit in the world and change the voltage and current fields accordingly.

        Parameters
        ----------
        circuit : Circuit
            A circuit.
        """
        for wire in circuit.wires:
            self._place_wire(wire)

        self.circuits.append(circuit)

    def place(self, an_object: Union[Circuit, Wire]):
        """
        Place an object in the world and change the voltage and current fields accordingly.

        Parameters
        ----------
        an_object : Union[Circuit, Wire]
            An object.
        """

        if isinstance(an_object, Wire):
            self._place_wire(an_object)
        elif isinstance(an_object, Circuit):
            self._place_circuit(an_object)

    def compute(self, nb_relaxation_iterations: int = 1000):
        """
        Calculates all the fields present in the world using the voltage and current fields produced by the wires in the
        circuits. The known fields are the voltage (self._wires_voltage) and current (self._wires_current) fields. The
        fields we need to compute are the potential (self._potential), the electric field (self._electric_field), the
        magnetic field (self._magnetic_field) and the energy flux (self._energy_flux).

        Parameters
        ----------
        nb_relaxation_iterations : int
            Number of iterations performed to obtain the potential by the relaxation method (default = 1000)
        """

        nb = LaplaceEquationSolver(nb_relaxation_iterations)
        self._potential = ScalarField(nb.solve(self._wires_voltage))

        if not self.wires:
            raise ValueError("Place at least one wire before computing the circuits' fields.")
        else:
            return self._potential

    def show_wires_voltage(self):
        """
        Shows wires' voltage field.
        """
        if self.wires:
            self._wires_voltage.show(title="Initial voltage")
        else:
            raise self.EmptyWorldException

    def show_potential(self):
        """
        Shows the electric potential.
        """
        if self.wires:
            self._potential.show(title="Potential")
        else:
            raise self.EmptyWorldException

    def show_electric_field(self, hide_wires: bool = True):
        """
        Shows the electric field.

        Parameters
        ----------
        hide_wires : bool
            Hide the electric field near the wires to produce a clearer stream plot.
        """
        if self.wires:
            if hide_wires:
                electric_field = VectorField(self._electric_field)

                for x, y in zip(np.nonzero(self._wires_voltage)[0], np.nonzero(self._wires_voltage)[1]):
                    electric_field[x, y] = np.array([np.nan, np.nan])
            else:
                electric_field = self._electric_field

            electric_field.show(title="Electric field")
        else:
            raise self.EmptyWorldException

    def show_magnetic_field(self):
        """
        Shows the z-component of the magnetic field.
        """
        if self.wires:
            self._magnetic_field.z.show(title="Magnetic field (z component)")
        else:
            raise self.EmptyWorldException

    def show_energy_flux(self):
        """
        Shows the energy flux.
        """
        if self.wires:
            self._energy_flux.show(title="Energy flux")
        else:
            raise self.EmptyWorldException

    def show_all(self):
        """
        Shows all fields.
        """
        if self.wires:
            self.show_wires_voltage()
            self.show_potential()
            self.show_electric_field()
            self.show_magnetic_field()
            self.show_energy_flux()
        else:
            raise self.EmptyWorldException
