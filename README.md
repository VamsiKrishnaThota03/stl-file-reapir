# STL Mesh Repair Tool

This tool helps repair STL mesh files by detecting and filling holes (open edges) in the mesh. It uses the `trimesh` library to load, manipulate, and repair the STL files. The program also provides a visualization of the mesh with highlighted open edges and repaired faces.

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `trimesh`
  - `numpy`
  - `matplotlib`
  - `tkinter` (for file dialog)

### Install the required libraries

You can install the required libraries by running the following commands:

```bash
pip install trimesh numpy matplotlib


How to Run the Program
1. Clone or Download the Code
Clone the repository or download the stl_repair.py file to your local machine.
git clone <repository_url>


2. Run the Program
Open a terminal or command prompt and navigate to the directory where the stl_repair.py file is located. Then, run the program using the following command:
python stl_repair.py


3. Select the STL File
After running the script, a file dialog will appear. Select the STL file you want to repair. Ensure that the file is in the correct format (.stl).

4. View the Repair Process
-->The program will automatically check for open edges (holes) in the mesh.
-->If open edges are found, it will try to fill them by adding new faces to close the holes.
-->A 3D visualization of the corrupted mesh will be displayed with red edges highlighting the open edges and yellow faces indicating problematic areas.
-->The program will repair the mesh and display a new visualization of the repaired mesh.


5. Save the Repaired Mesh
After repairing the mesh, the program will save the repaired STL file to the specified location with the name repaired_cube.stl by default. You can modify this in the code if needed.

Example Usage
Run the program by executing the following command:
python stl_repair.py

In the file dialog, select an STL file (e.g., input_model.stl).

The program will display two visualizations:

One showing the corrupted mesh with open edges.
One showing the repaired mesh with the holes filled.
The repaired mesh will be saved as repaired_cube.stl in the same directory as the script.