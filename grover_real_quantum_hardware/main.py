# Credit: IBM Quantum Learning: https://learning.quantum.ibm.com/tutorial/grovers-algorithm
# With slight modifications, I am using the same code to simulate the Grover's algorithm
# Set the IBM Quantum API key as an environment variable in the directory in which this script is run in a .env file
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("IBM_QUANTUM_API_TOKEN")

import matplotlib.pyplot as plt

def plot_results(results):
    x, y = list(results.keys()), list(results.values())

    plt.bar(x, y, color='blue')
    plt.xlabel('Bitstring')
    plt.ylabel('Quasi-probability')
    plt.title('Grover\'s algorithm results')
    plt.show()

import json
def save_results(results):
    with open("./grover_real_quantum_hardware/results.json", "w") as f:
        json.dump(results, f, indent=4)

# Import necessary libraries
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler


# Set the IBM Quantum service
service = QiskitRuntimeService(channel="ibm_quantum", token=API_KEY)
backend = service.backend("ibm_kyiv")

def grover_oracle(marked_states):
    """Build a Grover oracle for multiple marked states

    Here we assume all input marked states have the same number of bits

    Parameters:
        marked_states (str or list): Marked states of oracle

    Returns:
        QuantumCircuit: Quantum circuit representing Grover oracle
    """
    if not isinstance(marked_states, list):
        marked_states = [marked_states]
    # Compute the number of qubits in circuit
    num_qubits = len(marked_states[0])

    qc = QuantumCircuit(num_qubits)
    # Mark each target state in the input list
    for target in marked_states:
        # Flip target bit-string to match Qiskit bit-ordering
        rev_target = target[::-1]
        # Find the indices of all the '0' elements in bit-string
        zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
        # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)
        # where the target bit-string has a '0' entry
        qc.x(zero_inds)
        qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
        qc.x(zero_inds)
    return qc

def execute_grover_algorithm(marked_states):

    oracle = grover_oracle(marked_states)

    # The GroverOperator takes an oracle circuit and returns a circuit that implements the Grover circuit itself with the oracle
    grover_op = GroverOperator(oracle)

    optimal_num_iterations = math.floor(
        math.pi / (4 * math.asin(math.sqrt(len(marked_states) / 2**grover_op.num_qubits)))
    )

    qc = QuantumCircuit(grover_op.num_qubits)
    # Create even superposition of all basis states
    qc.h(range(grover_op.num_qubits))
    # Apply Grover operator the optimal number of times
    qc.compose(grover_op.power(optimal_num_iterations), inplace=True)
    # Measure all qubits
    qc.measure_all()

    # Optimizing problem for quantum execution
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    target = backend.target
    pm = generate_preset_pass_manager(target=target, optimization_level=3)
    circuit_isa = pm.run(qc)


    # Execute the circuit on the quantum backend
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = 10_000
    result = sampler.run([circuit_isa]).result()
    dist = result[0].data.meas.get_counts()
    
    save_results(dist)
    plot_results(dist)

BITSTRING_2_QUBITS = "01" # Qiskit runtime: 4s *Produces good result.
BITSTRING_3_QUBITS = "001" # Qiskit runtime: 4s *Produces good result.
BITSTRING_4_QUBITS = "0101" # Qiskit runtime: 5s
BITSTRING_6_QUBITS = "010011" # Qiskit runtime: 16s
BITSTRING_8_QUBITS = "00101101" # Qiskit runtime: 74s
BITSTRING_10_QUBITS = "0010110101" # Qiskit runtime: 273s

execute_grover_algorithm([BITSTRING_2_QUBITS])