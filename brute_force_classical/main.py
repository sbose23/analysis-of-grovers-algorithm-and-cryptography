from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time, json
import matplotlib.pyplot as plt

def plot_runtime(runtimeData):
    x, y = list(runtimeData.keys()), list(runtimeData.values())

    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel('Key space size (bits)')
    plt.ylabel('Time (s)')
    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.title('Brute-force AES key search runtime growth')
    plt.grid(True)

    plt.show()

def plot_runtime_increase(runtimeIncreaseData):
    x, y = list(runtimeIncreaseData.keys()), list(runtimeIncreaseData.values())

    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel('Key space size (bits)')
    plt.ylabel('Percentage increase in runtime over last (%)')
    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.title('Brute-force AES key search runtime increase trend')
    plt.grid(True)

    plt.show()


# Generate a 16 byte key
def generate_key(i, key_bits):
    # Using i, and integer, generate a key that is padded based on the size of this integer
    byte_length = (key_bits + 7) // 8 
    key_bytes = i.to_bytes(byte_length, 'big') 
    return key_bytes.ljust(16, b'\x00')  # Pad to 16 bytes (AES Standard Key Size)

def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, AES.block_size))

def decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        return unpad(cipher.decrypt(ciphertext), AES.block_size)
    except ValueError:
        return None  # Incorrect padding means wrong key

def test_brute_force_key_search(plaintext):

    runtimeData = {}
    runtimeIncreaseData = {}

    for key_space_size in range(2, 25):
        key_space = 2 ** key_space_size
        random_key = key_space // 2 # Pick the median for consistency
        true_key = generate_key(random_key, key_space_size)
        ciphertext = encrypt(plaintext, true_key)
        
        start_time = time.time()
        for i in range(key_space):
            test_key = generate_key(i, key_space_size)
            decrypted = decrypt(ciphertext, test_key)
            if decrypted == plaintext:
                print(f"Key found at {i} for key space 2^{key_space_size}")
                break
        end_time = time.time()
        runtimeData[key_space_size] = end_time - start_time
        # Store the percentage increase in runtime over the previous bitstring length rounded to 2 decimal places
        if key_space_size > 2:
            runtimeIncreaseData[key_space_size] = round((runtimeData[key_space_size] - runtimeData[key_space_size - 1]) / runtimeData[key_space_size - 1] * 100, 2)

    # Write the runtime data to a JSON file
    with open('./brute_force_classical/runtime_data.json', 'w') as f:
        json.dump(runtimeData, f, indent=3)

    # Write the runtime increase data to a JSON file
    with open('./brute_force_classical/runtime_increase_data.json', 'w') as f:
        json.dump(runtimeIncreaseData, f, indent=3)
        
        plot_runtime(runtimeData)
    plot_runtime_increase(runtimeIncreaseData)

plaintext = b"Secret Message"
test_brute_force_key_search(plaintext)
