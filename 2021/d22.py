import numpy as np

file = '2021/inputs/d22.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

commands = []
command_locs = []
for l in lines:
    o,loc = l.split(' ')
    xyz_range = [list(map(int, xyz[2:].split('..'))) for xyz in loc.split(',')]
    commands.append(o)
    command_locs.append(xyz_range)
command_locs = np.array(command_locs)

def process_commands(commands, command_locs, range_max=50):
    cubes_init = np.zeros([2*range_max+1]*3, dtype=bool)
    cubes_init.fill(False)
    for i,(o,l) in enumerate(zip(commands, command_locs)):
        if (l[:,0]<-range_max).any() or (l[:,1]>range_max).any():
            continue
        xm,ym,zm = np.clip(l[:,0], -range_max, range_max) + range_max
        xp,yp,zp = np.clip(l[:,1], -range_max, range_max) + range_max
        # print(i,xm,xp,ym,yp,zm,zp)
        if o == 'on':
            cubes_init[xm:xp+1, ym:yp+1, zm:zp+1] = True
        else :
            cubes_init[xm:xp+1, ym:yp+1, zm:zp+1] = False
    return cubes_init

def process_commands_efficient(commands, command_locs):
    command_locs = command_locs.copy()
    command_locs[:,:,1] += 1

    Xs = np.unique(command_locs[:,0,:].flatten())
    Ys = np.unique(command_locs[:,1,:].flatten())
    Zs = np.unique(command_locs[:,2,:].flatten())
    map_Xs = {x:i for i,x in enumerate(Xs)}
    map_Ys = {y:i for i,y in enumerate(Ys)}
    map_Zs = {z:i for i,z in enumerate(Zs)}
    mapped_locs = np.zeros([len(commands), 3, 2], dtype=int)
    for i,(o,l) in enumerate(zip(commands, command_locs)):
        mapped_locs[i,0,:] = [map_Xs[l[0,0]], map_Xs[l[0,1]]]
        mapped_locs[i,1,:] = [map_Ys[l[1,0]], map_Ys[l[1,1]]]
        mapped_locs[i,2,:] = [map_Zs[l[2,0]], map_Zs[l[2,1]]]

    cubes_init = np.zeros([len(Xs)-1, len(Ys)-1, len(Zs)-1], dtype=bool)
    cubes_init.fill(False)
    for i,(o,l) in enumerate(zip(commands, mapped_locs)):
        if o == 'on':
            cubes_init[l[0,0]:l[0,1], l[1,0]:l[1,1], l[2,0]:l[2,1]] = True
        else :
            cubes_init[l[0,0]:l[0,1], l[1,0]:l[1,1], l[2,0]:l[2,1]] = False

    cube_sizes = (Xs[1:] - Xs[:-1])[:,None,None] * (Ys[1:] - Ys[:-1])[None,:,None] * (Zs[1:] - Zs[:-1])[None,None,:]
    return cubes_init, cube_sizes

cubes = process_commands(commands, command_locs)
print('P1', cubes.sum())

cubes, cubes_sizes = process_commands_efficient(commands, command_locs)
print('P2', (cubes*cubes_sizes).sum())
