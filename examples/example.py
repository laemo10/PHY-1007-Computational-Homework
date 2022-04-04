import env_examples  # Modifies path, DO NOT REMOVE

from src import Circuit, Current, Wire, World, fields



if __name__ == "__main__":
    world = World(shape=(101, 101))

    A = Wire((25,25),(50,25),(1,0,0),-10)
    B = Wire((50,25), (75,25),(1,0,0),10)
    C = Wire((75,25), (75,75),(0,1,0), 10)
    D = Wire((75,75), (50,75),(-1,0,0), 10)
    E = Wire((50,75), (25,75),(-1,0,0), -10)
    F = Wire((25,75), (25,25),(0,-1,0), -10)

    A1 = Wire((15,0),(25,0),(1,0,0),10)
    B1 = Wire((25,0), (25,15),(0,1,0),10)
    C1 = Wire((25,15), (60,15),(1,0,0), 10)
    D1 = Wire((60,15), (60,25),(0,1,0), 10)
    E1 = Wire((25,25), (60,25),(-1,0,0), 10)
    F1 = Wire((25,25), (25,40),(0,1,0), 10)
    G1 = Wire((15,40), (25,40),(-1,0,0), 10)
    H1 = Wire((15,25), (15,40),(0,-1,0), 10)
    I1 = Wire((0,25), (15,25),(-1,0,0), 10)
    J1 = Wire((0,25), (0,15),(0,-1,0), 10)
    K1 = Wire((0,15), (15,15),(1,0,0), 10)
    L1 = Wire((15,0), (15,15),(0,-1,0), 10)

    wires = [
        # TODO : Add wires here
        #A,B,C,D, E, F,
        A1, B1, C1, D1, E1, F1, G1, H1, I1, J1, K1, L1
    ]

    circuit = Circuit(wires=wires)

    world.place(circuit)

    world.compute(100)

    #world.show_all()

    world.show_potential()
    #world.show_wires_voltage()
    