# to execute from the FreeCAD console:
# execfile ("F:/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/carriage.py");
# execfile ("C:/Users/felipe/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/carriage.py");

# to excute from command line in windows:
# "C:\Program Files\FreeCAD 0.15\bin\freecadcmd" carriage.py

# directory where you want to save the files
#filepath = "./"
#filepath = "F/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/"
filepath = "C:/Users/felipe/urjc/proyectos/2015_impresora3d/vulcanus_max/cad/"

# name of the file
filename = "carriage"

import FreeCAD;
import Part;
import Draft;
#import copy;
#import Mesh;

doc = FreeCAD.newDocument();

import mat_cte  # import material constants and other constants
import mfc      # import my functions for freecad

from mfc import V0, VX, VY, VZ, V0ROT, addBox, addCyl, fillet_len
from mfc import addBolt, addBoltNut_hole, NutHole
from mat_cte import TOL

""" ------------------- dimensions: --------------------------
"""


# radius for the fillet of 4 corners of the carriage
CAR_FLLT_R = 4.0

# The diameter of the rods is 10
ROD_DIAM = 10.0;
# Add 2 mm, because it is just to leave space for the rod
# and hold the linear bearings
ROD_DIAM_SPACE = ROD_DIAM + 2

# Separation between the rods axis (Y dimension)
ROD_SEP = 50.0

# This separation can be smaller, then OUT_SEP_X maybe shouldn't be relative
# to OUT_SEP
OUT_SEP = 14.0  # default distance to the ends
# On the X axis we need a larger separation because of the extruder size
OUT_SEP_X = OUT_SEP + 3   

# The piece will hold 2 LME10UU linear bearings, tolerance added
BEARING_L_TOL = mat_cte.LME10UU_BEARING_L + TOL;
BEARING_D_TOL = mat_cte.LME10UU_BEARING_D + TOL;

# Distance between the rod axis to the end (it has to be larger than the 
# radius of the bearing

DIST_RODAX_END = BEARING_D_TOL/2.0 + OUT_SEP

CAR_X = 2.0 * BEARING_L_TOL + 3 * OUT_SEP_X

#BEARING_SEP = CAR_X - 2 * BEARING_L_TOL

CAR_Y = ROD_SEP + 2.0* DIST_RODAX_END

CAR_Z = 25.0 / 2

# ---------------- extruder shape -------------------------------------------
# separation of the extruders, measured from the center.
# with the fan, the extruder are about 30mm wide. So 15mm from the center.
# giving 10mm separation, results in 40mm separation
# and total length of 70mm
EXTR_WIDTH = 30.0  
EXTR_RAD = 11.0  # Radius of the heat sink
EXTR_SPACE = 3.0 # Space between the extruders
EXTR_SPACE_OUT = 10.0 # Space to the end
EXTR_SEP = EXTR_WIDTH + EXTR_SPACE

EXTR_IN_D     = mat_cte.E3DV6_IN_DIAM  + TOL

EXTR_IN_H     = mat_cte.E3DV6_IN_H - TOL 
EXTR_OUT_D    = mat_cte.E3DV6_OUT_DIAM + TOL
EXTR_OUTUP_H  = mat_cte.E3DV6_OUTUP_H 
EXTR_OUTBOT_H = mat_cte.E3DV6_OUTBOT_H + TOL

EXTR_HOLD_FLLT_R = 2.0

# this is the distance that the bottom of the bottom ring will be outside
# of the carriage
EXTR_BOT_OUT = 1.0  

# constant related to bolts
BOLT_R = 3
M3_HEAD_R = mat_cte.D912_HEAD_D[BOLT_R] / 2.0
M3_HEAD_L = mat_cte.D912_HEAD_L[BOLT_R] + TOL
M3_HEAD_R_TOL = M3_HEAD_R + TOL/2.0 # smaller TOL, because it's small
M3_SHANK_R_TOL = BOLT_R / 2.0 + TOL/2.0

M3_NUT_R = mat_cte.NUT_D934_D[BOLT_R] / 2.0
M3_NUT_L = mat_cte.NUT_D934_L[BOLT_R] + TOL
#  1.5 TOL because diameter values are minimum, so they may be larger
M3_NUT_R_TOL = M3_NUT_R + 1.5*TOL
XTR_BOT_OUT = 1.0  

# constant related to inserted nuts. For example, to make a leadscrew
# The nut height multiplier to have enough space to introduce it
NUT_HOLE_MULT_H = 1.8 
M3NUT_HOLE_H = NUT_HOLE_MULT_H * M3_NUT_L  
NUT_HOLE_EDGSEP = 3 # separation from the  edge

#M3_2APOT_TOL = mat_cte.NUT_D934_2A[3] +  TOL
# Apotheme is: R * cos(30) = 0.866
M3_2APOT_TOL = 2* M3_NUT_R_TOL * 0.866



# Outer up ring
extr_outup = addCyl (r=EXTR_OUT_D/2.0, h=EXTR_OUTUP_H, name="extr_outup");
extr_outup_2 = addCyl (r=EXTR_OUT_D/2.0, h=EXTR_OUTUP_H, name="extr_outup_2");
extr_outup_pos = FreeCAD.Vector(0,0,EXTR_OUTBOT_H + EXTR_IN_H-EXTR_BOT_OUT)
extr_outup.Placement = FreeCAD.Placement(extr_outup_pos, V0ROT, V0)
extr_outup_2.Placement = FreeCAD.Placement(extr_outup_pos, V0ROT, V0)
# Inner ring
extr_in = addCyl (r=EXTR_IN_D/2.0, h=EXTR_IN_H, name="extr_in");
extr_in_2 = addCyl (r=EXTR_IN_D/2.0, h=EXTR_IN_H, name="extr_in_2");
extr_in_pos = FreeCAD.Vector(0,0,EXTR_OUTBOT_H-EXTR_BOT_OUT)
extr_in.Placement = FreeCAD.Placement(extr_in_pos, V0ROT, V0)
extr_in_2.Placement = FreeCAD.Placement(extr_in_pos, V0ROT, V0)
# Outer bottom ring
extr_outbot = addCyl (r=EXTR_OUT_D/2.0, h=EXTR_OUTBOT_H, name="extr_outbot");
extr_outbot_2 = addCyl (r=EXTR_OUT_D/2.0, h=EXTR_OUTBOT_H, name="extr_outbot_2");
extr_outbot_pos = FreeCAD.Vector(0,0,-EXTR_BOT_OUT)
extr_outbot.Placement = FreeCAD.Placement(extr_outbot_pos, V0ROT,V0)
extr_outbot_2.Placement = FreeCAD.Placement(extr_outbot_pos, V0ROT,V0)

extr_rings_list = [extr_outup, extr_in, extr_outbot]
extr_rings_1 = doc.addObject("Part::MultiFuse", "extr_rings_1")
extr_rings_1.Shapes = extr_rings_list
extr_ring_1_pos = FreeCAD.Vector(EXTR_SEP/2.0,0,0)
extr_rings_1.Placement = FreeCAD.Placement(extr_ring_1_pos, V0ROT, V0)

extr_rings_list_2 = [extr_outup_2, extr_in_2, extr_outbot_2]
extr_rings_2 = doc.addObject("Part::MultiFuse", "extr_rings_2")
extr_rings_2.Shapes = extr_rings_list_2
extr_ring_2_pos = FreeCAD.Vector(-EXTR_SEP/2.0,0,0)
extr_rings_2.Placement = FreeCAD.Placement(extr_ring_2_pos, V0ROT, V0)

# create a simple copy of it . It doesn't work this way
"""
extr_rings_2 =doc.addObject("Part::Feature", "extr_rings_2") = extr_rings_1 
extr_rings_2.Shape = extr_rings_1.Shape 
"""


# ----------- fuse the extrusors rings
extr_holder_holes_list = []
extr_holder_holes_list.append (extr_rings_1)
extr_holder_holes_list.append (extr_rings_2)


# --------------------- extruder holders -----------------------------

# Extruder separation between axis + 2*radius (each side) + 2* extruder space
# to the end. We need to add some space for the nut holes: 8
EXTR_HOLD_X = 2* EXTR_WIDTH + 3.0*EXTR_SPACE + 10
# a little bigger so the heat sink can pass through
# the half of the total, because there are 2 extruder holders, one on the 
# + side of Y, and the other on the negative
EXTR_HOLD_Y = EXTR_RAD + 2* TOL 
EXTR_HOLD_Z = EXTR_IN_H + EXTR_OUTUP_H + EXTR_OUTBOT_H - EXTR_BOT_OUT

extr_hold_1 = addBox(EXTR_HOLD_X, EXTR_HOLD_Y, EXTR_HOLD_Z, "extr_hold_1", cx=1)
extr_hold_2 = addBox(EXTR_HOLD_X, EXTR_HOLD_Y, EXTR_HOLD_Z, "extr_hold_2")
extr_hold_2_pos = FreeCAD.Vector(-EXTR_HOLD_X/2.0,-EXTR_HOLD_Y,0)
extr_hold_2.Placement = FreeCAD.Placement (extr_hold_2_pos, V0ROT, V0) 

# ------------------  Tabs to attach both extruder holders
extr_hold_1_app_list = [extr_hold_1]
extr_hold_1_cut_list = []
extr_hold_2_app_list = [extr_hold_2]
extr_hold_2_cut_list = []

# Tab Dimensions:
# this is the distance from the exterior circle to the end:
# (EXTR_HOLD_X - EXTR_SEP - EXTR_OUT_D)/2.0
extr_hold_tab_x = ((EXTR_HOLD_X - EXTR_SEP - EXTR_OUT_D)/2.0)/ 1.25
extr_hold_tab_y = EXTR_HOLD_Y
extr_hold_tab_z = EXTR_HOLD_Z / 2.0

# for the Y Axis: +1: the union to superimpose, the cut to cut away
# On the others, for cutting we need +1, but not for adding
# --- tab 0
extr_hold_tab0 = addBox (extr_hold_tab_x,
                         extr_hold_tab_y+1,
                         extr_hold_tab_z - TOL/2,
                         "extr_hold_tab0")
extr_hold_tab0_hole = addBox (extr_hold_tab_x+1+TOL,
                              extr_hold_tab_y+1,
                              extr_hold_tab_z + 1 + TOL/2,
                              "extr_hold_tab0_hole")
extr_hold_tab0.Placement.Base = FreeCAD.Vector( -(EXTR_HOLD_X / 2.0),
                                                 -1,
                                                 EXTR_HOLD_Z / 2.0 + TOL/2)
extr_hold_2_app_list.append(extr_hold_tab0)
extr_hold_tab0_hole.Placement.Base = FreeCAD.Vector( -(EXTR_HOLD_X / 2.0)-1,
                                                 0,
                                                 EXTR_HOLD_Z / 2.0 - TOL/2)
extr_hold_1_cut_list.append(extr_hold_tab0_hole)

# --- tab 1
extr_hold_tab1 = addBox (extr_hold_tab_x,
                         extr_hold_tab_y+1,
                         extr_hold_tab_z - TOL/2,
                         "extr_hold_tab1")
extr_hold_tab1_hole = addBox (extr_hold_tab_x+1+TOL,
                              extr_hold_tab_y+1,
                              extr_hold_tab_z+1 + TOL/2,
                              "extr_hold_tab1_hole")
extr_hold_tab1.Placement.Base = FreeCAD.Vector( -(EXTR_HOLD_X / 2.0),
                                                 -extr_hold_tab_y,
                                                 0)
extr_hold_1_app_list.append(extr_hold_tab1)
extr_hold_tab1_hole.Placement.Base = FreeCAD.Vector( -(EXTR_HOLD_X / 2.0)-1,
                                                     -(extr_hold_tab_y+1),
                                                     -1)
extr_hold_2_cut_list.append(extr_hold_tab1_hole)

# --- tab 2
extr_hold_tab2 = addBox (extr_hold_tab_x,
                         extr_hold_tab_y+1,
                         extr_hold_tab_z - TOL/2,
                         "extr_hold_tab2")
extr_hold_tab2_hole = addBox (extr_hold_tab_x+1+TOL,
                              extr_hold_tab_y+1,
                              extr_hold_tab_z+1 +TOL/2,
                              "extr_hold_tab2_hole")
extr_hold_tab2.Placement.Base = FreeCAD.Vector(
                                       (EXTR_HOLD_X / 2.0)- extr_hold_tab_x,
                                        -extr_hold_tab_y,
                                        EXTR_HOLD_Z / 2.0 + TOL/2)
extr_hold_1_app_list.append(extr_hold_tab2)
extr_hold_tab2_hole.Placement.Base = FreeCAD.Vector( 
                                     (EXTR_HOLD_X / 2.0)- extr_hold_tab_x - TOL,
                                      -(extr_hold_tab_y+1),
                                      EXTR_HOLD_Z / 2.0 - TOL/2)
extr_hold_2_cut_list.append(extr_hold_tab2_hole)

# --- tab 3
extr_hold_tab3 = addBox (extr_hold_tab_x,
                         extr_hold_tab_y+1,
                         extr_hold_tab_z - TOL/2,
                         "extr_hold_tab3")
extr_hold_tab3_hole = addBox (extr_hold_tab_x+1+TOL,
                              extr_hold_tab_y+1,
                              extr_hold_tab_z+1+TOL/2,
                              "extr_hold_tab3_hole")
extr_hold_tab3.Placement.Base = FreeCAD.Vector( 
                                       (EXTR_HOLD_X / 2.0)- extr_hold_tab_x,
                                        -1,
                                         0)
extr_hold_2_app_list.append(extr_hold_tab3)
extr_hold_tab3_hole.Placement.Base = FreeCAD.Vector( 
                                     (EXTR_HOLD_X / 2.0)- extr_hold_tab_x - TOL,
                                      0,
                                      -1)
extr_hold_1_cut_list.append(extr_hold_tab3_hole)


extr_hold1_holes_joint = doc.addObject("Part::MultiFuse", 
                                       "extr_hold1_holes_joint")
extr_hold1_holes_joint.Shapes = extr_hold_1_cut_list

extr_hold1_tabs_joint = doc.addObject("Part::MultiFuse", 
                                       "extr_hold1_tabs_joint")
extr_hold1_tabs_joint.Shapes = extr_hold_1_app_list

extr_hold1_joint = doc.addObject("Part::Cut", 
                                 "extr_hold1_joint")
extr_hold1_joint.Base = extr_hold1_tabs_joint
extr_hold1_joint.Tool = extr_hold1_holes_joint


extr_hold2_holes_joint = doc.addObject("Part::MultiFuse", 
                                       "extr_hold2_holes_joint")
extr_hold2_holes_joint.Shapes = extr_hold_2_cut_list

extr_hold2_tabs_joint = doc.addObject("Part::MultiFuse", 
                                       "extr_hold2_tabs_joint")
extr_hold2_tabs_joint.Shapes = extr_hold_2_app_list

extr_hold2_joint = doc.addObject("Part::Cut", 
                                 "extr_hold2_joint")
extr_hold2_joint.Base = extr_hold2_tabs_joint
extr_hold2_joint.Tool = extr_hold2_holes_joint

""" 
Now we don't fillet them because they are going to be printed from that end

# ------------------ fillet the extruder holder 1
extr_hold_1_fillist = []
edge_ind = 1
for edge_i in extr_hold_1.Shape.Edges:
    # we want to take the external vertical edges
    if edge_i.Length == EXTR_HOLD_Z and edge_i.Vertexes[0].Y == EXTR_HOLD_Y:
      extr_hold_1_fillist.append((edge_ind, EXTR_HOLD_FLLT_R, EXTR_HOLD_FLLT_R))
    edge_ind += 1
extr_hold_1_fllt = doc.addObject("Part::Fillet", "extr_hold_1_fllt")
extr_hold_1_fllt.Base = extr_hold_1
extr_hold_1_fllt.Edges = extr_hold_1_fillist
# to hide the objects in freecad gu
if extr_hold_1.ViewObject != None:
  extr_hold_1.ViewObject.Visibility = False

# ------------------ fillet the extruder holder 2
extr_hold_2_fillist = []
edge_ind = 1
for edge_i in extr_hold_2.Shape.Edges:
    # we want to take the external vertical edges
    if edge_i.Length == EXTR_HOLD_Z and edge_i.Vertexes[0].Y == -EXTR_HOLD_Y:
      extr_hold_2_fillist.append((edge_ind, EXTR_HOLD_FLLT_R, EXTR_HOLD_FLLT_R))
    edge_ind += 1
extr_hold_2_fllt = doc.addObject("Part::Fillet", "extr_hold_2_fllt")
extr_hold_2_fllt.Base = extr_hold_2
extr_hold_2_fllt.Edges = extr_hold_2_fillist
# to hide the objects in freecad gu
if extr_hold_2.ViewObject != None:
  extr_hold_2.ViewObject.Visibility = False

"""


        

# --------------------- the boxes of the carriage ------
carlow_box = addBox(CAR_X, CAR_Y, CAR_Z, "carlow_box", cx = 1, cy=1)
#   Fillet on the vertical edges
carlow_box_fllt = fillet_len (carlow_box, CAR_Z, CAR_FLLT_R, "carlow_box_fllt")

carhig_box = addBox(CAR_X, CAR_Y, CAR_Z, "carhig_box", cx = 1, cy=1)
#   Fillet on the vertical edges
carhig_box_fllt = fillet_len (carhig_box, CAR_Z, CAR_FLLT_R, "carhig_box_fllt")
carhig_box_fllt.Placement.Base = FreeCAD.Vector (0,0, CAR_Z)


# ------------------- Inner rectangle hole for the lower extruder holder

INRECT_X = EXTR_HOLD_X + 2*TOL # 2* TOL, for each side
# x2 because the holder is half on Y, and since they are 2, also the tolerances
INRECT_Y = 2.0 * (EXTR_HOLD_Y + TOL)
inrect = addBox (INRECT_X, INRECT_Y, CAR_Z+2, "inrect")

inrect_pos = FreeCAD.Vector(-INRECT_X/2.0, -INRECT_Y/2.0, -1)

inrect.Placement = FreeCAD.Placement(inrect_pos, V0ROT, V0) 

# fillet the inner rectangles. The radius has - tolerance because it is the
# outer
# we don't fillet it, because the extruder holders aren't either
#inrect_fllt = fillet_len (inrect, CAR_Z+2, EXTR_HOLD_FLLT_R-TOL, "inrect_fllt")

# holes for the lower carriage
holes_lowcar_list = []
#holes_list.append(inrect_fllt)
holes_lowcar_list.append(inrect)
# holes for the higher carriage
holes_higcar_list = []

# rectangle for the upper carriage, because the extruder holder is a little
# bit lower

if (CAR_Z - EXTR_HOLD_Z) > TOL :
    extrhold_higcar = addBox (EXTR_HOLD_X,
                              2*EXTR_HOLD_Y,
                              CAR_Z - EXTR_HOLD_Z -TOL +1,
                              "extrhold_higcar")
    extrhold_higcar.Placement.Base = FreeCAD.Vector (-EXTR_HOLD_X/2.0,
                                                     -EXTR_HOLD_Y,
                                                      EXTR_HOLD_Z+TOL)
    carhig_fuse = doc.addObject("Part::Fuse", "carghig_fuse")
    carhig_fuse.Base = carhig_box_fllt
    carhig_fuse.Tool = extrhold_higcar
else: # if it is less than the tolerance, we don't do it
    carhig_fuse = carhig_box_fllt
 

# ------------------- Rod holes

rod_p = addCyl(ROD_DIAM_SPACE/2.0, CAR_X+2, "rod_p")
rod_p_pos = FreeCAD.Vector(-CAR_X/2.0-1, ROD_SEP/2.0, CAR_Z)
rod_p.Placement = FreeCAD.Placement (rod_p_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)

rod_n = addCyl(ROD_DIAM_SPACE/2.0, CAR_X+2, "rod_n")
rod_n_pos = FreeCAD.Vector(-CAR_X/2.0-1, -ROD_SEP/2.0, CAR_Z)
rod_n.Placement = FreeCAD.Placement (rod_n_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)

holes_lowcar_list.append(rod_n)
holes_lowcar_list.append(rod_p)
holes_higcar_list.append(rod_n)
holes_higcar_list.append(rod_p)

# -------------------- Bearing holes

""" # better with a loop
bearing_1 = addCyl(BEARING_D_TOL/2.0, BEARING_L_TOL, "bearing_1")
bearing_1_pos = FreeCAD.Vector(OUT_SEP/2.0, ROD_SEP/2.0, CAR_Z)
bearing_1.Placement = FreeCAD.Placement (bearing_1_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)
bearing_2 = addCyl(BEARING_D_TOL/2.0, BEARING_L_TOL, "bearing_2")
bearing_2_pos = FreeCAD.Vector(-OUT_SEP/2.0 - BEARING_L_TOL, ROD_SEP/2.0, CAR_Z)
bearing_2.Placement = FreeCAD.Placement (bearing_2_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)
bearing_3 = addCyl(BEARING_D_TOL/2.0, BEARING_L_TOL, "bearing_3")
bearing_3_pos = FreeCAD.Vector(OUT_SEP/2.0, -ROD_SEP/2.0, CAR_Z)
bearing_3.Placement = FreeCAD.Placement (bearing_3_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)
bearing_4 = addCyl(BEARING_D_TOL/2.0, BEARING_L_TOL, "bearing_4")
bearing_4_pos = FreeCAD.Vector(-OUT_SEP/2.0 - BEARING_L_TOL, -ROD_SEP/2.0, CAR_Z)
bearing_4.Placement = FreeCAD.Placement (bearing_4_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)
"""

for i in range (4):
    bearing = addCyl(BEARING_D_TOL/2.0, BEARING_L_TOL, "bearing_" + str(i))
    if i % 2 == 0: # is even, 0, 2
      x_bearing = OUT_SEP_X/2.0
    else:
      x_bearing = - OUT_SEP_X/2.0 - BEARING_L_TOL
    if i == 0 or i == 1:
      y_bearing = ROD_SEP/2.0
    else:
      y_bearing = -ROD_SEP/2.0
    bearing_pos = FreeCAD.Vector(x_bearing, y_bearing, CAR_Z)
    bearing.Placement = FreeCAD.Placement (bearing_pos,
                                           FreeCAD.Rotation(VY,90),
                                           V0)
    holes_lowcar_list.append(bearing)
    holes_higcar_list.append(bearing)


#  -----------------------holes for the upper carriage,
# ---------------- to be able to introduce the filament
# radius is +1, to make it a little bit larger
higcar_fil_hole_z = 2*CAR_Z - EXTR_HOLD_Z + 2 
higcar_fil_hole1 = addCyl (r=(EXTR_OUT_D/2.0) +1, h=higcar_fil_hole_z,
                          name="higcar_fil_hole1");
higcar_fil_hole2 = addCyl (r=(EXTR_OUT_D/2.0) +1, h=higcar_fil_hole_z,
                          name="higcar_fil_hole2");
higcar_fil_hole1.Placement.Base = FreeCAD.Vector ( EXTR_SEP/2.0,
                                                   0,
                                                   EXTR_HOLD_Z-1)
higcar_fil_hole2.Placement.Base = FreeCAD.Vector (-EXTR_SEP/2.0,
                                                   0,
                                                   EXTR_HOLD_Z-1)

holes_higcar_list.append(higcar_fil_hole1)
holes_higcar_list.append(higcar_fil_hole2)

# ---------------------- adding M3 bolts

# bolt to attach both extruder holders

# a M3 DIN 912 bolt with L=20 is going to be used,
# the total is 20 + l_head = 20+3= 23
# the total hole is 2*EXTR_HOLD_Y = 2*11,8 = 23,6
# So we make the l_nut = M3_NUT_L + (2*EXTR_HOLD_Y - 23)

bolt20m3_length = 20 + M3_HEAD_L
if (2*EXTR_HOLD_Y < bolt20m3_length):
    print ("Error in extruder holder Y dimension: " + str(2*EXTR_HOLD_Y) 
           + " have to be larger than bolt length: " + str(bolt20m3_length) )
boltextr_lnut = M3_NUT_L + (2*EXTR_HOLD_Y - bolt20m3_length)


boltextr = addBoltNut_hole (r_shank   = M3_SHANK_R_TOL,
                            l_bolt    = 2 * EXTR_HOLD_Y,
                            r_head    = M3_HEAD_R_TOL,
                            l_head    = M3_HEAD_L,
                            r_nut     = M3_NUT_R_TOL,
                            l_nut     = boltextr_lnut,
                            hex_head  = 0, extra=1,
                            supp_head = 1, supp_nut=1,
                            headdown  = 1, name="m3_extrbolt_hole")

boltextr.Placement.Base = FreeCAD.Vector (0, EXTR_HOLD_Y, EXTR_HOLD_Z/2)
boltextr.Placement.Rotation = FreeCAD.Rotation (VX, 90)
extr_holder_holes_list.append (boltextr)

# center bolts: only for upper carriage and extruder holder
m3bolts_center = [] 
for i in range (0, 2): # 0 and 1
    # create 2 central bolt holes
    boltcen = addBoltNut_hole (r_shank   = M3_SHANK_R_TOL,
                            l_bolt    = 2 * CAR_Z,
                            r_head    = M3_HEAD_R_TOL,
                            l_head    = M3_HEAD_L,
                            r_nut     = M3_NUT_R_TOL,
                            l_nut     = M3_NUT_L,
                            hex_head  = 0, extra=1,
                            # extruder holder printed vertically, nosupport nut
                            supp_head = 1, supp_nut=0,
                            headdown  = 0, name="m3_bolt_hole")
    if i == 0:
        m3bolt_x = (EXTR_HOLD_X / 2.0) - (extr_hold_tab_x/2.0)
    else:
        # the previous value, but negative
        m3bolt_x =  - m3bolt_x
    m3bolt_y = 0
    # rotation to have more space on the X axis. Get the apotheme
    #bolt_rot = FreeCAD.Rotation (VZ, 30)
    bolt_rot = FreeCAD.Rotation (VZ, 0) # no rotation
    bolt_pos = FreeCAD.Vector(m3bolt_x, m3bolt_y, 0)
    boltcen.Placement = FreeCAD.Placement (bolt_pos, bolt_rot, V0)
    m3bolts_center.append (boltcen)

extr_holder_holes_list.extend (m3bolts_center)
holes_higcar_list.extend (m3bolts_center)

m3bolts_sides  = [] # for lower and upper carriage
for i in range (1, 7):  # 1 to 6
    boltsid = addBoltNut_hole (r_shank   = M3_SHANK_R_TOL,
                            l_bolt    = 2 * CAR_Z,
                            r_head    = M3_HEAD_R_TOL,
                            l_head    = M3_HEAD_L,
                            r_nut     = M3_NUT_R_TOL,
                            l_nut     = M3_NUT_L,
                            hex_head  = 0, extra=1,
                            supp_head = 1, supp_nut=1,
                            headdown  = 0, name="m3_bolt_hole")

    if i < 4 : # on positive Y
        m3bolt_y = CAR_Y/2.0 - OUT_SEP/2.0
    else:
        m3bolt_y = - (CAR_Y/2.0 - OUT_SEP/2.0)
    if i % 3 == 1:
        m3bolt_x = CAR_X/2.0 - OUT_SEP_X/2.0
    elif i % 3 == 2:
        m3bolt_x = 0
    else:
        m3bolt_x = -(CAR_X/2.0 - OUT_SEP_X/2.0)
    m3bolts_sides.append (boltsid)
    bolt_rot = FreeCAD.Rotation (VZ, 0) # no rotation

    bolt_pos = FreeCAD.Vector(m3bolt_x, m3bolt_y, 0)
    boltsid.Placement = FreeCAD.Placement (bolt_pos, bolt_rot, V0)

# list to substract the bolt holes to the lower carriage
# use extend instead of append, so the m3bolts is not appended as a list
# but appended each element
holes_lowcar_list.extend (m3bolts_sides)
holes_higcar_list.extend (m3bolts_sides)



# --------------------------- belt clamp and tensioner
# radius of the cylinder
"""                           
          TOPVIEW                    
                CLAMPBLOCK          
                    CB             
                    ____     
           CB_W  {  XXXX       ___
           CB_IW {  ____      /   \
 0,1 or 2: CB_MW {  XXXX      |   |   CCYL: CLAMPCYL 
           CB_IW {  ____      \___/
           CB_W  {  XXXX     
        
                    CB_L  CS


    Y A  (width)
      |
      |---> X (length)

  arguments:

  midblock: 0 or 1. It will add a none/single width middle block
                    In the future I may consider a double middle block (2)

"""


class Gt2BeltClamp:

    # space for the 2 belts to clamp them
    # the GT2 belt is 1.38mm width. 2 together facing teeth will be about 2mm
    # I make it 2.8mm
    # Internal Width of the Clamp Block
    CB_IW = 2.8
    # Width of the exterior clamp blocks (Y axis)
    CB_W = 4.0
    # Length of the clamp blocks (X axis)
    CB_L = 12.0
    # GT2 height is 6 mm, making the heigth 8mm
    C_H = 8.0
    # GT2 Clamp Cylinder radius
    CCYL_R = 4.0
    # separation between the clamp blocks and the clamp cylinder
    CS = 3.0


    """
    how much the rail is inside

     ________________________________________________    
    |        
    |   __________________________
     \                        ____ CBASERAILIND 
      |       
     /  _____ CBASE_RAIL ___
    |
    |_________________________ CBASE_WALL _________ CBASE_H

    |-|
      CBASERAILIND_SIG (it is 45 degrees). SIG: can be + or -

    if midblock > 0 this will be the indentation, 
    if midblock == 0 it will be outward, like this:
        _________
       |         |
      /           \ 
     |             |
      \           /
       |_________|
      
    """
  
    # Clamp base
    CBASE_H = CAR_Z
    CBASE_L = CB_L + CS + 2*CCYL_R
    # divides how much is rail and how much is wall
    # It has to be greater than 1. If it is 1, there is no wall.
    # if it is 2. Half is wall, half is indent
    CBASE_RAIL_DIV = 1.6 #2.0
    CBASE_RAIL = CBASE_H / CBASE_RAIL_DIV # rail for the base
    # the part that is wall, divided by 2, because one goes at the bottom
    # and the other on top
    CBASE_WALL = (CBASE_H - CBASE_RAIL)/2.0 # rail for the base
    # Indentation, if midblock == 0, the Indentation is negative, which means
    # it will be outward, otherwise, inward
    CBASERAILIND = CBASE_RAIL/3.0

    def __init__(self, midblock, name):
        self.midblock = midblock
        # Width of the interior/middle clamp blocks
        self.CB_MW = midblock * self.CB_W
        if midblock == 0:
            self.CBASE_W =     self.CB_IW + 2 * self.CB_W 
            self.CBASERAILIND_SIG = - self.CBASERAILIND 
            # Since the indentation is outwards, we have to add it
            self.TotW = self.CBASE_W + 2 *  self.CBASERAILIND
            # external indent, so all the internal elements have to have this
            # nternal offset. In Y axis
            self.extind = self.CBASERAILIND 
        else:
            self.CBASE_W = 2 * self.CB_IW + 2 * self.CB_W + self.CB_MW
            self.CBASERAILIND_SIG = self.CBASERAILIND 
            # Since the indentation is inward, it is just the base
            self.TotW = self.CBASE_W 
            # no external indent, so the internal elements don't have to have 
            # this internal offset
            self.extind = 0
  
        gt2_clamp_list = []
        # we make it using points-plane and extrusions
        #gt2_base =addBox (self.CBASE_L, self.CBASE_W, self.CBASE_H, "gt2_base")
        gt2_cb_1 = addBox (self.CB_L, self.CB_W, self.C_H+1, name + "_cb1")
        gt2_cb_1.Placement.Base = FreeCAD.Vector (self.CBASE_L-self.CB_L,
                                                  self.extind,
                                                  self.CBASE_H-1)
        gt2_clamp_list.append (gt2_cb_1)
        if midblock > 0:
          gt2_cb_2 = addBox (self.CB_L, self.CB_MW, self.C_H+1, name + "_cb2")
          gt2_cb_2.Placement.Base = FreeCAD.Vector (self.CBASE_L-self.CB_L,
		                                   self.CB_W + self.CB_IW + self.extind,
		                                   self.CBASE_H-1)
          gt2_clamp_list.append (gt2_cb_2)

        gt2_cb_3 = addBox (self.CB_L, self.CB_W, self.C_H + 1, name + "_cb3")
        gt2_cb_3.Placement.Base = FreeCAD.Vector (self.CBASE_L-self.CB_L,
                                        self.CBASE_W - self.CB_W + self.extind,
		                                self.CBASE_H-1)
        gt2_clamp_list.append (gt2_cb_3)
 
        gt2_cyl = addCyl (self.CCYL_R,  self.C_H + 1, name + "_cyl")
        gt2_cyl.Placement.Base = FreeCAD.Vector (self.CCYL_R, 
                                             self.CBASE_W/2 + self.extind,
                                             self.CBASE_H-1)
        gt2_clamp_list.append (gt2_cyl)

        # base
        # calling to the method that gets a list of the points to make 
        # the polygon of the base
        #gt2_base_list = self.get_base_list_v()
        # doing this because the carriage is already printed, so I am going
        # to make the base smaller to fit. CHANGE to the upper sentence
        gt2_base_list = self.get_base_list_v(offs_y = -TOL/2, offs_z = - TOL)
        """
        gt2_base_plane_yz = Part.makePolygon(gt2_base_list)
        gt2_base = gt2_base_plane_xy.extrude(FreeCAD.Vector(self.CBASE_L,0,0))
        """
        gt2_base_plane_yz = doc.addObject("Part::Polygon",
                                           name + "base_plane_yz")
        gt2_base_plane_yz.Nodes = gt2_base_list
        gt2_base_plane_yz.Close = True
        gt2_base = doc.addObject("Part::Extrusion",
                                           name + "extr_base")
        gt2_base.Base = gt2_base_plane_yz
        gt2_base.Dir = (self.CBASE_L,0,0)
        gt2_base.Solid = True

        gt2_clamp_list.append(gt2_base)

        gt2_clamp_basic = doc.addObject("Part::MultiFuse", name + "clamp_base")
        gt2_clamp_basic.Shapes = gt2_clamp_list

        # creation of the same base, but with a little offset to be able to 
        # cut the piece where it will be inserted
        #gt2_baseof_list = self.get_base_list_v(offs_y = TOL, offs_z = TOL/2.0)
        # CHANGE TO THE UPPER SENTENCE
        gt2_baseof_list = self.get_base_list_v(offs_y = TOL, offs_z = 0)
        gt2_baseof_plane_yz = doc.addObject("Part::Polygon",
                                           name + "_baseof_plane_yz")
        gt2_baseof_plane_yz.Nodes = gt2_baseof_list
        gt2_baseof_plane_yz.Close = True
        gt2_baseof = doc.addObject("Part::Extrusion",
                                   name + "_baseof")
        gt2_baseof.Base = gt2_baseof_plane_yz
        gt2_baseof.Dir = (self.CBASE_L,0,0)
        gt2_baseof.Solid = True

        self.BaseOffset = gt2_baseof

        # hole for the leadscrew bolt
        # the head is longer because it can be inserted deeper into the piece
        # so a shorter bolt will be needed
        gt2_base_lscrew = addBolt (M3_SHANK_R_TOL, self.CBASE_L,
                                   M3_HEAD_R_TOL, 2.5*M3_HEAD_L,
                                   extra = 1, support = 0,
                                   name= name + "_base_lscrew")
    
        gt2_base_lscrew.Placement.Base = FreeCAD.Vector (self.CBASE_L,
                                                self.CBASE_W/2.0 + self.extind,
                                                self.CBASE_H/2.0)
        gt2_base_lscrew.Placement.Rotation = FreeCAD.Rotation (VY, -90)

        # ------------ hole for a nut, also M3, for the leadscrew 
        gt2_base_lscrew_nut = doc.addObject("Part::Prism", 
                                            name + "_base_lscrew_nut")
        gt2_base_lscrew_nut.Polygon = 6
        gt2_base_lscrew_nut.Circumradius = M3_NUT_R_TOL
        gt2_base_lscrew_nut.Height = M3NUT_HOLE_H 
        gt2_base_lscrew_nut.Placement.Rotation = \
                                      gt2_base_lscrew.Placement.Rotation 
                  # + TOL so it will be a little bit higher, so more room
        gt2_base_lscrew_nut.Placement.Base = FreeCAD.Vector (
                              #(self.CBASE_L-M3_HEAD_L)/2.0 - M3NUT_HOLE_H/2.0,
                               NUT_HOLE_EDGSEP,
                               self.CBASE_W/2.0 + self.extind,
                               self.CBASE_H/2.0 + TOL) 
        gt2_base_lscrew_nut.Placement.Rotation = FreeCAD.Rotation (VY, 90)
        # ------------ hole to reach out the nut hole
 
        # X is the length: M3NUT_HOLE_H. Y is the width. M3_2APOT_TOL
        gt2_base_lscrew_nut2 = addBox (M3NUT_HOLE_H,
                                       M3_2APOT_TOL,
                                       self.CBASE_H/2.0 + TOL,
                                       name + "_base_lscrew_nut2")
        gt2_base_lscrew_nut2.Placement.Base = (
                              #((self.CBASE_L-M3_HEAD_L) - M3NUT_HOLE_H)/2.0,
                               NUT_HOLE_EDGSEP,
                               (self.CBASE_W - M3_2APOT_TOL)/2.0 + self.extind,
                                0)

        gt2_base_holes_l = [ gt2_base_lscrew,
                             gt2_base_lscrew_nut,
                             gt2_base_lscrew_nut2]

        # fuse the holes
        gt2_clamp_holes = doc.addObject("Part::MultiFuse", name + "_clamp_hole")
        gt2_clamp_holes.Shapes = gt2_base_holes_l
        # Substract the holes 
        gt2_clamp = doc.addObject("Part::Cut", name)
        gt2_clamp.Base = gt2_clamp_basic
        gt2_clamp.Tool = gt2_clamp_holes

        self.CadObj = gt2_clamp

    # --------------------------------------------------------------------
    # obtains the list of vectors for the base of the clamp
    # offs_y: if zero it takes normal points
    # offs_z added because it didn't fit
    # offs_z: if zero it takes normal points
    #  CBASERAILIND_SIG <0:              CBASERAILIND_SIG > 0
    #  lv5         _________               ___________
    #  lv4        |         |             |
    #  lv3       /           \             \ 
    #  lv2      |             |             |
    #  lv1       \           /             / 
    #  lv0        |_________|             |_
    #         
    #
    #
    def get_base_list_v(self, offs_y = 0, offs_z = 0):

        if self.CBASERAILIND_SIG < 0:
            offs_zsig = - offs_z
        else:
            offs_zsig =  offs_z

        # Points that make the shape of the base
        # left side (offs is negative
        gt2_base_lv00 = FreeCAD.Vector (0,
                                        0 - offs_y,
                                        0)
        # offs_z higher when CBASERAILIND_SIG > 0
        gt2_base_lv01 = FreeCAD.Vector (0,
                                        0 - offs_y,
                                        self.CBASE_WALL + offs_zsig)
        gt2_base_lv02 = FreeCAD.Vector (
                                0,
                                self.CBASERAILIND_SIG - offs_y,
                                self.CBASE_WALL + self.CBASERAILIND + offs_zsig)
        # offs_z negative (lower)
        gt2_base_lv03 = FreeCAD.Vector (0,
                            self.CBASERAILIND_SIG - offs_y,
                            self.CBASE_WALL + 2*self.CBASERAILIND - offs_zsig)
        gt2_base_lv04 = FreeCAD.Vector (0,0 - offs_y,
                                self.CBASE_WALL + self.CBASE_RAIL - offs_zsig)
        gt2_base_lv05 = FreeCAD.Vector (0,0 - offs_y,
                                        self.CBASE_H)
        # right side (offs_y is positive
        gt2_base_rv00 = FreeCAD.Vector (0,
                                        self.CBASE_W + offs_y,
                                        0)
        gt2_base_rv01 = FreeCAD.Vector (0,
                                        self.CBASE_W + offs_y,
                                        self.CBASE_WALL + offs_zsig)
        gt2_base_rv02 = FreeCAD.Vector (0,
                               self.CBASE_W - self.CBASERAILIND_SIG + offs_y,
                               self.CBASE_WALL + self.CBASERAILIND + offs_zsig)
        gt2_base_rv03 = FreeCAD.Vector (0,
                             self.CBASE_W - self.CBASERAILIND_SIG + offs_y,
                             self.CBASE_WALL + 2*self.CBASERAILIND - offs_zsig)
        gt2_base_rv04 = FreeCAD.Vector (0,
                             self.CBASE_W + offs_y,
                             self.CBASE_WALL + self.CBASE_RAIL - offs_zsig)
        gt2_base_rv05 = FreeCAD.Vector (0,
                                        self.CBASE_W + offs_y,
                                        self.CBASE_H)
    
        gt2_base_list = [
                         gt2_base_lv00,
                         gt2_base_lv01,
                         gt2_base_lv02,
                         gt2_base_lv03,
                         gt2_base_lv04,
                         gt2_base_lv05,
                         gt2_base_rv05,
                         gt2_base_rv04,
                         gt2_base_rv03,
                         gt2_base_rv02,
                         gt2_base_rv01,
                         gt2_base_rv00
                        ]

        # if it is negative, the indentation will be outwards, so we will
        # make the Y=0 on the most outward point, except for the offs_y
        # that will be negative when Y=0
        if self.CBASERAILIND_SIG < 0:
            addofs = FreeCAD.Vector (0, - self.CBASERAILIND_SIG,0)
            gt2_base_list = [x + addofs for x in gt2_base_list]

        return gt2_base_list
    
# end class Gt2BeltClamp:


# ------------------   Belt clamp
# h: the handler of the freecad object
h_gt2clamp0 =  Gt2BeltClamp (midblock =0, name="gt2clamp0")
gt2clamp0 = h_gt2clamp0.CadObj 
BELT_CLAMP_SEP = 2.4
gt2clamp0.Placement.Base = FreeCAD.Vector (CAR_X / 2, BELT_CLAMP_SEP/2, CAR_Z)

# offset of the base
gt2clamp0_of = h_gt2clamp0.BaseOffset 
#gt2clamp0_of.Placement.Base = gt2clamp0.Placement.Base

# the other belt clamp
h_gt2clamp1 =  Gt2BeltClamp (midblock =0, name="gt2clamp1")
gt2clamp1 = h_gt2clamp1.CadObj 
gt2clamp1.Placement.Base = FreeCAD.Vector (CAR_X / 2,
                                         -BELT_CLAMP_SEP/2 - h_gt2clamp1.TotW,
                                          CAR_Z)

# offset of the base
gt2clamp1_of = h_gt2clamp1.BaseOffset 
#gt2clamp1_of.Placement.Base = gt2clamp1.Placement.Base

#h_gt2clamp1 =  Gt2BeltClamp (midblock =1, name="gt2clamp1")

# --------------------------- Belt Clamp Carriage Rails BCCR
# they are a part of the lower carriage
# I will put the bolt head on the BCCR not on the moving belt clamp

# the space between the rods. ROD_DIAM_SPACE is a little bit longer than
# ROD_DIAM, so it will not touch the rods
BCCR_Y = ROD_SEP - ROD_DIAM_SPACE
# how large we want the run of the belt clamp to be, on the X direction
# M3 DIN912 bolts have thread length of 18mm. So it can't be longer
BCCR_RUN = 15 
# the support of the nut. We take the same dimensions as in the belt clamp
# the nut will be on the moving part
#BCCR_NUT_SUP_X = 2*NUT_HOLE_EDGSEP + M3NUT_HOLE_H
BCCR_NUT_SUP_X = NUT_HOLE_EDGSEP 
BCCR_X =  h_gt2clamp1.CBASE_L + BCCR_RUN + BCCR_NUT_SUP_X

bccr_box = addBox (BCCR_X, BCCR_Y, 2 * CAR_Z, "bccr_box")
bccr_box.Placement.Base = FreeCAD.Vector (CAR_X/2.0 - 0.7*OUT_SEP_X,
                                          -BCCR_Y/2.0,
                                          0)
bccr_fllt = fillet_len (bccr_box, 2*CAR_Z, CAR_FLLT_R, "bccr_fllt")

# a similar bccr_box, but bigger (with offset) to cut it to the higcar
bccr_box_of = addBox (BCCR_X, BCCR_Y + 2*TOL, 2 * CAR_Z, "bccr_box")
bccr_box_of.Placement.Base = FreeCAD.Vector (CAR_X/2.0 - 0.7*OUT_SEP_X - TOL,
                                             -BCCR_Y/2.0 - TOL,
                                             0)

"""
This rotation will not work
bccr_box_of_clone = Draft.clone(bccr_box_of)
bccr_box_of_clone.Placement.Rotation = FreeCAD.Rotation (VZ,180)
holes_higcar_list.append(bccr_box_of_clone)
"""

# Taking away a small indent that results from cutting bccr_box_of
bccr_box_of_clean = addBox (BCCR_X, ROD_SEP, ROD_DIAM_SPACE/2.0,
                            "bccr_box_of_clean")
bccr_box_of_clean.Placement.Base = FreeCAD.Vector (
                                              CAR_X/2.0 - 0.7*OUT_SEP_X - TOL,
                                             -ROD_SEP/2.0,
                                              CAR_Z)
# If I fuse them, then I can clone and just rotate. Because the new object
# will be in absolute position (0,0,0)
fuse_bccr_box_of = doc.addObject("Part::Fuse", "fuse_bccr_box_of")
fuse_bccr_box_of.Base = bccr_box_of
fuse_bccr_box_of.Tool = bccr_box_of_clean

#holes_higcar_list.append(bccr_box_of_clean)
holes_higcar_list.append(fuse_bccr_box_of)

fuse_bccr_box_of_clone = Draft.clone(fuse_bccr_box_of)
# I can do this rotation because they have been fused
fuse_bccr_box_of_clone.Placement.Rotation = FreeCAD.Rotation (VZ,180)
holes_higcar_list.append(fuse_bccr_box_of_clone)

# Holes on the higher carriage to make space to introduce the bolts that
# are used as leadscrews for the belt clamps

# From the center of the circle of the extruders
higcar_lscrew_hole_x = bccr_box_of_clean.Placement.Base.x - EXTR_SEP/2.0 + 1
# +1 as tolerance
higcar_lscrew_hole_y = 2 * M3_HEAD_R + 2
# +1 as tolerance, +1 tu cut above
higcar_lscrew_hole_z = CAR_Z / 2.0 + M3_HEAD_R + 1 + 1

higcar_lscrew_hole_pos_x = (  bccr_box_of_clean.Placement.Base.x 
                            - higcar_lscrew_hole_x +1)
higcar_lscrew_hole_pos_y = (  BELT_CLAMP_SEP /2.0
                            + h_gt2clamp1.TotW/2.0
                            - higcar_lscrew_hole_y/2.0)
higcar_lscrew_hole_pos_z = 2 * CAR_Z - higcar_lscrew_hole_z + 1

higcar_lscrew_hole0 = addBox ( higcar_lscrew_hole_x,
                               higcar_lscrew_hole_y,
                               higcar_lscrew_hole_z,
                               "highcar_lscrew_hole0")

higcar_lscrew_hole0.Placement.Base = FreeCAD.Vector (
                                        higcar_lscrew_hole_pos_x,
                                        higcar_lscrew_hole_pos_y,
                                        higcar_lscrew_hole_pos_z)

higcar_lscrew_hole1 = addBox ( higcar_lscrew_hole_x,
                               higcar_lscrew_hole_y,
                               higcar_lscrew_hole_z,
                               "highcar_lscrew_hole1")

higcar_lscrew_hole1.Placement.Base = FreeCAD.Vector (
                              higcar_lscrew_hole_pos_x,
                             -higcar_lscrew_hole_pos_y - higcar_lscrew_hole_y,
                              higcar_lscrew_hole_pos_z)

higcar_lscrew_fuse = doc.addObject("Part::Fuse", "higcar_lscrew_fuse")
higcar_lscrew_fuse.Base = higcar_lscrew_hole0
higcar_lscrew_fuse.Tool = higcar_lscrew_hole1

higcar_lscrew_fuse_clone = Draft.clone(higcar_lscrew_fuse)
higcar_lscrew_fuse_clone.Placement.Rotation = FreeCAD.Rotation (VZ,180)

holes_higcar_list.append(higcar_lscrew_fuse)
holes_higcar_list.append(higcar_lscrew_fuse_clone)

# Make the length of the gt2clamp_of (offset of the base) to cut the whole
# Belt Clamp Carriage Rail. Make it as long as the BCCR

gt2clamp0_of.Dir = (BCCR_X - BCCR_NUT_SUP_X + 1, 0 , 0)
gt2clamp0_of.Placement.Base = FreeCAD.Vector (
                                   # leaving the space for the nut
                                   bccr_box.Placement.Base.x + BCCR_NUT_SUP_X,
                                   gt2clamp0.Placement.Base.y,
                                   gt2clamp0.Placement.Base.z )

gt2clamp1_of.Dir = (BCCR_X - BCCR_NUT_SUP_X + 1, 0 , 0)
gt2clamp1_of.Placement.Base = FreeCAD.Vector (
                                   # leaving the space for the nut
                                   bccr_box.Placement.Base.x + BCCR_NUT_SUP_X,
                                   gt2clamp1.Placement.Base.y,
                                   gt2clamp1.Placement.Base.z )

# ---- Bottom Hole to be able to see from below
bccr_bthole0 = addBox (BCCR_X - 2 * NUT_HOLE_EDGSEP,
                       M3_2APOT_TOL, # to see the nut 
                       CAR_Z + 2 ,
                        "bccr_bthole0", cy=1)
# small fillet, radius 2
bccr_bthole0_fllt = fillet_len (bccr_bthole0, CAR_Z +2, 2, "bccr_bthole0_fllt")
bccr_bthole0_fllt.Placement.Base = FreeCAD.Vector (
                     bccr_box.Placement.Base.x + NUT_HOLE_EDGSEP,
                     gt2clamp0.Placement.Base.y + h_gt2clamp0.TotW / 2.0,
                     -1)

# ---- the other Bottom Hole to be able to see from below
bccr_bthole1 = addBox (BCCR_X - 2 * NUT_HOLE_EDGSEP,
                       M3_2APOT_TOL, # to see the nut 
                       CAR_Z + 2 ,
                        "bccr_bthole1", cy=1)
# small fillet, radius 2
bccr_bthole1_fllt = fillet_len (bccr_bthole1, CAR_Z +2, 2, "bccr_bthole1_fllt")
bccr_bthole1_fllt.Placement.Base = FreeCAD.Vector (
                     bccr_box.Placement.Base.x + NUT_HOLE_EDGSEP,
                     gt2clamp1.Placement.Base.y + h_gt2clamp1.TotW / 2.0,
                     -1)
# fuse these holes, to be able to clone them and easily rotate them

bccr_bthole_fused = doc.addObject("Part::Fuse", "bccr_bthole_fused")
bccr_bthole_fused.Base = bccr_bthole0_fllt
bccr_bthole_fused.Tool = bccr_bthole1_fllt


# clone these holes
bccr_bthole_fused_clone = Draft.clone(bccr_bthole_fused)
bccr_bthole_fused_clone.Placement.Rotation = FreeCAD.Rotation (VZ,180)

# Hole for the bolt

bccr_bolthole0 = addCyl (r = M3_SHANK_R_TOL, h = NUT_HOLE_EDGSEP + 2,
                         name = "bccr_bolthole0")
bccr_bolthole0.Placement.Base = FreeCAD.Vector (
                         bccr_box.Placement.Base.x -1,
                         gt2clamp0.Placement.Base.y + h_gt2clamp0.TotW / 2.0,
                         CAR_Z + h_gt2clamp0.CBASE_H/2.0)
bccr_bolthole0.Placement.Rotation = FreeCAD.Rotation (VY, 90)

bccr_bolthole1 = addCyl (r = M3_SHANK_R_TOL, h = NUT_HOLE_EDGSEP + 2,
                         name = "bccr_bolthole1")
bccr_bolthole1.Placement.Base = FreeCAD.Vector (
                         bccr_box.Placement.Base.x -1,
                         gt2clamp1.Placement.Base.y + h_gt2clamp1.TotW / 2.0,
                         CAR_Z + h_gt2clamp1.CBASE_H/2.0)
bccr_bolthole1.Placement.Rotation = FreeCAD.Rotation (VY, 90)

bccr_holes_list = [gt2clamp0_of, gt2clamp1_of,
                   bccr_bthole0_fllt, bccr_bthole1_fllt, 
                   bccr_bolthole0, bccr_bolthole1 ]

# these need to be added also to the lowcarriage
holes_lowcar_list.append(bccr_bthole_fused)
holes_lowcar_list.append(bccr_bthole_fused_clone)

# union of all the bccr holes
bccr_holes = doc.addObject("Part::MultiFuse", "bccr_holes")
bccr_holes.Shapes = bccr_holes_list

bccr_final = doc.addObject("Part::Cut", "bccr_final")
bccr_final.Base = bccr_fllt
bccr_final.Tool = bccr_holes

bccr_final_clone = Draft.clone(bccr_final )
bccr_final_clone.Placement.Rotation = FreeCAD.Rotation (VZ,180)




""" No nut hole

h_bccr_nuthole0 = NutHole (nut_r  = M3_NUT_R_TOL,
                           nut_h  = M3NUT_HOLE_H,
                           # + TOL to have a little bit more room for the nut
                           hole_h = h_gt2clamp0.CBASE_H/2.0 + TOL, 
                           name   = "bccr_nuthole0",
                           extra  = 1,
                           # the height of the nut on the X axis
                           x_nut_h = 1,
                           cx = 0, # not centered on x
                           cy = 1, # centered on y, on the center of the hexagon
                           holedown = 0)

bccr_nuthole0 = h_bccr_nuthole0.CadObj

bccr_nuthole0.Placement.Base = FreeCAD.Vector (
                         bccr_box.Placement.Base.x + NUT_HOLE_EDGSEP,
                         gt2clamp0.Placement.Base.y + h_gt2clamp0.TotW / 2.0,
                         # minus TOL because the hole is on top
                         CAR_Z + h_gt2clamp0.CBASE_H/2.0 - TOL)
"""

                         
              

"""
# ------------ hole for a nut, also M3, for the leadscrew 
bccr_nut0 = doc.addObject("Part::Prism", "bccr_nut0")
bccr_nut0.Polygon = 6
bccr_nut0.Circumradius = M3_NUT_R_TOL
bccr_nut0.Height = M3NUT_HOLE_H 
bccr_nut0.Placement.Rotation = gt2_base_lscrew.Placement.Rotation 
bccr_nut0.Placement.Base = FreeCAD.Vector (
                         bccr_box.Placement.Base.x + NUT_HOLE_EDGSEP,
                         gt2clamp0.Placement.Base.y + h_gt2clamp0.TotW / 2.0,
                         CARZ + gt2clamp0.CBASE_H/2.0 + TOL)
        
# ------------ hole to reach out the nut hole
# X is the length: M3NUT_HOLE_H. Y is the width. M3_2APOT_TOL
bccr_nuthole0 = addBox (M3NUT_HOLE_H,
                        M3_2APOT_TOL,
                        gt2clamp0.CBASE_H/2.0 + TOL,
                        "bccr_nuthole0")
bccr_nuthole0.Placement.Base = (
       bccr_box.Placement.Base.x + NUT_HOLE_EDGSEP,
       gt2clamp0.Placement.Base.y + h_gt2clamp0.TotW / 2.0 - M3_2APOT_TOL/2.0,
       CARZ + gt2clamp0.CBASE_H/2.0 + TOL)

     gt2_base_holes_l = [ gt2_base_lscrew,
                             gt2_base_lscrew_nut,
                             gt2_base_lscrew_nut2]
"""


# --------------------------- Union and Cut of all the holes
# --------------------- extruder holder holes --------------------


fuse_extr_holder_holes = doc.addObject("Part::MultiFuse", 
                                       "fuse_extr_holder_holes")
fuse_extr_holder_holes.Shapes = extr_holder_holes_list

# cut the holes for the extruder holders

tot_extr_hold_1 = doc.addObject("Part::Cut", "tot_extr_hold_1")
#tot_extr_hold_1.Base = extr_hold_1_fllt
tot_extr_hold_1.Base = extr_hold1_joint
tot_extr_hold_1.Tool = fuse_extr_holder_holes
        
tot_extr_hold_2 = doc.addObject("Part::Cut", "tot_extr_hold_2")
#tot_extr_hold_2.Base = extr_hold_2_fllt
tot_extr_hold_2.Base = extr_hold2_joint
tot_extr_hold_2.Tool = fuse_extr_holder_holes


""" the refinement is not working
# refine the shape
tot_extr_hold_1ref = doc.addObject("Part::Feature", "tot_extr_hold1_ref")
tot_extr_hold_1ref.Shape = tot_extr_hold_1.Shape.removeSplitter()
tot_extr_hold_2ref = doc.addObject("Part::Feature", "tot_extr_hold2_ref")
tot_extr_hold_2ref.Shape = tot_extr_hold_2.Shape.removeSplitter()

# Export them to .stl and .step
Part.export([tot_extr_hold_1ref], filepath + tot_extr_hold_1.Name + ".stl")
Part.export([tot_extr_hold_1ref], filepath + tot_extr_hold_1.Name + ".step")
Part.export([tot_extr_hold_2ref], filepath + tot_extr_hold_2.Name + ".stl")
Part.export([tot_extr_hold_2ref], filepath + tot_extr_hold_2.Name + ".step")
"""

# --------------------- Lower carriage holes --------------------
fuse_lowcar_holes = doc.addObject("Part::MultiFuse", "fuse_lowcar_holes")
fuse_lowcar_holes.Shapes = holes_lowcar_list
# --------------------- Higher carriage holes --------------------
fuse_higcar_holes = doc.addObject("Part::MultiFuse", "fuse_higcar_holes")
fuse_higcar_holes.Shapes = holes_higcar_list

# --------------------------- Cut the holes lower carriage holes

lowcar_hole = doc.addObject("Part::Cut", "lowcar_hole")
lowcar_hole.Base = carlow_box_fllt
lowcar_hole.Tool = fuse_lowcar_holes

lowcar_bccr_list = [ lowcar_hole, bccr_final, bccr_final_clone]
lowcar_bccr = doc.addObject("Part::MultiFuse", "lowcar_bccr")
lowcar_bccr.Shapes = lowcar_bccr_list


higcar_hole = doc.addObject("Part::Cut", "higcar_hole")
higcar_hole.Base = carhig_fuse
higcar_hole.Tool = fuse_higcar_holes

doc.recompute()

# Export to .stl and .step
"""
Part.export([tot_extr_hold_1], filepath + tot_extr_hold_1.Name + ".stl")
Part.export([tot_extr_hold_1], filepath + tot_extr_hold_1.Name + ".step")
Part.export([tot_extr_hold_2], filepath + tot_extr_hold_2.Name + ".stl")
Part.export([tot_extr_hold_2], filepath + tot_extr_hold_2.Name + ".step")
Part.export([lowcar_bccr], filepath + lowcar_bccr.Name + ".stl")
Part.export([lowcar_bccr], filepath + lowcar_bccr.Name + ".step")
Part.export([higcar_hole], filepath + higcar_hole.Name + ".stl")
Part.export([higcar_hole], filepath + higcar_hole.Name + ".step")
Part.export([gt2clamp0], filepath + "gt2clamp" + ".stl")
Part.export([gt2clamp0], filepath + "gt2clamp" + ".step")
"""


"""
doc.saveAs(filepath + filename + ".FCStd");

# Export the stl and the step files

Part.export([sk_final], filepath + filename + ".stl")
Part.export([sk_final], filepath + filename + ".step")
"""
