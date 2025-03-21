import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import numpy as np
from jaxfluids import InputManager, InitializationManager, SimulationManager
from jaxfluids_postprocess import load_data, create_2D_animation, create_2D_figure

# SETUP SIMULATION
input_manager = InputManager("cylinder_flow.json", "numerical_setup.json")
initialization_manager = InitializationManager(input_manager)
sim_manager = SimulationManager(input_manager)

# RUN SIMULATION
jxf_buffers = initialization_manager.initialization()
sim_manager.simulate(jxf_buffers)

# LOAD DATA
path = sim_manager.output_writer.save_path_domain
quantities = ["velocity", "density", "pressure", "vorticity", "levelset"]
jxf_data = load_data(path, quantities)

cell_centers = jxf_data.cell_centers
data = jxf_data.data
times = jxf_data.times

# PLOT
nrows_ncols = (1,1)
levelset = data["levelset"]
vorticity = data["vorticity"][:,2]
mask = levelset < 0
vorticity = np.ma.masked_where(mask, vorticity)


plot_dict = {"vorticity": vorticity}

# CREATE ANIMATION
create_2D_animation(
    plot_dict, 
    cell_centers,
    times,
    nrows_ncols=nrows_ncols, 
    plane="xy", 
    interval=200,
    dpi=200)

# CREATE FIGURE
create_2D_figure(
    plot_dict, 
    nrows_ncols, 
    cell_centers=cell_centers,
    plane="xy", plane_value=0.0, 
    save_fig="cylinder_flow.png")