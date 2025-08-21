import os, math, logging
from cutqc.main import CutQC
from helper_functions.benchmarks import generate_circ

if __name__ == "__main__":
    # "supremacy" 
    # "sycamore"
    # "hwea"
    # "bv"
    # "qft"
    # "aqft"
    # "adder"
    # "regular"

    CIRCUIT_TYPE = "bv"
    NUM_QUBITS = 22

    OUT_DIR = f"out/{CIRCUIT_TYPE}"
    os.makedirs(OUT_DIR, exist_ok=True)
    CIRCUIT_NAME = f"{CIRCUIT_TYPE}-{NUM_QUBITS}"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=f"{OUT_DIR}/{CIRCUIT_NAME}.log",
        filemode="w",
    )
    logging.getLogger('PIL').setLevel(logging.ERROR)
    logging.getLogger('matplotlib').setLevel(logging.ERROR)


    circuit = generate_circ(
        num_qubits=NUM_QUBITS,
        depth=2,
        circuit_type=CIRCUIT_TYPE,
        reg_name="q",
        connected_only=True, # Only Connected Circuit Needs Cutting
        seed=None,
    )
    circuit.draw(output='mpl', filename=f'{OUT_DIR}/{CIRCUIT_NAME}.png')

    cutqc = CutQC(
        circuit=circuit,
        cutter_constraints={
            "max_subcircuit_width": 4,
            "max_subcircuit_cuts": 16,
            "subcircuit_size_imbalance": 2,
            "max_cuts": 16,
            "num_subcircuits": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        },
        verbose=True,
    )

    cutqc.cut()
    for idx, subcircuit in enumerate(cutqc.cut_solution['subcircuits']):
        subcircuit.draw(output='mpl', filename=f'{OUT_DIR}/{CIRCUIT_NAME}-{idx}.png')
    
    # breakpoint()
    cutqc.evaluate(num_shots_fn=None)
    cutqc.build(mem_limit=20, recursion_depth=3) # 更快的速度：设置一个较小的 mem_limit。recursion_depth 控制了一个迭代优化的过程，用来弥补由较小 mem_limit 带来的精度损失。
    # cutqc.verify() # 计算完整的量子态作为label很耗时
    logging.info(f"Cut: {cutqc.num_recursions} recursions.")
    logging.info(cutqc.approximation_bins)
