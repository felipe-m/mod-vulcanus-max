# to execute from the FreeCAD console:
# execfile ("F:/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/carriage_bolt.py");
# execfile ("C:/Users/felipe/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/carriage_bolt.py");

# to excute from command line in windows:
# "C:\Program Files\FreeCAD 0.15\bin\freecadcmd" carriage_bolt.py

# directory where you want to save the files
#filepath = "./"
#filepath = "F/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/"
filepath = "C:/Users/felipe/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/"

# name of the file
filename = "carriage_bolt"

import FreeCAD;
import Part;
#import Draft;
#import copy;
#import Mesh;

doc = FreeCAD.newDocument();

import mat_cte  # import material constants and other constants
import mfc      # import my functions for freecad

from mfc import V0, VX, VY, VZ, V0ROT, addBox, addCyl , fillet_len

""" ------------------- dimensions: --------------------------
"""


# Carriage inner rectangle (for the hot end)
INRECT_X = 36
INRECT_Y = 20
# separation between inner rectangles, and also to the end of the piece
INRECT_XSEP = 12

# carriage total x dimension:
#CAR_X = 2 * INRECT_X + 3 * INRECT_XSEP

# radius for the fillet of 4 corners of the carriage
CAR_FLLT_R = 4

# The diameter of the rods is 10
ROD_DIAM = 10;
# Add 2 mm, because it is just to leave space for the rod
# and hold the linear bearings
rod_diam_space = ROD_DIAM + 2

# Separation between the rods axis (Y dimension)
ROD_SEP = 50

OUT_SEP = 10  # default distance to the ends

# The piece will hold 2 LME10UU linear bearings, tolerance added
BEARING_L_TOL = mat_cte.LME10UU_BEARING_L + mat_cte.TOL;
BEARING_D_TOL = mat_cte.LME10UU_BEARING_D + mat_cte.TOL;

# Distance between the rod axis to the end (it has to be larger than the 
# radius of the bearing

DIST_RODAX_END = BEARING_D_TOL/2 + OUT_SEP

CAR_X = 2 * BEARING_L_TOL + 3 * OUT_SEP

#BEARING_SEP = CAR_X - 2 * BEARING_L_TOL

CAR_Y = ROD_SEP + 2* DIST_RODAX_END

CAR_Z = 10.5

# ---------------- extruder shape -------------------------------------------
# separation of the extruders, measured from the center.
# with the fan, the extruder are about 30mm wide. So 15mm from the center.
# giving 10mm separation, results in 40mm separation
# and total length of 70mm
EXTR_WIDTH = 30
EXTR_RAD = 11  # Radius of the heat sink
EXTR_SPACE = 5 # Space between the extruders
EXTR_SPACE_OUT = 10 # Space to the end
EXTR_SEP = EXTR_WIDTH + EXTR_SPACE

EXTR_IN_D     = mat_cte.E3DV6_IN_DIAM  + mat_cte.TOL
EXTR_IN_H     = mat_cte.E3DV6_IN_H 
EXTR_OUT_D    = mat_cte.E3DV6_OUT_DIAM + mat_cte.TOL
EXTR_OUTUP_H  = mat_cte.E3DV6_OUTUP_H 
EXTR_OUTBOT_H = mat_cte.E3DV6_OUTBOT_H + mat_cte.TOL

# this is the distance that the bottom of the bottom ring will be outside
# of the 
EXTR_BOT_OUT = 1  

# Outer up ring
extr_outup = addCyl (r=EXTR_OUT_D/2, h=EXTR_OUTUP_H, name="extr_outup");
extr_outup_2 = addCyl (r=EXTR_OUT_D/2, h=EXTR_OUTUP_H, name="extr_outup_2");
extr_outup_pos = FreeCAD.Vector(0,0,EXTR_OUTBOT_H + EXTR_IN_H-EXTR_BOT_OUT)
extr_outup.Placement = FreeCAD.Placement(extr_outup_pos, V0ROT, V0)
extr_outup_2.Placement = FreeCAD.Placement(extr_outup_pos, V0ROT, V0)
# Inner ring
extr_in = addCyl (r=EXTR_IN_D/2, h=EXTR_IN_H, name="extr_in");
extr_in_2 = addCyl (r=EXTR_IN_D/2, h=EXTR_IN_H, name="extr_in_2");
extr_in_pos = FreeCAD.Vector(0,0,EXTR_OUTBOT_H-EXTR_BOT_OUT)
extr_in.Placement = FreeCAD.Placement(extr_in_pos, V0ROT, V0)
extr_in_2.Placement = FreeCAD.Placement(extr_in_pos, V0ROT, V0)
# Outer bottom ring
extr_outbot = addCyl (r=EXTR_OUT_D/2, h=EXTR_OUTBOT_H, name="extr_outbot");
extr_outbot_2 = addCyl (r=EXTR_OUT_D/2, h=EXTR_OUTBOT_H, name="extr_outbot_2");
extr_outbot_pos = FreeCAD.Vector(0,0,-EXTR_BOT_OUT)
extr_outbot.Placement = FreeCAD.Placement(extr_outbot_pos, V0ROT,V0)
extr_outbot_2.Placement = FreeCAD.Placement(extr_outbot_pos, V0ROT,V0)

extr_rings_list = [extr_outup, extr_in, extr_outbot]
extr_rings_1 = doc.addObject("Part::MultiFuse", "extr_rings_1")
extr_rings_1.Shapes = extr_rings_list
extr_ring_1_pos = FreeCAD.Vector(EXTR_SEP/2,0,0)
extr_rings_1.Placement = FreeCAD.Placement(extr_ring_1_pos, V0ROT, V0)

extr_rings_list_2 = [extr_outup_2, extr_in_2, extr_outbot_2]
extr_rings_2 = doc.addObject("Part::MultiFuse", "extr_rings_2")
extr_rings_2.Shapes = extr_rings_list_2
extr_ring_2_pos = FreeCAD.Vector(-EXTR_SEP/2,0,0)
extr_rings_2.Placement = FreeCAD.Placement(extr_ring_2_pos, V0ROT, V0)

# create a simple copy of it . It doesn't work this way
"""
extr_rings_2 =doc.addObject("Part::Feature", "extr_rings_2") = extr_rings_1 
extr_rings_2.Shape = extr_rings_1.Shape 
"""

# --------------------- extruder holders -----------------------------

# Extruder separation between axis + 2*radius (each side) + 2* extruder space
# to the end
EXTR_HOLD_X = EXTR_SEP + EXTR_WIDTH + 2*EXTR_SPACE_OUT 
EXTR_HOLD_Y = EXTR_RAD # + EXTR_SPACE 
EXTR_HOLD_Z = EXTR_IN_H + EXTR_OUTUP_H + EXTR_OUTBOT_H - EXTR_BOT_OUT

extr_hold_1 = addBox(EXTR_HOLD_X, EXTR_HOLD_Y, EXTR_HOLD_Z, "extr_hold_1", cx=1)
extr_hold_1_pos = FreeCAD.Vector(-EXTR_HOLD_X/2,0,0)
#extr_hold_1.Placement 

# --------------------- the total box ----------------------
total_box = addBox(CAR_X, CAR_Y, CAR_Z, "total_box", cx = 1, cy=1)
#   Fillet on the vertical edges
tot_box_fllt = fillet_len (total_box, CAR_Z, CAR_FLLT_R, "tot_box_fllt")


# ------------------- Inner rectangle holes

# p: the one on the positive side | n: on the negative side
inrect_p = addBox (INRECT_X, INRECT_Y, CAR_Z+2, "inrect_p", cx=1, cy=1)
inrect_n = addBox (INRECT_X, INRECT_Y, CAR_Z+2, "inrect_n", cx=1, cy=1)

inrect_p_pos = FreeCAD.Vector(INRECT_XSEP/2, -INRECT_Y/2, -1)
inrect_n_pos = FreeCAD.Vector(-INRECT_XSEP/2 - INRECT_X, -INRECT_Y/2, -1)

inrect_p.Placement = FreeCAD.Placement(inrect_p_pos, V0ROT, V0) 
inrect_n.Placement = FreeCAD.Placement(inrect_n_pos, V0ROT, V0) 

# fillet the inner rectangles
inrect_p_fllt = fillet_len (inrect_p, CAR_Z+2, CAR_FLLT_R, "inrect_p_fllt")
inrect_n_fllt = fillet_len (inrect_n, CAR_Z+2, CAR_FLLT_R, "inrect_n_fllt")

holes_list = []
holes_list.append(inrect_p_fllt)
holes_list.append(inrect_n_fllt)


# ------------------- Rod holes

rod_p = addCyl(rod_diam_space/2, CAR_X+2, "rod_p")
rod_p_pos = FreeCAD.Vector(-CAR_X/2-1, ROD_SEP/2, CAR_Z)
rod_p.Placement = FreeCAD.Placement (rod_p_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)

rod_n = addCyl(rod_diam_space/2, CAR_X+2, "rod_n")
rod_n_pos = FreeCAD.Vector(-CAR_X/2-1, -ROD_SEP/2, CAR_Z)
rod_n.Placement = FreeCAD.Placement (rod_n_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)

holes_list.append(rod_n)
holes_list.append(rod_p)

# -------------------- Bearing holes

""" # better with a loop
bearing_1 = addCyl(BEARING_D_TOL/2, BEARING_L_TOL, "bearing_1")
bearing_1_pos = FreeCAD.Vector(OUT_SEP/2, ROD_SEP/2, CAR_Z)
bearing_1.Placement = FreeCAD.Placement (bearing_1_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)
bearing_2 = addCyl(BEARING_D_TOL/2, BEARING_L_TOL, "bearing_2")
bearing_2_pos = FreeCAD.Vector(-OUT_SEP/2 - BEARING_L_TOL, ROD_SEP/2, CAR_Z)
bearing_2.Placement = FreeCAD.Placement (bearing_2_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)
bearing_3 = addCyl(BEARING_D_TOL/2, BEARING_L_TOL, "bearing_3")
bearing_3_pos = FreeCAD.Vector(OUT_SEP/2, -ROD_SEP/2, CAR_Z)
bearing_3.Placement = FreeCAD.Placement (bearing_3_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)
bearing_4 = addCyl(BEARING_D_TOL/2, BEARING_L_TOL, "bearing_4")
bearing_4_pos = FreeCAD.Vector(-OUT_SEP/2 - BEARING_L_TOL, -ROD_SEP/2, CAR_Z)
bearing_4.Placement = FreeCAD.Placement (bearing_4_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)
"""

for i in range (4):
    bearing = addCyl(BEARING_D_TOL/2, BEARING_L_TOL, "bearing_" + str(i))
    if i % 2 == 0: # is even, 0, 2
      x_bearing = OUT_SEP/2
    else:
      x_bearing = - OUT_SEP/2 - BEARING_L_TOL
    if i == 0 or i == 1:
      y_bearing = ROD_SEP/2
    else:
      y_bearing = -ROD_SEP/2
    bearing_pos = FreeCAD.Vector(x_bearing, y_bearing, CAR_Z)
    bearing.Placement = FreeCAD.Placement (bearing_pos,
                                           FreeCAD.Rotation(VY,90),
                                           V0)
    holes_list.append(bearing)

# --------------------------- Union of all the holes

fuse_holes = doc.addObject("Part::MultiFuse", "fuse_holes")
fuse_holes.Shapes = holes_list

# --------------------------- Cut all the holes

carr_hole = doc.addObject("Part::Cut", "carr_hole")
carr_hole.Base = tot_box_fllt
carr_hole.Tool = fuse_holes

doc.recompute()

"""
doc.saveAs(filepath + filename + ".FCStd");

# Export the stl and the step files

Part.export([sk_final], filepath + filename + ".stl")
Part.export([sk_final], filepath + filename + ".step")
"""
