from qiskit_algorithms import Grover
from qiskit.primitives import Sampler
from qiskit.quantum_info import Statevector
from qiskit_algorithms import AmplificationProblem
import matplotlib.pyplot as plt
import time, random, json

def construct_bitstring(n):
    # Construct a random bitstring for specifying a good state
    bitstring = ""
    for _ in range(n + 1):
        bitstring += str(random.randint(0, 1))
    return bitstring

def plot_runtime(runtimeData):
    x, y = list(runtimeData.keys()), list(runtimeData.values())

    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel('Bitstring length')
    plt.ylabel('Time (s)')
    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.title('Grover\'s algorithm runtime trend')
    plt.grid(True)

    plt.show()

def plot_runtime_increase(runtimeIncreaseData):
    x, y = list(runtimeIncreaseData.keys()), list(runtimeIncreaseData.values())

    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel('Bitstring length')
    plt.ylabel('Percentage increase in runtime over last (%)')
    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.title('Grover\'s algorithm runtime increase trend')
    plt.grid(True)

    plt.show()

def test_grover_runtime():

  runtimeData = {}
  runtimeIncreaseData = {}

  for i in range(2, 11):
    print(i)
    good_state = construct_bitstring(i)

    oracle = Statevector.from_label(good_state)
    problem = AmplificationProblem(oracle, is_good_state=[good_state])
    grover = Grover(sampler=Sampler())

    # Measure the time taken to complete Grover's algorithm
    start_time = time.perf_counter()
    result = grover.amplify(problem)
    end_time = time.perf_counter()

    # Exit out of this experiment if the measurement was not as expected
    if result.top_measurement != good_state:
      print("Something went wrong")
      break

    runtimeData[i] = end_time - start_time
    
    # Store the percentage increase in runtime over the previous bitstring length rounded to 2 decimal places
    if i > 2:
        runtimeIncreaseData[i] = round((runtimeData[i] - runtimeData[i - 1]) / runtimeData[i - 1] * 100, 2)

  # Write the runtime data to a JSON file
  with open('./grover_runtime_analysis/runtime_data.json', 'w') as f:
    json.dump(runtimeData, f, indent=3)

  # Write the runtime increase data to a JSON file
  with open('./grover_runtime_analysis/runtime_increase_data.json', 'w') as f:
    json.dump(runtimeIncreaseData, f, indent=3)

  # Plot the trends
  plot_runtime(runtimeData)
  plot_runtime_increase(runtimeIncreaseData)

test_grover_runtime()