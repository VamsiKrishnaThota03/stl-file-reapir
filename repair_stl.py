import trimesh
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

def load_and_parse_stl(file_path):
    try:
        print(f"Loading STL file: {file_path}")
        original_mesh = trimesh.load(file_path, force="mesh")
        print("STL file loaded successfully.")
        return original_mesh
    except Exception as e:
        print(f"Error loading STL file: {e}")
        return None

def find_open_edges(stl_mesh):
    print("Finding open edges...")

    edge_occurrences = {}
    for face in stl_mesh.faces:
        edges = [
            tuple(sorted((face[0], face[1]))),
            tuple(sorted((face[1], face[2]))),
            tuple(sorted((face[2], face[0]))),
        ]
        for edge in edges:
            if edge in edge_occurrences:
                edge_occurrences[edge] += 1
            else:
                edge_occurrences[edge] = 1
    
    open_edges = [edge for edge, count in edge_occurrences.items() if count == 1]
    
    print(f"Number of open edges: {len(open_edges)}")
    return open_edges

def fill_holes_manually(stl_mesh, open_edges):
    print("Filling holes manually...")
    new_faces = []
    vertices = stl_mesh.vertices
    edges = list(open_edges)

    for edge in edges:
        v1, v2 = edge
        for i, vertex in enumerate(vertices):
            if i != v1 and i != v2:
                new_faces.append([v1, v2, i])

    new_faces = np.array(new_faces)
    if len(new_faces) > 0:
        stl_mesh.faces = np.vstack([stl_mesh.faces, new_faces])
        stl_mesh.fix_normals()
    print(f"Added {len(new_faces)} new faces to close holes.")

def repair_mesh_manually(stl_mesh):
    """Repair the mesh manually by filling holes and ensuring watertightness."""
    print("Starting manual repair...")
    open_edges = find_open_edges(stl_mesh)
    
    if len(open_edges) == 0:
        print("No open edges found. Mesh is already watertight. Skipping repair.")
        return stl_mesh, False 
    
    fill_holes_manually(stl_mesh, open_edges)
    stl_mesh.fix_normals()
    print("Manual repair completed.")
    return stl_mesh, True

def display_mesh_with_edges_and_faces(stl_mesh, open_edges, title="Mesh Visualization"):
    """Visualize the STL file, highlighting open edges and broken faces."""
    print(f"Visualizing {title}...")
    vertices = stl_mesh.vertices
    faces = stl_mesh.faces
    
    # Identify problematic faces
    problematic_faces = set()
    edge_to_face_map = {tuple(sorted(edge)): [] for edge in open_edges}
    for face_index, face in enumerate(faces):
        edges = [
            tuple(sorted((face[0], face[1]))),
            tuple(sorted((face[1], face[2]))),
            tuple(sorted((face[2], face[0]))),
        ]
        for edge in edges:
            if edge in edge_to_face_map:
                edge_to_face_map[edge].append(face_index)
    
    for edge, face_indices in edge_to_face_map.items():
        problematic_faces.update(face_indices)

    plt.ion()

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    mesh_poly = Poly3DCollection(vertices[faces], alpha=0.3, edgecolor="k")
    ax.add_collection3d(mesh_poly)

    for edge in open_edges:
        v1, v2 = edge
        ax.plot(
            [vertices[v1, 0], vertices[v2, 0]],
            [vertices[v1, 1], vertices[v2, 1]],
            [vertices[v1, 2], vertices[v2, 2]],
            color="r",
            lw=2,
        )

    for face_index in problematic_faces:
        face_vertices = faces[face_index]
        poly = vertices[face_vertices]
        face_poly = Poly3DCollection([poly], alpha=0.5, facecolor="yellow")
        ax.add_collection3d(face_poly)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(title)
    plt.show()

    plt.pause(15)

    plt.close(fig)

def save_repaired_stl(stl_mesh, output_path):
    try:
        print(f"Saving repaired STL file to: {output_path}")
        stl_mesh.export(output_path)
        print("Repaired STL file saved successfully.")
    except Exception as e:
        print(f"Error saving STL file: {e}")

if __name__ == "__main__":
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    Tk().withdraw()
    input_file_path = askopenfilename(filetypes=[("STL files", "*.stl")])

    if not input_file_path:
        print("No file selected. Exiting...")
        exit()

    output_file_path = "repaired_cube.stl"

    mesh_data = load_and_parse_stl(input_file_path)
    if not mesh_data:
        exit("Failed to load STL file.")

    open_edges = find_open_edges(mesh_data)

    if len(open_edges) > 0:
        display_mesh_with_edges_and_faces(mesh_data, open_edges, title="Corrupted Mesh")

    repaired_mesh, repaired = repair_mesh_manually(mesh_data)

    if not repaired:
        print("Mesh is already watertight. Exiting process.")
        exit()

    open_edges_after_repair = find_open_edges(repaired_mesh)

    display_mesh_with_edges_and_faces(repaired_mesh, open_edges_after_repair, title="Repaired Mesh")

    save_repaired_stl(repaired_mesh, output_file_path)
