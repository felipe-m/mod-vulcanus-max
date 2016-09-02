# file with constants about diferents materials and pieces used in the printer
# and some other general constants for the printer

# directory 
#filepath = "./"
filepath = "F/urjc/proyectos/2015_impresora3d/vulcanus_max/cad"
#filepath = "C:/Users/felipe/urjc/proyectos/2015_impresora3d/vulcanus_max/cad"


# ---------------------- Tolerance in mm
TOL = 0.4
STOL = TOL / 2       # smaller tolerance

# ---------------------- Bearings
# The piece will hold 2 LME10UU linear bearings
LME10UU_BEARING_L = 29; #the length of the bearing
LME10UU_BEARING_D = 19; #diamenter of the bearing


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

# separation of the extruders.
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

