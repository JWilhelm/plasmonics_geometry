def write_xyz_file(filename, atoms):
    num_atoms = len(atoms)
    with open(filename, 'w') as f:
        f.write(str(num_atoms) + '\n')
        f.write('Na atoms arranged in a square pyramid\n')
        for atom in atoms:
            f.write('Na {:.6f} {:.6f} {:.6f}\n'.format(*atom))

def generate_square_pyramid(lattice_const, n_vertical_double_layers_pyr, d, rc):
    atoms = []
    for i_layer in range(n_vertical_double_layers_pyr):
      for i in range(2):
        n_edge = 2*i_layer + i 
        z = (i_layer + 0.5*i) * lattice_const
        for i_x in range(n_edge+1):
          for j_y in range(n_edge+1):     
            if i_x < d or i_x > n_edge-d or j_y < d or j_y > n_edge-d or \
              n_edge > 2*n_vertical_double_layers_pyr-d-1:
              if rc and n_edge == 2*n_vertical_double_layers_pyr-1 and \
                 (i_x==0 or i_x==n_edge or j_y==0 or j_y==n_edge):
                 continue
              x = (i_x-n_edge/2) * lattice_const
              y = (j_y-n_edge/2) * lattice_const    
              atoms.append((x,y,z))
    return atoms

def generate_cube(lattice_const, n_dl, d, dist_frontier_atoms, atoms, n_xy):
    for k_z in range(n_dl):    
      for k in range(2):
#        n_edge_atoms = 2*n_dl-1
        n_edge_atoms = 2*n_xy-1   
        for i_x in range(n_edge_atoms-k):
          for j_y in range(n_edge_atoms-k):
            i_x_adj = i_x+k/2
            j_y_adj = j_y+k/2             
            k_z_adj = k_z+k/2             
            x = (i_x_adj-n_xy+1) * lattice_const
            y = (j_y_adj-n_xy+1) * lattice_const
            z = -(k_z_adj) * lattice_const - dist_frontier_atoms
            if k_z_adj < n_dl-0.7:
              if i_x_adj < d or i_x_adj > n_edge_atoms-d-1 or j_y_adj < d or j_y_adj > n_edge_atoms-d-1 or \
                 k_z_adj < d or k_z_adj > n_dl-d-1:
                 atoms.append((x,y,z))
            print(x,y,z)
    return atoms

# ONLY CHANGE THESE PARAMETERS
lattice_const = 4.282
n_vertical_double_layers_pyr = 5
n_vertical_double_layers_cub = 5
n_xy_cube = 5
thickness_pyr = 5
thickness_cub = 5    
round_corners = True
dist_frontier_atoms = 3.0
# END PARAMETER CHANGE


# Generate the atoms for the square pyramid
atoms = generate_square_pyramid(lattice_const, n_vertical_double_layers_pyr, thickness_pyr, round_corners)
atoms = generate_cube          (lattice_const, n_vertical_double_layers_cub, thickness_cub, dist_frontier_atoms, \
                                atoms, n_xy_cube)  

# Write the atoms to an XYZ file
filename = 'nat_'+str(len(atoms))+'_parameters_'+\
str(n_vertical_double_layers_pyr)+'_'+\
str(n_vertical_double_layers_cub)+'_'+\
str(n_xy_cube)+'_'+\
str(thickness_pyr )+'_'+\
str(thickness_cub)+'_'+\
str(dist_frontier_atoms)+\
'.xyz'
write_xyz_file(filename, atoms)

print('XYZ file "{}" has been created.'.format(filename))
