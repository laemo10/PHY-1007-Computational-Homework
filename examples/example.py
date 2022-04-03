import env_examples  # Modifies path, DO NOT REMOVE

from src import Circuit, Current, Wire, World, fields



if __name__ == "__main__":
    world = World(shape=(51, 51))

    A = Wire((14,14),(34,14),(1,0,0),10)
    B = Wire((34,14), (34,34),(0,1,0),10)
    C = Wire((34,34), (14,34),(-1,0,0), 10)
    D = Wire((14,34), (14,14),(0,-1,0), 10)

    wires = [
        # TODO : Add wires here
        A,B,C,D
    ]

    circuit = Circuit(wires=wires)

    world.place(circuit)

    #world.compute(100)

    #world.show_all()

    #world.show_potential()
    world.show_wires_voltage()
    