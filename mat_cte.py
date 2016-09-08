# file with constants about diferents materials and pieces used in the printer
# and some other general constants for the printer

# directory 
#filepath = "./"
filepath = "F/urjc/proyectos/2015_impresora3d/vulcanus_max/cad"
#filepath = "C:/Users/felipe/urjc/proyectos/2015_impresora3d/vulcanus_max/cad"


# ---------------------- Tolerance in mm
TOL = 0.4
STOL = TOL / 2.0       # smaller tolerance

# height of the layer to print. To make some supports, ie: bolt's head
LAYER3D_H = 0.3  

# ---------------------- Bearings
# The piece will hold 2 LME10UU linear bearings
LME10UU_BEARING_L = 29.0; #the length of the bearing
LME10UU_BEARING_D = 19.0; #diamenter of the bearing


# Carriage inner rectangle (for the hot end)
inrect_x = 36.0
inrect_y = 20.0
# separation between inner rectangles, and also to the end of the piece
inrect_xsep = 12.0

# carriage total x dimension:
car_x = 2.0 * inrect_x + 3 * inrect_xsep

# radius for the fillet of 4 corners of the carriage
car_fllt_r = 4.0

# The diameter of the rods is 10
rod_diam = 10.0;
# Add 2 mm, because it is just to leave space for the rod
# and hold the linear bearings
rod_diam_space = rod_diam + 2.0

# Separation between the rods axis (Y dimension)
rod_sep = 50.0

# Distance between the rod axis to the end (it has to be larger than the 
# radius of the bearing

dist_rodax_end = 20.0

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

E3DV6_IN_DIAM = 12.0
E3DV6_IN_H = 6.0
E3DV6_OUT_DIAM = 16.0
E3DV6_OUTUP_H = 3.7
E3DV6_OUTBOT_H = 3.0

# separation of the extruders.
# with the fan, the extruder are about 30mm wide. So 15mm from the center.
# giving 10mm separation, results in 40mm separation
# and total length of 70mm
extrud_sep = 40.0

# DIN-912 bolt dimmensions
# head: the index is the M, i.e: M3, M4, ..., the value is the diameter of the head of the bolt
D912_HEAD_D = {3: 5.5, 4: 7.0, 5: 8.5, 6:10.0, 8:13.0, 10:18.0} 
# length: the index is the M, i.e: M3, M4, ..., the value is the length of the head of the bolt
# well, it is the same as the M, never mind...
D912_HEAD_L =  {3: 3.0,4: 4.0, 5: 5.0,  6:6.0, 8:8.0,  10:10.0} 

# Nut DIN934 dimensions
"""
       ___     _
      /   \    |   s_max: double the apothem
      \___/    |_

   r is the circumradius,  usually called e_min
"""

# the circumdiameter, min value
NUT_D934_D = {3: 6.01, 4: 7.66, 5: 8.79}
# double the apotheme, max value
NUT_D934_2A = {3: 5.5, 4: 7.0,  5: 8.0}
# the heigth, max value
NUT_D934_L  = {3: 2.4, 4: 3.2,  5: 4.0}

# tightening bolt with added tolerances:
# Bolt's head radius
#tbolt_head_r = (tol * d912_head_d[sk_12['tbolt']])/2 
# Bolt's head lenght
#tbolt_head_l = tol * d912_head_l[sk_12['tbolt']] 
# Mounting bolt radius with added tolerance
#mbolt_r = tol * sk_12['mbolt']/2

