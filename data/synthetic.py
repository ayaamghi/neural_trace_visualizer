# create_zarr.py
import numpy as np
import zarr
import os
import shutil
import time

# --- Instructions ---
# Run this script from inside the 'data' directory to create the
# 'synthetic_traces.zarr' store in the correct location.
#
# Correct usage:
# cd data
# python create_zarr.py
# --------------------


# --- 1. Configuration ---
NUM_TIMESTEPS = 7879
NUM_NEURONS = 71721
ZARR_OUTPUT_DIR = 'synthetic_traces.zarr'
# The output path is now relative to where the script is run.
output_path = ZARR_OUTPUT_DIR


# --- 2. Create the Data ---
# WARNING: This will create a large array in memory (~2.3 GB).
print(f"Allocating a NumPy array with shape ({NUM_TIMESTEPS}, {NUM_NEURONS})...")
print("This may take a moment and require significant RAM.")

start_time = time.time()
sample_data = np.random.randn(NUM_TIMESTEPS, NUM_NEURONS).astype('float32')
# Add a sample "spike" to a neuron for interest
sample_data[1000:1500, 5000] += 5
print(f"NumPy array created in {time.time() - start_time:.2f} seconds.")


# --- 3. Save to Zarr with Matching Properties ---
if os.path.exists(output_path):
    print(f"Removing existing directory at '{output_path}'...")
    shutil.rmtree(output_path)

print(f"Saving new Zarr store with matching chunks at '{output_path}'...")
start_time = time.time()

# Use zarr.open() in write mode ('w') to specify all properties
z = zarr.open(
    output_path,
    mode='w',
    shape=sample_data.shape,
    dtype=sample_data.dtype,
    chunks=(32, 16384),  # <-- Match the original chunk size
    compressor=None,     # <-- Match the original (no compression)
    zarr_version=2       # <-- Match the original format version
)
# Write the NumPy data to the newly configured Zarr array
z[:] = sample_data

print(f"Zarr store saved in {time.time() - start_time:.2f} seconds.")


# --- 4. Verify ---
print("\nVerifying the saved array...")
reopened_array = zarr.open(output_path, mode='r')

print(f"✅ Array successfully created and verified!")
print(f"  - Shape: {reopened_array.shape}")
print(f"  - Data Type: {reopened_array.dtype}")
print(f"  - Chunks: {reopened_array.chunks}") # This will now show (32, 16384)

