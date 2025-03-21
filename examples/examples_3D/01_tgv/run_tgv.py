import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import matplotlib.pyplot as plt
import numpy as np

from jaxfluids import InputManager, InitializationManager, SimulationManager
from jaxfluids_postprocess import load_data, create_2D_animation

# SETUP SIMULATION
input_manager = InputManager("tgv.json", "numerical_setup.json")
initialization_manager = InitializationManager(input_manager)
sim_manager = SimulationManager(input_manager)

# RUN SIMULATION
jxf_buffers = initialization_manager.initialization()
sim_manager.simulate(jxf_buffers)

# LOAD DATA
path = sim_manager.output_writer.save_path_domain
quantities = ["velocity"]
jxf_data = load_data(path, quantities)

cell_centers = jxf_data.cell_centers
data = jxf_data.data
times = jxf_data.times

plot_dict = {
    "u": data["velocity"][:,0],
    "v": data["velocity"][:,1],
    "w": data["velocity"][:,2],
}

# PLOT
nrows_ncols = (1,3)
os.makedirs("images", exist_ok=True)
create_2D_animation(plot_dict, cell_centers, times, nrows_ncols=nrows_ncols, plane="xy",
                    plane_value=np.pi/4, interval=100,
                    save_png="images", fig_args={"figsize": (10,3)}, dpi=100)

data_ref = np.loadtxt("tgv_reference_data.txt")
TKE = 0.5 * np.mean(np.sum(data["velocity"]**2, axis=1), axis=(-1,-2,-3))

fig, ax = plt.subplots()
ax.plot(times[:-1], -(TKE[1:]-TKE[:-1])/(times[1:]-times[:-1]), label="present")
ax.plot(data_ref[:,0], data_ref[:,1], marker='o', color="k", linestyle="none", label="Brachet 1991")
ax.set_xlabel("time")
ax.set_ylabel("rate of energy dissipation")
ax.legend()
fig.savefig("energy_dissipation.png", bbox_inches="tight", dpi=200)
plt.show()
plt.close()