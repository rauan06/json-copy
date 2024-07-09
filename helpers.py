import ctypes
import subprocess

run_command = ['./hello']
run_result = subprocess.run(run_command, capture_output=True, text=True)
    
# Print the output of the C program
print("Program output: " + run_result.stdout)


# Load the shared library
# Use 'mylib.dll' on Windows
mylib = ctypes.CDLL('./mylib.so')

# Define the argument and return types of the add function
mylib.add.argtypes = [ctypes.c_int, ctypes.c_int]
mylib.add.restype = ctypes.c_int

# Call the add function
result = mylib.add(1000000, 3)
print(f"Result of add(1000000, 3): {result}")
