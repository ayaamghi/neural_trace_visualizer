# create_zarr.py
import numpy as np
import zarr
import os
import shutil
import time

# --- 1. Configuration ---
NUM_TIMESTEPS = 7879
NUM_NEURONS = 71721
ZARR_OUTPUT_DIR = 'synthetic_traces.zarr'
output_path = os.path.join('data', ZARR_OUTPUT_DIR)

# --- 2. Create the Data ---
print("Allocating NumPy array...")
sample_data = np.random.randn(NUM_TIMESTEPS, NUM_NEURONS).astype('float32')
sample_data[1000:1500, 5000] += 5
print("NumPy array created.")

# --- 3. Save to Zarr as a Group ---
if os.path.exists(output_path):
    print(f"Removing existing directory at '{output_path}'...")
    shutil.rmtree(output_path)

print(f"Saving new Zarr store as a group at '{output_path}'...")

# Create the root group first. This makes the .zgroup file.
root_group = zarr.group(store=output_path, overwrite=True)

# Now, create your data array INSIDE that group.
# We'll name the array 'traces'.
traces_array = root_group.create_dataset(
    'traces',
    shape=sample_data.shape,
    chunks=(32, 16384),
    dtype=sample_data.dtype
)
traces_array[:] = sample_data

print("Zarr group and dataset saved.")

# --- 4. Verify ---
print("\nVerifying the saved group...")
reopened_group = zarr.open(output_path, mode='r')
print("✅ Group and array created successfully!")
print(f"  - Contents: {list(reopened_group.keys())}")
print(f"  - Array Shape: {reopened_group['traces'].shape}")
print(f"  - Array Chunks: {reopened_group['traces'].chunks}")