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
#import Draft;
#import copy;
#import Mesh;

doc = FreeCAD.newDocument();

import mat_cte  # import material constants and other constants
import mfc      # import my functions for freecad

from mfc import V0, VX, VY, VZ, V0ROT, addBox, addCyl, fillet_len
from mfc import addBolt, addBoltNut_hole
from mat_cte import TOL

""" ------------------- dimensions: --------------------------
"""


# radius for the fillet of 4 corners of the carriage
CAR_FLLT_R = 4.0

# The diameter of the rods is 10
ROD_DIAM = 10.0;
# Add 2 mm, because it is just to leave space for the rod
# and hold the linear bearings
rod_diam_space = ROD_DIAM + 2

# Separation between the rods axis (Y dimension)
ROD_SEP = 50.0

OUT_SEP = 14.0  # default distance to the ends

# The piece will hold 2 LME10UU linear bearings, tolerance added
BEARING_L_TOL = mat_cte.LME10UU_BEARING_L + TOL;
BEARING_D_TOL = mat_cte.LME10UU_BEARING_D + TOL;

# Distance between the rod axis to the end (it has to be larger than the 
# radius of the bearing

DIST_RODAX_END = BEARING_D_TOL/2.0 + OUT_SEP

CAR_X = 2.0 * BEARING_L_TOL + 3 * OUT_SEP

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

fuse_extr_holder_holes = doc.addObject("Part::MultiFuse", 
                                       "fuse_extr_holder_holes")
fuse_extr_holder_holes.Shapes = extr_holder_holes_list

# --------------------- extruder holders -----------------------------

# Extruder separation between axis + 2*radius (each side) + 2* extruder space
# to the end
EXTR_HOLD_X = EXTR_SEP + EXTR_WIDTH + 2.0*EXTR_SPACE 
# a little bigger so the heat sink can pass through
EXTR_HOLD_Y = EXTR_RAD + 2* TOL 
EXTR_HOLD_Z = EXTR_IN_H + EXTR_OUTUP_H + EXTR_OUTBOT_H - EXTR_BOT_OUT

extr_hold_1 = addBox(EXTR_HOLD_X, EXTR_HOLD_Y, EXTR_HOLD_Z, "extr_hold_1", cx=1)
extr_hold_2 = addBox(EXTR_HOLD_X, EXTR_HOLD_Y, EXTR_HOLD_Z, "extr_hold_2")
extr_hold_2_pos = FreeCAD.Vector(-EXTR_HOLD_X/2.0,-EXTR_HOLD_Y,0)
extr_hold_2.Placement = FreeCAD.Placement (extr_hold_2_pos, V0ROT, V0) 




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

# cut the holes for the extruder

tot_extr_hold_1 = doc.addObject("Part::Cut", "tot_extr_hold_1")
tot_extr_hold_1.Base = extr_hold_1_fllt
tot_extr_hold_1.Tool = fuse_extr_holder_holes
        
tot_extr_hold_2 = doc.addObject("Part::Cut", "tot_extr_hold_2")
tot_extr_hold_2.Base = extr_hold_2_fllt
tot_extr_hold_2.Tool = fuse_extr_holder_holes
        

# --------------------- the total box of the carriage ------
total_box = addBox(CAR_X, CAR_Y, CAR_Z, "total_box", cx = 1, cy=1)
#   Fillet on the vertical edges
tot_box_fllt = fillet_len (total_box, CAR_Z, CAR_FLLT_R, "tot_box_fllt")


# ------------------- Inner rectangle hole for the extruder holder

INRECT_X = EXTR_HOLD_X + TOL
# x2 because the holder is half on Y, and since they are 2, also the tolerances
INRECT_Y = 2.0 * (EXTR_HOLD_Y + TOL)
inrect = addBox (INRECT_X, INRECT_Y, CAR_Z+2, "inrect")

inrect_pos = FreeCAD.Vector(-INRECT_X/2.0, -INRECT_Y/2.0, -1)

inrect.Placement = FreeCAD.Placement(inrect_pos, V0ROT, V0) 

# fillet the inner rectangles. The radius has - tolerance because it is the
# outer
inrect_fllt = fillet_len (inrect, CAR_Z+2, EXTR_HOLD_FLLT_R-TOL, "inrect_fllt")

holes_list = []
holes_list.append(inrect_fllt)


# ------------------- Rod holes

rod_p = addCyl(rod_diam_space/2.0, CAR_X+2, "rod_p")
rod_p_pos = FreeCAD.Vector(-CAR_X/2.0-1, ROD_SEP/2.0, CAR_Z)
rod_p.Placement = FreeCAD.Placement (rod_p_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)

rod_n = addCyl(rod_diam_space/2.0, CAR_X+2, "rod_n")
rod_n_pos = FreeCAD.Vector(-CAR_X/2.0-1, -ROD_SEP/2.0, CAR_Z)
rod_n.Placement = FreeCAD.Placement (rod_n_pos,
                                     FreeCAD.Rotation(VY,90),
                                     V0)

holes_list.append(rod_n)
holes_list.append(rod_p)

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
      x_bearing = OUT_SEP/2.0
    else:
      x_bearing = - OUT_SEP/2.0 - BEARING_L_TOL
    if i == 0 or i == 1:
      y_bearing = ROD_SEP/2.0
    else:
      y_bearing = -ROD_SEP/2.0
    bearing_pos = FreeCAD.Vector(x_bearing, y_bearing, CAR_Z)
    bearing.Placement = FreeCAD.Placement (bearing_pos,
                                           FreeCAD.Rotation(VY,90),
                                           V0)
    holes_list.append(bearing)


# ---------------------- adding M3 bolts
BOLT_R = 3
M3_HEAD_R = mat_cte.D912_HEAD_D[BOLT_R] / 2.0
M3_HEAD_L = mat_cte.D912_HEAD_L[BOLT_R] + TOL
M3_HEAD_R_TOL = M3_HEAD_R + TOL/2.0 # smaller TOL, because it's small
M3_SHANK_R_TOL = BOLT_R / 2.0 + TOL/2.0

M3_NUT_R = mat_cte.NUT_D934_D[BOLT_R] / 2.0
M3_NUT_L = mat_cte.NUT_D934_L[BOLT_R] + TOL
#  1.5 TOL because diameter values are minimum, so they may be larger
M3_NUT_R_TOL = M3_NUT_R + 1.5*TOL

m3bolts = []
for i in range (0, 7):
  # create 6 bolt holes
  bolt = addBoltNut_hole (r_shank  = M3_SHANK_R_TOL,
                          l_bolt   = 2 * CAR_Z,
                          r_head   = M3_HEAD_R_TOL,
                          l_head   = M3_HEAD_L,
                          r_nut    = M3_NUT_R_TOL,
                          l_nut    = M3_NUT_L,
                          hex_head = 0, extra=1, name="m3_bolt_hole")
  if i == 0:  ## this will be centered
    m3bolt_x = 0
    m3bolt_y = 0
  else:
    if i < 4 : # on positive Y
      m3bolt_y = CAR_Y/2.0 - OUT_SEP/2.0
    else:
      m3bolt_y = - (CAR_Y/2.0 - OUT_SEP/2.0)
    if i % 3 == 1:
      m3bolt_x = CAR_X/2.0 - OUT_SEP/2.0
    elif i % 3 == 2:
      m3bolt_x = 0
    else:
      m3bolt_x = -(CAR_X/2.0 - OUT_SEP/2.0)

  bolt_pos = FreeCAD.Vector(m3bolt_x, m3bolt_y, 0)
  bolt.Placement = FreeCAD.Placement (bolt_pos, V0ROT, V0)
  m3bolts.append (bolt)

  # substract the bolt holes to the carriage
  # use extend instead of append, so the m3bolts is not appended as a list
  # but appended each element
  holes_list.extend (m3bolts)



# --------------------------- belt clamp and tensioner
# radius of the cylinder
"""                           
          TOPVIEW                    
                CLAMPBLOCK          
                    CB             
                    ____     
           CB_W  {  XXXX       ___
           CB_IW {  ____      /   \
   1 or 2: CB_MW {  XXXX      |   |   CCYL: CLAMPCYL 
           CB_IW {  ____      \___/
           CB_W  {  XXXX     
        
                    CB_L  CS


    Y A  (width)
      |
      |---> X (length)

  arguments:

  midblock: 1 or 2. It will add a none/single/double width middle block

"""


def add_2waybeltclamp (midblock = 1) :

    # space for the 2 belts to clamp them
    # the GT2 belt is 1.38mm width. 2 together facing teeth will be about 2mm
    # I make it 2.8mm
    # Internal Width of the Clamp Block
    GT2_CB_IW = 2.8
    # Width of the exterior clamp blocks (Y axis)
    GT2_CB_W = 4.0
    # Width of the interior/middle clamp blocks
    GT2_CB_MW = midblock * GT2_CB_W
    # Length of the clamp blocks (X axis)
    GT2_CB_L = 12.0
    # GT2 height is 6 mm, making the heigth 8mm
    GT2_C_H = 8.0
    # GT2 Clamp Cylinder radius
    GT2_CCYL_R = 4.0
    # separation between the clamp blocks and the clamp cylinder
    GT2_CS = 3.0

    """
    how much the rail is inside

     ________________________________________________    
    |        
    |   __________________________
     \                        ____ GT2_CBASERAILIND 
      |       
     /  _____ GT2_CBASE_RAIL ___
    |
    |_________________________ GT2_CBASE_WALL _________ GT2_CBASE_H

    |-|
      GT2_CBASERAILIND_SIG (it is 45 degrees). SIG: can be + or -

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
    GT2_CBASE_H = CAR_Z
    GT2_CBASE_L = GT2_CB_L + GT2_CS + 2*GT2_CCYL_R
    if midblock == 0:
      GT2_CBASE_W =     GT2_CB_IW + 2 * GT2_CB_W 
    else:
      GT2_CBASE_W = 2 * GT2_CB_IW + 2 * GT2_CB_W + GT2_CB_MW

    # divides how much is rail and how much is wall
    # It has to be greater than 1. If it is 1, there is no wall.
    # if it is 2. Half is wall, half is indent
    GT2_CBASE_RAIL_DIV = 1.6 #2.0
    GT2_CBASE_RAIL = GT2_CBASE_H / GT2_CBASE_RAIL_DIV # rail for the base
    # the part that is wall, divided by 2, because one goes at the bottom
    # and the other on top
    GT2_CBASE_WALL = (GT2_CBASE_H - GT2_CBASE_RAIL)/2.0 # rail for the base
    # Indentation, if midblock == 0, the Indentation is negative, which means
    # it will be outward, otherwise, inward
    GT2_CBASERAILIND = GT2_CBASE_RAIL/3.0
    if midblock == 0:
      GT2_CBASERAILIND_SIG = - GT2_CBASERAILIND 
    else:
      GT2_CBASERAILIND_SIG = GT2_CBASERAILIND 
  
    gt2_clamp_list = []
    # we make it using points-plane and extrusions
    #gt2_base = addBox (GT2_CBASE_L, GT2_CBASE_W, GT2_CBASE_H, "gt2_base")
    gt2_cb_1 = addBox (GT2_CB_L, GT2_CB_W, GT2_C_H+1, "gt2_cb_1")
    gt2_cb_1.Placement.Base = FreeCAD.Vector (GT2_CBASE_L-GT2_CB_L,
                                              0,
                                              GT2_CBASE_H-1)
    gt2_clamp_list.append (gt2_cb_1)
    if midblock > 0:
      gt2_cb_2 = addBox (GT2_CB_L, GT2_CB_MW, GT2_C_H+1, "gt2_cb_2")
      gt2_cb_2.Placement.Base = FreeCAD.Vector (GT2_CBASE_L-GT2_CB_L,
		                                        GT2_CB_W + GT2_CB_IW,
		                                        GT2_CBASE_H-1)
      gt2_clamp_list.append (gt2_cb_2)

    gt2_cb_3 = addBox (GT2_CB_L, GT2_CB_W, GT2_C_H + 1, "gt2_cb_3")
    gt2_cb_3.Placement.Base = FreeCAD.Vector (GT2_CBASE_L-GT2_CB_L,
		                                GT2_CBASE_W - GT2_CB_W,
		                                GT2_CBASE_H-1)
    gt2_clamp_list.append (gt2_cb_3)
 
    gt2_cyl = addCyl (GT2_CCYL_R,  GT2_C_H + 1, "gt2_cyl")
    gt2_cyl.Placement.Base = FreeCAD.Vector (GT2_CCYL_R, 
                                             GT2_CBASE_W/2,
                                             GT2_CBASE_H-1)
    gt2_clamp_list.append (gt2_cyl)


 

    # left side
    gt2_base_lv00 = FreeCAD.Vector (0,
                                    0,
                                    0)
    gt2_base_lv01 = FreeCAD.Vector (0,
                                    0,
                                    GT2_CBASE_WALL)
    gt2_base_lv02 = FreeCAD.Vector (0,
                                    GT2_CBASERAILIND_SIG,
                                    GT2_CBASE_WALL + GT2_CBASERAILIND)
    gt2_base_lv03 = FreeCAD.Vector (0,
                                    GT2_CBASERAILIND_SIG,
                                    GT2_CBASE_WALL + 2*GT2_CBASERAILIND)
    gt2_base_lv04 = FreeCAD.Vector (0,0,
                                    GT2_CBASE_WALL + GT2_CBASE_RAIL)
    gt2_base_lv05 = FreeCAD.Vector (0,0,
                                    GT2_CBASE_H)

    # left side
    gt2_base_rv00 = FreeCAD.Vector (0,
                                    GT2_CBASE_W,
                                    0)
    gt2_base_rv01 = FreeCAD.Vector (0,
                                    GT2_CBASE_W,
                                    GT2_CBASE_WALL)
    gt2_base_rv02 = FreeCAD.Vector (0,
                                    GT2_CBASE_W - GT2_CBASERAILIND_SIG,
                                    GT2_CBASE_WALL + GT2_CBASERAILIND)
    gt2_base_rv03 = FreeCAD.Vector (0,
                                    GT2_CBASE_W - GT2_CBASERAILIND_SIG,
                                    GT2_CBASE_WALL + 2*GT2_CBASERAILIND)
    gt2_base_rv04 = FreeCAD.Vector (0,
                                    GT2_CBASE_W,
                                    GT2_CBASE_WALL + GT2_CBASE_RAIL)
    gt2_base_rv05 = FreeCAD.Vector (0,GT2_CBASE_W,
                                    GT2_CBASE_H)

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
    """
    gt2_base_plane_yz = Part.makePolygon(gt2_base_list)
    gt2_base = gt2_base_plane_xy.extrude(FreeCAD.Vector(GT2_CBASE_L,0,0))
    """
    gt2_base_plane_yz = doc.addObject("Part::Polygon", "gt2_base_plane_yz")
    gt2_base_plane_yz.Nodes = gt2_base_list
    gt2_base_plane_yz.Close = True
    gt2_base = doc.addObject("Part::Extrusion", "gt2_base_plane_yz")
    gt2_base.Base = gt2_base_plane_yz
    gt2_base.Dir = (GT2_CBASE_L,0,0)
    gt2_base.Solid = True

    gt2_clamp_list.append(gt2_base)

    gt2_clamp_basic = doc.addObject("Part::MultiFuse", "gt2_clamp_basic")
    gt2_clamp_basic.Shapes = gt2_clamp_list

    """
    """

    # hole for the leadscrew bolt
    gt2_base_lscrew = addBolt (M3_SHANK_R_TOL, GT2_CBASE_L,
                               M3_HEAD_R_TOL, M3_HEAD_L,
                               extra = 1, support = 0,
                               name= "gt2_base_lscrew")
    
    gt2_base_lscrew.Placement.Base = FreeCAD.Vector (GT2_CBASE_L,
                                                     GT2_CBASE_W/2.0,
                                                     GT2_CBASE_H/2.0)
    gt2_base_lscrew.Placement.Rotation = FreeCAD.Rotation (VY, -90)

    # ------------ hole for a nut, also M3, for the leadscrew 
    gt2_base_lscrew_nut = doc.addObject("Part::Prism", "gt2_base_lscrew_nut")
    gt2_base_lscrew_nut.Polygon = 6
    gt2_base_lscrew_nut.Circumradius = M3_NUT_R_TOL
    # The nut height multiplier to have enough space to introduce it
    NUT_HOLE_MULT_H = 2 
    NUT_HOLE_H = NUT_HOLE_MULT_H * M3_NUT_L
    gt2_base_lscrew_nut.Height = NUT_HOLE_H 
    gt2_base_lscrew_nut.Placement = gt2_base_lscrew.Placement 
    gt2_base_lscrew_nut.Placement.Base = FreeCAD.Vector (
                                  (GT2_CBASE_L-M3_HEAD_L)/2.0 - NUT_HOLE_H/2.0,
                                   GT2_CBASE_W/2.0,
                                   GT2_CBASE_H/2.0)
    gt2_base_lscrew_nut.Placement.Rotation = FreeCAD.Rotation (VY, 90)
    # ------------ hole to reach out the nut hole
    #M3_2APOT_TOL = mat_cte.NUT_D934_2A[3] +  TOL
    M3_2APOT_TOL = 2* M3_NUT_R_TOL * 0.866 # Apotheme is: R * cos(30) = 0.866
    # X is the length: NUT_HOLE_H. Y is the width. M3_2APOT_TOL
    gt2_base_lscrew_nut2 = addBox (NUT_HOLE_H, M3_2APOT_TOL, GT2_CBASE_H/2.0,
                                   "gt2_base_lscrew_nut2")
    gt2_base_lscrew_nut2.Placement.Base = (
                               ((GT2_CBASE_L-M3_HEAD_L) - NUT_HOLE_H)/2.0,
                                (GT2_CBASE_W - M3_2APOT_TOL)/2.0,
                                 0)

    gt2_base_holes_l = [ gt2_base_lscrew,
                         gt2_base_lscrew_nut,
                         gt2_base_lscrew_nut2]

    # fuse the holes
    gt2_clamp_holes = doc.addObject("Part::MultiFuse", "gt2_clamp_hole")
    gt2_clamp_holes.Shapes = gt2_base_holes_l
    # Substract the holes 
    gt2_clamp = doc.addObject("Part::Cut", "gt2_clamp")
    gt2_clamp.Base = gt2_clamp_basic
    gt2_clamp.Tool = gt2_clamp_holes
    
    return gt2_clamp
    """
    """

"""
gt2_clamp = add_2waybeltclamp (midblock =1)
gt2_clamp.Placement.Base = FreeCAD.Vector (CAR_X / 2, 2, CAR_Z)
"""

gt2_clamp_0 = add_2waybeltclamp (midblock =0)
gt2_clamp_0.Placement.Base = FreeCAD.Vector (CAR_X / 2, 2, CAR_Z)

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
