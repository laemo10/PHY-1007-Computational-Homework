import env_examples  # Modifies path, DO NOT REMOVE

from src import Circuit, Current, Wire, World, fields



if __name__ == "__main__":
    world = World(shape=(51, 51))

    A = Wire((0,0),(20,0),(1,0,0),10)
    B = Wire((20,0), (20,20),(0,1,0),10)
    C = Wire((20,20), (0,20),(-1,0,0), 10)
    D = Wire((0,20), (0,0),(0,-1,0), 10)

    wires = [
        # TODO : Add wires here
        A,B,C,D
    ]

    circuit = Circuit(wires=wires)

    world.place(circuit)

    world.compute()

    #world.show_all()

    world.show_potential()
    #world.show_wires_voltage()
    