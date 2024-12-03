import trimesh
import numpy as np

# Step 1: Create a simple cube mesh
mesh = trimesh.primitives.Box(extents=(1, 1, 1))

# Save the valid STL file
valid_stl_path = "valid_cube.stl"
mesh.export(valid_stl_path)
print(f"Valid STL saved as {valid_stl_path}.")

# Step 2: Corrupt the STL file
corrupted_stl_path = "corrupted_cube.stl"

# Read the valid STL file into a binary array
with open(valid_stl_path, "rb") as file:
    stl_data = bytearray(file.read())

# Introduce corruption by removing random bytes
corrupt_percentage = 0.01  # Remove 1% of the bytes
num_bytes_to_remove = int(len(stl_data) * corrupt_percentage)

for _ in range(num_bytes_to_remove):
    random_index = np.random.randint(0, len(stl_data))
    stl_data[random_index] = np.random.randint(0, 256)  # Randomize byte

# Save the corrupted STL file
with open(corrupted_stl_path, "wb") as file:
    file.write(stl_data)

print(f"Corrupted STL saved as {corrupted_stl_path}.")
