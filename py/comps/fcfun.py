# ----------------------------------------------------------------------------
# -- FreeCad Functions
# -- comps library
# -- Python functions for FreeCAD
# ----------------------------------------------------------------------------
# -- (c) Felipe Machado
# -- Area of Electronics. Rey Juan Carlos University (urjc.es)
# -- October-2016
# ----------------------------------------------------------------------------
# --- LGPL Licence
# ----------------------------------------------------------------------------

import FreeCAD
import Part
import math
import logging
import DraftVecUtils

#from FreeCAD import Base

# ---------------------- can be taken away after debugging
import os
import sys
# directory this file is
filepath = os.getcwd()
import sys
# to get the components
# In FreeCAD can be added: Preferences->General->Macro->Macro path
sys.path.append(filepath)
# ---------------------- can be taken away after debugging


import kcomp

from kcomp import LAYER3D_H


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# vector constants
V0 = FreeCAD.Vector(0,0,0)
VX = FreeCAD.Vector(1,0,0)
VY = FreeCAD.Vector(0,1,0)
VZ = FreeCAD.Vector(0,0,1)
VXN = FreeCAD.Vector(-1,0,0)
VYN = FreeCAD.Vector(0,-1,0)
VZN = FreeCAD.Vector(0,0,-1)

# color constants
WHITE  = (1.0, 1.0, 1.0)
BLACK  = (0.0, 0.0, 0.0)

RED    = (1.0, 0.0, 0.0)
GREEN  = (0.0, 1.0, 0.0)
BLUE   = (0.0, 0.0, 1.0)

YELLOW = (1.0, 1.0, 0.0)
MAGENT = (1.0, 0.0, 1.0)
CIAN   = (0.0, 1.0, 1.0)

ORANGE = (1.0, 0.5, 0.0)
ORANGE_08 = (1.0, 0.8, 0.0)

RED_05    = (1.0, 0.5, 0.5)
GREEN_05  = (0.5, 1.0, 0.5)
BLUE_05   = (0.5, 0.5, 1.0)

RED_07    = (1.0, 0.7, 0.7)
GREEN_07  = (0.7, 1.0, 0.7)
BLUE_07   = (0.7, 0.7, 1.0)

RED_D07    = (0.7, 0.0, 0.0)
GREEN_D07  = (0.0, 0.7, 0.0)
BLUE_D07   = (0.0, 0.0, 0.7)

YELLOW_05 = (1.0, 1.0, 0.5)
MAGENT_05 = (1.0, 0.5, 1.0)
CIAN_05   = (0.5, 1.0, 1.0)

YELLOW_08 = (1.0, 1.0, 0.8)
MAGENT_08 = (1.0, 0.8, 1.0)
CIAN_08   = (0.8, 1.0, 1.0)

DSKYBLUE   = (0.0, 0.7, 1.0)
LSKYBLUE   = (0.5, 0.7, 1.0)

# no rotation vector
V0ROT = FreeCAD.Rotation(VZ,0)

EQUAL_TOL = 0.001 # less than a micron is the same


COS30 = 0.86603   
COS45 = 0.707   

# to compare numbers that they are almost the same, but because of 
# floating point calculations they are not exactly the same
def equ (x,y):

    p = DraftVecUtils.precision()
    if round(x,p) == round(y,p):
        return True
    else:
        return False




def fc_isperp (fc1, fc2):

    """ return 1 if fc1 and fc2 are perpendicular, 0 if they are not
    Args:
        fc1: FreeCAD.Vector
        fc2: FreeCAD.Vector
    Return:
         1 if fc1 and fc2 are perpendicular, 0 if they are not 
    """

    if DraftVecUtils.isNull(fc1) == 1 or DraftVecUtils.isNull(fc2) == 1:
        # if any of them are null, they are not perpendicular
        return 0
    else:
        nperp = fc1.dot(fc2)
        nperp_round = round(nperp,DraftVecUtils.precision())
        if nperp_round == 0:
            return 1
        else:
            return 0


def fc_isparal (fc1, fc2):

    """ return 1 if fc1 and fc2 are paralell (colinear), 0 if they are not
    Args:
        fc1: FreeCAD.Vector
        fc2: FreeCAD.Vector
    Return:
         1 if fc1 and fc2 are parallel, 0 if they are not 
    """

    if DraftVecUtils.isNull(fc1) == 1 or DraftVecUtils.isNull(fc2) == 1:
        # if any of them are null, they are not parallel
        return 0
    else:
        # scale both to 1, normalize
        n1 = DraftVecUtils.scaleTo(fc1,1)
        n2 = DraftVecUtils.scaleTo(fc2,1)
        n1neg = n1.negative()
        if (DraftVecUtils.equals(n1,n2) or
            DraftVecUtils.equals(n1neg,n2)):
            return 1
        else:
            return 0

def fc_isparal_nrm (fc1, fc2):

    """
    Very similar to fc_isparal, but in this case the arguments are normalized
    so, less operations to do.
    return 1 if fc1 and fc2 are paralell (colinear), 0 if they are not
    Args:
        fc1: FreeCAD.Vector
        fc2: FreeCAD.Vector
    Return:
         1 if fc1 and fc2 are parallel, 0 if they are not 
    """

    if DraftVecUtils.isNull(fc1) == 1 or DraftVecUtils.isNull(fc2) == 1:
        # if any of them are null, they are not parallel
        return 0
    else:
        fc1neg = fc1.negative()
        if (DraftVecUtils.equals(fc1,fc2) or
            DraftVecUtils.equals(fc1neg,fc2)):
            return 1
        else:
            return 0


def fc_isonbase (fcv):

    """ just tells if a vector has 2 of the coordinates zero
        So it is on just a base vector
    """

    if fcv.x == 0:
        if fcv.y == 0: # (0,0, )
            if fcv.z == 0:
                # null vector
                return 0  # (0,0,0)
            else: 
                return 1  # (0,0,Z)
        else:  # (0,Y, )
            if fcv.z == 0:
                return 1  # (0,Y,0)
            else:
                return 0  # (0,Y,Z)
    else: #(X, , )
        if fcv.y == 0: # (X,0, )
            if fcv.z == 0:
                return 1  # (X,0,0)
            else: 
                return 0  # (X,0,Z)
        else: # (X,Y, )
            return 0


def get_fc_perpend1(fcv):
    """ gets a 'random' perpendicular FreeCAD.Vector

    Parameters:
    -----------
        fcv : FreeCAD.Vector
    """

    if DraftVecUtils.isNull(fcv):
        logger.error('null vector')

    if fc_isonbase(fcv) == 1: # 2 of the bases are 0
         # just move them
        fcp = FreeCAD.Vector(fcv.z, fcv.x, fcv.y)
    elif fcv.x == 0:
        fcp = FreeCAD.Vector(0, fcv.z, -fcv.y)
    elif fcv.y == 0:
        fcp = FreeCAD.Vector(-fcv.z, 0, fcv.x)
    elif fcv.z == 0:
        fcp = FreeCAD.Vector(fcv.y, -fcv.x, 0)
    else: # none of them are zero (same as before)
        fcp = FreeCAD.Vector(fcv.y, -fcv.x, 0)

    return fcp



def add_fcobj(shp, name, doc = None):
    """ just creates a freeCAD object of the shape, just to save one line"""
    if doc is None:
        doc = FreeCAD.ActiveDocument
    fcobj = doc.addObject("Part::Feature", name)
    fcobj.Shape = shp
    return fcobj
  

def addBox(x, y, z, name, cx= False, cy=False):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
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


# adds a box, centered on the specified axis, with its
# Placement and Rotation at zero. So it can be referenced absolutely from
# its given position

def addBox_cen(x, y, z, name, cx= False, cy=False, cz=False):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument

    if cx == True:
        x0 = -x/2.0
        x1 =  x/2.0
    else:
        x0 =  0
        x1 =  x
    if cy == True:
        y0 = -y/2.0
        y1 =  y/2.0
    else:
        y0 =  0
        y1 =  y
    if cz == True:
        z0 = - z/2.0
    else:
        z0 = 0

    p00 = FreeCAD.Vector (x0,y0,z0)
    p10 = FreeCAD.Vector (x1,y0,z0)
    p11 = FreeCAD.Vector (x1,y1,z0)
    p01 = FreeCAD.Vector (x0,y1,z0)
    sq_list = [p00, p10, p11, p01]
    square =  doc.addObject("Part::Polygon",name + "_sq")
    square.Nodes =sq_list
    square.Close = True
    square.ViewObject.Visibility = False
    box = doc.addObject ("Part::Extrusion", name)
    box.Base = square
    box.Dir = (0,0, z)
    box.Solid = True
    # we need to recompute if we want to do operations on this object
    doc.recompute()
    
    return box


# adds a shape of box, referenced on the specified axis, with its
# Placement and Rotation at zero. So it can be referenced absolutely from
# its given position

def shp_boxcen(x, y, z, cx= False, cy=False, cz=False, pos=V0):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument

    if cx == True:
        x0 = -x/2.0
        x1 =  x/2.0
    else:
        x0 =  0
        x1 =  x
    if cy == True:
        y0 = -y/2.0
        y1 =  y/2.0
    else:
        y0 =  0
        y1 =  y
    if cz == True:
        z0 = - z/2.0
    else:
        z0 = 0

    p00 = FreeCAD.Vector (x0,y0,z0) + pos
    p10 = FreeCAD.Vector (x1,y0,z0) + pos
    p11 = FreeCAD.Vector (x1,y1,z0) + pos
    p01 = FreeCAD.Vector (x0,y1,z0) + pos
    # the square
    shp_wire_sq = Part.makePolygon([p00, p10, p11, p01, p00])
    # the face
    shp_face_sq = Part.Face(shp_wire_sq)
    shp_box = shp_face_sq.extrude(FreeCAD.Vector(0,0,z))

    doc.recompute()
    
    return shp_box


# The same as shp_boxcen, but when it is used to cut. So sometimes it is 
# useful to leave an extra 1mm on some sides to avoid making cuts sharing
# faces. The extra part is added but not influences on the reference
# Arguments:
# x, y , z: the size of the edges of the box
# cx, cy , cz: if the box will be centered on any of these axis
# cx, cy , cz: if the box will be centered on any of these axis
# xtr_x, xtr_nx, xtr_y, xtr_ny, xtr_z , xtr_nz:   
# if an extra mm will be added, the number will determine the size
#
#
#
#                     | Y    cy=1, xtr_ny=1
#                     |
#                1    |
#                _________
#               | |       |
#               | |       |
#               | |       |
#               | |       |
#               |_|_______|


def shp_boxcenxtr(x, y, z, cx= False, cy=False, cz=False,
                  xtr_nx = 0, xtr_x = 0,
                  xtr_ny = 0, xtr_y = 0,
                  xtr_nz = 0, xtr_z = 0,
                  pos=V0):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument

    if cx == True:
        x0 = -x/2.0 - xtr_nx
        x1 =  x/2.0 + xtr_x
    else:
        x0 =  0 - xtr_nx
        x1 =  x + xtr_x
    if cy == True:
        y0 = -y/2.0 - xtr_ny
        y1 =  y/2.0 + xtr_y
    else:
        y0 =  0 - xtr_ny
        y1 =  y + xtr_y
    if cz == True:
        z0 = -z/2.0 - xtr_nz
    else:
        z0 = 0 - xtr_nz

    p00 = FreeCAD.Vector (x0,y0,z0) + pos
    p10 = FreeCAD.Vector (x1,y0,z0) + pos
    p11 = FreeCAD.Vector (x1,y1,z0) + pos
    p01 = FreeCAD.Vector (x0,y1,z0) + pos
    # the square
    shp_wire_sq = Part.makePolygon([p00, p10, p11, p01, p00])
    # the face
    shp_face_sq = Part.Face(shp_wire_sq)
    shp_box = shp_face_sq.extrude(FreeCAD.Vector(0,0, z+xtr_z+xtr_nz))

    doc.recompute()
    
    return shp_box

# same as shp_boxcen but with a filleted dimension
def shp_boxcenfill (x, y, z, fillrad,
                   fx=False, fy=False, fz=True,
                   cx= False, cy=False, cz=False, pos=V0):

    shp_box = shp_boxcen (x=x, y=y, z=z, cx=cx, cy=cy, cz=cz, pos=pos)
    edg_list = []
    for ind, edge in enumerate(shp_box.Edges):
        vertex0 = edge.Vertexes[0]
        vertex1 = edge.Vertexes[1]
        p0 = vertex0.Point
        p1 = vertex1.Point
        vdif = p1 - p0
        if vdif.x != 0 and fx==True:
            edg_list.append(edge)
        elif vdif.y != 0 and fy==True:
            edg_list.append(edge)
        elif vdif.z != 0 and fz==True:
            edg_list.append(edge)
    shp_boxfill = shp_box.makeFillet(fillrad, edg_list)
    return (shp_boxfill)

# same as shp_boxcen but with a chamfered dimension
def shp_boxcenchmf (x, y, z, chmfrad,
                   fx=False, fy=False, fz=True,
                   cx= False, cy=False, cz=False, pos=V0):

    shp_box = shp_boxcen (x=x, y=y, z=z, cx=cx, cy=cy, cz=cz, pos=pos)
    edg_list = []
    for ind, edge in enumerate(shp_box.Edges):
        vertex0 = edge.Vertexes[0]
        vertex1 = edge.Vertexes[1]
        p0 = vertex0.Point
        p1 = vertex1.Point
        vdif = p1 - p0
        if vdif.x != 0 and fx==True:
            edg_list.append(edge)
        elif vdif.y != 0 and fy==True:
            edg_list.append(edge)
        elif vdif.z != 0 and fz==True:
            edg_list.append(edge)
    shp_boxchmf = shp_box.makeChamfer(chmfrad, edg_list)
    return (shp_boxchmf)

# Makes a box with width, depth, heigth.
# Originally:
# box_w: The width is X
# box_d: The depth is Y
# box_h: The Height is Z
# and then rotation will be referred to axis_w  = (1,0,0) and 
#                                       axis_nh = (0,0,-1)
# centered on any of the dimensions:
# cw, cd, ch 

# check if it makes sense to have this small function
def shp_box_rot (box_w, box_d, box_h,
                  axis_w = 'x', axis_nh = '-z', cw=1, cd=1, ch=1 ):


    shp_box = shp_boxcen(x=box_w, y=box_d, z=box_h,
              cx= cw, cy=cd, cz=ch, pos=V0)
    vrot = calc_rot(getvecofname(axis_w), getvecofname(axis_nh))
    shp_box.Placement.Rotation = vrot

    return shp_box


def shp_box_dir (box_w, box_d, box_h,
                    fc_axis_w = V0,
                    fc_axis_h =VZ,
                    fc_axis_d = VY,
                    cw=1, cd=1, ch=1,
                    pos=V0):

    """"
    Makes a shape of a box given its 3 dimensions: width, depth and height
    and the direction of the height and depth dimensions.
    The position of the box is given and also if the position is given
    by a corner or its center
             ________
            |\       \
            | \       \  
            |  \_______\  
             \ |       |
              \|_______|


     Example of not centered on origin

       Z=fc_axis_h      . Y = fc_axis_d
             :         .     
             :   __________
             :  /:   .   / |
             : / :  .   /  | h
             :/________/   |
             |   :.....|...|3
             |  / 4    |  /
             | /       | /  d
             |/________|/.....................X
             1          2
                   w


     Example of centered on origin

       Z=fc_axis_h               Y  = fc_axis_d
                    :           .     
                 __________   .
                /:  :    / |.
               / :  :   / .| h
              /__:_____/.  |
             |   :.....|...|3
             |  / 4 :..|../........................X
             | /       | /  d
             |/________|/
             1          2
                   w

    Args:
        box_w: width of the box
        box_d: depth of the box
        box_h: heiht of the box
        fc_axis_h: FreeCAD vector that has the direction of the height
        fc_axis_d: FreeCAD vector that has the direction of the depth
        fc_axis_w: FreeCAD vector that has the direction of the width
                   Not necessary, unless cw=0, then it indicates the 
                   direction of w, it has to be perpendicular to the previous
                   if = V0, the perpendicular will be calculated
        cw: 1 the width dimension is centered, 0 it is not
        cd: 1 the depth is centered, 0 it is not
        ch: 1 the height dimension is centered, 0 it is not
        pos: FreeCAD.Vector of the position of the box, it can be the center
             one corner, or a point centered in the dimensions given by
             cw, cd, ch

    """
    # normalize the axis, just in case:
    axis_h = DraftVecUtils.scaleTo(fc_axis_h,1)
    axis_d = DraftVecUtils.scaleTo(fc_axis_d,1)
    if fc_axis_w == V0:
        axis_w = axis_d.cross(axis_h)
    else:
        axis_w = DraftVecUtils.scaleTo(fc_axis_w,1)

    #get the points of the base: width x depth
    # if not centered, the first vertex of the base is on V0
    if cw == 1:
        # just scale and not scaleTo because they are unit vectors
        w_neg = DraftVecUtils.scale(axis_w, -box_w/2.)
        w_pos = DraftVecUtils.scale(axis_w,  box_w/2.)
    else:
        w_neg = V0
        w_pos = DraftVecUtils.scale(axis_w,  box_w)

    if cd == 1:
        d_neg = DraftVecUtils.scale(axis_d, -box_d/2.)
        d_pos = DraftVecUtils.scale(axis_d,  box_d/2.)
    else:
        d_neg = V0
        d_pos = DraftVecUtils.scale(axis_d,  box_d)

    if ch == 1:
        h_neg = DraftVecUtils.scale(axis_h, -box_h/2.)
    else:
        h_neg = V0
        

    v1 = pos + w_neg + d_neg + h_neg
    v2 = pos + w_pos + d_neg + h_neg
    v3 = pos + w_pos + d_pos + h_neg
    v4 = pos + w_neg + d_pos + h_neg

    # make a wire with the points
    wire_base = Part.makePolygon([v1,v2,v3,v4,v1])

    # make the face of the wire
    shp_facebase = Part.Face(wire_base)
    # length of the extrusion
    v_extr = DraftVecUtils.scale(axis_h, box_h)
    shp_box = shp_facebase.extrude(v_extr)

    return(shp_box)

    
def shp_box_dir_xtr (box_w, box_d, box_h,
                     fc_axis_h =VZ,
                     fc_axis_d = VY,
                     fc_axis_w = V0,
                     cw=1, cd=1, ch=1,
                     xtr_h = 0, xtr_nh = 0,
                     xtr_d = 0, xtr_nd = 0,
                     xtr_w = 0, xtr_nw = 0,
                     pos=V0):

    """"
    Makes a shape of a box given its 3 dimensions: width, depth and height
    and the direction of the height and depth dimensions.
    The position of the box is given and also if the position is given
    by a corner or its center
    extra mm to make cuts
             ________
            |\       \
            | \       \  
            |  \_______\  
             \ |       |
              \|_______|


     Example of not centered on origin

       Z=fc_axis_h      . Y = fc_axis_d
             :         .     
             :   __________
             :  /:   .   / |
             : / :  .   /  | h
             :/________/   |
             |   :.....|...|3
             |  / 4    |  /
             | /       | /  d
             |/________|/.....................X
             1          2
                   w


     Example of centered on origin

       Z=fc_axis_h               Y  = fc_axis_d
                    :           .     
                 __________   .
                /:  :    / |.
               / :  :   / .| h
              /__:_____/.  |
             |   :.....|...|3
             |  / 4 :..|../........................X
             | /       | /  d
             |/________|/
             1          2
                   w

    Args:
        box_w: width of the box
        box_d: depth of the box
        box_h: heiht of the box
        fc_axis_h: FreeCAD vector that has the direction of the height
        fc_axis_d: FreeCAD vector that has the direction of the depth
        fc_axis_w: FreeCAD vector that has the direction of the width
                   Not necessary, unless cw=0, then it indicates the 
                   direction of w, it has to be perpendicular to the previous
        cw: 1 the width dimension is centered, 0 it is not
        cd: 1 the depth is centered, 0 it is not
        ch: 1 the height dimension is centered, 0 it is not
        xtr_w, xtr_nw, xtr_d, xtr_nd, xtr_h , xtr_nh:   
            if an extra mm will be added, the number will determine the size
            useful to make cuts
        pos: FreeCAD.Vector of the position of the box, it can be the center
             one corner, or a point centered in the dimensions given by
             cw, cd, ch

    """
    # normalize the axis, just in case:
    axis_h = DraftVecUtils.scaleTo(fc_axis_h,1)
    axis_d = DraftVecUtils.scaleTo(fc_axis_d,1)
    if fc_axis_w == V0:
        axis_w = axis_d.cross(axis_h)
    else:
        axis_w = DraftVecUtils.scaleTo(fc_axis_w,1)

    #get the points of the base: width x depth
    # if not centered, the first vertex of the base is on V0
    if cw == 1:
        w_neg = DraftVecUtils.scale(axis_w, -box_w/2. - xtr_nw)
        w_pos = DraftVecUtils.scale(axis_w,  box_w/2. + xtr_w)
    else:
        w_neg = DraftVecUtils.scale(axis_w, - xtr_nw)
        w_pos = DraftVecUtils.scale(axis_w,   box_w + xtr_w)

    if cd == 1:
        d_neg = DraftVecUtils.scale(axis_d, -box_d/2. - xtr_nd)
        d_pos = DraftVecUtils.scale(axis_d,  box_d/2. + xtr_d)
    else:
        d_neg = DraftVecUtils.scale(axis_d, - xtr_nd)
        d_pos = DraftVecUtils.scale(axis_d,   box_d + xtr_d)

    if ch == 1:
        h_neg = DraftVecUtils.scale(axis_h, -box_h/2. - xtr_nh)
    else:
        h_neg = DraftVecUtils.scale(axis_h, - xtr_nh)
        

    v1 = pos + w_neg + d_neg + h_neg
    v2 = pos + w_pos + d_neg + h_neg
    v3 = pos + w_pos + d_pos + h_neg
    v4 = pos + w_neg + d_pos + h_neg

    # make a wire with the points
    wire_base = Part.makePolygon([v1,v2,v3,v4,v1])

    # make the face of the wire
    shp_facebase = Part.Face(wire_base)
    # length of the extrusion
    v_extr = DraftVecUtils.scale(axis_h, box_h + xtr_h + xtr_nh)
    shp_box = shp_facebase.extrude(v_extr)

    return(shp_box)


def shp_boxdir_fillchmfplane (
                     box_w, box_d, box_h,
                     axis_d = VY,
                     axis_w = V0,
                     axis_h = VZ,
                     cw=1, cd=1, ch=1,
                     xtr_d = 0, xtr_nd = 0,
                     xtr_w = 0, xtr_nw = 0,
                     xtr_h = 0, xtr_nh = 0,
                     fillet = 1,
                     radius = 1.,
                     plane_fill = VZ,
                     both_planes = 1,
                     edge_dir = V0,
                     pos=V0):
    """
    Creates a box shape (cuboid) along 3 axis.
    The shape will be filleted or chamfered on the edges of the plane defined
    by the plane_fill vector. If both_planes == 1, both faces will be
    filleted/chamfered
    if both_planes == 0, only the face that plane_fill is normal and goes
    outwards
    if edge_dir has an edge direction, only those edges in that direction will
    be filleted/chamfered

     Example of not centered on origin: cd=0, cw=0, ch=0

          axis_h        . axis_d
             :         .     
             :   __________....
             :  /:   .   / |  :
             : / :  .   /  |  :h
             :/________/   |  :
             |   :.....|...|..:.. 
             |  /      |  /    .
             | /       | /    . d
             |/________|/.................> axis_w
             :         :
             :....w....:


     Example of centered on origin: cd=1, cw=1, ch=1

                 axis_h           axis_d
                    :           .     
                 __________   .
                /:  :    / |.
               / :  :   / .| h
              /__:_____/.  |
             |   :.....|...| 
             |  /   :..|../..............> axis_w
             | /       | /   
             |/________|/
                         
                   w

      Example of parameter both_planes and edge_dir
               
      if both_planes == 1:
          if edge_dir == V0:
              edges_to_chamfer = [1,2,3,4,5,6,7,8]
          elif edge_dir == axis_w:
              edges_to_chamfer = [2,4,6,8]
          elif edge_dir == axis_d:
              edges_to_chamfer = [1,3,5,7]
      elif both_planes == 0:
          if edge_dir == V0:
              edges_to_chamfer = [1,2,3,4]
          elif edge_dir == axis_w:
              edges_to_chamfer = [2,4]
          elif edge_dir == axis_d:
              edges_to_chamfer = [1,3]

      axis_h=plane_fill
             :               
             :   ____2_____
             :  /:       / |
             : 1 :      3  |
             :/_____4__/   |
             |   :...6.|...|
             |  /      |  /
             | 5       | 7 
             |/___8____|/.................> axis_w

      Another example of parameter both_planes

      if both_planes == 1:
          edges_to_chamfer = [1,2,3,4,5,6,7,8]
      elif both_planes == 0:
          edges_to_chamfer = [5,6,7,8]

          axis_h
             :               
             :   ____2_____
             :  /:       / |
             : 1 :      3  |
             :/_____4__/   |
             |   :...6.|...|
             |  /      |  /
             | 5       | 7 
             |/___8____|/.................> axis_w
             :
             :
             :
             V
           plane_fill = axis_h.negative()



    Parameters:
    -----------
    box_d : positive float
        depth of the box
    box_w : positive float
        width of the box
    box_h : positive float
        height of the box
    axis_d : FreeCAD.Vector
        depth vector of the coordinate system
    axis_w : FreeCAD.Vector
        width vector of the coordinate system, can be V0 if centered
        and will be perpendicular to axis_d and axis_w
    axis_h : FreeCAD.Vector
        height vector of the coordinate system
    cw : int
        1: centered along axis_w
    cd : int
        1: centered along axis_d
    ch : int
        1: centered along axis_h
    xtr_d : float, >= 0
        extra depth, if there is an extra depth along axis_d
    xtr_nd : float, >= 0
        extra depth, if there is an extra depth along axis_d.negative
    xtr_w : float, >= 0
        extra width, if there is an extra width along axis_w
    xtr_nw : float, >= 0
        extra width, if there is an extra width along axis_w.negative
    xtr_h : float, >= 0
        extra height, if there is an extra height along axis_h
    xtr_nh : float, >= 0
        extra height, if there is an extra height along axis_h.negative
    fillet : int
        1: to fillet the edges
        0: to chamfer the edges
    radius : float >= 0
        radius of the fillet/chamfer
    plane_fill = FreeCAD.Vector
        Vector perpendicular to the face that is going to be filleted/chamfered
    both_planes : int
        0: fillet/chamfer only the edges on the face perpendicular to
           plane_fill and on the face that plane_fill goes outwards. See drawing
        1: fillet/chamfer the edges on both faces perpendicular to
           plane_fill 
    edge_dir : FreeCAD.Vector
        V0: fillet/chamfer all the edges of that/those faces
        axis: fillet/chamfer only the edges of that/those faces that are
              paralell to this axis
    pos : FreeCAD.Vector
        Position of the box

    Returns:
    -----------
    Shape of the filleted/chamfered box

    """

    doc = FreeCAD.ActiveDocument
    # normalize axes:
    # axis_l.normalize() could be used, but would change the vector
    # used as parameter
    axis_d = DraftVecUtils.scaleTo(axis_d,1)
    axis_h = DraftVecUtils.scaleTo(axis_h,1)
    if axis_w == V0:
       axis_w = axis_d.cross(axis_h)
    else:
       axis_w = DraftVecUtils.scaleTo(axis_w,1)
    plane_fill =  DraftVecUtils.scaleTo(plane_fill,1)
    edge_dir =  DraftVecUtils.scaleTo(edge_dir,1)
    n_plane_fill = plane_fill.negative() 

    shp_box = shp_box_dir_xtr (
                     box_w = box_w, box_d = box_d, box_h = box_h,
                     fc_axis_h = axis_h, fc_axis_d = axis_d, fc_axis_w = axis_w,
                     cw=cw, cd=cd, ch=ch,
                     xtr_d = xtr_d, xtr_nd = xtr_nd,
                     xtr_w = xtr_h, xtr_nw = xtr_nw,
                     xtr_h = xtr_h, xtr_nh = xtr_nh,
                     pos=pos)
    edg_list = []
    if both_planes == 0: # need to sort the edges in two planes
        edg_list_plane1 = []
        edg_list_plane2 = []
        ind_edg_plane1 = 0
        ind_edg_plane2 = 0

    for ind, edge in enumerate(shp_box.Edges):
        vertex0 = edge.Vertexes[0]
        vertex1 = edge.Vertexes[1]
        p0 = vertex0.Point
        p1 = vertex1.Point
        vdif = p1 - p0
        vdif.normalize()
        # check that they are not parallel to the normal:
        if not fc_isparal_nrm(vdif, plane_fill) :
            # all the edges or check if they are parallel to edge_dir
            if edge_dir == V0 or fc_isparal_nrm(vdif,edge_dir):
                if both_planes == 1:
                    edg_list.append(edge)
                else: #only take one face
                    scalar_proy = p0.dot(plane_fill)
                    #logger.debug ('%i', scalar_proy)
                    # see if this value is in either list
                    if ind_edg_plane1 > 0:
                        # check if they are equal, but with a precision
                        if equ(scalarproy_edg_plane1, scalar_proy) :
                            ind_edg_plane1 += 1
                            edg_list_plane1.append(edge)
                        else: # not in the same plane. Plane 2 list
                            if ind_edg_plane2 > 0:
                                if equ(scalarproy_edg_plane2, scalar_proy) :
                                    ind_edg_plane2 += 1
                                    edg_list_plane2.append(edge)
                                else:
                                    logger.error('error in plane to fillet')
                            else: # first edge on list 2
                                ind_edg_plane2 = 1
                                edg_list_plane2.append(edge)
                                scalarproy_edg_plane2 = scalar_proy
                    else: # first edge on plane 1
                        ind_edg_plane1 = 1
                        edg_list_plane1.append(edge)
                        scalarproy_edg_plane1 = scalar_proy

    if both_planes == 0:
        if ind_edg_plane1 > 0:
            if scalarproy_edg_plane1 > scalarproy_edg_plane2:
                edg_list = edg_list_plane1
            else:
                edg_list = edg_list_plane2
        elif edge_dir == V0:
            logger.debug('No axis edge to fillet or chamfer')
        else:
            logger.debug('Probably wrong edge_dir')

    if len(edg_list) != 0:
        if fillet == 1:
            #logger.debug('%s', str(edg_list))
            shp_fillchmf = shp_box.makeFillet(radius, edg_list)
        else:
            #logger.debug('%s', str(edg_list))
            shp_fillchmf = shp_box.makeChamfer(radius, edg_list)
        doc.recompute()
        return shp_fillchmf
    else:
        logger.debug('No edge to fillet or chamfer')
        return

# Test shp_boxdir_fillchmfplane
#doc = FreeCAD.newDocument()
#shp=shp_boxdir_fillchmfplane(10,3,4,
#                             xtr_d = 1, xtr_nd = 3,
#                             xtr_w = 2, xtr_nw = 2,
#                             xtr_h = 3, xtr_nh = 1,
#                             ch=0,
#                             fillet=0,plane_fill=VYN, both_planes=0,
#                             edge_dir = VZ,
#                             pos=FreeCAD.Vector(1,2,4))
#Part.show(shp)

# def shp_face_lgrail 
# adds a shape of the profile (face) of a linear guide rail, the dent is just
# rough, to be able to see that it is a profile
# Arguments:
# rail_w : width of the rail
# rail_h : height of the rail
# axis_l : the axis where the lenght of the rail is: 'x', 'y', 'z'
# axis_b : the axis where the base of the rail is poingint:
#           'x', 'y', 'z', '-x', '-y', '-z',
# It will be centered on the width axis, and zero on the length and height
#                        Z
#                       |
#               _________________ 5
#              |                 | 4
#               \             3 /   A little dent to see that it is a rail
#               /               \ 2
#              |                 |
#              |                 |
#              |_________________|  _____________ Y
#                                 1

def shp_face_lgrail (rail_w, rail_h, axis_l = 'x', axis_b = '-z'):

    #First we do it on like it is axis_l = 'x' and axis_h = 'z' 
    #so we draw width on Y and height on Z


    v1  = FreeCAD.Vector(0,  rail_w/2., 0)
    v1n = FreeCAD.Vector(0, -rail_w/2., 0)
    v2  = FreeCAD.Vector(0,  rail_w/2.,  rail_h/2.)
    v2n = FreeCAD.Vector(0, -rail_w/2.,  rail_h/2.)
    v3  = FreeCAD.Vector(0,  rail_w/2.-rail_h/8.,rail_h/2. + rail_h/8.)
    v3n = FreeCAD.Vector(0, -rail_w/2.+rail_h/8.,rail_h/2. + rail_h/8.)
    v4  = FreeCAD.Vector(0,  rail_w/2.,  rail_h/2. + rail_h/4.)
    v4n = FreeCAD.Vector(0, -rail_w/2.,  rail_h/2. + rail_h/4.)
    v5  = FreeCAD.Vector(0,  rail_w/2.,  rail_h)
    v5n = FreeCAD.Vector(0, -rail_w/2.,  rail_h)

    # the square
    shp_wire_rail = Part.makePolygon([v1, v2, v3, v4, v5,
                                    v5n, v4n, v3n, v2n, v1n, v1])

    vrot = calc_rot(getvecofname(axis_l), getvecofname(axis_b))
    # the face
    #shp_wire_rail.rotate(vrot) # It doesn't work
    shp_wire_rail.Placement.Rotation = vrot
    shp_face_rail = Part.Face(shp_wire_rail)
    
    return (shp_face_rail)


# ------------------------ def shp_face_rail 
# adds a shape of the profile (face) of a rail
# Arguments:
# rail_w : width of the rail
# rail_ws : small width of the rail
# rail_h : height of the rail
# rail_h_plus : above the rail can be some height to attach, o whatever
#               it is not inluded on rail_h
# offs_w : offset on the width, to make the hole
# offs_h : offset on the heigth, to make the hole
# axis_l : the axis where the lenght of the rail is: 'x', 'y', 'z'
# axis_b : the axis where the base of the rail is poingint:
#           'x', 'y', 'z', '-x', '-y', '-z',
# It will be centered on the width axis, and zero on the length and height
# hole_d : diameter of a hole inside the rail. To have a leadscrew
# hole_relpos_z: relative position of the center of the hole, relative
#          to the height (the rail_h, not the total height (rail_h+rail_h_plus)
#                        Z
#                       |
#                  ___________ 4 ___________
#                 |           | ____________ rail_h_plus
#                 |           |        |
#                 |           | 3      + rail_h
#                /     ___     \       |
#               /     /   \     \ 2    | _______ hole_relpos_z*rail_h
#              |      \___/      |     |
#              |_________________|  _____________ Y
#                                 1
#                  |--rail_ws-| 
#              |----  rail_w ----| 

def shp_face_rail (rail_w, rail_ws, rail_h,
                   rail_h_plus = 0,
                   offs_w = 0, offs_h = 0,
                   axis_l = 'x', axis_b = '-z',
                   hole_d = 0, hole_relpos_z=0.4):
# hole_relpos_z is the relative position referenced to rail_h

    #First we do it on like it is axis_l = 'x' and axis_h = 'z' 
    #so we draw width on Y and height on Z

    #dent = rail_h / 3.
    dent = (rail_w - rail_ws)/2.
    

    y1 = rail_w/2 + offs_w
    y3 = rail_w/2 -dent + offs_w
    z0 = - offs_h
    #z2 = dent + offs_h
    z2 = (rail_h - dent)/2. + offs_h
    z3 = (rail_h - dent)/2. + dent + offs_h
    z4 = rail_h + rail_h_plus + 2*offs_h

    v1  = FreeCAD.Vector(0,  y1, z0)
    v1n = FreeCAD.Vector(0, -y1, z0)
    v2  = FreeCAD.Vector(0,  y1, z2)
    v2n = FreeCAD.Vector(0, -y1, z2)
    v3  = FreeCAD.Vector(0,  y3, z3)
    v3n = FreeCAD.Vector(0, -y3, z3)
    v4  = FreeCAD.Vector(0,  y3, z4)
    v4n = FreeCAD.Vector(0, -y3, z4)

    # the square
    shp_wire_rail = Part.makePolygon([v1, v2, v3, v4,
                                      v4n, v3n, v2n, v1n, v1])

    vrot = calc_rot(getvecofname(axis_l), getvecofname(axis_b))
    # the face
    #shp_wire_rail.rotate(vrot) # It doesn't work
    shp_wire_rail.Placement.Rotation = vrot
    shp_face_rail = Part.Face(shp_wire_rail)
    #Part.show(shp_face_rail)

    if hole_d > 0:
        cir = Part.makeCircle (hole_d/2.,
                               FreeCAD.Vector(0, 0, hole_relpos_z*rail_h), VX)
        cir.Placement.Rotation = vrot
        wire_cir = Part.Wire(cir)
        face_cir = Part.Face(wire_cir)
        #Part.show(shp_thruhole)
        shp_face_rail = shp_face_rail.cut(face_cir)
        #return shp_face_hole

    
    return shp_face_rail




# Add cylinder r: radius, h: height 
def addCyl (r, h, name):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    cyl =  doc.addObject("Part::Cylinder",name)
    cyl.Radius = r
    cyl.Height = h
    return cyl

# Add cylinder in a position. So it is in a certain position, with its
# Placement and Rotation at zero. So it can be referenced absolutely from
# its given position
#     r: radius,
#     h: height 
#     name 
#     axis: 'x', 'y' or 'z'
#           'x' will along the x axis
#           'y' will along the y axis
#           'z' will be vertical
#     h_disp: displacement on the height. 
#             if 0, the base of the cylinder will be on the plane
#             if -h/2: the plane will be cutting h/2
def addCyl_pos (r, h, name, axis = 'z', h_disp = 0):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    cir =  doc.addObject("Part::Circle", name + "_circ")
    cir.Radius = r

    if axis == 'x':
        rot = FreeCAD.Rotation (VY, 90)
        cir.Placement.Base = (h_disp, 0, 0)
        extdir = (h,0,0) # direction for the extrusion
    elif axis == 'y':
        rot = FreeCAD.Rotation (VX, -90)
        cir.Placement.Base = (0, h_disp, 0)
        extdir = (0,h,0)
    else: # 'z' or any other 
        rot = FreeCAD.Rotation (VZ, 0)
        cir.Placement.Base = (0, 0, h_disp)
        extdir = (0,0,h)

    cir.Placement.Rotation = rot

    # to hide the circle
    if cir.ViewObject != None:
      cir.ViewObject.Visibility=False

    cyl = doc.addObject ("Part::Extrusion", name)
    cyl.Base = cir 
    cyl.Dir  = extdir 
    cyl.Solid  = True 

    return cyl



# same as addCyl_pos, but avoiding the creation of many FreeCAD objects
# Add cylinder
#     r: radius,
#     h: height 
#     name 
#     normal: FreeCAD.Vector pointing to the normal (if its module is not one,
#             the height will be larger than h
#     pos: position of the cylinder

def addCylPos (r, h, name, normal = VZ, pos = V0):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument

    cir =  Part.makeCircle (r,   # Radius
                            pos,     # Position
                            normal)  # direction

    #print "circle: %", cir_out.Curve

    wire_cir = Part.Wire(cir)
    face_cir = Part.Face(wire_cir)

    dir_extrus = DraftVecUtils.scaleTo(normal, h)
    shp_cyl = face_cir.extrude(dir_extrus)

    cyl = doc.addObject("Part::Feature", name)
    cyl.Shape = shp_cyl

    return cyl


# same as addCylPos, but just creates the shape
# Add cylinder
#     r: radius,
#     h: height 
#     normal: FreeCAD.Vector pointing to the normal (if its module is not one,
#             the height will be larger than h
#     pos: position of the cylinder

def shp_cyl (r, h, normal = VZ, pos = V0):

    cir =  Part.makeCircle (r,   # Radius
                            pos,     # Position
                            normal)  # direction

    #print "circle: %", cir_out.Curve

    wire_cir = Part.Wire(cir)
    face_cir = Part.Face(wire_cir)

    dir_extrus = DraftVecUtils.scaleTo(normal, h)
    shpcyl = face_cir.extrude(dir_extrus)

    return shpcyl


# Add cylinder, can be centered on the position, and also can have an extra
#  mm on top and bottom to make cuts
#     r: radius,
#     h: height 
#     normal: FreeCAD.Vector pointing to the normal 
#     ch : centered on the middle, of the height
#     xtr_top : extra on top (but does not influence the centering)
#     xtr_bot : extra on bottom (but does not influence the centering)
#     pos: position of the cylinder
#     

def shp_cylcenxtr (r, h, normal = VZ,
                         ch = 1, xtr_top=0, xtr_bot=0, pos = V0):

    # Normalize the normal, in case it is not one:
    nnormal = DraftVecUtils.scaleTo(normal, 1)
    if ch == 1: # we have to move the circle half the height down + xtr_bot
        basepos = pos - DraftVecUtils.scaleTo(nnormal, h/2. + xtr_bot)
    else:
        basepos = pos - DraftVecUtils.scaleTo(nnormal, xtr_bot)

    cir =  Part.makeCircle (r,   # Radius
                            basepos,     # Position
                            nnormal)  # direction

    #print "circle: %", cir.Curve

    wire_cir = Part.Wire(cir)
    face_cir = Part.Face(wire_cir)

    dir_extrus = DraftVecUtils.scaleTo(normal, h+xtr_bot+xtr_top)
    shpcyl = face_cir.extrude(dir_extrus)

    return shpcyl


def shp_cyl_gen (r, h, axis_h = VZ, 
                       axis_ra = None, axis_rb = None,
                       pos_h = 0, pos_ra = 0, pos_rb = 0,
                       xtr_top=0, xtr_bot=0, xtr_r=0, pos = V0):
    """
    This is a generalization of shp_cylcenxtr.
    Makes a cylinder in any position and direction, with optional extra
    heights and radius, and various locations in the cylinder

    Returns: a TopoShape

    Parameters:
    -----------
    r : float
        radius of the cylinder
    h : float
        height of the cylinder
    axis_h : FreeCAD.Vector
        vector along the cylinder height
    axis_ra : FreeCAD.Vector
        vector along the cylinder radius, a direction perpendicular to axis_h
        only make sense if pos_ra = 1.
        It can be None.
    axis_rb : FreeCAD.Vector
        vector along the cylinder radius,
        a direction perpendicular to axis_h and axis_rb
        only make sense if pos_rb = 1
        It can be None
    pos_h : int
        location of pos along axis_h (0, 1)
        0: the cylinder pos is centered along its height
        1: the cylinder pos is at its base (not considering xtr_h)
    pos_ra : int
        location of pos along axis_ra (0, 1)
        0: pos is at the circunference center
        1: pos is at the circunsference, on axis_ra, at r from the circle center
           (not at r + xtr_r)
    pos_rb : int
        location of pos along axis_rb (0, 1)
        0: pos is at the circunference center
        1: pos is at the circunsference, on axis_rb, at r from the circle center
           (not at r + xtr_r)
    xtr_top : float
        Extra height on top, it is not taken under consideration when
        calculating the cylinder center along the height
    xtr_bot : float
        Extra height at the bottom, it is not taken under consideration when
        calculating the cylinder center along the height or the position of
        the base
    xtr_r : float
        Extra length of the radius, it is not taken under consideration when
        calculating pos_ra or pos_rb
    pos : FreeCAD.Vector
        Position of the cylinder, taking into account where the center is



    
    pos_h = 1, pos_ra = 0, pos_rb = 0
    pos at 1:
            axis_rb
              :
              :
             . .    
           .     .
         (    o    ) ---- axis_ra       This o will be pos_o (origin)
           .     .
             . .    

           axis_h
              :
              :
          ...............
         :____:____:....: xtr_top
         |         |
         |         |
         |         |
         |         |
         |         |
         |         |
         |____1____|...............> axis_ra
         :....o....:....: xtr_bot             This o will be pos_o


    pos_h = 0, pos_ra = 1, pos_rb = 0
    pos at x:

       axis_rb
         :
         :
         :   . .    
         : .     .
         x         ) ----> axis_ra
           .     .
             . .    

           axis_h
              :
              :
          ...............
         :____:____:....: xtr_top
         |         |
         |         |
         |         |
         x         |....>axis_ra
         |         |
         |         |
         |_________|.....
         :....o....:....: xtr_bot        This o will be pos_o


    pos_h = 0, pos_ra = 1, pos_rb = 1
    pos at x:

       axis_rb
         :
         :
         :   . .    
         : .     .
         (         )
           .     .
         x   . .     ....> axis_ra

        axis_h
         :
         :
          ...............
         :____:____:....: xtr_top
        ||         |
        ||         |
        ||         |
        |x         |....>axis_ra
        ||         |
        ||         |
        ||_________|.....
        ::....o....:....: xtr_bot
        :;
        xtr_r

   """
   

    # calculate pos_o, which is at the center of the circle and at the base
    # counting xtr_bot if is is > 0
    axis_h = DraftVecUtils.scaleTo(axis_h, 1)
    
    if pos_ra == 0:
        ra_to_o = V0
    else:
        if axis_ra is not None:
            axis_ra = DraftVecUtils.scaleTo(axis_ra, 1)
            ra_to_o = DraftVecUtils.scale(axis_ra, r)
        else :
            logger.error('axis_ra not defined while pos_ra ==1')

    if pos_rb == 0:
        rb_to_o = V0
    else:
        if axis_rb is not None:
            axis_rb = DraftVecUtils.scaleTo(axis_rb, 1)
            rb_to_o = DraftVecUtils.scale(axis_rb, r)
        else :
            logger.error('axis_rb not defined while pos_rb ==1')

    if pos_h == 0: # we have to move the circle half the height down + xtr_bot
        h_to_o = DraftVecUtils.scale(axis_h, -(h/2. + xtr_bot))
    else:
        h_to_o = DraftVecUtils.scale(axis_h, - xtr_bot)

    pos_o = pos + h_to_o + ra_to_o + rb_to_o

    cir =  Part.makeCircle (r + xtr_r,   # Radius
                            pos_o,        # Position
                            axis_h)      # direction

    wire_cir = Part.Wire(cir)
    face_cir = Part.Face(wire_cir)

    extrude_dir = DraftVecUtils.scale(axis_h, h+xtr_bot+xtr_top)
    shpcyl = face_cir.extrude(extrude_dir)

    return shpcyl

#cyl = shp_cyl_gen (r=2, h=2, axis_h = VZ, 
#                       axis_ra = VX, axis_rb = VY,
#                       pos_h = 1, pos_ra = 1, pos_rb = 0,
#                       xtr_top=0, xtr_bot=1, xtr_r=2,
#                       pos = V0)
#                       #pos = FreeCAD.Vector(1,2,0))
#Part.show(cyl)



# Add cylinder, with inner hole:
#     r_ext: external radius,
#     r_int: internal radius,
#     h: height 
#     name 
#     axis: 'x', 'y' or 'z'
#           'x' will along the x axis
#           'y' will along the y axis
#           'z' will be vertical
#     h_disp: displacement on the height. 
#             if 0, the base of the cylinder will be on the plane
#             if -h/2: the plane will be cutting h/2

def addCylHole (r_ext, r_int, h, name, axis = 'z', h_disp = 0):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    cyl_ext =  addCyl (r_ext, h, name + "_ext")
    cyl_int =  addCyl (r_int, h + 2, name + "_int")

    if axis == 'x':
        rot = FreeCAD.Rotation (VY, 90)
        cyl_ext.Placement.Base = (h_disp, 0, 0)
        cyl_int.Placement.Base = (h_disp-1, 0, 0)
    elif axis == 'y':
        rot = FreeCAD.Rotation (VX, -90)
        cyl_ext.Placement.Base = (0, h_disp, 0)
        cyl_int.Placement.Base = (0, h_disp-1, 0)
    else: # 'z' or any other 
        rot = FreeCAD.Rotation (VZ, 0)
        cyl_ext.Placement.Base = (0, 0, h_disp)
        cyl_int.Placement.Base = (0, 0, h_disp-1)

    cyl_ext.Placement.Rotation = rot
    cyl_int.Placement.Rotation = rot

    cylHole = doc.addObject("Part::Cut", name)
    cylHole.Base = cyl_ext
    cylHole.Tool = cyl_int

    return cylHole

# Same as addCylHole, but just a shape
# Add cylinder, with inner hole:
#     r_ext: external radius,
#     r_int: internal radius,
#     h: height 
#     axis: 'x', 'y' or 'z'
#           'x' will along the x axis
#           'y' will along the y axis
#           'z' will be vertical
#     h_disp: displacement on the height. 
#             if 0, the base of the cylinder will be on the plane
#             if -h/2: the plane will be cutting h/2

def shp_cylhole (r_ext, r_int, h, axis = 'z', h_disp = 0.):

    normal = getfcvecofname(axis)
    pos_ext = DraftVecUtils.scaleTo(normal, h_disp)
    pos_int = DraftVecUtils.scaleTo(normal, h_disp-1)

    shp_cyl_ext =  shp_cyl (r_ext, h, normal = normal, pos=pos_ext)
    shp_cyl_int =  shp_cyl (r_int, h+2, normal = normal, pos=pos_int)

    shp_cyl_hole = shp_cyl_ext.cut(shp_cyl_int)

    return shp_cyl_hole


# same as addCylHole, but avoiding the creation of many FreeCAD objects
# Add cylinder, with inner hole:
#     r_out: outside radius,
#     r_in : inside radius,
#     h: height 
#     name 
#     normal: FreeCAD.Vector pointing to the normal (if its module is not one,
#             the height will be larger than h
#     pos: position of the cylinder

def addCylHolePos (r_out, r_in, h, name, normal = VZ, pos = V0):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument

    cir_out =  Part.makeCircle (r_out,   # Radius
                                pos,     # Position
                                normal)  # direction
    cir_in =  Part.makeCircle (r_in,   # Radius
                                pos,     # Position
                                normal)  # direction

    #print "in: %", cir_in.Curve
    #print "out: %", cir_out.Curve

    wire_cir_out = Part.Wire(cir_out)
    wire_cir_in  = Part.Wire(cir_in)
    face_cir_out = Part.Face(wire_cir_out)
    face_cir_in  = Part.Face(wire_cir_in)

    face_cir_hole = face_cir_out.cut(face_cir_in)
    dir_extrus = DraftVecUtils.scaleTo(normal, h)
    shp_cyl_hole = face_cir_hole.extrude(dir_extrus)

    cyl_hole = doc.addObject("Part::Feature", name)
    cyl_hole.Shape = shp_cyl_hole

    return cyl_hole



def shp_cylholedir (r_out, r_in, h, normal = VZ, pos = V0):

    """
        same as addCylHolePos, but just a shape
        same as shp_cylhole, but this one accepts any normal
    Arguments
        r_out: outside radius,
        r_in : inside radius,
        h: height 
        normal: FreeCAD.Vector pointing to the normal (if its module is not one,
                the height will be larger than h
        pos: position of the cylinder
    """


    cir_out =  Part.makeCircle (r_out,   # Radius
                                pos,     # Position
                                normal)  # direction
    cir_in =  Part.makeCircle (r_in,   # Radius
                                pos,     # Position
                                normal)  # direction


    wire_cir_out = Part.Wire(cir_out)
    wire_cir_in  = Part.Wire(cir_in)
    face_cir_out = Part.Face(wire_cir_out)
    face_cir_in  = Part.Face(wire_cir_in)

    face_cir_hole = face_cir_out.cut(face_cir_in)
    dir_extrus = DraftVecUtils.scaleTo(normal, h)
    shp_cyl_hole = face_cir_hole.extrude(dir_extrus)

    return shp_cyl_hole



def shp_cylhole_gen (r_out, r_in, h,
                     axis_h = VZ, axis_ra = None, axis_rb = None,
                     pos_h = 0, pos_ra = 0, pos_rb = 0,
                     xtr_top=0, xtr_bot=0,
                     xtr_r_out=0, xtr_r_in=0,
                     pos = V0):
    """
    This is a generalization of shp_cylholedir.
    Makes a hollow cylinder in any position and direction, with optional extra
    heights, and inner and outer radius, and various locations in the cylinder

    Returns: a TopoShape

    Parameters:
    -----------
    r_out : float
        radius of the outside cylinder
    r_in : float
        radius of the inner hole of the cylinder
    h : float
        height of the cylinder
    axis_h : FreeCAD.Vector
        vector along the cylinder height
    axis_ra : FreeCAD.Vector
        vector along the cylinder radius, a direction perpendicular to axis_h
        it is not necessary if pos_ra == 0
        It can be None, but if None, axis_rb has to be None
    axis_rb : FreeCAD.Vector
        vector along the cylinder radius,
        a direction perpendicular to axis_h and axis_ra
        it is not necessary if pos_ra == 0
        It can be None
    pos_h : int
        location of pos along axis_h (0, 1)
        0: the cylinder pos is centered along its height, not considering
           xtr_top, xtr_bot
        1: the cylinder pos is at its base (not considering xtr_h)
    pos_ra : int
        location of pos along axis_ra (0, 1)
        0: pos is at the circunference center
        1: pos is at the inner circunsference, on axis_ra, at r_in from the
           circle center (not at r_in + xtr_r_in)
        2: pos is at the outer circunsference, on axis_ra, at r_out from the
           circle center (not at r_out + xtr_r_out)
    pos_rb : int
        location of pos along axis_ra (0, 1)
        0: pos is at the circunference center
        1: pos is at the inner circunsference, on axis_rb, at r_in from the
           circle center (not at r_in + xtr_r_in)
        2: pos is at the outer circunsference, on axis_rb, at r_out from the
           circle center (not at r_out + xtr_r_out)
    xtr_top : float
        Extra height on top, it is not taken under consideration when
        calculating the cylinder center along the height
    xtr_bot : float
        Extra height at the bottom, it is not taken under consideration when
        calculating the cylinder center along the height or the position of
        the base
    xtr_r_in : float
        Extra length of the inner radius (hollow cylinder),
        it is not taken under consideration when calculating pos_ra or pos_rb.
        It can be negative, so this inner radius would be smaller
    xtr_r_out : float
        Extra length of the outer radius
        it is not taken under consideration when calculating pos_ra or pos_rb.
        It can be negative, so this outer radius would be smaller
    pos : FreeCAD.Vector
        Position of the cylinder, taking into account where the center is


    
    pos_h = 1, pos_ra = 0, pos_rb = 0
    pos at 1:
            axis_rb
              :
              :
             . .    
           . . . .
         ( (  0  ) ) ---- axis_ra
           . . . .
             . .    

           axis_h
              :
              :
          ...............
         :____:____:....: xtr_top
         | :     : |
         | :     : |
         | :     : |
         | :  0  : |     0: pos would be at 0, if pos_h == 0
         | :     : |
         | :     : |
         |_:__1__:_|....>axis_ra
         :.:..o..:.:....: xtr_bot        This o will be pos_o (orig)
         : :  :
         : :..:
         :  + :
         :r_in:
         :    :
         :....:
           +
          r_out
         

    Values for pos_ra  (similar to pos_rb along it axis)


           axis_h
              :
              :
          ...............
         :____:____:....: xtr_top
         | :     : |
         | :     : |
         | :     : |
         2 1  0  : |....>axis_ra    (if pos_h == 0)
         | :     : |
         | :     : |
         |_:_____:_|.....
         :.:..o..:.:....: xtr_bot        This o will be pos_o (orig)
         : :  :
         : :..:
         :  + :
         :r_in:
         :    :
         :....:
           +
          r_out

   """
   

    # calculate pos_o, which is at the center of the circle and at the base
    # counting xtr_bot it is is > 0
    axis_h = DraftVecUtils.scaleTo(axis_h, 1)
    
    # vectors from o (orig) along axis_h, to the pos_h points
    h_o = {}
    h_o[0] =  DraftVecUtils.scale(axis_h, h/2. + xtr_bot)
    h_o[1] =  DraftVecUtils.scale(axis_h, xtr_bot)

    # vectors from o (orig) along axis_ra, to the pos_ra points
    ra_o = {}
    ra_o[0] = V0
    if pos_ra != 0:
        if axis_ra is not None:
            axis_ra = DraftVecUtils.scaleTo(axis_ra, 1)
            ra_o[1] = DraftVecUtils.scale(axis_ra, - r_in)
            ra_o[2] = DraftVecUtils.scale(axis_ra, - r_out)
        else :
            logger.error('axis_ra not defined while pos_ra ==1')
    
    # vectors from o (orig) along axis_rb, to the pos_rb points
    rb_o = {}
    rb_o[0] = V0
    if pos_rb != 0:
        if axis_rb is not None:
            axis_rb = DraftVecUtils.scaleTo(axis_rb, 1)
            rb_o[1] = DraftVecUtils.scale(axis_rb, - r_in)
            rb_o[2] = DraftVecUtils.scale(axis_rb, - r_out)
        else :
            logger.error('axis_rb not defined while pos_rb ==1')

    pos_o = pos + (h_o[pos_h] + ra_o[pos_ra] + rb_o[pos_rb]).negative()

    shp_hollowcyl = shp_cylholedir (r_out = r_out + xtr_r_out,
                                    r_in  = r_in + xtr_r_in,
                                    h =  h+xtr_bot+xtr_top,
                                    normal = axis_h,
                                    pos = pos_o)

    return shp_hollowcyl

#cyl = shp_cylhole_gen (r_in=2, r_out=5, h=4,
#                       #axis_h = FreeCAD.Vector(1,1,0), 
#                       axis_h = VZ,
#                       axis_ra = VX, axis_rb = VYN,
#                       pos_h = 0,  pos_ra = 1, pos_rb = 2,
#                       xtr_top=0, xtr_bot=1,
#                       xtr_r_in=0, xtr_r_out=-1,
#                       pos = V0)
#                       #pos = FreeCAD.Vector(1,2,3))
#Part.show(cyl)

def add2CylsHole (r1, h1, r2, h2, thick,
                  normal = VZ, pos = V0):

    """ Creates a piece formed by 2 hollow cylinders

              :.. h1 .....+..h2..:
              :           :      :
           ...:___________:      :
      thick...|.......... |      :
              |         : |______:.....
              |         :........|    :
              |         :        |    + r2
              |         :        |....:
              |         :........|    :
              |         :  ______|    + r1
              |.........: |           :
              |___________|...........:

    Arguments:
        r1: radius of the 1st cylinder. The first cylinder relative to 
            the position pos
        h1: height of the 1st cylinder (seen from outside)
        r2: radius of the 2nd cylinder
        h2: height of the 2nd cylinder (seen from outside)
        normal: direction of the height
        pos: position of the center

    """

    # normalize de axis just in case:
    nnormal = DraftVecUtils.scaleTo(normal,1)

    # the smaller radius cylinder will be larger, add thick   

    if r1 < r2:
        h1_real = h1 + thick
        h2_real = h2
        pos_cyl2 = pos + DraftVecUtils.scaleTo(nnormal, h1) 
        rs = r1  # small radius
        rl = r2  # large radius
        pos_innercyl_large = pos + DraftVecUtils.scaleTo(nnormal, h1+thick)
        # inner height of the large cylinder
        innercyl_h_l = h2 - thick
        # extra for the cut, depending which side it is
        inncercyl_larg_xtrbot = 0
        inncercyl_larg_xtrtop = 1
    elif r1 > r2:
        h1_real = h1
        h2_real = h2 + thick        
        pos_cyl2 = pos + DraftVecUtils.scaleTo(nnormal, h1-thick) 
        rs = r2  # small radius
        rl = r1  # large radius
        pos_innercyl_large = pos
        # inner height of the large cylinder
        innercyl_h_l = h1 - thick
        # extra for the cut, depending which side it is
        inncercyl_larg_xtrbot = 1
        inncercyl_larg_xtrtop = 0
    else:
        logger.debug('Cylinders have the same radius')

    shp_cyl1 = shp_cyl(r1, h1_real, nnormal, pos)
    shp_cyl2 = shp_cyl(r2, h2_real, nnormal, pos_cyl2)
    shp_ext = shp_cyl1.fuse(shp_cyl2)

    # thruhole of the smaller radius
    shp_innercyl_s = shp_cylcenxtr (rs-thick, h = h1+h2, normal = nnormal,
                                    ch = 0, xtr_top=1, xtr_bot=1, pos = pos)
    # thruhole of the larger radius
    shp_innercyl_l = shp_cylcenxtr (rl-thick, h = innercyl_h_l,
                                    normal = nnormal,
                                    ch = 0,
                                    xtr_top=inncercyl_larg_xtrtop,
                                    xtr_bot=inncercyl_larg_xtrbot,
                                    pos = pos_innercyl_large)

    shp_innercyl = shp_innercyl_s.fuse(shp_innercyl_l)

    shp_2cyls = shp_ext.cut(shp_innercyl)
    return (shp_2cyls)
    



def add3CylsHole (r1, h1, r2, h2, rring, hring, thick,
                  normal = VZ, pos = V0):

    """ Creates a piece formed by 2 hollow cylinders, and a ring
        on the side of the larger cylinder

        ref


               _:.. h1 .....+..h2..:
              | |           :      :
           ...| |___________:      :
      thick...|.|.......... |      :
              | |         : |______:.....
              | |         :........|    :
              | |         :        |    + r2
              * |         :        |....:.......
              | |         :........|    :      :
              | |         :  ______|    + r1   :
              |.|.........: |           :      :
              | |___________|...........:      + rring
              | |                              :
              |_|..............................:
              : :
               + hring

    Arguments:
        r1: radius of the 1st cylinder. The first cylinder relative to 
            the position pos (if this is larger than r2, the ring will go first)
        h1: height of the 1st cylinder (seen from outside)
        r2: radius of the 2nd cylinder
        h2: height of the 2nd cylinder (seen from outside)
        rring: radius of the ring, it has to be larger than r1, and r2
        hring: height of the ring, it has to be larger than r1, and r2
        thick: thickness of the walls, excluding the ring
        normal: direction of the height
        pos: position of the center

    """

    # normalize de axis just in case:
    nnormal = DraftVecUtils.scaleTo(normal,1)

    if r1 > rring or r2 > rring:
        logger.error('r ring has to be larger the the other radius' )

    # the smaller radius cylinder will be larger, add thick   

    if r1 < r2: # the smaller radius cylinder first
        shp_cyl1 = shp_cyl(r1, h1 + 1, nnormal, pos)
        pos_cyl2 = pos + DraftVecUtils.scaleTo(nnormal, h1) 
        shp_cyl2 = shp_cyl(r2, h2 + hring/2., nnormal, pos_cyl2)
        pos_ring = pos + DraftVecUtils.scaleTo(nnormal, h1+ h2) 
        shp_ring = shp_cyl(rring, hring, nnormal, pos_ring)

        # thruhole of the smaller radius
        shp_innercyl_s = shp_cylcenxtr (r1-thick, h = h1+h2+hring,
                                        normal = nnormal,
                                        ch = 0, xtr_top=1, xtr_bot=1,
                                        pos = pos)
        # thruhole of the larger radius
        pos_innercyl_l = pos + DraftVecUtils.scaleTo(nnormal, h1+thick)
        shp_innercyl_l = shp_cylcenxtr (r2-thick, h = h2 + hring - thick,
                                        normal = nnormal,
                                        ch = 0,
                                        xtr_top=1,
                                        xtr_bot=0,
                                        pos = pos_innercyl_l)
    elif r1 > r2: # the ring first, then the larger radius, and then the smaller
        shp_ring = shp_cyl(rring, hring, nnormal, pos)
        pos_cyl1 = pos + DraftVecUtils.scaleTo(nnormal, hring) 
        shp_cyl1 = shp_cylcenxtr(r1, h1, nnormal, ch=0,
                                 xtr_top = 0, xtr_bot = hring/2., 
                                 pos = pos_cyl1)
        pos_cyl2 = pos_cyl1 + DraftVecUtils.scaleTo(nnormal, h1-thick)
        shp_cyl2 = shp_cyl(r2,h2+thick, nnormal, pos_cyl2)
        # thruhole of the smaller radius
        shp_innercyl_s = shp_cylcenxtr (r2-thick, h = h1+h2+hring,
                                        normal = nnormal,
                                        ch = 0, xtr_top=1, xtr_bot=1,
                                        pos = pos)
        # thruhole of the larger radius
        pos_innercyl_l = pos + DraftVecUtils.scaleTo(nnormal, h1+thick)
        shp_innercyl_l = shp_cylcenxtr (r1-thick, h = h1 + hring - thick,
                                        normal = nnormal,
                                        ch = 0,
                                        xtr_top=0,
                                        xtr_bot=1,
                                        pos = pos)
    else:
        logger.debug('Cylinders have the same radius')

    shp_ext = shp_cyl1.multiFuse([shp_cyl2, shp_ring])
    shp_innercyl = shp_innercyl_s.fuse(shp_innercyl_l)
    shp_2cyls_ring = shp_ext.cut(shp_innercyl)
    return (shp_2cyls_ring)
    



# ------------------- def shp_stadium_wire
# Creates a wire (shape), that is a rectangle with semicircles at a pair of
# opposite sides. Also called discorectangle
# it will be centered on XY
#                              Y
#              _____ .. r      |_X
#             (_____)--
#              :   :
#              :.l.:
#
# l: length of the parallels
# r: Radius of the semicircles
# axis_rect: 'x' the parallels are on axis X (as in the drawing)
#             'y' the parallels are on axis Y
# pos_z: position on the Z axis

def shp_stadium_wire (l, r, axis_rect='x', pos_z=0):

    # considering axis_rect == 'x', if not, later it is rotated
    # center points of the semicircles:
    cen   = FreeCAD.Vector (l/2., 0, pos_z)
    cen_n = FreeCAD.Vector (-l/2., 0, pos_z)
    arch   = Part.makeCircle (r, cen, VZ, 270, 90)
    arch_n = Part.makeCircle (r, cen_n, VZ, 90, 270)
    # points of the lines
    p_x_y   = FreeCAD.Vector(l/2.,r, pos_z)
    p_nx_y  = FreeCAD.Vector(-l/2.,r, pos_z)
    p_x_ny   = FreeCAD.Vector(l/2.,-r, pos_z)
    p_nx_ny  = FreeCAD.Vector(-l/2.,-r, pos_z)
    lin_y =  Part.Line(p_x_y, p_nx_y).toShape() 
    lin_ny = Part.Line(p_nx_ny, p_x_ny).toShape() 

    list_elem = [arch, lin_y, arch_n, lin_ny]
    if axis_rect == 'y':
        for elem in list_elem:
            # arguments of rotate: rotation center, rotation axis, angle
            elem.rotate(V0,VZ,90)

    wire_stadium = Part.Wire (list_elem)

    #Part.show(wire_stadium)
    return (wire_stadium)

# same as shp_stadium_wire, but returns a face
def shp_stadium_face (l, r, axis_rect='x', pos_z=0):

    shpStadiumWire = shp_stadium_wire (l, r, axis_rect, pos_z)
    shpStadiumFace = Part.Face (shpStadiumWire)
    return shpStadiumFace




# ------------------- def shp_stadium_wire_dir

def shp_stadium_wire_dir (length, radius, fc_axis_l = VX,
                          fc_axis_s = VY,
                          ref_l = 1,
                          ref_s = 1,
                          pos=V0):

    """
    Same as shp_stadium_wire but in any direction
    Also called discorectangle
  
                                   fc_axis_s
                                    |
               _____ .. radius      |--> fc_axis_l
              (_____)--
               :   :
               :.l.:
               length
 
    Arguments:
    length: length of the parallels
    radius: Radius of the semicircles
    fc_axis_l: vector on the direction of the paralles
    fc_axis_s: vector on the direction perpendicular to the paralles
    ref_l: reference (zero) of the fc_axis_l
            1: reference on the center (makes axis_s symmetrical)
            2: reference at one of the semicircle centers (point 2)
               the other circle center will be on the direction of fc_axis_l
            3: reference at the end (point 3)
               the other end will be on the direction of fc_axis_l
    ref_s: reference (zero) of the fc_axis_s
            1: reference at the center (makes axis_l symmetrical): p 1,2,3
            2: reference at the parallels lines: p: 4, 5 
               the other parallel will be on the direction of fc_axis_s
    pos: FreeCAD vector of the position of the reference


          fc_axis_s              in this drawing, 
           :  p_edge             the zero is on point 2
           :_________           ref_l = 2, ref_s = 1
          /          \
         3 2    1     ) -------> fc_axis_l
          \5____4____/   n_edge
             n_edge        
     n circle        p circle

    returns the shape of the wire
    """

    # normalize the axis
    axis_l = DraftVecUtils.scaleTo(fc_axis_l,1)
    axis_s = DraftVecUtils.scaleTo(fc_axis_s,1)




    #        axis_s: 1, 2, 3 are the points in s
    #      ____:_____
    #     /    3     \
    #    3 2   1    4 5 --> axis_l: 3, 2, 1, are the points in l
    #     \____2_____/
    #           
    #
    
    # ----- Distance vectors on axis_l
    # distance from 1 to 2 in axis_l
    fc_1_2_l = DraftVecUtils.scale(axis_l, -length/2.)
    fc_2_3_l = DraftVecUtils.scale(axis_l, -radius)
    fc_1_3_l = fc_1_2_l + fc_2_3_l
    fc_1_4_l = fc_1_2_l.negative()
    fc_1_5_l = fc_1_3_l.negative()
    # ----- reference to 1 on axis_l
    #d vector to go from the reference point to point 1 in l
    if ref_l == 1:  # ref on stadium center
        refto_1_l = V0
    elif ref_l == 2:  # ref on circle center (left)
        refto_1_l = fc_1_4_l # or fc_1_2_l.negative()
    elif ref_l == 3:  # ref at the left end
        refto_1_l = fc_1_5_l # or fc_1_3_l.negative
    else:
        logger.error('wrong ref_l in shp_stadium_wire_dir')


    # ----- Distance vectors on axis_s
    # distance from 1 to 2 in axis_s
    fc_1_2_s = DraftVecUtils.scale(axis_s, -radius)
    fc_1_3_s = fc_1_2_s.negative()
    #fc_2_3_s = DraftVecUtils.scale(axis_s, 2*radius)
    # ----- reference to 1 on axis_s
    #d vector to go from the reference point to point 1 in s
    if ref_s == 1:  # ref on stadium center
        refto_1_s = V0
    elif ref_s == 2:  # ref at the bottom
        refto_1_s = fc_1_3_s # or fc_1_2_s.negative()
    else:
        logger.error('wrong ref_l in shp_stadium_wire_dir')

    # Now define the center point of the stadium. This is an absolute position,
    # and everything will be defined from this point
    # ln: L axis Negative side
    # lp: L axis Positive side
    # sn: S axis Negative side
    # sp: S axis Positive side
    # s0: S axis at zero
    #
    #         axis_s
    #    ln_sp :
    #      ____:____lp_sp       
    #     /          \
    # ln_s0    cs     ) lp_s0 -------> axis_l
    #     \__________/
    #    ln_sn       lp_sn
    #
    #        axis_s: 1, 2, 3 are the points in s
    #      ____:_____
    #     /    3     \
    #    3 2   1    4 5 --> axis_l: 3, 2, 1, are the points in l
    #     \____2_____/
    #           
    #
    
    # Define these 6 points from cs_pos (Center Stadium pos)
    cs_pos = pos + refto_1_l + refto_1_s

    ln_s0_pos = cs_pos + fc_1_3_l
    lp_s0_pos = cs_pos + fc_1_5_l

    ln_sp_pos = cs_pos + fc_1_2_l + fc_1_3_s
    lp_sp_pos = cs_pos + fc_1_4_l + fc_1_3_s

    ln_sn_pos = cs_pos + fc_1_2_l + fc_1_2_s
    lp_sn_pos = cs_pos + fc_1_4_l + fc_1_2_s

    lin_p =  Part.Line(ln_sp_pos, lp_sp_pos).toShape() 
    arch_p = Part.Arc(lp_sp_pos, lp_s0_pos, lp_sn_pos).toShape()
    lin_n = Part.Line(lp_sn_pos, ln_sn_pos).toShape() 
    arch_n = Part.Arc(ln_sn_pos, ln_s0_pos, ln_sp_pos).toShape()
    wire_stadium = Part.Wire ([lin_p, arch_p, lin_n, arch_n])

    #Part.show(wire_stadium)
    return (wire_stadium)


def shp_stadium_dir (
                     length, radius, height,
                     fc_axis_h = VZ,
                     fc_axis_l = VX,
                     fc_axis_s = V0,
                     ref_l = 1,
                     ref_s = 1,
                     ref_h = 1,
                     xtr_h = 0,
                     xtr_nh = 0,
                     pos=V0):

    """ 
    makes a stadium shape in any direction
    see shp_stadium_wire_dir for the arguments

    height: height the stadium
    fc_axis_s: direction on the short axis, not necessary if ref_s == 1
         it will be the perpendicular of the other 2 vectors
    fc_axis_h: vector on the height direction
    ref_l: reference (zero) of the fc_axis_l
            1: reference on the center (makes axis_s symmetrical)
            2: reference at one of the semicircle centers (point 2)
               the other circle center will be on the direction of fc_axis_l
            3: reference at the end (point 3)
               the other end will be on the direction of fc_axis_l
    ref_s: reference (zero) of the fc_axis_s
            1: reference at the center (makes axis_l symmetrical): p 1,2,3
            2: reference at the parallels lines: p: 4, 5 
               the other parallel will be on the direction of fc_axis_s
    ref_h: 1: reference is at the center of the height
           2: reference is at the bottom
    xtr_h: if >0 it will be that extra height on the direction of fc_axis_h
    xtr_nh: if >0 it will be that extra height on the opositve direction of
             fc_axis_h
        


        fc_axis_s
          :
          :_________           ref_l = 2, ref_s = 1
          /          \
         3 2    1     ) -------> fc_axis_l
          \5____4____/ 

        fc_axis_h
         _:___________ ............................
        |             |                            :
        |             |                            :
        |      1      |      ref_h=1               + h
        |             |                            :
        |______2______|.......> fc_axis_l .........:  ref_h=2

    """

    # normalize the axis
    axis_l = DraftVecUtils.scaleTo(fc_axis_l,1)
    axis_h = DraftVecUtils.scaleTo(fc_axis_h,1)
    axis_h_n = axis_h.negative()
    if fc_axis_s == V0:
        axis_s = axis_l.cross(axis_h)
    else:
        axis_s = DraftVecUtils.scaleTo(fc_axis_s,1)

    
    if ref_h == 1: # we have to move the stadium half the height down + xtr_nh
        basepos = pos + DraftVecUtils.scale(axis_h_n, height/2. + xtr_nh)
    else:
        basepos = pos + DraftVecUtils.scale(axis_h_n, xtr_nh)

    shp_stadium_wire = shp_stadium_wire_dir (length=length,
                                             radius=radius,
                                             fc_axis_l = axis_l,
                                         fc_axis_s = axis_s,
                                         ref_l = ref_l, ref_s = ref_s,
                                         pos = basepos)

    # make a face of the wire
    shp_stadium_face = Part.Face (shp_stadium_wire)
    # extrude it
    dir_extrud = DraftVecUtils.scaleTo(axis_h, height + xtr_nh + xtr_h)
    shp_stadium = shp_stadium_face.extrude(dir_extrud)
    return (shp_stadium)


#shp_std = shp_stadium_dir (
#                     length=20, radius=5, height=40,
#                     fc_axis_l = VX,
#                     #fc_axis_s = VY,
#                     fc_axis_h = VZ,
#                     ref_l = 2,
#                     ref_s = 1,
#                     ref_h = 2,
#                     #xtr_h = 0,
#                     xtr_nh = 1,
#                     pos=FreeCAD.Vector(0,0,-1))


def shp_2stadium_dir (
                     length, r_s, r_l,
                     h_tot, h_rl,
                     fc_axis_h = VZ,
                     fc_axis_l = VX,
                     ref_l = 1,
                     rl_h0 = 1,
                     xtr_h = 0,
                     xtr_nh = 0,
                     pos=V0):

    """ makes to concentric stadiums, useful for making rails for bolts
        the length is the same for both. Changes the radius and the height
        The smaller radius will have the largest length

        rl_h0 = 1: the large stadium is at h=0

                    fc_axis_h 
             ________:________......................
            |   :         :   |                    :
            |   :         :   |                    :
         ___|   :         :   |___ ........        + h_tot
        |       :         :       |        : h_rl  :
        |_______:____*____:_______|........:.......: ......> fc_axis_l
        :   :   :         :
        :...:.+.:.........:
        :    r_s:   lenght
        :       :
        :       :
        :.r_l...:


        rl_h0 = 0 : the large stadium is at the end of h
        
                    fc_axis_h 
         ____________:____________..............
        |       :         :       |    : h_rl  :
        |___    :         :    ___|....:       :
            |   :         :   |                :+ h_tot
        :   |   :         :   |                :
        :   |___:____*____:___|................: ......> fc_axis_l
        :   :   :         :
        :...:.+.:.........:
        :    r_s:   length
        :       :
        :       :
        :.r_l...:

    on the axis_h, the h_rl stadium can be at the reference, or at the
    end of the reference (rl_h0 =0)

    ref_l points:

         fc_axis_s
           :
           :_________         
          /          \
         ( 2    1     ) -------> fc_axis_l
          \__________/ 


    Arguments:
    length: length of the parallels, from one semicircle center to the other
    r_s: Smaller radius of the semicircles
    r_l: Larger radius of the semicircles
    h_tot: Total height
    h_rl: height of the larger radius stadium
    fc_axis_h: vector on the direction of the height
    fc_axis_l: vector on the direction of the parallels, 
    ref_l: reference (zero) of the fc_axis_l
            1: reference on the center (makes axis_s symmetrical)
            2: reference at one of the semicircle centers (point 2)
               the other circle center will be on the direction of fc_axis_l
    rl_h0: 1: if the larger radius stadium is at the beginning of the axis_h
           0: at the end of axis_h

    xtr_h: if >0 it will be that extra height on the direction of fc_axis_h
    xtr_nh: if >0 it will be that extra height on the opositve direction of
             fc_axis_h
    pos: position of the reference


    """

    # normalize the axis_h
    axis_h = DraftVecUtils.scaleTo(fc_axis_h,1)

    # the r_s (smaller radius ) stadium goes all over the height
    if not (ref_l == 1 or ref_l == 2):
        logger.error('wrong value for ref_l')

    if  rl_h0 == 1: # the larger stadium is at the beginning:
        pos_rl = pos
        axis_h_rl = axis_h
        # no extra for the shorter stadium, so the surfaces are not in the
        # same plane
        xtr_nh_rs = 0
        xtr_h_rs = xtr_h
        xtr_nh_rl = xtr_nh
        xtr_h_rl = 0  # no extra on positive side, because it is inside
    else:
        pos_rl = pos + DraftVecUtils.scale(axis_h, h_tot)
        axis_h_rl = axis_h.negative()
        xtr_nh_rs = xtr_nh
        xtr_h_rs = 0
        xtr_nh_rl = xtr_h
        xtr_h_rl = 0 # no extra on positive side because is inside
                    

    shp_stadium_rs = shp_stadium_dir(length = length,
                                     radius = r_s, height = h_tot,
                                     fc_axis_l = fc_axis_l,
                                     fc_axis_h = axis_h,
                                     ref_l = ref_l,
                                     ref_s = 1,
                                     ref_h = 2, #ref at the end
                                     xtr_h = xtr_h_rs,
                                     xtr_nh = xtr_nh_rs,
                                     pos = pos)

    shp_stadium_rl = shp_stadium_dir(length = length,
                                     radius = r_l, height = h_rl,
                                     fc_axis_l = fc_axis_l,
                                     fc_axis_h = axis_h_rl,
                                     ref_l = ref_l,
                                     ref_s = 1,
                                     ref_h = 2, #ref at the end
                                     xtr_h = xtr_h_rl,
                                     xtr_nh = xtr_nh_rl,
                                     pos = pos_rl)

    shp_2stadium = shp_stadium_rs.fuse(shp_stadium_rl)
    shp_2stadium = shp_2stadium.removeSplitter()

    return (shp_2stadium)


#shp_2std = shp_2stadium_dir (
#                     length = 20, r_s = 10, r_l = 15,
#                     h_tot = 30, h_rl = 10,
#                     fc_axis_h = VZ,
#                     fc_axis_l = VX,
#                     ref_l = 2,
#                     rl_h0 = 2,
#                     xtr_h = 0,
#                     xtr_nh = 3,
#                     pos=V0)














# ------------------- def shp_belt_wire_dir

def shp_belt_wire_dir (center_sep, rad1, rad2, fc_axis_l = VX,
                       fc_axis_s = VY,
                       ref_l = 1,
                       ref_s = 1,
                       pos=V0):

    """
    Makes a shape of a wire with to circles and exterior tangent lines
    check: https://en.wikipedia.org/wiki/Tangent_lines_to_circles
    It is not easy to draw it well
    rad1 and rad2 can be exchanged, rad1 doesnt have to be larger

            ....                    fc_axis_s
           :    ( \ tangent          |
      rad1 :   (    \  .. rad2       |--> fc_axis_l, on the direction of rad2
           .--(  +   +)--
               (    /:
                ( /  :
                 :   :
                 :...:
                   + center_sep

 

                  ....                fc_axis_s
                 :    ( \ tangent       |
            rad1 :   (    \  .. rad2    |
                  --(  +   +)--         |--> fc_axis_l, on the direction of rad2
                     (    /:             centered on this axis
                      ( /  :
                       :   :
                       :...:
             ref_l: 3  2 1

 
    Arguments:
    center_sep: separation of the circle centers
    rad1: Radius of the firs circle, on the opposite direction of fc_axis_l
    fc_axis_l: vector on the direction circle centers, pointing to rad2
    fc_axis_s: vector on the direction perpendicular to fc_axis_l, on the plane
               of the wire
    ref_l: reference (zero) of the fc_axis_l
            1: reference on the center 
            2: reference at one of the semicircle centers (point 2)
               the other circle center will be on the direction of fc_axis_l
            3: reference at the end of rad1 circle
               the other end will be on the direction of fc_axis_l
    pos: FreeCAD vector of the position of the reference


    returns the shape of the wire
    """

    # normalize the axis
    axis_l = DraftVecUtils.scaleTo(fc_axis_l,1)
    axis_s = DraftVecUtils.scaleTo(fc_axis_s,1)


    #        ....                fc_axis_s
    #            :    ( \ tangent       |
    #       rad1 :   (    \  .. rad2    |
    #             --3  2 1 45--         |--> fc_axis_l, on the direction of rad2
    #                (    /:             centered on this axis
    #                 ( /  :
    #                  :   :
    #                  :...:
    #                    + center_sep
       

    # ----- Distance vectors on axis_l
    # distance from 1 to 2 in axis_l
    fc_1_2_l = DraftVecUtils.scale(axis_l, -center_sep/2.)
    fc_2_3_l = DraftVecUtils.scale(axis_l, -rad1)
    fc_2_4_l = DraftVecUtils.scale(axis_l, center_sep)
    fc_4_5_l = DraftVecUtils.scale(axis_l, rad2)
    fc_2_5_l = fc_2_4_l + fc_4_5_l
    # ----- reference is point 2 on axis_l
    # vector to go from the reference point to point 2 in l
    if ref_l == 1:  # ref on circle center sep
        refto_2_l = fc_1_2_l
    elif ref_l == 2:  # ref on circle center (rad1)
        refto_2_l = V0
    elif ref_l == 3:  # ref at the left end
        refto_2_l = fc_2_3_l.negative()
    else:
        logger.error('wrong ref_l in shp_belt_wire_dir')


    # Now define the center of the rad1 circle
    # and everything will be defined from this point
    # ln: L axis Negative side
    # lp: L axis Positive side
    # sn: S axis Negative side
    # sp: S axis Positive side
    # s0: S axis at zero
    #
    #        ....      ln_sp          fc_axis_s
    #            :    ( \ tangent     |
    #       rad1 :   (    \ lp_sp     |
    #           ln_s0  2   4lp_s0     |--> fc_axis_l, on the direction of rad2
    #                (    / lp_sn        centered on this axis
    #                 ( /
    #                  lp_sp
    #
    
    # cs_rad1 is point 2 (center of circle 1)
    cs_rad1 = pos +  refto_2_l
    # cs_rad2 is point 4 (center of circle 2)
    cs_rad2 = cs_rad1 + fc_2_4_l
    # ln_s0 is point 3 
    ln_s0_pos = cs_rad1 + fc_2_3_l
    # lp_s0 is point 5 
    lp_s0_pos = cs_rad2 + fc_4_5_l

    dif_rad = float(abs(rad1 - rad2))
    # Since we take our reference on axis_l, they are aligned, like if they were
    # on axis X, and axis Y would be zero.
    # therefore, angle gamma is zero (se wikipedia)
    # check: https://en.wikipedia.org/wiki/Tangent_lines_to_circles
    # the angle beta of the tanget is calculate from pythagoras:
    # the length (separation between centers) and dif_rad
    beta = math.atan (dif_rad/center_sep)
    print ('beta %f', 180*beta/math.pi)
    print ('beta %f', beta*math.pi/2)
    # depending on who is larger rad1 or rad2, the negative angle will be either
    # on top or down of axis_s

    #
    #                 (          \
    #                ( /alfa   beta\ which is 90-beta
    #               (               )
    #                (             / 
    #                 (          /
    #  
   
    cos_beta = math.cos(beta) 
    sin_beta = math.sin(beta) 
    tan_axis_s_rad1add = DraftVecUtils.scale(axis_s, rad1 * cos_beta)
    tan_axis_s_rad2add = DraftVecUtils.scale(axis_s, rad2 * cos_beta)
    if rad1 > rad2: # then it will be positive on axis_l on rad1 and rad2
        tan_axis_l_rad1add = DraftVecUtils.scale(axis_l, rad1 * sin_beta)
        tan_axis_l_rad2add = DraftVecUtils.scale(axis_l, rad2 * sin_beta)
    else:
        tan_axis_l_rad1add = DraftVecUtils.scale(axis_l, - rad1 * sin_beta)
        tan_axis_l_rad2add = DraftVecUtils.scale(axis_l, - rad2 * sin_beta)

    ln_sp_pos = cs_rad1 + tan_axis_l_rad1add + tan_axis_s_rad1add 
    ln_sn_pos = cs_rad1 + tan_axis_l_rad1add + tan_axis_s_rad1add.negative() 
    lp_sp_pos = cs_rad2 + tan_axis_l_rad2add + tan_axis_s_rad2add 
    lp_sn_pos = cs_rad2 + tan_axis_l_rad2add + tan_axis_s_rad2add.negative() 
    
    
    lin_p =  Part.Line(ln_sp_pos, lp_sp_pos).toShape() 
    arch_p = Part.Arc(lp_sp_pos, lp_s0_pos, lp_sn_pos).toShape()
    lin_n = Part.Line(lp_sn_pos, ln_sn_pos).toShape() 
    arch_n = Part.Arc(ln_sn_pos, ln_s0_pos, ln_sp_pos).toShape()
    wire_belt = Part.Wire ([lin_p, arch_p, lin_n, arch_n])

    #Part.show(wire_belt)
    return (wire_belt)


#belt_wire = shp_belt_wire_dir (center_sep = 70, rad1= 20, rad2=30,
#                       fc_axis_l = VX,
#                       fc_axis_s = VY,
#                       ref_l = 1,
#                       pos=FreeCAD.Vector(1,2,3))


def shp_belt_dir (center_sep, rad1, rad2, height,
                  fc_axis_h = VZ,
                  fc_axis_l = VX,
                  ref_l = 1,
                  ref_h = 1,
                  xtr_h = 0,
                  xtr_nh = 0,
                  pos=V0):

    """
    Makes a shape of 2 tangent circles (like a belt joining 2 circles).
    check shp_belt_wire_dir
    
    Arguments:
    center_sep: separation of the circle centers
    rad1: Radius of the first circle, on the opposite direction of fc_axis_l
    rad2: Radius of the second circle, on the direction of fc_axis_l
    height: height of the shape
    fc_axis_l: vector on the direction circle centers, pointing to rad2
    fc_axis_h: vector on the hieght direction
    ref_l: reference (zero) of the fc_axis_l
            1: reference on the center 
            2: reference at one of the semicircle centers (point 2)
               the other circle center will be on the direction of fc_axis_l
            3: reference at the end of rad1 circle
               the other end will be on the direction of fc_axis_l
    ref_h: 1: reference is at the center of the height
           2: reference is at the bottom
    xtr_h: if >0 it will be that extra height on the direction of fc_axis_h
    xtr_nh: if >0 it will be that extra height on the opositve direction of
             fc_axis_h
    pos: FreeCAD vector of the position of the reference

    returns the shape
    """

        # normalize the axis
    axis_l = DraftVecUtils.scaleTo(fc_axis_l,1)
    axis_h = DraftVecUtils.scaleTo(fc_axis_h,1)
    axis_h_n = axis_h.negative()
    axis_s = axis_l.cross(axis_h)
    
    if ref_h == 1: # we have to move the stadium half the height down + xtr_nh
        basepos = pos + DraftVecUtils.scale(axis_h_n, height/2. + xtr_nh)
    else:
        basepos = pos + DraftVecUtils.scale(axis_h_n, xtr_nh)

    shp_belt_wire = shp_belt_wire_dir (center_sep = center_sep,
                                       rad1 = rad1, rad2 = rad2,
                                       fc_axis_l = axis_l,
                                       fc_axis_s = axis_s,
                                       ref_l = ref_l,
                                       pos=basepos)

    # make a face of the wire
    shp_belt_face = Part.Face (shp_belt_wire)
    # extrude it
    dir_extrud = DraftVecUtils.scaleTo(axis_h, height + xtr_nh + xtr_h)
    shp_belt = shp_belt_face.extrude(dir_extrud)
    return (shp_belt)



#belt_shp = shp_belt_dir (center_sep = 70, rad1= 20, rad2=30, height = 10,
#                       fc_axis_l = VX,
#                       fc_axis_h = VZ,
#                       ref_l = 1,
#                       ref_h = 1,
#                       xtr_h = 0,
#                       xtr_nh = 0,
#                       pos=V0);
#Part.show(belt_shp)

def shp_hollowbelt_dir (center_sep, rad1, rad2,
                        rad_thick,
                        height,
                        fc_axis_h = VZ,
                        fc_axis_l = VX,
                        ref_l = 1,
                        ref_h = 1,
                        xtr_h = 0,
                        xtr_nh = 0,
                        pos=V0):

    """
    Makes a shape of 2 tangent circles (like a belt joining 2 circles).
    check shp_belt_wire_dir
    
    Arguments:
    center_sep: separation of the circle centers
    rad1: Internal radius of the first circle, on the opposite direction of
          fc_axis_l
    rad2: Internal radius of the second circle, on the direction of fc_axis_l
    rad_thick: increment to rad1 and rad2 to make the thickness. 
    height: height of the shape
    fc_axis_l: vector on the direction circle centers, pointing to rad2
    fc_axis_h: vector on the hieght direction
    ref_l: reference (zero) of the fc_axis_l
            1: reference on the center 
            2: reference at one of the semicircle centers (point 2)
               the other circle center will be on the direction of fc_axis_l
            3: reference at the end of rad1 circle
               the other end will be on the direction of fc_axis_l
    ref_h: 1: reference is at the center of the height
           2: reference is at the bottom
    xtr_h: if >0 it will be that extra height on the direction of fc_axis_h
    xtr_nh: if >0 it will be that extra height on the opositve direction of
             fc_axis_h
    pos: FreeCAD vector of the position of the reference

    returns the shape
    """


    belt_shp = shp_belt_dir (center_sep = center_sep,
                             rad1=rad1+rad_thick,
                             rad2=rad2+rad_thick,
                             height =height,
                             fc_axis_l = fc_axis_l,
                             fc_axis_h = fc_axis_h,
                             ref_l = ref_l,
                             ref_h = ref_h,
                             xtr_h = xtr_h,
                             xtr_nh = xtr_nh,
                             pos=pos);

    belt_shp_hole = shp_belt_dir (center_sep = center_sep,
                             rad1=rad1,
                             rad2=rad2,
                             height =height,
                             fc_axis_l = fc_axis_l,
                             fc_axis_h = fc_axis_h,
                             ref_l = ref_l,
                             ref_h = ref_h,
                             xtr_h = xtr_h+1,
                             xtr_nh = xtr_nh+1,
                             pos=pos);

    shp_belthole = belt_shp.cut(belt_shp_hole)

    shp_belthole = shp_belthole.removeSplitter()
    #Part.show(shp_belthole)

    return(shp_belthole)

#shp_belthollow = shp_hollowbelt_dir (
#                       center_sep = 70, rad1= 50, rad2=30,
#                       rad_thick = 4,
#                       height = 10,
#                       fc_axis_l = VX,
#                       fc_axis_h = VZ,
#                       ref_l = 2,
#                       ref_h = 1,
#                       xtr_h = 0,
#                       xtr_nh = 0,
#                       pos=V0);
    



# ------------------- def shpRndRectWire
# Creates a wire (shape), that is a rectangle with rounded edges.
# if r== 0, it will be a rectangle
# x: dimension of the base, on the X axis
# y: dimension of the height, on the Y axis
# r: radius of the rouned edge. 
# The wire will be centered
#
#                   Y
#                   |_ X
#               
#       ______     ___ y
#      /      \ r
#      |      |
#      |      |              z=0
#      |      |
#      \______/    ___
#      
#      |_______| x


def shpRndRectWire (x=1, y=1, r= 0.5, zpos = 0):

    #doc = FreeCAD.ActiveDocument

    if 2*r >= x or 2*r >= y:
        print "Radius too large: addRoundRectan"
        if x > y:
            r = y/2.0 - 0.1 # otherwise there will be a problem
        else:
            r = x/2.0 - 0.1 
    
    # points as if they were on X - Y
    #        lyy
    #    r_y      rx_y
    #       ______     
    # 0_ry /      \ x_ry
    #      |      |
    # lx0  |      |        lxx
    # 0_r  |      | x_r
    #      \______/  
    #      r_0  rx_0
    #         ly0


    x_0  =   - x/2.0
    x_r  = r - x/2.0
    x_rx = x/2.0 - r
    x_x  = x/2.0 
    y_0  =   - y/2.0
    y_r  = r - y/2.0
    y_ry = y/2.0 - r
    y_y  = y/2.0 

    # Lines:
    p_r_0  = FreeCAD.Vector(x_r,  y_0, zpos)
    p_rx_0 = FreeCAD.Vector(x_rx, y_0, zpos)
    # toShape, because otherwise we couldn't make the wire.
    # by doing this we are creating an edge
    # an alternative would be to use makeLine
    ly0 = Part.Line(p_r_0, p_rx_0).toShape() # Horizontal lower line

    p_x_r  = FreeCAD.Vector(x_x   ,y_r, zpos)
    p_x_ry = FreeCAD.Vector(x_x   ,y_ry, zpos)
    lxx = Part.Line(p_x_r, p_x_ry).toShape() # vertical on the right

    p_r_y  = FreeCAD.Vector(x_r,  y_y, zpos)
    p_rx_y = FreeCAD.Vector(x_rx, y_y, zpos)
    lyy = Part.Line(p_r_y, p_rx_y).toShape() # Horizontal top line

    p_0_r  = FreeCAD.Vector(x_0, y_r,  zpos)
    p_0_ry = FreeCAD.Vector(x_0, y_ry, zpos)
    lx0 = Part.Line(p_0_r, p_0_ry).toShape()  # vertical on the left
    # if I wanted to see these shapes
    #fc_ly0 = doc.addObject("Part::Feature", "ly0")
    #fc_ly0.Shape = ly0
    #fc_lxx = doc.addObject("Part::Feature", "lxx")
    #fc_lxx.Shape = lxx
    #fc_lyy = doc.addObject("Part::Feature", "lyy")
    #fc_lyy.Shape = lyy
    #fc_lx0 = doc.addObject("Part::Feature", "lx0")
    #fc_lx0.Shape = lx0

    if r > 0:
        # center points of the 4 archs:
        pcarch_00 = FreeCAD.Vector (x_r,  y_r,zpos)
        pcarch_x0 = FreeCAD.Vector (x_rx, y_r,zpos)
        pcarch_0y = FreeCAD.Vector (x_r,  y_ry,zpos)
        pcarch_xy = FreeCAD.Vector (x_rx, y_ry,zpos)
        dircir = FreeCAD.Vector (0,0,1)

        # ALTERNATIVE 1: Making the OpenCascade shape,
        # and adding it to a Freecad Object
        arch_00 = Part.makeCircle (r, pcarch_00, dircir, 180, 270) 
        arch_x0 = Part.makeCircle (r, pcarch_x0, dircir, 270, 0) 
        arch_0y = Part.makeCircle (r, pcarch_0y, dircir, 90, 180) 
        arch_xy = Part.makeCircle (r, pcarch_xy, dircir, 0, 90) 
        # freecad object
        #fc_arch_00 = doc.addObject("Part::Feature", "arch_00")
        #fc_arch_00.Shape = arch_00
        #fc_arch_x0 = doc.addObject("Part::Feature", "arch_x0")
        #fc_arch_x0.Shape = arch_x0
        #fc_arch_0y = doc.addObject("Part::Feature", "arch_0y")
        #fc_arch_0y.Shape = arch_0y
        #fc_arch_xy = doc.addObject("Part::Feature", "arch_xy")
        #fc_arch_xy.Shape = arch_xy
 
        # ALTERNATIVE 2: using the Part::Circle
        # you have to place it with Placement
        #cir_00 = doc.addObject("Part::Circle","cir_00")
        #cir_00.Angle0 = 180
        #cir_00.Angle1 = 270
        #cir_00.Radius = r
        #cir_00.Placement.Base = pcarch_00

        # Make a wire
        # it seems that it matters the order
        # for this example, it doesnt work if I do Part.Shape as in the 
        # example:
        # http://freecadweb.org/wiki/index.php?title=Topological_data_scripting
        wire_rndrect = Part.Wire ([
                                     lx0,
                                     arch_00,
                                     ly0,
                                     arch_x0,
                                     lxx,
                                     arch_xy,
                                     lyy,
                                     arch_0y
                                    ])
    else: # just a rectangle
        wire_rndrect = Part.Wire ([
                                     lx0,
                                     ly0,
                                     lxx,
                                     lyy,
                                    ])


    return wire_rndrect


# same as shpRndRectWire, but returns a face
def shp_rndrect_face (x, y, r=0.5, pos_z=0):

    shp_RndRectWire = shpRndRectWire (x, y, r=r, zpos= pos_z)
    shpRndRectFace = Part.Face (shp_RndRectWire)
    return shpRndRectFace

#doc = FreeCAD.newDocument()

#wire1 = shp_stadium_wire (4, 2, axis_rect='y', pos_z=2)

#wire1 = shpRndRectWire (x=10, y=12,  r=0)

#wire2 = shpaddRndRectWire (x=10-2, y=12-2, r= 0 )


#rndrect_1 = doc.addObject("Part::Feature", "rndrect_1")
#rndrect_1.Shape = wire1
#rndrect_2 = doc.addObject("Part::Feature", "rndrect_2")
#rndrect_2.Shape = wire2
#face1 = Part.Face(wire1)
#face2 = Part.Face(wire2)
#cut = face1.cut(face2)
#extr = cut.extrude(Base.Vector(0,0,5))
#Part.show(extr)

    #extr_rndrect = doc.addObject("Part::Extrusion", name)
    #extr_rndrect.Base = rndrect
    #extr_rndrect.Dir = (0,0,2)
    #extr_rndrect.Solid = True
    #shp_rndrect = Part.Shape 
    #fc_rndrect = doc.addObject("Part::Feature", "fc_rndrect")
    #fc_rndrect.Shape = shp_rndrect

#doc.recompute()
    

# ------------------- def wire_sim_xy
# Creates a wire (shape), from a list of points on the positive quadrant of XY
# the wire is simmetrical to both X and Y
# vecList: list of FreeCAD Vectors, the have to be in order clockwise
# if the first or the last points are not on the axis, a new point will be
# created
#
#                   Y
#                   |_ X
#               
#       __|__  
#      /  |  \ We receive these points
#      |  |  |
#      |  |--------          z=0
#      |     |
#      \_____/  
#      

def wire_sim_xy (vecList):

    edgList = []
    if vecList[0].x != 0:
        # the first element is not on the Y axis,so we create a first point
        vec = FreeCAD.Vector (0, vecList[0].y, vecList[0].z)
        seg = Part.Line(vec, vecList[0]) # segment
        edg = seg.toShape() # edge
        edgList.append(edg) # append to the edge list
    listlen = len(vecList)
    for index, vec in enumerate(vecList):
        if vec.x < 0 or vec.y < 0:
            logger.error('WireSimXY with negative points')
        if index < listlen-1: # it is not the last element
            seg = Part.Line(vec, vecList[index+1])
            edg = seg.toShape()
            edgList.append(edg)
        index += 1
    if vecList[-1].y != 0: # the last element is not on the X axis
        vec = FreeCAD.Vector (vecList[-1].x, 0, vecList[-1].z)
        seg = Part.Line(vecList[-1], vec)
        edg = seg.toShape()
        edgList.append(edg)
    # the wire for the first cuadrant, quarter
    quwire = Part.Wire(edgList)
    # mirror on Y axis
    MirY = FreeCAD.Matrix()
    MirY.scale(FreeCAD.Vector(-1,1,1))
    mir_quwire = quwire.transformGeometry(MirY)
    # another option
    # mir_quwire   = quwire.mirror(FreeCAD.Vector(0,0,0), FreeCAD.Vector(1,0,0))

    #halfwire = Part.Wire([quwire, mir_quwire]) # get the half wire
    halfwire = Part.Wire([mir_quwire, quwire]) # get the half wire
    # otherwise it doesnt work because the edges are not aligned
    halfwire.fixWire() 
    # mirror on X axis
    MirX = FreeCAD.Matrix()
    MirX.scale(FreeCAD.Vector(1,-1,1))
    mir_halfwire = halfwire.transformGeometry(MirX)
    totwire = Part.Wire([mir_halfwire, halfwire]) # get the total wire
    totwire.fixWire() 

    return totwire

# ------------------- end def wire_sim_xy


def regpolygon_vecl (n_sides, radius, x_angle=0):

    """
    calculates the vertexes of a regular polygon. Returns a list of 
    FreeCAD vectors with the vertexes. The first vertex will be repeated
    at the end, this is needed to close the wire to make the shape
    The polygon will be on axis XY (z=0). 

    Args:
        n_sides: number of sides of the polygon
        radius: Circumradius of the polygon
        x_angle: if zero, the first vertex will be on axis x (y=0)
                 if x_angle != 0, it will rotated some angle

    Returns:
        a list of FreeCAD.Vector of the vertexes

    """

    v = FreeCAD.Vector(radius, 0, 0)
    if x_angle != 0:
        # rotate the polygon
        x_angle_rad = math.radians(x_angle)
        # uses radians, rotates around Z axis
        # It seems that the angle of the function is wrong, changing the sign
        v = DraftVecUtils.rotate2D(v,-x_angle_rad)
    vec_vertex_list = [v]
    # divide the 360 degrees by the number of sides
    polygon_angle = 2*math.pi / n_sides
    for i in xrange(n_sides):
        v = DraftVecUtils.rotate2D(v,polygon_angle)
        # the first vertex will be also the last one
        vec_vertex_list.append(v)
    return (vec_vertex_list)


def regpolygon_dir_vecl (n_sides, radius, fc_normal, fc_verx1, pos):

    """
    Similar to regpolygon_vecl but in any place and direction of the space
    calculates the vertexes of a regular polygon. Returns a list of 
    FreeCAD vectors with the vertexes. The first vertex will be repeated
    at the end, this is needed to close the wire to make the shape
    The polygon will have the center in pos. The normal on fc_normal
    The direction of the first vertex on fc_verx_1

    Args:
        n_sides: number of sides of the polygon
        radius: Circumradius of the polygon
        fc_normal: FreeCAD.Vector with the direction of the normal
        fc_verx1: FreeCAD.Vector of direction of the first vertex
        pos: FreeCAD.Vector with the position of the center

    Returns:
        a list of FreeCAD.Vector of the vertexes

    """

    # normalize the normal direction
    nnormal = DraftVecUtils.scaleTo(fc_normal,1)

    # check if the vectors are perpendicular
    if not fc_isperp(nnormal, fc_verx1):
        logger.error('Vectors are Not perpendicular')
    #direction of the first vertex scaled to the radius
    n1dir_rad = DraftVecUtils.scaleTo(fc_verx1,radius)

    vertex_list = []
    # divide the 360 degrees by the number of sides
    polygon_angle = 2*math.pi / n_sides
    for i in range(n_sides):
        rot_angle = i*polygon_angle
        # Rotate n1dir, and then add to pos
        vertex = pos + DraftVecUtils.rotate(n1dir_rad,rot_angle,nnormal)
        vertex_list.append(vertex)
    # the first vertex will be also the last one
    vertex_list.append(vertex_list[0])
        
    return (vertex_list)




def shp_regpolygon_face (n_sides, radius,
                         n_axis='z', v_axis='x',
                         edge_rot=0, pos=V0):
    """
    makes the shape of a face of a regular polygon

    Args:
        n_sides: number of sides of the polygon
        radius: Circumradius of the polygon
        n_axis: Axis of the normal: 'x', '-x', 'y', '-y', 'z', '-z'
        v_axis : perpendicular to n_axis, pointing to the first vertex,
                 unless, x_angle is != 0. the vertex will be rotated
                 x_angle degrees for v_axis
        x_angle: if zero, the first vertex will be on axis v_axis 
                 if x_angle != 0, it will rotated some angle
        pos:  FreeCAD.Vector of the position of the center. Default (0,0,0)

    Returns:
        a shape (TopoShape) of the face

    """

    rpolygon_vlist = regpolygon_vecl (n_sides, radius, x_angle=edge_rot)
    rpolygon_wire = Part.makePolygon(rpolygon_vlist)
    vrot = calc_rot_z(getvecofname(n_axis), getvecofname(v_axis))
    rpolygon_wire.Placement.Rotation = vrot
    rpolygon_wire.Placement.Base = pos
    shp_rpolygon_face = Part.Face(rpolygon_wire)
    return shp_rpolygon_face
    


def shp_regpolygon_dir_face (n_sides, radius,
                         fc_normal=VZ, fc_verx1=VX,
                         pos=V0):
    """
    Similar to shp_regpolygon_face, but in any direction of the space
    makes the shape of a face of a regular polygon

    Args:
        n_sides: number of sides of the polygon
        radius: Circumradius of the polygon
        fc_normal: FreeCAD.Vector with the direction of the normal
        fc_verx1: FreeCAD.Vector of direction of the first vertex
        pos: FreeCAD.Vector of the position of the center. Default (0,0,0)

    Returns:
        a shape (TopoShape) of the face

    """

    rpolygon_vlist = regpolygon_dir_vecl (n_sides, radius, fc_normal,
                                          fc_verx1, pos)
    rpolygon_wire = Part.makePolygon(rpolygon_vlist)
    shp_rpolygon_face = Part.Face(rpolygon_wire)
    return shp_rpolygon_face


def shp_regprism (n_sides, radius, length,
                    n_axis='z', v_axis='x',
                    centered = 0,
                    edge_rot=0, pos=V0):
    """
    makes a shape of a face of a regular polygon

    Args:
        n_sides: number of sides of the polygon
        radius: Circumradius of the polygon
        length: length of the polygon
        n_axis: Axis of the normal: 'x', '-x', 'y', '-y', 'z', '-z'
        v_axis : perpendicular to n_axis, pointing to the first vertex,
                 unless, x_angle is != 0. the vertex will be rotated
                 x_angle degrees for v_axis
        centered: 1 if the extrusion is centered on pos (symmetrical)
        x_angle: if zero, the first vertex will be on axis v_axis 
                 if x_angle != 0, it will rotated some angle
        pos:  FreeCAD.Vector of the position of the center. Default (0,0,0)

    Returns:
        a shape (TopoShape) of the regular prism

    """

    shp_rpolygon_face = shp_regpolygon_face (n_sides,
                                             radius,
                                             n_axis = n_axis,
                                             v_axis = v_axis,
                                             edge_rot=edge_rot,
                                             pos = pos)
    vec_n_axis = getfcvecofname(n_axis)
    shp_rprism = shp_extrud_face(shp_rpolygon_face, length, vec_n_axis,centered)
    return shp_rprism


def shp_regprism_xtr (n_sides, radius, length,
                    n_axis='z', v_axis='x',
                    centered = 0,
                    xtr_top = 0,
                    xtr_bot = 0,
                    edge_rot=0, pos=V0):
    """
    makes a shape of a face of a regular polygon.
    Includes the posibility to add extra length on top and bottom.
    On top is easy, but at the bottom, the reference will be no counting that
    extra lenght added. This is useful to make boolean difference

    Args:
        n_sides: number of sides of the polygon
        radius: Circumradius of the polygon
        length: length of the polygon
        n_axis: Axis of the normal: 'x', '-x', 'y', '-y', 'z', '-z'
        v_axis : perpendicular to n_axis, pointing to the first vertex,
                 unless, x_angle is != 0. the vertex will be rotated
                 x_angle degrees for v_axis
        centered: 1 if the extrusion is centered on pos (symmetrical)
        xtr_top: add an extra lenght on top. If 0, nothing added
        xtr_bot: add an extra lenght at the bottom. If 0, nothing added
        x_angle: if zero, the first vertex will be on axis v_axis 
                 if x_angle != 0, it will rotated some angle
        pos:  FreeCAD.Vector of the position of the center. Default (0,0,0)

    Returns:
        a shape (TopoShape) of the regular prism

    """

    vec_n_axis = getfcvecofname(n_axis)
    if centered == 0:
        if xtr_bot > 0:
            # bring back the extra distance
            pos = pos - DraftVecUtils.scaleTo(vec_n_axis,xtr_bot)
    else:
        #centered, find the new center, related to how much is increased
        # on top and bottom
        pos = pos + (xtr_top - xtr_bot)/2.

    shp_rpolygon_face = shp_regpolygon_face (n_sides,
                                             radius,
                                             n_axis = n_axis,
                                             v_axis = v_axis,
                                             edge_rot=edge_rot,
                                             pos = pos)
    totlen = length + xtr_bot + xtr_top
    shp_rprism = shp_extrud_face(shp_rpolygon_face,
                                 totlen, vec_n_axis,centered)
    return shp_rprism

def shp_regprism_dirxtr (n_sides, radius, length,
                    fc_normal=VZ, fc_verx1=VX,
                    centered = 0,
                    xtr_top = 0,
                    xtr_bot = 0,
                    pos=V0):
    """
    Similar to shp_regprism_xtr, but in any direction
    makes a shape of a face of a regular polygon.
    Includes the posibility to add extra length on top and bottom.
    On top is easy, but at the bottom, the reference will be no counting that
    extra lenght added. This is useful to make boolean difference

    Args:
        n_sides: number of sides of the polygon
        radius: Circumradius of the polygon
        length: length of the polygon
        fc_normal: FreeCAD.Vector with the direction of the normal
        fc_verx1: FreeCAD.Vector of direction of the first vertex
        centered: 1 if the extrusion is centered on pos (symmetrical)
        xtr_top: add an extra lenght on top. If 0, nothing added
        xtr_bot: add an extra lenght at the bottom. If 0, nothing added
        pos:  FreeCAD.Vector of the position of the center. Default (0,0,0)

    Returns:
        a shape (TopoShape) of the regular prism

    """

    # normalize the normal:
    nnorm = DraftVecUtils.scaleTo(fc_normal, 1)
    totlen = length + xtr_bot + xtr_top
    if centered == 0:
        if xtr_bot > 0:
            # bring back the extra distance
            pos = pos - DraftVecUtils.scaleTo(nnorm,xtr_bot)
    else: #centered, find the new center
        movcenter = (xtr_top - xtr_bot)/2.
        pos = pos + DraftVecUtils.scaleTo(nnorm,movcenter) 

    shp_rpolygon_face = shp_regpolygon_dir_face (n_sides, radius,
                                                  nnorm, fc_verx1,
                                                  pos)
    shp_rprism = shp_extrud_face(shp_rpolygon_face,
                                 totlen, nnorm,centered)
    return shp_rprism


# ------------------ shp_extrud_face
# extrudes a face on any plane
# returns a shape
# 
#  Arguments:
# face: face to be extruded. 
# length: extrusion length
# centered: 1 if the extrusion is centered (simetrical) 0 if it is not
# vec_extr_axis: Typically, it will be the same as vec_facenormal.
#                by default, if it is 0, it will be equal to vec_facenormal
#    It doesn't have to be on an axis, it can be diagonally

def shp_extrud_face (face, length, vec_extr_axis, centered=0):

    
    # Normalize the extrusion vector
    vec_extr = DraftVecUtils.scaleTo(vec_extr_axis,length)

    if centered == 1:
        #we have to move it back half the lenght of the extrusion
        # either this or DraftVecUtils.neg( )
        pos = V0 - DraftVecUtils.scaleTo(vec_extr_axis,length/2.)
        face.Placement.Base = pos
 
    shp_extrusion = face.extrude(vec_extr)

    return (shp_extrusion)

            

# ------------------ shp_extrud_face_rot
# extrudes a face that is on plane XY, includes a rotation
# returns a shape
# 
#             Y
#             :
#         ____:___           
#         \   :   |
#          \  :...|...... X
#           \     |
#            \____|
#
#
#
# face: face to be extruded. On plane XY
# 
# vec_facenormal: FreeCAD vector that indicates where the normal of the 
#    face will point. The normal of the original face is VZ, but this 
#    function may rotate it depending on this argument
#    It has to be on an axis: 'x', 'y', ..
# vec_edgx: FreeCAD vector that indicates where the edge X will be after
#    the rotation
#    It has to be on an axis: 'x', 'y', ..
# length: extrusion length
# centered: 1 if the extrusion is centered (simetrical) 0 if it is not
# vec_extr_axis: Typically, it will be the same as vec_facenormal.
#                by default, if it is 0, it will be equal to vec_facenormal
#    It doesn't have to be on an axis, it can be diagonally

def shp_extrud_face_rot (face, vec_facenormal, vec_edgx, length, centered=0,
                     vec_extr_axis = 0):

    
    # since vec2 of calc_rot is referenced to VNZ, vec_facenomal is negated
    vec_nfacenormal = DraftVecUtils.neg(vec_facenormal)
    vrot = fc_calc_rot(vec_edgx, vec_nfacenormal)
    face.Placement.Rotation = vrot
    if vec_extr_axis == 0: # default case
        vec_extr_axis = vec_facenormal
    # Normalize the extrusion vector
    vec_extr = DraftVecUtils.scaleTo(vec_extr_axis,length)

    if centered == 1:
        #we have to move it back half the lenght of the extrusion
        # either this or DraftVecUtils.neg( )
        pos = V0 - DraftVecUtils.scaleTo(vec_extr_axis,length/2.)
        face.Placement.Base = pos
 
    shp_extrusion = face.extrude(vec_extr)

    # Reset the rotation of the original face
    # I am not sure, but I think it is necessary if I want to use it again
    # outside of the function
    face.Placement.Rotation = V0ROT
    face.Placement.Base = V0

    return (shp_extrusion)




def addBolt (r_shank, l_bolt, r_head, l_head,
             hex_head = 0, extra=1, support=1, headdown = 1, name="bolt"):
    """ 
    Creates the hole for the bolt shank and the head or the nut
    Tolerances have to be included

    Args:
        r_shank: Radius of the shank (tolerance included)
        l_bolt: total length of the bolt: head & shank
        r_head: radius of the head (tolerance included)
        l_head: length of the head
        hex_head: inidicates if the head is hexagonal or rounded
              1: hexagonal
              0: rounded
        h_layer3d: height of the layer for printing, if 0, means that the
                   support is not needed
        extra: 1 if you want 1 mm on top and botton to avoid cutting on the same
               plane pieces after making cuts (boolean difference) 
        support: 1 if you want to include a triangle between the shank and the
                 head to support the shank and not building the head on the
                 air using kcomp.LAYER3D_H
        headdown: 1 if the head is down. 0 if it is up
    """

    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    elements = []
    # shank
    shank =  doc.addObject("Part::Cylinder", name + "_shank")
    shank.Radius = r_shank
    shank.Height = l_bolt + 2*extra
    pos = FreeCAD.Vector(0,0,-extra)
    shank.Placement = FreeCAD.Placement(pos, V0ROT, V0)
    elements.append (shank)
    # head:
    if hex_head == 0:
        head =  doc.addObject("Part::Cylinder", name + "_head")
        head.Radius = r_head
    else:
        head =  doc.addObject("Part::Prism", name + "_head")
        head.Polygon = 6
        head.Circumradius = r_head

    head.Height = l_head + extra
    if headdown == 1:
        zposhead = -extra
    else:
        zposhead = l_bolt - l_head
    poshead =  FreeCAD.Vector(0,0,zposhead)
    head.Placement.Base = poshead
    elements.append (head)
    # support for the shank:
    if support==1 and kcomp.LAYER3D_H > 0:
        sup1 = doc.addObject("Part::Prism", name + "_sup1")
        sup1.Polygon = 3
        sup1.Circumradius = r_shank * 2
        # we could put it just on top of the head, but since we are going to 
        # make an union, we put it from the bottom (no need to include extra)
        # sup1.Height = kcomp.LAYER3D_H
        # pos1 = FreeCAD.Vector(0,0,l_head)
        # rot30z = FreeCAD.Rotation(VZ,30)
        # sup1.Placement = FreeCAD.Placement(pos1, rot30z, V0)
        sup1.Height = l_head + kcomp.LAYER3D_H
        # rotation make only make sense for hexagonal head, but it doesn't
        # matter for rounded head
        rot30z = FreeCAD.Rotation(VZ,30)
        if headdown == 1:
            zposheadsup1 = 0
        else:
            zposheadsup1 = l_bolt - l_head - kcomp.LAYER3D_H
        sup1.Placement.Base = FreeCAD.Vector(0,0,zposheadsup1)
        sup1.Placement.Rotation = rot30z
        # take vertex away:
        if hex_head == 0:
            sup1away = doc.addObject("Part::Cylinder", name + "_sup1away")
            sup1away.Radius = r_head
        else:
            sup1away = doc.addObject("Part::Prism", name + "_sup1away")
            sup1away.Polygon = 6
            sup1away.Circumradius = r_head
        # again, we take all the height
        sup1away.Height =  l_head + kcomp.LAYER3D_H
        sup1away.Placement.Base = sup1.Placement.Base
        sup1cut = doc.addObject("Part::Common", "sup1cut")
        sup1cut.Base = sup1
        sup1cut.Tool = sup1away
        elements.append (sup1cut)
        # another support
        # 1.15 is the relationship between the Radius and the Apothem
        # of the hexagon: sqrt(3)/2 . I make it slightly smaller
        sup2 = doc.addObject("Part::Prism", name + "_sup2")
        sup2.Polygon = 6
        sup2.Circumradius = r_shank * 1.15
        sup2.Height = l_head + 2* kcomp.LAYER3D_H
        if headdown == 1:
            zposheadsup2 = 0
        else:
            zposheadsup2 = l_bolt - l_head - 2* kcomp.LAYER3D_H
        sup2.Placement.Base = FreeCAD.Vector(0,0,zposheadsup2)
        elements.append (sup2)
  
    # union of elements
    bolt =  doc.addObject("Part::MultiFuse", name)
    bolt.Shapes = elements
    return bolt
"""
    bolt =  doc.addObject("Part::Fuse", name)
    bolt.Base = shank
    bolt.Tool = head
"""





def shp_bolt (r_shank, l_bolt, r_head, l_head,
              hex_head = 0,
              xtr_head=1,
              xtr_shank=1,
              support=1,
              axis = 'z',
              hex_ref = 'x',
              hex_rot_angle = 0,
              pos = V0):
    """ 
    Similar to addBolt, but creates a shape instead of a FreeCAD Object
    Creates a shape of the bolt shank and head or the nut
    Tolerances have to be included if you want it for making a hole

    It is referenced at the end of the head

    Args:
        r_shank: Radius of the shank (tolerance included)
        l_bolt: total length of the bolt: head & shank
        r_head: radius of the head (tolerance included)
        l_head: length of the head
        hex_head: inidicates if the head is hexagonal or rounded
              1: hexagonal
              0: rounded
        h_layer3d: height of the layer for printing, if 0, means that the
                   support is not needed
        xtr_head: 1 if you want 1 mm on the head to avoid cutting on the same
               plane pieces after making cuts (boolean difference) 
        xtr_shank: 1 if you want 1 mm at the opposite side of the head to
               avoid cutting on the same plane pieces after making cuts
               (boolean difference) 
        support: 1 if you want to include a triangle between the shank and the
                 head to support the shank and not building the head on the
                 air using kcomp.LAYER3D_H
        axis: 'x', '-x', 'y', '-y', 'z', '-z': defines the orientation
           for example:
           axis = '-z':              Z
                                     :
                         ....... ____:____
             xtr_head=1  .......|    :....|...... X
                                |         |
                                |__     __|
                                   |   |
                                   |   |
                                   |   |
                                   |___|

           axis = 'z':               Z
                                     :
                                     :
                                    _:_
                                   | : |
                                   | : |
                                   | : |
                                 __| : |__
                                |    :    |
             xtr_head=1  .......|    :....|...... X
                         .......|____:____|

        hex_ref: In case of a hexagonal head, this will indicate the
                 axis that the first vertex of the nut will point
                 hex_ref has to be perpendicular to axis, if not, it will be
                 changed
        hex_rot_angle: Angle in degrees. In case of a hexagonal head, it will
           indicate the angle of rotation of the hexagon referenced to hex_ref.

        pos: FreeCAD.Vector of the position of the center of the head of the
              bolt



    """

    elements = []
    v_axis = getfcvecofname(axis)
    # It is built as its orientation is 'z', it will be rotated at the end
    # shank
    # In shp_cylcenxtr, xtr_bot is where pos is (0). The head
    #   and xtr_bot is the other end (-z) if axis '-z'. The end of the shank
    shp_shank = shp_cylcenxtr (r_shank, l_bolt, v_axis,
                                ch=0,
                                # the shank end is top
                                xtr_top = xtr_shank,
                                # the head end is bottom
                                # No need to add extra, the head will do
                                xtr_bot = 0,
                                pos = pos)
    elements.append (shp_shank)
    # head:
    if hex_head == 0:
        shp_head = shp_cylcenxtr (r_head, l_head, v_axis,
                                   ch=0,
                                   # no extra on top, the shank will be there
                                   xtr_top = 0,
                                   xtr_bot = xtr_head,
                                   pos = pos)
    else:
        # check if axis and hex_ref are the same vector (wrong)
        if vecname_paral (axis, hex_ref):
            hex_ref = get_vecname_perpend(axis)
        shp_head = shp_regprism_xtr (n_sides=6,
                                     radius = r_head,
                                     length = l_head,
                                     n_axis=axis,
                                     v_axis=hex_ref,
                                     centered = 0,
                                     # no extra on top, the shank will be there
                                     xtr_top = 0,
                                     xtr_bot = xtr_head,
                                     edge_rot = hex_rot_angle,
                                     pos=pos)

    # Dont append the head, because multifuse requieres one outside
    #elements.append (shp_head)
    # support for the shank:
    if support==1 and kcomp.LAYER3D_H > 0:
        # we could put it just on top of the head, but since we are going to 
        # make an union, we put it from the bottom (no need to include extra)
        shp_sup1 = shp_regprism (n_sides=3,
                                 radius = 2*r_shank,
                                 length = l_head + kcomp.LAYER3D_H,
                                 n_axis=axis,
                                 v_axis=hex_ref,
                                 centered = 0,
                                 edge_rot = hex_rot_angle + 30,
                                 pos=pos)
        # take vertexes away:
        sup1away_l = l_head + kcomp.LAYER3D_H
        if hex_head == 0:
            shp_sup1away = shp_cyl(r_head, sup1away_l, v_axis, pos)
        else:
            shp_sup1away = shp_regprism(n_sides=6,
                                        radius= r_head,
                                        length= sup1away_l,
                                        n_axis = axis,
                                        v_axis = hex_ref,
                                        centered = 0,
                                        edge_rot = hex_rot_angle,
                                        pos = pos)
        shp_sup1cut = shp_sup1.common(shp_sup1away)
        elements.append (shp_sup1cut)
        # another support
        # 1.15 is the relationship between the Radius and the Apothem
        # of the hexagon: sqrt(3)/2 . I make it slightly smaller
        shp_sup2 = shp_regprism (n_sides=6,
                                 radius = 1.15*r_shank,
                                 length = l_head + 2* kcomp.LAYER3D_H,
                                 n_axis=axis,
                                 v_axis=hex_ref,
                                 centered = 0,
                                 edge_rot = hex_rot_angle,
                                 pos=pos)
        elements.append (shp_sup2)
  
    # union of elements
    shp_bolt = shp_head.multiFuse(elements)
    shp_bolt = shp_bolt.removeSplitter()
    return shp_bolt




def shp_bolt_dir (r_shank, l_bolt, r_head, l_head,
              hex_head = 0,
              xtr_head=1,
              xtr_shank=1,
              support=1,
              fc_normal = VZ,
              fc_verx1 = VX,
              #default value has to be 0 for backward compatibility
              #because it didnt exist before
              pos_n = 0,
              pos = V0):
    """ 
    Similar to shp_bolt, but it can be done in any direction
    Creates a shape, not a of a FreeCAD Object
    Creates a shape of the bolt shank and head or the nut
    Tolerances have to be included if you want it for making a hole

    It is referenced at the end of the head

    Args:
        r_shank: Radius of the shank (tolerance included)
        l_bolt: total length of the bolt: head & shank
        r_head: radius of the head (tolerance included)
        l_head: length of the head
        hex_head: inidicates if the head is hexagonal or rounded
              1: hexagonal
              0: rounded
        h_layer3d: height of the layer for printing, if 0, means that the
                   support is not needed
        xtr_head: 1 if you want 1 mm on the head to avoid cutting on the same
               plane pieces after making cuts (boolean difference) 
        xtr_shank: 1 if you want 1 mm at the opposite side of the head to
               avoid cutting on the same plane pieces after making cuts
               (boolean difference) 
        support: 1 if you want to include a triangle between the shank and the
                 head to support the shank and not building the head on the
                 air using kcomp.LAYER3D_H
        fc_normal: FreeCAD.Vector: defines the orientation
           for example:
           fc_normal = (0,0,-1):     Z
                                     :
                         ....... ____:____
           ..xtr_head=1  .......|    :....|...... X  pos_n = 0
           :      l_head+:      |         |
           :             :......|__     __|          pos_n = 1
           :+ l_bolt               |   |
           :                       |   |
           :.......................|   |.............pos_n = 2
                                   |___|....xtr_shank
                                     :
                                     :
                                   fc_normal



           fc_normal = (0,0,1):      Z
                                     :
                                     :
                                    _:_
                                   | : |
                                   | : |
                                   | : |
                                 __| : |__
                                |    :    |
             xtr_head=1  .......|    :....|...... X
                         .......|____:____|

        fc_verx1: In case of a hexagonal head, this will indicate the
                 axis that the first vertex of the nut will point
                 it has to be perpendicular to fc_normal, 

        pos_n: location of pos along the normal, at the cylinder center
            0: at the top of the head (excluding xtr_head)
            1: at the union of the head and the shank
            2: at the end of the shank (excluding xtr_shank)

        pos: FreeCAD.Vector of the position of the center of the head of the
              bolt



    """

    elements = []
    nnormal = DraftVecUtils.scaleTo(fc_normal,1)

    # vectors to pos_n = 0 (to the end of the head)
    n0to = {}
    n0to[0] = V0
    n0to[1] = DraftVecUtils.scale(nnormal, l_head) # xtr_head not included
    n0to[2] = DraftVecUtils.scale(nnormal, l_bolt) # xtr_head/shank not included
    pos0 = pos + (n0to[pos_n]).negative()

    shp_shank = shp_cylcenxtr (r_shank, l_bolt, nnormal,
                                ch=0,
                                # the shank end is top
                                xtr_top = xtr_shank,
                                # the head end is bottom
                                # No need to add extra, the head will do
                                xtr_bot = 0,
                                pos = pos0)
    elements.append (shp_shank)
    # head:
    if hex_head == 0:
        shp_head = shp_cylcenxtr (r_head, l_head, nnormal,
                                  ch=0,
                                  # no extra on top, the shank will be there
                                  xtr_top = 0,
                                  xtr_bot = xtr_head,
                                  pos = pos0)
        if not fc_isperp(nnormal, fc_verx1):
            # get any perpendicular vector:
            fc_verx1 = get_fc_perpend1(nnormal)     
    else:
        # check if fc_normal and fc_verx1 are perpendicular
        if not fc_isperp(nnormal, fc_verx1):
            logger.debug('Vectors are not perpendicular')
            # get any perpendicular vector:
            fc_verx1 = get_fc_perpend1(nnormal)

        shp_head = shp_regprism_dirxtr (
                                     n_sides=6,
                                     radius = r_head,
                                     length = l_head,
                                     fc_normal=nnormal,
                                     fc_verx1=fc_verx1,
                                     centered = 0,
                                     # no extra on top, the shank will be there
                                     xtr_top = 0,
                                     xtr_bot = xtr_head,
                                     pos=pos0)

    # Dont append the head, because multifuse requires one outside of the list
    # elements.append (shp_head)
    # support for the shank:
    if support==1 and kcomp.LAYER3D_H > 0:
        # we could put it just on top of the head, but since we are going to 
        # make an union, we put it from the bottom (no need to include extra)
        # have to rotate 30 degrees the vertex for this triangle
        fc_verx1_triangle = DraftVecUtils.rotate(fc_verx1, math.pi/6., nnormal)
        shp_sup1 = shp_regprism_dirxtr (n_sides=3,
                                 radius = 2*r_shank,
                                 length = l_head + kcomp.LAYER3D_H,
                                 fc_normal=nnormal,
                                 fc_verx1=fc_verx1_triangle,
                                 centered = 0,
                                 pos=pos0)
        # take vertexes away:
        sup1away_l = l_head + kcomp.LAYER3D_H
        if hex_head == 0:
            shp_sup1away = shp_cyl(r_head, sup1away_l, nnormal, pos0)
        else:
            shp_sup1away = shp_regprism_dirxtr (
                                        n_sides=6,
                                        radius= r_head,
                                        length= sup1away_l,
                                        fc_normal=nnormal,
                                        fc_verx1=fc_verx1,
                                        centered = 0,
                                        pos = pos0)
        shp_sup1cut = shp_sup1.common(shp_sup1away)
        elements.append (shp_sup1cut)
        # another support
        # 1.15 is the relationship between the Radius and the Apothem
        # of the hexagon: sqrt(3)/2 . I make it slightly smaller
        shp_sup2 = shp_regprism_dirxtr (
                                 n_sides=6,
                                 radius = 1.15*r_shank,
                                 length = l_head + 2* kcomp.LAYER3D_H,
                                 fc_normal=nnormal,
                                 fc_verx1=fc_verx1,
                                 centered = 0,
                                 pos=pos0)
        elements.append (shp_sup2)
  
    # union of elements
    shp_bolt = shp_head.multiFuse(elements)
    shp_bolt = shp_bolt.removeSplitter()
    return shp_bolt

#doc = FreeCAD.newDocument()
#shp = shp_bolt_dir (r_shank = 5, l_bolt=50, r_head=10, l_head=12,
#                   hex_head = 1,
#                   xtr_head=1,
#                   xtr_shank=1,
#                   support=0,
#                   fc_normal = FreeCAD.Vector(1,1,1),
#                   fc_verx1 = VX,
#                   pos_n = 1,
#                   pos = V0)
#Part.show(shp)


def addBoltNut_hole (r_shank,        l_bolt, 
                     r_head,         l_head,
                     r_nut,          l_nut,
                     hex_head = 0,   extra=1,
                     supp_head=1,    supp_nut=1,
                     headdown=1,     name="bolt"):

    """
    Creates the hole for the bolt shank, the head and the nut.
    The bolt head will be at the botton, and the nut will be on top
    Tolerances have to be already included in the argments values

    Args:
        r_shank: Radius of the shank (tolerance included)
        l_bolt: total length of the bolt: head & shank
        r_head: radius of the head (tolerance included)
        l_head: length of the head
        r_nut : radius of the nut (tolerance included)
        l_nut : length of the nut. It doesn't have to be the length of the nut
                but how long you want the nut to be inserted
        hex_head: inidicates if the head is hexagonal or rounded
                  1: hexagonal
                  0: rounded
        zpos_nut: inidicates the height position of the nut, the lower part     
        h_layer3d: height of the layer for printing,
                   if 0, means that the support is not needed
        extra: 1 if you want 1 mm on top and botton to avoid cutting on the same
                 plane pieces after makeing differences 
        support: 1 if you want to include a triangle between the shank and the
                 head to support the shank and not building the head on the air
                 using kcomp.LAYER3D_H
    """
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    elements = []
    bolt = addBolt  (r_shank  = r_shank,
                     l_bolt   = l_bolt,
                     r_head   = r_head,
                     l_head   = l_head,
                     hex_head = hex_head,
                     extra    = extra,
                     support  = supp_head,
                     headdown = headdown,
                     name     = name + "_bolt")

    nut = doc.addObject("Part::Prism", name + "_nut")
    nut.Polygon = 6
    nut.Circumradius = r_nut
    nut.Height = l_nut + extra
    if headdown == 1:
        pos = FreeCAD.Vector (0, 0, l_bolt - l_nut)
    else:
        pos = FreeCAD.Vector (0, 0, -extra)
    nut.Placement = FreeCAD.Placement(pos, V0ROT, V0)
    elements.append (bolt)
    elements.append (nut)
    # support for the nut
    if supp_nut == 1 and kcomp.LAYER3D_H > 0:
        supnut1 = doc.addObject("Part::Prism", name + "_nutsup1")
        supnut1.Polygon = 3
        supnut1.Circumradius = r_shank * 2
        supnut1.Height = l_nut + kcomp.LAYER3D_H
        if headdown == 1:
            pos_supnut1 = FreeCAD.Vector (0, 0,
                                          l_bolt - l_nut - kcomp.LAYER3D_H)
        else:
            pos_supnut1 = V0
        rot30z = FreeCAD.Rotation(VZ,30)
        supnut1.Placement = FreeCAD.Placement(pos_supnut1, rot30z, V0)
        # take vertex away:
        supnut1away = doc.addObject("Part::Prism", name + "_supnut1away")
        supnut1away.Polygon = 6
        supnut1away.Circumradius = r_nut
        supnut1away.Height =  supnut1.Height
        supnut1away.Placement = FreeCAD.Placement(pos_supnut1, V0ROT, V0)
        supnut1cut = doc.addObject("Part::Common", "supnut1_cut")
        supnut1cut.Base = supnut1
        supnut1cut.Tool = supnut1away
        elements.append (supnut1cut)
        # the other support
        # 1.15 is the relationship between the Radius and the Apothem
        # of the hexagon: sqrt(3)/2 . I make it slightly smaller
        supnut2 = doc.addObject("Part::Prism", name + "_supnut2")
        supnut2.Polygon = 6
        supnut2.Circumradius = r_shank * 1.15
        supnut2.Height = l_nut + 2* kcomp.LAYER3D_H
        if headdown == 1:
            pos_supnut2 = FreeCAD.Vector(0,0,
                                         l_bolt - l_nut - 2*kcomp.LAYER3D_H)
        else:
            pos_supnut2 = V0
        supnut2.Placement = FreeCAD.Placement(pos_supnut2, V0ROT, V0)
        elements.append (supnut2)

    boltnut = doc.addObject("Part::MultiFuse", "boltnut")
    boltnut.Shapes = elements
    return boltnut
      



def shp_boltnut_dir_hole (r_shank,        l_bolt, 
                          r_head,         l_head,
                          r_nut,          l_nut,
                          hex_head=0,   
                          xtr_head=1,     xtr_nut=1,
                          supp_head=1,    supp_nut=1,
                          headstart=1,    
                          fc_normal = VZ, fc_verx1=V0,
                          pos = V0):

    """
    similar to addBoltNut_hole, but in any direction and creates shapes,
    not FreeCAD Objects
    Creates the hole for the bolt shank, the head and the nut.
    The bolt head will be at the botton, and the nut will be on top
    Tolerances have to be already included in the argments values

    Args:
        r_shank: Radius of the shank (tolerance included)
        l_bolt: total length of the bolt: head & shank
        r_head: radius of the head (tolerance included)
        l_head: length of the head
        r_nut : radius of the nut (tolerance included)
        l_nut : length of the nut. It doesn't have to be the length of the nut
                but how long you want the nut to be inserted
        hex_head: inidicates if the head is hexagonal or rounded
                  1: hexagonal
                  0: rounded
        xtr_head: 1 if you want an extra size on the side of the head
                   to avoid cutting on the same plane pieces after making
                   differences 
        xtr_nut: 1 if you want an extra size on the side of the nut
                   to avoid cutting on the same plane pieces after making
                   differences 
        supp_head: 1 if you want to include a triangle between the shank and the
                 head to support the shank and not building the head on the air
                 using kcomp.LAYER3D_H
        supp_nut: 1 if you want to include a triangle between the shank and the
                 nut to support the shank and not building the nut on the air
                 using kcomp.LAYER3D_H
        headstart: if on pos you have the head, or if you have it on the
                   other end
        fc_normal: direction of the bolt
        fc_verx1:  direction of the first vertex of the hexagonal nut.
                 Perpendicular to fc_normal. If not perpendicular or zero,
                 means that it doesn't matter which direction and the function
                 will obtain one perpendicular direction
        pos: position of the head (if headstart) or of the nut 
    """
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument

    # normalize
    nnormal = DraftVecUtils.scaleTo(fc_normal,1)
    if not fc_isperp(nnormal, fc_verx1):
        # if they are not perpendicular (or if fc_verx1 is null)
        # get a perpendicular vector
        nverx1 = get_fc_perpend1(nnormal)
    else:
        nverx1 = DraftVecUtils.scaleTo(fc_verx1,1)

    # vector from the origin position (pos) to the end
    pos2end = DraftVecUtils.scaleTo(nnormal, l_bolt)
    # nnormal negated
    nnormal_neg = DraftVecUtils.scaleTo(nnormal,-1)
    if headstart == 1:
        #the head will be on pos and the nut on pos + l_bolt
        pos_head = pos
        pos_nut = pos + pos2end
        nnormal_head = nnormal
        nnormal_nut = nnormal_neg
    else:
        #the nut will be on pos and the head on pos + l_bolt
        pos_head = pos + pos2end
        pos_nut = pos
        nnormal_head = nnormal_neg
        nnormal_nut = nnormal


    # bolt with the head:
    shp_bolt = shp_bolt_dir  (r_shank  = r_shank,
                          l_bolt   = l_bolt,
                          r_head   = r_head,
                          l_head   = l_head,
                          hex_head = hex_head,
                          xtr_head = xtr_head,
                          xtr_shank = 0, # no need, the nut will go extra
                          support   = supp_head,
                          fc_normal = nnormal_head,
                          fc_verx1  = nverx1,
                          pos_n     = 0,
                          pos       = pos_head)

    # Nut:
    shp_nut = shp_regprism_dirxtr ( 
                                     n_sides = 6,
                                     radius  = r_nut,
                                     length  = l_nut,
                                     fc_normal = nnormal_nut,
                                     fc_verx1  = nverx1,
                                     centered  = 0,
                                     # no extra on top, the shank will be there
                                     xtr_top   = 0,
                                     xtr_bot   = xtr_nut,
                                     pos       = pos_nut)

    nut_elements = [shp_nut]
    # support for the nut
    if supp_nut == 1 and kcomp.LAYER3D_H > 0:
        # rotate 30 degrees
        nverx1_triangle =  DraftVecUtils.rotate(nverx1,
                                                -math.pi/6., nnormal_nut)
        shp_sup1 = shp_regprism_dirxtr (n_sides=3,
                                 radius = 2*r_shank,
                                 length = l_nut + kcomp.LAYER3D_H,
                                 fc_normal=nnormal_nut,
                                 fc_verx1=nverx1_triangle,
                                 centered = 0,
                                 pos=pos_nut)
        # take vertexes away:
        sup1away_l = l_nut + kcomp.LAYER3D_H
        shp_sup1away = shp_regprism_dirxtr (
                                        n_sides=6,
                                        radius= r_nut,
                                        length= sup1away_l,
                                        fc_normal=nnormal_nut,
                                        fc_verx1=nverx1,
                                        centered = 0,
                                        pos = pos_nut)
        shp_sup1cut = shp_sup1.common(shp_sup1away)
        nut_elements.append (shp_sup1cut)

        # another support
        # 1.15 is the relationship between the Radius and the Apothem
        # of the hexagon: sqrt(3)/2 . I make it slightly smaller
        shp_sup2 = shp_regprism_dirxtr (
                                 n_sides=6,
                                 radius = 1.15*r_shank,
                                 length = l_nut + 2* kcomp.LAYER3D_H,
                                 fc_normal=nnormal_nut,
                                 fc_verx1=nverx1,
                                 centered = 0,
                                 pos=pos_nut)
        nut_elements.append (shp_sup2)
        

    # union of elements
    shp_boltnut = shp_bolt.multiFuse(nut_elements)
    shp_boltnut = shp_boltnut.removeSplitter()
    return shp_boltnut


# ------------------- def aluprof_vec
# Creates a wire (shape), that is an approximation of a generic alum
# profile extrusion 
# width: the total width of the profile, it is a square
# thick: the thickness of the side
# slot: the width of the rail 
# insquare: the width of the inner square
# indiam: the diameter of the inner hole
#
#                   Y
#                   |_ X
#      :----- width ----:
#      :       slot     :
#      :      :--:      :
#      :______:  :______:
#      |    __|  |__    |
#      | |\ \      / /| |
#      |_| \ \____/ / |_| ...........
#          |        | ......        insquare
#          |  (  )  | ......indiam  :
#       _  |  ____  | ..............:
#      | | / /    \ \ | |
#      | |/ /_    _\ \| | .... 
#      |______|  |______| ....thick

#                                   Y values:
#   :  3 _____ 4
#   :   |_1  7| ................... 1,2: width/2 - thick
#   :  2 / /|_| ....................7: width/2- (thick+thick*cos45)
#   :___/ / 6  5 .....................              5,6: slot/2.
#   :  0  |8     :8:insquare/2-thick*cos45  0:insquare/2  :
#   :.....|......:..........................:.............:


# obtains the points of the aluminum profile positive quadrant

def aluprof_vec (width, thick, slot, insquare):


    y = []
    y.append(insquare/2)               # y0, x8
    y.append(width/2. - thick)         # y1, x7
    y.append(y[-1])                    # y2, x6,  y2==y1
    y.append(width/2.)                 # y3, x5
    y.append(y[-1])                    # y4, x4,  y4==y3
    y.append(slot/2.)                  # y5, x3
    y.append(y[-1])                    # y6, x2   y6==y5
    y.append(width/2.-thick*(1+COS45))  # y7, x1
    y.append(insquare/2.-thick*COS45)        # y8, x0

    n = len(y)-1

    vec = []
    for ind in range(len(y)):
        vec.append(FreeCAD.Vector(y[n-ind], y[ind], 0))

    return (vec)

    

"""
    y1 = insquare/2          # x9
    y2 = width/2. - thick    # x8
    y3 = y2                  # x7
    y4 = width/2.            # x6
    y5 = y4                  # x5
    y6 = width/2. - slot/2.  # x4
    y7 = y6                  # x3
    y8 = width/2.-2*thick    # x2
    y9 = insquare/2.-thick   # x1
"""

    
# ------------------- def shp_aluwire_dir

def shp_aluwire_dir (width, thick, slot, insquare,
                    fc_axis_x=VX, fc_axis_y=VY,
                    ref_x = 1, ref_y = 1,
                    pos=V0):


    """
    Creates a wire (shape), that is an approximation of a generic alum
    profile extrusion. Creates it in any position an any direction
    width: the total width of the profile, it is a square
    thick: the thickness of the side
    slot: the width of the rail 
    insquare: the width of the inner square
    indiam: the diameter of the inner hole
    fc_axis_x : is a generic X axis, can be any
        1: reference (zero) at the center
        2: reference (zero) at the side, the other end side will be on the
           direction of fc_axis_x
    fc_axis_y : is a generic Y axis, can be any perpendicular to fc_axis_y
        1: reference (zero) at the center
        2: reference (zero) at the side, the other end side will be on the
           direction of fc_axis_y
    ref_x: reference (zero) on the fc_axis_x
    ref_y: reference (zero) on the fc_axis_1
    pos: position of the center
    
                      Y
                      |_ X
         :----- width ----:
         :       slot     :
         :      :--:      :
         :______:  :______:
         |    __|  |__    |
         | |\ \      / /| |
         |_| \ \____/ / |_| ...........
             |        | ......        insquare
             |  (  )  | ......indiam  :
          _  |  ____  | ..............:
         | | / /    \ \ | |
         | |/ /_    _\ \| | .... 
         |______|  |______| ....thick
    
                                      Y values:
      :  3 _____ 4
      :   |_1  7| ................... 1,2: width/2 - thick
      :  2 / /|_| ....................7: width/2- (thick+thick*cos45)
      :___/ / 6  5 .....................              5,6: slot/2.
      :  0  |8     :8:insquare/2-thick*cos45  0:insquare/2  :
      :.....|......:..........................:.............:
    
     ref_x= 1 ; ref_y = 1
               fc_axis_w
                :
                :
             _  :  _
            |_|_:_|_|
      ........|.:.|........ fc_axis_p
             _|_:_|_
            |_| : |_|
                :
                :
                :
   
   
     ref_x= 2 ; ref_y = 1 (the zero of axis_y is at the center)
                          (the zero of axis_x is at one side)

                fc_axis_y
                :       
                :      
                :  
                :_     _ 
                |_|___|_|
      ..........:.|...|........ fc_axis_x
                :_|___|_
                |_|   |_|
                :
                :
                :

    """

    axis_x = DraftVecUtils.scaleTo(fc_axis_x, 1)
    axis_y = DraftVecUtils.scaleTo(fc_axis_y, 1)

    # Get the center position
    if ref_x == 2:
        ref2center_x = DraftVecUtils.scale(axis_x, width/2.)
    else:
        ref2center_x = V0
    if ref_y == 2:
        ref2center_y = DraftVecUtils.scale(axis_y, width/2.)
    else:
        ref2center_y = V0

    center_pos = pos + ref2center_x + ref2center_y

    y = []
    y.append(insquare/2)               # y0, x8
    y.append(width/2. - thick)         # y1, x7
    y.append(y[-1])                    # y2, x6,  y2==y1
    y.append(width/2.)                 # y3, x5
    y.append(y[-1])                    # y4, x4,  y4==y3
    y.append(slot/2.)                  # y5, x3
    y.append(y[-1])                    # y6, x2   y6==y5
    y.append(width/2.-thick*(1+COS45))  # y7, x1
    y.append(insquare/2.-thick*COS45)        # y8, x0

    n = len(y)-1

    #
    #       1st point
    #       |      go clockwise
    #    2  |  1
    #   ----|----
    #    3  |  4
    #       |
    #
    #

    vec = []
    # First quadrant
    for ind in range(len(y)):
        point = (center_pos + DraftVecUtils.scale(axis_x,  y[n-ind])
                            + DraftVecUtils.scale(axis_y,  y[ind]))
        vec.append(point)
    # 4 quadrant
    for ind in range(len(y)):
        point = (center_pos + DraftVecUtils.scale(axis_x,  y[ind])
                            + DraftVecUtils.scale(axis_y, -y[n-ind]))
        vec.append(point)
    # 3 quadrant
    for ind in range(len(y)):
        point = (center_pos + DraftVecUtils.scale(axis_x, -y[n-ind])
                            + DraftVecUtils.scale(axis_y, -y[ind]))
        vec.append(point)
    # 2 quadrant
    for ind in range(len(y)):
        point = (center_pos + DraftVecUtils.scale(axis_x, -y[ind])
                            + DraftVecUtils.scale(axis_y,  y[n-ind]))
        vec.append(point)

    # The first point has to be the last to close the wire
    vec.append(vec[0])


    shp_aluwire = Part.makePolygon(vec)

    return (shp_aluwire)

    
  
# -------------------- NutHole -----------------------------
# adding a Nut hole (hexagonal) with a prism attached to introduce the nut
# tolerances are included
# nut_r : circumradius of the hexagon
# nut_h : height of the nut, usually larger than the actual nut height, to be
#         able to introduce it
# hole_h: the hole height, from the center of the hexagon to the side it will
#         see light
# name:   name of the object (string)
# extra:  1 if you want 1 mm out of the hole, to cut
# nuthole_x: 1 if you want that the nut height to be along the X axis
#           and the 2*apotheme on the Y axis
#           ie. Nut hole facing X
#         0 if you want that the nut height to be along the Y axis
#           ie. Nut hole facing Y
# cx:     1 if you want the coordinates referenced to the x center of the piece
#         it can be done because it is a new shape formed from the union
# cy:     1 if you want the coordinates referenced to the y center of the piece
# holedown:  I THINK IS THE OTHER WAY; CHECK
#             0: the z0 is the bottom of the square (hole)
#             1: the z0 is the center of the hexagon (nut)
#              it can be done because it is a new shape formed from the union
#
#    0               1       
#       /\              __
#      |  |            |  |
#      |  |            |  |
#      |__|__ z = 0    |  | -- z = 0
#                       \/

class NutHole (object):

    def __init__(self, nut_r, nut_h, hole_h, name,
                 extra = 1, nuthole_x = 1, cx=0, cy=0, holedown = 0):
        self.nut_r   = nut_r
        self.nut_h   = nut_h
        self.nut_2ap = 2 * nut_r * COS30    #Apotheme = R * cos (30)
        self.hole_h  = hole_h
        self.name    = name
        self.extra   = extra
        self.nuthole_x = nuthole_x
        self.cx      = cx
        self.cy      = cy
        self.holedown = holedown
  
        doc = FreeCAD.ActiveDocument
        self.doc     = doc

        # the nut
        nut = doc.addObject("Part::Prism", name + "_nut")
        nut.Polygon = 6
        nut.Circumradius = nut_r
        nut.Height = nut_h
        self.nutObj  = nut

        if nuthole_x == 1:
            x_hole = nut_h
            y_hole = self.nut_2ap
            nutrot = FreeCAD.Rotation(VY,90)
            if cx == 1: #centered on X,
                xpos_nut = - nut_h / 2.0
            else:
                xpos_nut = 0
            if cy == 1: #centered on Y, already is
                ypos_nut = 0
            else:
              # already starting on y=0
              ypos_nut = self.nut_2ap/2.0
        else : # nut h is on Y
            x_hole = self.nut_2ap
            y_hole = nut_h
            # the rotation of the nut will be on X
            # this is a rotation of Yaw and Pitch, because we want to have the
            # vertex on top, not the face of the hexagonal prism
            nutrot = FreeCAD.Rotation(90,90,0)
            if cx == 1: #centered on X, already is
                xpos_nut = 0
            else:
                # move to the half of the apotheme
                xpos_nut = self.nut_2ap/2.0
            if cy == 1: #centered on Y, 
                ypos_nut = - nut_h / 2.0
            else:
                # already starting on y=0
                ypos_nut = 0

        hole = addBox (x_hole, y_hole, hole_h + extra, name + "_hole",
                     cx = cx, cy = cy)
        self.holeObj = hole

        if holedown== 1:
            # the nut will be top
            zpos_nut = hole_h
            if extra > 0: # then we will have to bring down the z of the hole
              hole.Placement.Base =   hole.Placement.Base \
                                    + FreeCAD.Vector(0,0,-extra)
        else:
            zpos_nut = 0

        nut.Placement.Base = FreeCAD.Vector (xpos_nut, ypos_nut, zpos_nut)
        nut.Placement.Rotation = nutrot

        nuthole =  doc.addObject("Part::Fuse", name)
        nuthole.Base = nut
        nuthole.Tool = hole
        self.fco = nuthole   # the FreeCad Object


 
# -------------------- shp_nuthole -----------------------------

def shp_nuthole (nut_r, nut_h, hole_h,
                 xtr_nut = 1, xtr_hole = 1,
                 fc_axis_nut = VX,
                 fc_axis_hole = VZ,
                 ref_nut_ax = 1,
                 ref_hole_ax = 1,
                 pos = V0):
    """
    similar to NutHole, but creates a shape, in any direction
    add a Nut hole (hexagonal) with a prism attached to introduce the nut
    tolerances are included
    nut_r : circumradius of the hexagon
    nut_h : height of the nut, usually larger than the actual nut height, to be
           able to introduce it
    hole_h: the hole height, from the center of the hexagon to the side it will
           see light
    xtr_nut:  1 if you want 1 mm out of the hole, to cut
    xtr_hole:  1 if you want 1 mm out of the hole, to cut
    fc_axis_nut: axis of the shank of the nut
    fc_axis_hole: axis of the shank of the nut
    ref_nut_ax: if it is referenced to the center, symmetrical point on the
                on the fc_axis_nut
    ref_hole_ax: if it is referenced at the center of the shank, or at the 
                 end of the hole, not counting extra
 
         fc_axis_hole               fc_axis_hole
            :                        :   
           _:_                      _:_ ..
          |   |                    |   |  :
          |   |                    |   |  + hole_h
          |___|----fc_axis_nut     |   |--:
          |   |                     \ /   + nut_r
          |___|                      V....:
          :   :
          :...:
           + nut_h

      ref_nut:

         fc_axis_hole               fc_axis_hole
            :                        :   
           _:_                      _:_
          |   |                    |   |
          |   |                    |   |
          2_1_|----fc_axis_nut     |   |
          |   |                     \ /
          |___|                      V

      ref_hole:

         fc_axis_hole               fc_axis_hole
            :                        :   
           _2_                      _2_
          |   |                    |   |
          |   |                    |   |
          |_1_|----fc_axis_nut     | 1 |
          |   |                     \ /
          |___|                      V


         fc_axis_hole
            :
           _:_ ...
          |.2.|...xtr_hole (but pos is not referenced on the xtr)
          |   |
          |   |
          |_1_|----fc_axis_nut             
          |   |                 ___  but pos is still referenced on the axis of
          |___|.....           |   |    the shank
                    xtr_nut....|___|

    """
    doc = FreeCAD.ActiveDocument
    # normalize axis:
    axis_nut = DraftVecUtils.scaleTo(fc_axis_nut,1)
    axis_hole = DraftVecUtils.scaleTo(fc_axis_hole,1)
    nut_2ap = 2 * nut_r * COS30    #Apotheme = R * cos (30)

    # --- Reference to point *: hole=1 , nut=2
    #    fc_axis_hole               fc_axis_hole
    #       :                        :   
    #      _2_                      _2_
    #     |   |                    |   |
    #     |   |                    |   |
    #     *___|----fc_axis_nut     | * |
    #     |   |                     \ /
    #     |___|                      V

    fc_1_2_nut  = DraftVecUtils.scale(axis_nut, -nut_h/2.) 
    fc_2_1_hole = DraftVecUtils.scale(axis_hole, -hole_h) 
    # ref to point nut=2 (*)
    #      _:_                      _:_
    #     |   |                    |   |
    #     |   |                    |   |
    #     *_1_|----fc_axis_nut     | * |
    #     |   |                    :\ /:
    #     |___|                    : V :
    #     :   :                    :   :
    #     :...:                    :...:
    #      + nut_h                  + nut_2ap

    if ref_nut_ax == 1:
        refto_2_nut = fc_1_2_nut
    else: 
        refto_2_nut = V0

    # ref to point axis_hole=1 (*)
    #     2___                      _2_...
    #     |   |                    |   |  + hole_h
    #     |   |                    |   |  :
    #     1___|----fc_axis_nut     | 1 |--
    #     |   |                     \ /
    #     |___|                      V
    #     :   :
    #     :...:
    #      + nut_h

    if ref_hole_ax == 1:
        refto_1_hole = V0
    else: 
        refto_1_hole = fc_2_1_hole

    # absolute position of point *: axis_nut = 2 , axis_hole = 1
    nut2_hole1_pos = pos + refto_2_nut + refto_1_hole

    # position of the nut, including the extra
    nut_pos = nut2_hole1_pos + DraftVecUtils.scale(axis_hole, -xtr_nut)

    shp_nut = shp_regprism_dirxtr ( 
                                         n_sides = 6,
                                         radius  = nut_r,
                                         length  = nut_h,
                                         fc_normal = axis_nut,
                                         fc_verx1  = axis_hole,
                                         centered  = 0,
                                         # no extra, tolerances included
                                         xtr_top   = 0,
                                         xtr_bot   = 0,
                                         pos       = nut_pos)

    # position is in nut2_hole1_pos, and then xtr are considered in both
    # directions
    shp_hole = shp_box_dir_xtr(box_w = nut_2ap,
                                     box_d = nut_h,
                                     box_h = hole_h,
                                     fc_axis_h = axis_hole,
                                     fc_axis_d = axis_nut,
                                     cw=1, cd=0, ch=0,
                                     xtr_h = xtr_hole,
                                     xtr_nh = xtr_nut,
                                     pos= nut2_hole1_pos)

    shp_nuthole = shp_nut.fuse(shp_hole)
    shp_nuthole = shp_nuthole.removeSplitter()
    doc.recompute() 
    return shp_nuthole

#doc = FreeCAD.newDocument()
#shpNuthole = shp_nuthole (nut_r = 5, nut_h = 4, hole_h = 10,
#             xtr_nut = 1, xtr_hole = 1,
#             fc_axis_nut = VY,
#             fc_axis_hole = VX,
#             ref_nut_ax = 1,
#             ref_hole_ax = 1,
#             pos = FreeCAD.Vector(1,1,2))
#Part.show(shpNuthole)


#  ---------------- Fillet on edges of a certain length
#   box:   is the original shape we want to fillet
#   e_len: the length of the edges that we want to fillet
#   radius: the radius of the fillet
#   name: the name of the shape we want to create

def fillet_len (box, e_len, radius, name):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    fllts_v = []
    edge_ind = 1
    #logger.debug('fillet_len: box %s - %s' %
    #                     ( str(box), str(box.Shape)))
    for edge_i in box.Shape.Edges:
        #logging.debug('fillet_len: edge Length: %s' % str(edge_i.Length))
        if edge_i.Length == e_len: # same length
        # the index is appeneded (edge_ind),not the edge itself (edge_i)
        # radius is twice, because it can be variable
            #logging.debug('fillet_len: append edge. Length: %s ' ,
            #               str(edge_i.Length))
            fllts_v.append((edge_ind, radius, radius))
        edge_ind += 1
    box_fllt = doc.addObject ("Part::Fillet", name)
    box_fllt.Base = box
    box_fllt.Edges = fllts_v
    # to hide the objects in freecad gui
    if box.ViewObject != None:
      box.ViewObject.Visibility=False
    return box_fllt

# Calculate Bolt separation
# We want to know how much separation is needed for a bolt
# The bolt (din912) head diameter is usually smaller than the nut (din934)
# The nut max value is give by its 2*apotheme (S) (wrench size)
#     so its max diameter is 2A x cos(30)
#
#     din912  din938
#       D     S(max)   D(max)
# M3:  5.5      5.5     6,35
# M4:  7.0      7.0     8,08
# M5:  8.5      8.0     9,24
# M6: 10.0     10.0    11,55
#
# So it will the nut what gives the separation
#
#         _____    :    _______ 
#        |     |_  :  _|    
#        |       | : |    
#        |       | : |  
#        |      _| : |_ 
#        |_____|   :   |______
#        :     :   :        
#        :..,..:.,.:        
#        : sep  rad:
#        :         :
#        :....,....:
#          bolt_sep 
#
# Arguments:
# bolt_d: diameter of the bolt: 3, 4, ... for M3, M4,... 
# hasnut: 1: if there is a nut
#         0: if there is not a nut, so just the bolt head (smaller)
# sep: separation from the outside of the nut to the end, if empty,
#      default value 2mm

def get_bolt_end_sep (bolt_d, hasnut, sep=2.):
    """
    Calculate Bolt separation

    Calculates know how much separation is needed for a bolt
    The bolt (din912) head diameter is usually smaller than the nut (din934)
    The nut max value is given by its 2*apotheme (S) (wrench size)
    so its max diameter is 2A x cos(30)

    Example of nut and bolt head sizes:

        din912  din938
          D     S(max)   D(max)
    M3:  5.5      5.5     6,35
    M4:  7.0      7.0     8,08
    M5:  8.5      8.0     9,24
    M6: 10.0     10.0    11,55

   Therefore, if there is a nut, the nut will be used to calculate the
   separation

          _____    :    _______ 
         |     |_  :  _|    
         |       | : |    
         |       | : |  
         |      _| : |_ 
         |_____|   :   |______
         :     :   :        
         :..,..:.,.:        
         : sep  rad:
         :         :
         :....,....:
           bolt_sep 
 
    Args:
        bolt_d: diameter of the bolt: 3, 4, ... for M3, M4,... 
        hasnut: 1: if there is a nut
                0: if there is not a nut, so just the bolt head (smaller)
        sep: separation from the outside of the nut to the end, if empty,
             default value 2mm

    Returns:
        (float): Minimum separation between the center of the bolt and the end

    """

    if hasnut == 1:
        diam = kcomp.NUT_D934_2A[bolt_d] / COS30 
    else: # no nut, calculate with bolt head
        diam = kcomp.D912_HEAD_D[bolt_d]

    rad  = diam/2.

    bolt_sep = rad + sep

    return bolt_sep

# ------------------- get_bolt_bearing_sep -------------------------
# same as get_bolt_end_sep, but when there is a bearing. 
# If there is a bearing, there will be more space because the nut is at
# the bottom or top, and the widest side is on the middle
#
#                            lbearing_r
#                    rad    ..+...
#                   ..+..  :      :
#         ______    :   :__:______:_
#        |      |_  :  _|      .* : 
#        |        | : |     .*    : this is the bearing section (circunference)
#        |        | : |    (      :
#        |       _| : |_   : *.   :
#        |______|   :   |__:____*_:
#                   :   :  :      :
#                   :   :.bsep    :
#                   :             :
#                   :.bolt_b_sep..:

#
# Arguments:
# bolt_d: diameter of the bolt: 3, 4, ... for M3, M4,... 
# hasnut: 1: if there is a nut
#         0: if there is not a nut, so just the bolt head (smaller)
# lbearing_r: radius of the linear bearing
# bsep: separation from the outside of the nut to the end of bearing
#       default value 0mm

def get_bolt_bearing_sep (bolt_d, hasnut, lbearing_r, bsep=0):

    if hasnut == 1:
        diam = kcomp.NUT_D934_2A[bolt_d] / COS30 
    else: # no nut, calculate with bolt head
        diam = kcomp.D912_HEAD_D[bolt_d]

    rad  = diam/2.

    bolt_b_sep = rad + bsep + lbearing_r

    return bolt_b_sep



#  ---------------- edgeonaxis
# It tells if an edge is on an axis
# Arguments:
# edge: an FreeCAD edge, with its vertexes
# axis: a text, being 'x', '-x', 'y', '-y', 'z', '-z'

def edgeonaxis (edge, axis):

    vex0 = edge.Vertexes[0]
    vex1 = edge.Vertexes[1]
    #logger.debug( "vex0.X: %s", vex0.X)
    #logger.debug( "vex1.X: %s", vex1.X)
    #logger.debug( "vex0.Y: %s", vex0.Y)
    #logger.debug( "vex1.Y: %s", vex1.Y)
    #logger.debug( "vex0.Z: %s", vex0.Z)
    #logger.debug( "vex1.Z: %s", vex1.Z)
    #logger.debug( "axis: %s",  axis)

    #v0x = vex0.X
    #v1x = vex1.X
    #v0y = vex0.Y
    #v1y = vex1.Y
    #v0z = vex0.Z
    #v1z = vex1.Z

    if (equ(vex0.X, vex1.X) and 
        equ(vex0.Y, vex1.Y) and
        equ(vex0.Z, vex1.Z)):
        logger.debug('edgeonaxis:  error, same point')
        return False
    elif equ(vex0.X, vex1.X) and equ(vex0.Y, vex1.Y):
        if axis == 'z' or axis == '-z':
            return True
        else:
            return False
    elif equ(vex0.X, vex1.X) and equ(vex0.Z, vex1.Z):
        if axis == 'y' or axis == '-y':
            return True
        else:
            return False
    elif equ(vex0.Y, vex1.Y) and equ(vex0.Z, vex1.Z):
        if axis == 'x' or axis == '-x':
            return True
        else:
            return False
    else:
        return False

def shp_filletchamfer_dir (shp, fc_axis = VZ,  fillet = 1, radius=1):
    """
        Fillet or chamfer edges on a certain axis
        For a shape
    Arguments:
        shp:   is the original shape we want to fillet or chamfer
        fillet: 1 if we are doing a fillet, 0 if it is a chamfer
        radius: the radius of the fillet or chamfer
        fc_axis  : FreeCAD.Vector the axis where the fillet will be

    """

    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    doc.recompute()  # you may hav problems if you dont do it
    edgelist = []
    # normalize the axis:
    nnorm = DraftVecUtils.scaleTo(fc_axis,1)
    # get the negative of the normalized vector
    nnorm_neg = nnorm.negative()
    for edge in shp.Edges:
        #logger.debug('filletchamfer: edge Length: %s', edge.Length)
        # get the FreeCAD.Vector with the point
        p0 = edge.Vertexes[0].Point
        p1 = edge.Vertexes[1].Point
        v_vertex = p1.sub(p0)  #substraction
        # I could calculate the angle, but I think it will take more
        # time than normalizing and checking if they are the same
        v_vertex.normalize()
        # check if they are the same vector (they are parallel):
        if ( DraftVecUtils.equals(v_vertex, nnorm) or
             DraftVecUtils.equals(v_vertex, nnorm_neg)):
            edgelist.append(edge)
            #logger.debug('append edge Length: %s', edge.Length)

    if len(edgelist) != 0:
        if fillet == 1:
            #logger.debug('%s', str(edgelist))
            shp_fillcham = shp.makeFillet(radius, edgelist)
        else:
            shp_fillcham = shp.makeChamfer(radius, edgelist)
        doc.recompute()
        return shp_fillcham
    else:
        logger.debug('No edge to fillet or chamfer')
        return



def shp_filletchamfer_dirs (shp, fc_axis_l, fillet = 1, radius=1):
    """
        Same as shp_filletchamfer_dir, but with a list of directions
    Arguments:
        shp:   is the original shape we want to fillet or chamfer
        fc_axis_l  : a list of FreeCAD.Vector. Each vector indicates the axis
                     where the fillet/chamfer will be
        fillet: 1 if we are doing a fillet, 0 if it is a chamfer
        radius: the radius of the fillet or chamfer

    """

    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    doc.recompute()  # you may hav problems if you dont do it
    edgelist = []
    n_axis_list = []
    for axis in fc_axis_l:
        # normalize the axis:
        nnorm = DraftVecUtils.scaleTo(axis,1)
        n_axis_list.append(nnorm)
        # get the negative of the normalized vector
        nnorm_neg = nnorm.negative()
        n_axis_list.append(nnorm_neg)
    #logger.debug('filletchamfer: elen: %s',  e_len)
    for edge in shp.Edges:
        #logger.debug('filletchamfer: edge Length: %s ind %s',
        #             edge.Length, edge_ind)
        # get the FreeCAD.Vector with the point
        if len(edge.Vertexes) == 2:
            p0 = edge.Vertexes[0].Point
            p1 = edge.Vertexes[1].Point
            v_vertex = p1.sub(p0)  #substraction
            # I could calculate the angle, but I think it will take more
            # time than normalizing and checking if they are the same
            v_vertex.normalize()
            # check if they are the same vector (they are parallel):
            for naxis in n_axis_list:
                if ( DraftVecUtils.equals(v_vertex, naxis)):
                    edgelist.append(edge)
                    break # breaks inside this for, but not the outer

    if len(edgelist) != 0:
        if fillet == 1:
            #logger.debug('%', str(edgelist))
            shp_fillcham = shp.makeFillet(radius, edgelist)
        else:
            shp_fillcham = shp.makeChamfer(radius, edgelist)
        doc.recompute()
        return shp_fillcham
    else:
        logger.debug('No edge to fillet or chamfer')
        return




def shp_filletchamfer_dirpt (shp, fc_axis = VZ, fc_pt = V0,  fillet = 1,
                             radius=1):
    """
        Fillet or chamfer edges on a certain axis and a point contained
        in that axis
        For a shape
    Arguments:
        shp:   is the original shape we want to fillet or chamfer
        fc_axis  : FreeCAD.Vector the axis where the fillet will be
        fc_pt  : FreeCAD.Vector of the point
        fillet: 1 if we are doing a fillet, 0 if it is a chamfer
        radius: the radius of the fillet or chamfer

    """

    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    doc.recompute()  # you may hav problems if you dont do it
    edgelist = []
    # normalize the axis:
    nnorm = DraftVecUtils.scaleTo(fc_axis,1)
    # get the negative of the normalized vector
    nnorm_neg = nnorm.negative()
    #logger.debug('filletchamfer: elen: %s',  e_len)
    for edge in shp.Edges:
        #logger.debug('filletchamfer: edge Length: %s ind %s',
        #             edge.Length, edge_ind)
        # get the FreeCAD.Vector with the point
        if len(edge.Vertexes) == 2:
            p0 = edge.Vertexes[0].Point
            p1 = edge.Vertexes[1].Point
            v_vertex = p1.sub(p0)  #substraction
            # I could calculate the angle, but I think it will take more
            # time than normalizing and checking if they are the same
            v_vertex.normalize()
            # check if they are the same vector (they are parallel):
            if ( DraftVecUtils.equals(v_vertex, nnorm) or
                 DraftVecUtils.equals(v_vertex, nnorm_neg)):
                # Now check if this vertex goes through the point
                # get the vector from a vertex to the point
                if DraftVecUtils.equals(p1, fc_pt): # same point
                    edgelist.append(edge)
                    break # vertex found
                else:
                    v_vertex_pt = p1.sub(fc_pt)
                    v_vertex_pt.normalize()
                    if ( DraftVecUtils.equals(v_vertex_pt, nnorm) or
                         DraftVecUtils.equals(v_vertex_pt, nnorm_neg)):
                        edgelist.append(edge)
                        break #only one

    if len(edgelist) != 0:
        if fillet == 1:
            #logger.debug('%', str(edgelist))
            shp_fillcham = shp.makeFillet(radius, edgelist)
        else:
            shp_fillcham = shp.makeChamfer(radius, edgelist)
        doc.recompute()
        return shp_fillcham
    else:
        logger.debug('No edge to fillet or chamfer')
        return


def shp_filletchamfer_dirpts (shp, fc_axis, fc_pts,  fillet = 1,
                             radius=1):
    """
        Fillet or chamfer edges on a certain axis and a list of point contained
        in that axis
        For a shape
    Arguments:
        shp:   is the original shape we want to fillet or chamfer
        fc_axis  : FreeCAD.Vector the axis where the fillet will be
        fc_pts  : FreeCAD.Vector list of the points
        fillet: 1 if we are doing a fillet, 0 if it is a chamfer
        radius: the radius of the fillet or chamfer

    """

    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    doc.recompute()  # you may hav problems if you dont do it
    edgelist = []
    # normalize the axis:
    nnorm = DraftVecUtils.scaleTo(fc_axis,1)
    # get the negative of the normalized vector
    nnorm_neg = nnorm.negative()
    #logger.debug('filletchamfer: elen: %s',  e_len)
    for edge in shp.Edges:
        #logger.debug('filletchamfer: edge Length: %s ind %s',
        #             edge.Length, edge_ind)
        # get the FreeCAD.Vector with the point
        if len(edge.Vertexes) == 2:
            p0 = edge.Vertexes[0].Point
            p1 = edge.Vertexes[1].Point
            v_vertex = p1.sub(p0)  #substraction
            # I could calculate the angle, but I think it will take more
            # time than normalizing and checking if they are the same
            v_vertex.normalize()
            # check if they are the same vector (they are parallel):
            if ( DraftVecUtils.equals(v_vertex, nnorm) or
                 DraftVecUtils.equals(v_vertex, nnorm_neg)):
                # Now check if this vertex goes through the point
                # get the vector from a vertex to the point
                for pti in fc_pts:
                    if DraftVecUtils.equals(p1, pti):
                        # same point
                        edgelist.append(edge)
                        break # vertex found
                    else:
                        v_vertex_pt = p1.sub(pti)
                        v_vertex_pt.normalize()
                        if ( DraftVecUtils.equals(v_vertex_pt, nnorm) or
                             DraftVecUtils.equals(v_vertex_pt, nnorm_neg)):
                            edgelist.append(edge)
                            break # vertex found

    if len(edgelist) != 0:
        if fillet == 1:
            #logger.debug('%', str(edgelist))
            shp_fillcham = shp.makeFillet(radius, edgelist)
        else:
            shp_fillcham = shp.makeChamfer(radius, edgelist)
        doc.recompute()
        return shp_fillcham
    else:
        logger.debug('No edge to fillet or chamfer')
        return shp



def shp_cir_fillchmf (shp, circen_pos = V0,  fillet = 1, radius=1):
    """
        Fillet or chamfer edges that is a circle, the shape has to be a 
        cylinder
    Arguments:
        shp:   is the original cylinder shape we want to fillet or chamfer
        circen_pos  : FreeCAD.Vector of the center of the circle
        fillet: 1 if we are doing a fillet, 0 if it is a chamfer
        radius: the radius of the fillet or chamfer

    """

    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    doc.recompute()  # you may hav problems if you dont do it
    edgelist = []
    for edge in shp.Edges:
        # get the edges, if it is a cylinder, 2 edges will have just one
        # point and one will have to (the height)
        # check if they are closed:
        if edge.Closed == True:
            # only one point
            # Get the center of Mass, which will be the center
            cen = edge.CenterOfMass
            # check if they are the same vector
            if ( DraftVecUtils.equals(circen_pos, cen)):
                edgelist.append(edge)
                break

    if len(edgelist) != 0:
        if fillet == 1:
            shp_fillcham = shp.makeFillet(radius, edgelist)
        else:
            shp_fillcham = shp.makeChamfer(radius, edgelist)
        doc.recompute()
        return shp_fillcham
    else:
        logger.debug('No edge to fillet or chamfer')
        return


def shp_cylfilletchamfer (shp, fillet = 1, radius=1):
    """
        Fillet or chamfer all edges of a cylinder
    Arguments:
        shp:   is the original cylinder shape we want to fillet or chamfer
        fillet: 1 if we are doing a fillet, 0 if it is a chamfer
        radius: the radius of the fillet or chamfer

    """

    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    doc.recompute()  # you may hav problems if you dont do it
    edgelist = []
    for edge in shp.Edges:
        # get the edges, if it is a cylinder, 2 edges will have just one
        # point and one will have to (the height)
        # check if they are closed:
        if edge.Closed == True:
            # only one point
            edgelist.append(edge)

    if len(edgelist) != 0:
        if fillet == 1:
            shp_fillcham = shp.makeFillet(radius, edgelist)
        else:
            shp_fillcham = shp.makeChamfer(radius, edgelist)
        doc.recompute()
        return shp_fillcham
    else:
        logger.debug('No edge to fillet or chamfer')
        return




#  --- Fillet or chamfer edges of a certain length, on a certain axis
#  --- and a certain coordinate
#  For a shape
#   shp:   is the original shape we want to fillet or chamfer
#   fillet: 1 if we are doing a fillet, 0 if it is a chamfer
#   e_len: the length of the edges that we want to fillet or chamfer
#          if e_len == 0, chamfer/fillet any length
#   radius: the radius of the fillet or chamfer
#   axis  : the axis where the fillet will be
#   xpos_chk,ypos_chk,zpos_chk  :  if the position will be checked
#   if axis = 'x', x_pos_check will not make sense
#   xpos,ypos,zpos  : the position

def shp_filletchamfer (shp, e_len, fillet = 1, radius=1, axis='x', 
                   xpos_chk = 0, ypos_chk = 0, zpos_chk=0,
                   xpos = 0, ypos = 0, zpos = 0
                    ):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    doc.recompute()  # you may hav problems if you dont do it
    edgelist = []
    #logger.debug('filletchamfer: elen: %s',  e_len)
    for edge_ind, edge in enumerate(shp.Edges):
        #logger.debug('filletchamfer: edge Length: %s ind %s',
        #             edge.Length, edge_ind)
        # using equ because float number can be not exactly the same
        if (e_len == 0 or equ(edge.Length, e_len)): # same length
            if edgeonaxis (edge, axis) == True:
                #logger.debug('edgeonaxis: Length: %s' % str(edge.Length))
                v0 = edge.Vertexes[0]
                v1 = edge.Vertexes[1]
                if axis == 'x' or axis == '-x':
                    if ypos_chk == True and zpos_chk == True:
                        # its on the axis, so just checking one edge
                        if equ(v0.Y, ypos) and equ(v0.Z, zpos):
                            edgelist.append(edge)
                    elif ypos_chk == True:
                        if equ(v0.Y, ypos):
                            edgelist.append(edge)
                    elif zpos_chk == True:
                        if equ(v0.Z, zpos):
                            edgelist.append(edge)
                    else: # all the edges on axis x with e_len are appended
                        edgelist.append(edge)
                elif axis == 'y' or axis == '-y':
                    if xpos_chk == True and zpos_chk == True:
                        if equ(v0.X, xpos) and equ(v0.Z, zpos):
                            edgelist.append(edge)
                    elif xpos_chk == True:
                        if equ(v0.X, xpos):
                            edgelist.append(edge)
                    elif zpos_chk == True:
                        if equ(v0.Z, zpos):
                            edgelist.append(edge)
                    else:
                        edgelist.append(edge)
                elif axis == 'z' or axis == '-z':
                    if xpos_chk == True and ypos_chk == True:
                        if equ(v0.X, ypos) and equ(v0.Y, ypos):
                            edgelist.append(edge)
                    elif xpos_chk == True:
                        if equ(v0.X, xpos):
                            edgelist.append(edge)
                    elif ypos_chk == True:
                        if equ(v0.Y, ypos):
                            edgelist.append(edge)
                    else:
                        edgelist.append(edge)

    if len(edgelist) != 0:
        if fillet == 1:
            logger.debug('%', str(edgelist))
            shp_fillcham = shp.makeFillet(radius, edgelist)
        else:
            shp_fillcham = shp.makeChamfer(radius, edgelist)
        doc.recompute()
        return shp_fillcham
    else:
        logger.debug('No edge to fillet or chamfer')
        return




#  --- Fillet or chamfer edges of a certain length, on a certain axis
#  --- and a certain coordinate
#   fco:   is the original FreeCAD object we want to fillet or chamfer
#   fillet: 1 if we are doing a fillet, 0 if it is a chamfer
#   e_len: the length of the edges that we want to fillet or chamfer
#          if e_len == 0, chamfer/fillet any length
#   radius: the radius of the fillet or chamfer
#   axis  : the axis where the fillet will be
#   xpos_chk,ypos_chk,zpos_chk  :  if the position will be checked
#   if axis = 'x', x_pos_check will not make sense
#   xpos,ypos,zpos  : the position
#   name: the name of the fco we want to create

def filletchamfer (fco, e_len, name, fillet = 1, radius=1, axis='x', 
                   xpos_chk = 0, ypos_chk = 0, zpos_chk=0,
                   xpos = 0, ypos = 0, zpos = 0,
                    ):
    # we have to bring the active document
    doc = FreeCAD.ActiveDocument
    doc.recompute()  # you may hav problems if you dont do it
    edgelist = []
    #logger.debug('filletchamfer: elen: %s',  e_len)
    for edge_ind, edge in enumerate(fco.Shape.Edges):
        #logger.debug('filletchamfer: edge Length: %s ind %s',
        #             edge.Length, edge_ind)
        # using equ because float number can be not exactly the same
        if (e_len == 0 or equ(edge.Length, e_len)): # same length
            if edgeonaxis (edge, axis) == True:
                #logger.debug('edgeonaxis: Length: %s' % str(edge.Length))
                v0 = edge.Vertexes[0]
                v1 = edge.Vertexes[1]
                if axis == 'x' or axis == '-x':
                    if ypos_chk == True and zpos_chk == True:
                        # its on the axis, so just checking one edge
                        if equ(v0.Y, ypos) and equ(v0.Z, zpos):
                            edgelist.append((edge_ind+1,radius,radius))
                    elif ypos_chk == True:
                        if equ(v0.Y, ypos):
                            edgelist.append((edge_ind +1,radius,radius))
                    elif zpos_chk == True:
                        if equ(v0.Z, zpos):
                            edgelist.append((edge_ind+1,radius,radius))
                    else: # all the edges on axis x with e_len are appended
                        edgelist.append((edge_ind+1,radius,radius))
                elif axis == 'y' or axis == '-y':
                    if xpos_chk == True and zpos_chk == True:
                        if equ(v0.X, xpos) and equ(v0.Z, zpos):
                            edgelist.append((edge_ind+1,radius,radius))
                    elif xpos_chk == True:
                        if equ(v0.X, xpos):
                            edgelist.append((edge_ind+1,radius,radius))
                    elif zpos_chk == True:
                        if equ(v0.Z, zpos):
                            edgelist.append((edge_ind+1,radius,radius))
                    else:
                        edgelist.append((edge_ind+1,radius,radius))
                elif axis == 'z' or axis == '-z':
                    if xpos_chk == True and ypos_chk == True:
                        if equ(v0.X, ypos) and equ(v0.Y, ypos):
                            edgelist.append((edge_ind+1,radius,radius))
                    elif xpos_chk == True:
                        if equ(v0.X, xpos):
                            edgelist.append((edge_ind+1,radius,radius))
                    elif ypos_chk == True:
                        if equ(v0.Y, ypos):
                            edgelist.append((edge_ind+1,radius,radius))
                    else:
                        edgelist.append((edge_ind+1,radius,radius))

    if len(edgelist) != 0:
        if fillet == 1:
            fco_fillcham = doc.addObject ("Part::Fillet", name)
        else:
            fco_fillcham = doc.addObject ("Part::Chamfer", name)
        fco_fillcham.Base = fco
        fco_fillcham.Edges = edgelist
        if fco.ViewObject != None:
            fco.ViewObject.Visibility=False
        doc.recompute()
        return fco_fillcham
    else:
        logger.debug('No edge to fillet or chamfer')
        return





#  ---------------- calc_rot -----------------------------
#  ---------------- Yaw, Pitch and Roll transfor
#  Having an object with an orientation defined by 2 vectors
#  the vectors a tuples, nor FreeCAD.Vectors
#  use the wrapper fc_calc_rot to have FreeCAD.Vector arguments
#  First vector original direction (x,y,z) is (1,0,0) 
#  Second vector original direction (x,y,z) is (0,0,-1) 
#  we want to rotate the object in an ortoghonal direction. The vectors
#  will be in -90, 180, or 90 degrees.
#  this function returns the Rotation given by yaw, pitch and roll
#  In case vec1 is (0,0,0), means that it doesn't matter that vector.
#  Yaw is the rotation of Z axis. Positive Yaw is like screwing up
#
#   Y         Y                   Y
#   |_X       :   yaw=0           :     yaw=60
#   /         :                   :   /
#  Z          :                   :  /
#             :                   : /
#             :________....  X    :/............ X
#
#
#  Z  Y       Z                   Z
#  |/_ X      :   pitch=0         :     pitch=-60
#             :                   :   /
#             :                   :  /
#             :                   : /
#             :________....  X    :/............ X
#
#
#             Z                   Z
#   Z         :   roll=0          :     roll=-60
#   |_Y       :                   :   /
#  /          :                   :  /
# X           :                   : /
#             :________....  Y    :/............ Y
#

#

def calc_rot (vec1, vec2):
           
    # rotation calculation
    if vec1 == (1,0,0):
        yaw = 0
        pitch = 0
        if vec2 == (0,1,0):
            roll  = 90
        elif vec2 == (0,-1,0):
            roll  = -90
        elif vec2 == (0,0,1):
            roll  = 180
        elif vec2 == (0,0,-1):
            roll  = 0
        else:
            print "error 1 in yaw-pitch-roll"
    elif vec1 == (-1,0,0):
        yaw = 180
        pitch = 0
        if vec2 == (0,1,0):
            roll  = -90 #negative because of the yaw
        elif vec2 == (0,-1,0):
            roll  = 90 # positive because of the yaw = 180
        elif vec2 == (0,0,1):
            roll = 180
        elif vec2 == (0,0,-1):
            roll  = 0
        else:
            print "error 2 in yaw-pitch-roll"
    elif vec1 == (0,1,0):
        yaw = 90
        pitch = 0
        if vec2 == (1,0,0):
            roll  = -90
        elif vec2 == (-1,0,0):
            roll  = 90
        elif vec2 == (0,0,1):
            roll  = 180
        elif vec2 == (0,0,-1):
            roll  = 0
        else:
            print "error 3 in yaw-pitch-roll"
    elif vec1 == (0,-1,0):
        yaw = -90
        pitch = 0
        if vec2 == (1,0,0):
            roll  = 90 
        elif vec2 == (-1,0,0):
            roll  = -90 
        elif vec2 == (0,0,1):
            roll  = 180
        elif vec2 == (0,0,-1):
            roll  = 0
        else:
            print "error 4 in yaw-pitch-roll"
    elif vec1 == (0,0,1):
        pitch = -90
        yaw = 0
        if vec2 == (1,0,0):
            roll  = 0 
        elif vec2 == (-1,0,0):
            roll  = 180 
        elif vec2 == (0,1,0):
            roll  = 90
        elif vec2 == (0,-1,0):
            roll  = -90
        else:
            print "error 5 in yaw-pitch-roll"
    elif vec1 == (0,0,-1):
        pitch = 90
        yaw = 0
        if vec2 == (1,0,0):
            roll  = 180 
        elif vec2 == (-1,0,0):
            roll  = 0 
        elif vec2 == (0,1,0):
            roll  = 90
        elif vec2 == (0,-1,0):
            roll  = -90
        else:
            print "error 6 in yaw-pitch-roll"
    elif vec1 == (0,0,0): # it doesn't matter the direction of vec1
        yaw = 0
        if vec2 == (1,0,0):
            pitch = -90
            roll  = 0 
        elif vec2 == (-1,0,0):
            pitch = 90
            roll  = 0 
        elif vec2 == (0,1,0):
            pitch = 0
            roll  = 90
        elif vec2 == (0,-1,0):
            pitch = 0
            roll  = -90
        elif vec2 == (0,0,1):
            pitch = 0
            roll  = 180
        elif vec2 == (0,0,-1):
            pitch = 0
            roll  = 0 # the same position
        else:
            print "error 7 in yaw-pitch-roll"



    vrot = FreeCAD.Rotation(yaw,pitch,roll)
    return vrot


def get_fcvectup (tup):
    """ Gets the FreeCAD.Vector of a tuple

    Args:
        tup: tuple of 3 elements

    Return: the FreeCAD.Vector
    """

    fcvec = FreeCAD.Vector(tup[0], tup[1], tup[2])
    return (fcvec)


#  ---------------- fc_calc_rot -----------------------------
# same as calc_rot but using FreeCAD.Vectors arguments

def fc_calc_rot (fc_vec1, fc_vec2):

    ##vec1 = (fc_vec1.X, fc_vec1.Y, fc_vec1.Z)
    ##vec2 = (fc_vec2.X, fc_vec2.Y, fc_vec2.Z)
    vrot = calc_rot(DraftVecUtils.tup(fc_vec1),DraftVecUtils.tup(fc_vec2))
    return vrot

def calc_rot_z (v_refz, v_refx):
    """
    calculates de rotation like calc_rot. However uses a different
    origin axis. calc_rot uses:
    vec1 original direction (x,y,z) is (0,0,1) 
    vec2 original direction (x,y,z) is (1,0,0) 
    So it makes a change of axis before calling calc_rot

    Args:
        v_refz: tuple or FreeCAD.Vector indicating the rotation from (0,0,1)
                to v_refz
        v_refx: tuple or FreeCAD.Vector indicating the rotation from (1,0,0)
                to v_refx
        these argument vectors a tuples, not FreeCAD.Vectors

    Returns:
        FreeCAD.Rotation value

    """

    if type(v_refz) is tuple:
        v_refz = get_fcvectup(v_refz)
        v_refx = get_fcvectup(v_refx)

    # since arg2 of calc_rot is referenced to VNZ, v_refz is negated
    # so v_refnz becomes referenced to VZ
    v_refnz = DraftVecUtils.neg(v_refz)
    vrot = fc_calc_rot(v_refx, v_refnz)
    return vrot
    

def get_rot (v1, v2):
    """ Calculate the rotation from v1 to v2
    the difference with previous verions, such fc_calc_rot, calc_rot, calc_rot
    is that it is for any vector direction.
    The difference with DraftVecUtils.getRotation is that getRotation doesnt
    work for vectors with 180 degrees.

    MAYBE IT IS NOT NECESSARY, just use FreeCAD.Rotation
    rotation.Axis, math.degrees(rotation.Angle)

    Parameters:
    -----------
    v1 : FreeCAD.Vector
    v2 : FreeCAD.Vector

    returns a tuple representing a quaternion rotation between v2 and v1
    """

    #normalize vectors
    nv1 = DraftVecUtils.scaleTo(v1,1.)
    nv2 = DraftVecUtils.scaleTo(v2,1.)

    if DraftVecUtils.equals(nv1,nv2.negative()):
        # we have to flip, but DraftVecUtils.getRotation doesnt get it done
        # for this case
        return FreeCAD.Rotation(VX,180)
    else:
        return DraftVecUtils.getRotation(nv1,nv2)


#  ---------------- calc_desp_ncen ------------------------
#  similar to calc_rot, but calculates de displacement, when we don't want
#  to have all of the dimensions centered
#  First vector original direction (x,y,z) is (1,0,0)
#  Second vector original direction (x,y,z) is (0,0,-1)
#  The arguments vec1, vec2 are tuples (x,y,z) but they may be also
#   FreeCAD.Vectors
#  vec1, vec2 have to be on the axis: x, -x, y, -y, z, -z
#  vec1 can be (0,0,0): it means that it doesn't matter how it is rotated
#  Length: original dimension on X
#  Width:  original dimension on Y
#  Height: original dimension on Z
# 
#  the picture is wrong, because originally it is centered, that's
#  why the position is moved only half of the dimension. But the concept
#  is valid 
#  
#      Z          . Y       length (x) = 1
#      :   _    .           width  (y) = 2
#      : /  /|              heigth (z) = 3
#      :/_ / |
#      |  |  |              vec1 original (before rotation) = VX
#      |  | /               vec2 original (before rotation) = -VZ
#      |__|/..............X
#
#
#    Example after rotation and change position
#
#      Z         . Y       length (x) = 3
#      :   ____.           width  (y) = 2
#      : /    /|           heigth (z) = 1
#      :/___ //                  vec1 = VZ
#      |____|/..............X    vec2 = VX
#
#    So we have to move X its original heith (3), otherwise it would
#       be on the negative side, like this
#
#           Z 
#           :    . Y       length (x) = 3
#          _:__.           width  (y) = 2
#        /  : /|           heigth (z) = 1
#       /___://                  vec1 = VZ
#      |____|/..............X    vec2 = VX

def calc_desp_ncen (Length, Width, Height, 
                     vec1, vec2, cx=False, cy=False, cz=False, H_extr = False):
           
    # rotation calculation
    x = 0
    y = 0
    z = 0
    if abs(vec1[0]) == 1: # X axis: vec1 == (1,0,0) or vec1 == (-1,0,0):
        if abs(vec2[1]) == 1:   # Y
            if cx == False:
                x = Length / 2.0
            if cy == False:
                y = Height / 2.0
            if cz == False:
                z = Width / 2.0
        elif abs(vec2[2]) == 1:    # Z
            if cx == False:
                x = Length / 2.0
            if cy == False:
                y = Width / 2.0
            if cz == False:
                z = Height / 2.0
        else:
            print "error 1 in calc_desp_ncen"
    elif abs(vec1[1]) == 1: # Y axis
        if abs(vec2[0]) == 1:   # X
            if cx == False:
                x = Height / 2.0
            if cy == False:
                y = Length / 2.0
            if cz == False:
                z = Width / 2.0
        elif abs(vec2[2]) == 1:    # Z
            if cx == False:
                x = Width / 2.0
            if cy == False:
                y = Length / 2.0
            if cz == False:
                z = Height / 2.0
        else:
            print "error 2 in calc_desp_ncen"
    elif abs(vec1[2]) == 1: # Z axis
        if abs(vec2[0]) == 1:   # X
            if cx == False:
                x = Height / 2.0
            if cy == False:
                y = Width / 2.0
            if cz == False:
                z = Length / 2.0
        elif abs(vec2[1]) == 1:    # Y
            if cx == False:
                x = Width / 2.0
            if cy == False:
                y = Height / 2.0
            if cz == False:
                z = Length / 2.0
        else:
            print "error 3 in calc_desp_ncen"
    elif (vec1[0]==0 and vec1[1]==0 and vec1[2]==0): 
        #It doesnt matter vec1. Probably it is symetrical on plane XY.
        # So Length and Width are the same
        if Width != Length:
            logger.error('Check rotation vec1=(0,0,0), and Length!=Width')
        if abs(vec2[0]) == 1:   # X. Pitch = -90. in calc_rot
            if cx == False:
                x = Height / 2.0
            if cy == False:
                y = Width / 2.0
            if cz == False:
                z = Length / 2.0
        elif abs(vec2[1]) == 1:   # Y. Roll = +-90. in calc_rot
            if cx == False:
                x = Length / 2.0
            if cy == False:
                y = Height / 2.0
            if cz == False:
                z = Width / 2.0
        elif abs(vec2[2]) == 1:    # Z. Nothing. Roll 0 or 180
            if cx == False:
                x = Width / 2.0
            if cy == False:
                y = Length / 2.0
            if cz == False:
                z = Height / 2.0
        else:
            print "error 4 in calc_desp_ncen"
    else:
        print "error 5 in calc_desp_ncen"


    vdesp = FreeCAD.Vector(x,y,z)
    return vdesp



#  ---------------- fc_calc_desp_ncen -----------------------------
# same as calc_desp_ncen but using FreeCAD.Vectors arguments

def fc_calc_desp_ncen (Length, Width, Height,
                       fc_vec1, fc_vec2,
                       cx=False, cy=False, cz=False, H_extr = False ):

    vec1 = DraftVecUtils.tup(fc_vec1)
    vec2 = DraftVecUtils.tup(fc_vec2)
    vdesp = calc_desp_ncen(Length, Width, Height,
                           vec1, vec2, cx, cy, cz, H_extr)
    return vdesp



def getvecofname(axis):

    if axis == 'x':
        vec = (1,0,0)
    elif axis == '-x':
        vec = (-1,0,0)
    elif axis == 'y':
        vec = (0,1,0)
    elif axis == '-y':
        vec = (0,-1,0)
    elif axis == 'z':
        vec = (0,0,1)
    elif axis == '-z':
        vec = (0,0,-1)

    return vec

#VX, VY, VZ,...
def getfcvecofname(axis):

    fc_vec = FreeCAD.Vector(getvecofname(axis))
    return fc_vec

def vecname_paral (vec1, vec2):
    """
    given to vectors by name 'x', '-x', ... indicates if they are parallel
    or not
    """
    paral = -1
    if vec1 == 'x' or vec1 == '-x':
        if vec2 == 'x' or vec2 == '-x':
            paral = 1
        else:
            paral = 0
    elif vec1 == 'y' or vec1 == '-y':
        if vec2 == 'y' or vec2 == '-y':
            paral = 1
        else:
            paral = 0
    elif vec1 == 'z' or vec1 == '-z':
        if vec2 == 'z' or vec2 == '-z':
            paral = 1
        else:
            paral = 0
    return paral
    
def get_vecname_perpend1(vecname):

    """ gets a perpendicular vecname

    Args:
        vec: 'x', '-x', 'y', '-y', 'z', '-z'
    """

    if vecname == 'x':
        return 'y'
    elif vecname == 'y':
        return 'z'
    elif vecname == 'z':
        return 'x'
    elif vecname == '-x':
        return '-y'
    elif vecname == '-y':
        return '-z'
    elif vecname == '-z':
        return '-x'


def get_vecname_perpend2(vecname):

    """ gets the other perpendicular vecname (see get_vecname_perpend

    Args:
        vec: 'x', '-x', 'y', '-y', 'z', '-z'
    """

    if vecname == 'x':
        return 'z'
    elif vecname == 'y':
        return 'x'
    elif vecname == 'z':
        return 'y'
    elif vecname == '-x':
        return '-z'
    elif vecname == '-y':
        return '-x'
    elif vecname == '-z':
        return '-y'


def get_nameofbasevec (fcvec):
    """ from a base vector either:
       (1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)
        gets its name: 'x', 'y',....
    """

    if fcvec.x==1 and fcvec.y==0 and fcvec.z==0:
        return 'x'
    elif fcvec.x==0 and fcvec.y==1 and fcvec.z==0:
        return 'y'
    elif fcvec.x==0 and fcvec.y==0 and fcvec.z==1:
        return 'z'
    elif fcvec.x==-1 and fcvec.y==0 and fcvec.z==0:
        return '-x'
    elif fcvec.x==0 and fcvec.y==-1 and fcvec.z==0:
        return '-y'
    elif fcvec.x==0 and fcvec.y==0 and fcvec.z==-1:
        return '-z'
    else:
        print "Not a base vector"


def get_fclist_4perp_vecname (vecname):

    """ gets a list of 4 FreCAD.Vector perpendicular to one vecname
         for example, from 'x' -> (0,1,0), (0,0,1), (0,-1,0), (0,0,-1)
    Args:
        vecname:  'x', '-x', 'y', '-y', 'z', '-z'
    """

    fc_p1 = getfcvecofname(get_vecname_perpend1(vecname))
    fc_p2 = getfcvecofname(get_vecname_perpend2(vecname))
    fc_list = [fc_p1, fc_p2, DraftVecUtils.neg(fc_p1), DraftVecUtils.neg(fc_p2)]
    return fc_list

def get_fclist_4perp_fcvec (fcvec):
    """ gets a list of 4 FreCAD.Vector perpendicular to one base vector
        fcvec can only be:
        (1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)
        for example, from (1,0,0) -> (0,1,0), (0,0,1), (0,-1,0), (0,0,-1)
    Args:
        fcvec: 
        (1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)
    """
    return (get_fclist_4perp_vecname(get_nameofbasevec(fcvec)))


def get_fclist_4perp2_vecname (vecname):

    """ gets a list of 4 FreCAD.Vector perpendicular to one vecname
         different from get_fclist_4perp_vecname
         for example, from 'x' -> (0,1,1), (0,-1,1), (0,-1,-1), (0,1,-1)
    Args:
        vecname:  'x', '-x', 'y', '-y', 'z', '-z'
    """

    fc_p1 = getfcvecofname(get_vecname_perpend1(vecname))
    fc_p1_neg = DraftVecUtils.neg(fc_p1)
    fc_p2 = getfcvecofname(get_vecname_perpend2(vecname))
    fc_p2_neg = DraftVecUtils.neg(fc_p2)
    fc_list = [(fc_p1     + fc_p2),
               (fc_p1     + fc_p2_neg),
               (fc_p1_neg + fc_p2_neg),
               (fc_p1_neg + fc_p2)]
    return fc_list

  
def get_fclist_4perp2_fcvec (fcvec):

    """ gets a list of 4 FreCAD.Vector perpendicular to one base vector
        fcvec can only be:
        (1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)
        for example, from (1,0,0) -> (0,1,1), (0,-1,1), (0,-1,-1), (0,1,-1)
    Args:
        fcvec: 
        (1,0,0), (0,1,0), (0,0,1), (-1,0,0), (0,-1,0), (0,0,-1)
    """
    return (get_fclist_4perp2_vecname(get_nameofbasevec(fcvec)))

def get_positive_vecname (vecname):

    """ it just get 'x' when vecname is 'x' or '-x', and the same
        for the others, because some functions receive only positive
        base vector
    Args:
        vecname:  'x', '-x', 'y', '-y', 'z', '-z'
    """

    if vecname == 'x' or vecname == '-x':
        return 'x'
    elif vecname == 'y' or vecname == '-y':
        return 'y'
    elif vecname == 'z' or vecname == '-z':
        return 'z'
    else:
        logger.error('Not a valid base vector name')



      

def fuseshplist (shp_list):

    """ since multifuse methods needs to be done by a shape and a list,
        and usually I have a list that I want to fuse, I make this function
        to save the inconvenience of doing everytime what I will do here
        Fuse multiFuse
    """

    if len(shp_list) > 0:
        shp1 = shp_list.pop() #remove and get the first element
        if len(shp_list) > 0:
            shpfuse = shp1.multiFuse(shp_list)
        else: #only one element, no fuse:
            logger.debug('only one element to fuse')
            shpfuse = shp1
    else:
        logger.debug('empty list to fuse')
        return

    return (shpfuse)
        
