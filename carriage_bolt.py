# to execute from the FreeCAD console:
# execfile ("F:/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/carriage_bolt.py");
# execfile ("C:/Users/felipe/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/carriage_bolt.py");

# to excute from command line in windows:
# "C:\Program Files\FreeCAD 0.15\bin\freecadcmd" sk12.py

# directory where you want to save the files
#filepath = "./"
#filepath = "F/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/"
filepath = "C:/Users/felipe/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/"

# name of the file
filename = "carriage_bolt"

doc = FreeCAD.newDocument();
import FreeCAD;
import Part;
#import Draft;
#import copy;
#import Mesh;


import mat_cte  # import material constants and other constants
#import mfc  # import my functions for freecad

""" ------------------- dimensions: --------------------------
"""

# The piece will hold 2 LME10UU linear bearings, tolerance added
bearing_l_tol = mat_cte.LME10UU_BEARING_L + mat_cte.TOL;
bearing_d_tol = mat_cte.LME10UU_BEARING_D + mat_cte.TOL;

# Carriage inner rectangle (for the hot end)
inrect_x = 36
inrect_y = 20
# separation between inner rectangles, and also to the end of the piece
inrect_xsep = 12

# carriage total x dimension:
car_x = 2 * inrect_x + 3 * inrect_xsep

# radius for the fillet of 4 corners of the carriage
car_fllt_r = 4

# The diameter of the rods is 10
rod_diam = 10;
# Add 2 mm, because it is just to leave space for the rod
# and hold the linear bearings
rod_diam_space = rod_diam + 2

# Separation between the rods axis (Y dimension)
rod_sep = 50

# Distance between the rod axis to the end (it has to be larger than the 
# radius of the bearing

dist_rodax_end = 20

car_y = rod_sep + dist_rodax_end

car_z = 10.5

# E3D V6 extrusor dimensions
"""
    ___________
   |           |   outup
    -----------
      |     |
      |     |      in
    ___________
   |           |   outbot
    -----------
"""

e3dv6_in_diam = 12
e3dv6_in_h = 6
e3dv6_out_diam = 16
e3dv6_outup_h = 3.7
e3dv6_outbot_h = 3

# separation of the extruders, measured from the center.
# with the fan, the extruder are about 30mm wide. So 15mm from the center.
# giving 10mm separation, results in 40mm separation
# and total length of 70mm
extrud_sep = 40

# DIN-912 bolt dimmensions
# head: the index is the M, i.e: M3, M4, ..., the value is the diameter of the head of the bolt
d912_head_d = {3: 5.5, 4: 7, 5: 8.5, 6:10, 8:13, 10:18} 
# length: the index is the M, i.e: M3, M4, ..., the value is the length of the head of the bolt
# well, it is the same as the M, never mind...
d912_head_l =  {3: 3,   4: 4, 5: 5,   6:6,  8:8,  10:10} 


# tightening bolt with added tolerances:
# Bolt's head radius
#tbolt_head_r = (tol * d912_head_d[sk_12['tbolt']])/2 
# Bolt's head lenght
#tbolt_head_l = tol * d912_head_l[sk_12['tbolt']] 
# Mounting bolt radius with added tolerance
#mbolt_r = tol * sk_12['mbolt']/2

# vector constants
v0 = FreeCAD.Vector(0,0,0)
vx = FreeCAD.Vector(1,0,0)
vy = FreeCAD.Vector(0,1,0)
vz = FreeCAD.Vector(0,0,1)

# no rotation vector
v0rot = FreeCAD.Rotation(vz,0)

def addBox(x, y, z, name, cx= False, cy=False):
    box =  doc.addObject("Part::Box",name)
    box.Length = x
    box.Width  = y
    box.Height = z
    xpos = 0
    ypos = 0
    # centered 
    if cx == True:
        xpos = -x/2
    if cy == True:
        ypos = -y/2
    box.Placement.Base =FreeCAD.Vector(xpos,ypos,0)
    return box

# Add cylinder r: radius, h: height, 
def addCylinder(r, h, name):
    cyl =  doc.addObject("Part::Cylinder",name)
    cyl.Radius = r
    cyl.Height = h
    return cyl


#  ---------------- Fillet on edges of a certain length
#   box:   is the original shape we want to fillet
#   e_len: the length of the edges that we want to fillet
#   radius: the radius of the fillet
#   name: the name of the shape we want to create

def fillet_len (box, e_len, radius, name):
    fllts_v = []
    edge_ind = 1
    for edge_i in box.Shape.Edges:
        if edge_i.Length == e_len: # same length
        # the index is appeneded (edge_ind),not the edge itself (edge_i)
        # radius is twice, because it can be variable
            fllts_v.append((edge_ind, radius, radius))
        edge_ind += 1
    box_fllt = doc.addObject ("Part::Fillet", name)
    box_fllt.Base = box
    box_fllt.Edges = fllts_v
    return box_fllt

# --------------------- the total box ----------------------
total_box = addBox(car_x, car_y, car_z, "total_box", cx = 1, cy=1)
#   Fillet on the vertical edges
tot_box_fllt = fillet_len (total_box, car_z, car_fllt_r, "tot_box_fllt")


# ------------------- Inner rectangle holes

# p: the one on the positive side | n: on the negative side
inrect_p = addBox (inrect_x, inrect_y, car_z+2, "inrect_p", cx=1, cy=1)
inrect_n = addBox (inrect_x, inrect_y, car_z+2, "inrect_n", cx=1, cy=1)

inrect_p_pos = FreeCAD.Vector(inrect_xsep/2, -inrect_y/2, -1)
inrect_n_pos = FreeCAD.Vector(-inrect_xsep/2 - inrect_x, -inrect_y/2, -1)

inrect_p.Placement = FreeCAD.Placement(inrect_p_pos, v0rot, v0) 
inrect_n.Placement = FreeCAD.Placement(inrect_n_pos, v0rot, v0) 

# fillet the inner rectangles
inrect_p_fllt = fillet_len (inrect_p, car_z+2, car_fllt_r, "inrect_p_fllt")
inrect_n_fllt = fillet_len (inrect_n, car_z+2, car_fllt_r, "inrect_n_fllt")

holes_list = []
holes_list.append(inrect_p_fllt)
holes_list.append(inrect_n_fllt)


# ------------------- Rod holes

rod_p = addCylinder(rod_diam_space/2, car_x+2, "rod_p")
rod_p_pos = FreeCAD.Vector(-car_x/2-1, rod_sep/2, car_z)
rod_p.Placement = FreeCAD.Placement (rod_p_pos,
                                     FreeCAD.Rotation(vy,90),
                                     v0)

rod_n = addCylinder(rod_diam_space/2, car_x+2, "rod_n")
rod_n_pos = FreeCAD.Vector(-car_x/2-1, -rod_sep/2, car_z)
rod_n.Placement = FreeCAD.Placement (rod_n_pos,
                                     FreeCAD.Rotation(vy,90),
                                     v0)

holes_list.append(rod_n)
holes_list.append(rod_p)

# --------------------------- Union of all the holes

fuse_holes = doc.addObject("Part::MultiFuse", "fuse_holes")
fuse_holes.Shapes = holes_list

# --------------------------- Cut all the holes

carr_hole = doc.addObject("Part::Cut", "carr_hole")
carr_hole.Base = tot_box_fllt
carr_hole.Tool = fuse_holes



doc.recompute()
"""
total_box_pos = FreeCAD.Vector(0,-sk_y/2,0)
total_box.Placement.Base = total_box_pos
"""
"""

# what we have to cut from the sides
side_box_y = (sk_y - sk_12['I'])/2
side_box_z = sk_z - sk_12['g']

side_cut_box_r = addBox (sk_x, side_box_y, side_box_z,
                     "side_box_r")
side_cut_pos_r = FreeCAD.Vector(0,sk_12['I']/2,sk_12['g'])
side_cut_box_r.Placement.Base = side_cut_pos_r

side_cut_box_l= addBox (sk_x, side_box_y, side_box_z,
                     "side_box_l")
side_cut_pos_l = FreeCAD.Vector(0,-sk_y/2,sk_12['g'])
side_cut_box_l.Placement.Base = side_cut_pos_l

# union 
side_boxes = doc.addObject("Part::Fuse", "side_boxes")
side_boxes.Base = side_cut_box_r
side_boxes.Tool = side_cut_box_l

# difference 
sk_shape = doc.addObject("Part::Cut", "sk_shape")
sk_shape.Base = total_box
sk_shape.Tool = side_boxes

# Shaft hole, its height has +2 to make it throughl L all de way
shaft_hole = addCylinder(sk_12['d']/2, sk_x+2, "shaft_hole")


"""
"""
First argument defines de position: -1, 0, h
Second argument rotation: 90 degrees rotation in Y.
Third argument the center of the rotation, in this case, it is in the cylinder
axis at the base of the cylinder 
"""
"""
shaft_hole.Placement = FreeCAD.Placement(FreeCAD.Vector(-1,0,sk_12['h']),
                                         FreeCAD.Rotation(vy,90),
                                         v0)

# the upper sepparation

up_sep = addBox( sk_x +2, up_sep_dist, sk_z-sk_12['h'] +1, "up_sep")
up_sep_pos = FreeCAD.Vector(-1, -up_sep_dist/2, sk_12['h']+1)
up_sep.Placement.Base = up_sep_pos

"""
"""
 Tightening bolt shaft hole, its height has +2 to make it throughl L all de way
 sk_12['tbolt'] is the diameter of the bolt: (M..) M4, ...
 tbolt_head_r: is the radius of the tightening bolt's head (including tolerance), which its bottom
 either
 - is at the middle point between
   - A: the total height :sk_z
   - B: the top of the shaft hole: sk_12['h']+sk_12['d']/2
   - so the result will be (A + B)/2
 or it is aligned with the top of the 12mm shaft, whose height is:  sk_12['h']+sk_12['d']/2
"""
"""
tbolt_shaft = addCylinder(sk_12['tbolt']/2,sk_12['I']+2, "tbolt_shaft")
tbolt_shaft_pos = FreeCAD.Vector(sk_x/2,
                                 sk_12['I']/2+1,
                                sk_12['h']+sk_12['d']/2+tbolt_head_r/tol)
                                #(sk_z + sk_12['h']+sk_12['d']/2)/2)
tbolt_shaft.Placement = FreeCAD.Placement(tbolt_shaft_pos,
                                         FreeCAD.Rotation(vx,90),
                                         v0)

# Head of the thigthening bolt
tbolt_head = addCylinder(tbolt_head_r,tbolt_head_l+1, "tbolt_head")
tbolt_head_pos = FreeCAD.Vector(sk_x/2,
                                sk_12['I']/2+1,
                                sk_12['h']+sk_12['d']/2+tbolt_head_r/tol)
                                #(sk_z + sk_12['h']+sk_12['d']/2)/2)
tbolt_head.Placement = FreeCAD.Placement(tbolt_head_pos,
                                         FreeCAD.Rotation(vx,90),
                                         v0)


#Make an union of all these parts

fuse_shaft_holes = doc.addObject("Part::MultiFuse", "fuse_shaft_holes")
fuse_shaft_holes.Shapes = [tbolt_head, tbolt_shaft, up_sep, shaft_hole]

#Cut from the sk_shape

sk_shape_w_holes = doc.addObject("Part::Cut", "sk_shape_w_holes")
sk_shape_w_holes.Base = sk_shape
sk_shape_w_holes.Tool = fuse_shaft_holes

#Mounting bolts
mbolt_sh_r = addCylinder(mbolt_r,sk_12['g']+2, "mbolt_sh_r")
mbolt_sh_l = addCylinder(mbolt_r,sk_12['g']+2, "mbolt_sh_l")

mbolt_sh_r_pos = FreeCAD.Vector(sk_x/2,
                                sk_12['B']/2,
                                -1)

mbolt_sh_l_pos = FreeCAD.Vector(sk_x/2,
                                -sk_12['B']/2,
                                -1)

mbolt_sh_r.Placement.Base = mbolt_sh_r_pos
mbolt_sh_l.Placement.Base = mbolt_sh_l_pos

"""
""" Equivalente expresions to the ones above
mbolt_sh_l.Placement = FreeCAD.Placement(mbolt_sh_l_pos, v0rot, v0)
mbolt_sh_r.Placement = FreeCAD.Placement(mbolt_sh_r_pos, v0rot, v0)
"""
"""

mbolts_sh = doc.addObject("Part::Fuse", "mbolts_sh")
mbolts_sh.Base = mbolt_sh_r
mbolts_sh.Tool = mbolt_sh_l

sk_final = doc.addObject("Part::Cut", "sk_final")
sk_final.Base = sk_shape_w_holes
sk_final.Tool = mbolts_sh


doc.recompute()

# saving the freecad file
doc.saveAs(filepath + filename + ".FCStd");

# Export the stl and the step files

Part.export([sk_final], filepath + filename + ".stl")
Part.export([sk_final], filepath + filename + ".step")


"""
"""
sk_center_pos = FreeCAD.Vector(0,-sk_center_y/2,0);


# this way, a shape is created
sk_center_box_sh = Part.makeBox(sk_x, sk_center_y, sk_z);
Part.show(sk_center_box_sh);
doc.recompute();

# this way, a box is created
sk_center_box_bx = doc.addObject("Part::Box","center_box");
sk_center_box_bx.Length = sk_x;
sk_center_box_bx.Width = sk_center_y;
sk_center_box_bx.Height = sk_z;
sk_center_box_bx.Placement.Base = sk_center_pos;

# this way, a box is created
sk_center_box_py = cube(sk_x, sk_center_y, sk_z).translate(0, -sk_center_y/2,0);
"""
