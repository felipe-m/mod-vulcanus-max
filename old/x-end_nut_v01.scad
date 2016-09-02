// al poner use, y no include, permite usar los modulos, pero no ejecuta los componentes
use <../../../2016_platform_cell/device/planos/biblioteca_componentes/propios/openscad/chaflanes.scad>

// 3D printer layer height
// This is used to make some structures of one layer to support
// for example the hole for the stud above the hole of the nut
// It is multiplied by 1.1 to be sure that the slicer makes it at
// least one layer high
slicer_layer_height = 0.25;
h_layer3d = 1.1 * slicer_layer_height;

// Tolerance
tol = 0.4;
// Tolerance for small objects
stol = 0.2;

// Base dimensions:
base_dim_x = 80;
base_dim_y = 54;
base_dim_z = 10.5;

// Base position of the lowest [X,Y,Z] corner
base_pos_x = -base_dim_x/2; //The base will be centered on X
base_pos_y = 0;
base_pos_z = 0; // the base is laying on plane Z=0

// Base vertical fillet radius
base_fillet_radius = 4;

//The piece will hold 2 LME10UU linear bearings
bearing_l = 29; //the length of the bearing
bearing_d = 19; //diamenter of the bearing

// add the tolerances:
bearing_l_tol = bearing_l + tol;
bearing_d_tol = bearing_d + tol;

// separation between the bearings (on the X dimension)
bearing_sep = 4;
// separation between the bearing and the X end
dist_bearingend_x0 = (base_dim_x - 2*bearing_l_tol - bearing_sep)/2;
if (dist_bearingend_x0 < 3)
{ 
    echo ("Error, not enought space: ", dist_bearingend_x0);
}

// bearing position. It also corresponds to the Y axis position
// distance from the bearing axis to the Y0. 
dist_bearingax_y0 = 20;

// separation between the center of the M3 bolts and Y end
// Axis distance - bearing radius: space available
m3_bolts_yend = (dist_bearingax_y0 - (bearing_d_tol/2))/2;

// The diameter of the Y Rod is 10
yrod_diam = 10;
// Add 2 mm, because it is just to leave space for the rod
// and hold the linear bearings
yrod_diam_space = yrod_diam + 2;

// The diameter of the X rods are 10
xrod_diam = 10;
xrod_diam_tol = 10 + stol;  //we need it very tight: small tolerance
// How much the X rods are inserted 20mm in the piece
xrod_insert = 20;
// Separation of the X rods axis
xrod_sep = 50;

// Nuts and bolt sizes
m3_r = 1.5;  // M3 diameter 3.2 mm for the tolerance
m4_r = 2;  // M4 diameter 4.2 mm for the tolerance

// M3 diameter 3.2 mm for the tolerance
m3_r_tol = m3_r + stol/2;  // stol/2 because is the radius
echo ("m3_r_tol", m3_r_tol);
// M4 diameter 4.2 mm for the tolerance
m4_r_tol = m4_r + stol/2;
echo ("m4_r_tol", m4_r_tol);

// M3 nut
m3_nut_r = 6.01/2;  // DIN934 M3 nut circumradius
m3_nut_h = 2.4;     // DIN934 M3 nut height

//less tolerance for small numbers. 0.2 (diameter)
m3_nut_r_tol = m3_nut_r + stol/2;  //radius: diam/2
m3_nut_h_tol = m3_nut_h + tol;

// M4 nut
m4_nut_r = 7.66/2;  // DIN934 M4 nut circumradius
m4_nut_h = 3.2;     // DIN934 M4 nut height

//less tolerance for small numbers. 0.2 (diameter)
m4_nut_r_tol = m4_nut_r + stol/2;  //radius: diam/2
m4_nut_h_tol = m4_nut_h + tol;


// M3 bolts positions
highposx_m3 = base_dim_x + base_pos_x-m3_bolts_yend;
lowposx_m3 = base_pos_x + m3_bolts_yend;
//echo ("highposx_m3", highposx_m3);
//echo ("lowposx_m3", lowposx_m3);
mid1posx_m3 = (highposx_m3 - lowposx_m3) /3 + lowposx_m3;
mid2posx_m3 = 2*(highposx_m3 - lowposx_m3) /3 + lowposx_m3;
//echo ("mid1posx_m3", mid1posx_m3);
//echo ("mid2posx_m3", mid2posx_m3);

// instead of having the middle bolts on the same X as the 
// low X row, they will be simetrically to the xrod position
midposxhigh_m3 = xrod_sep/2 - (highposx_m3 - xrod_sep/2);

lowposy_m3  = base_pos_y + m3_bolts_yend;
highposy_m3 = base_pos_y + base_dim_y - m3_bolts_yend;

// M4 bolts positions
posy_m4 = base_pos_y + base_dim_y - xrod_insert + m4_r_tol;
// distance between m4 bolts, used for the idler pullews
dist_m4 = 18;


// X rod insertion, only needs to move it on the X axis: x_pos
module xrod_insert (x_pos)
{
  translate ([x_pos, base_dim_y-xrod_insert, base_dim_z])
    rotate ([-90,0,0])
    cylinder (r=xrod_diam_tol/2, h=xrod_insert+1, $fa=1, $fs=0.5);
}


// the hole for the bolt shank and the nut
module m3_halfboltnut_hole ()
{
  union () {
    // we make it all the way, although it is not necessary because
    // on the lower part it will be also the nut  
    translate([0,0,-1])
      cylinder (r= m3_r_tol, h= base_dim_z+2, $fa=1, $fs=0.5);
    translate([0,0,-1])
      cylinder (r= m3_nut_r_tol, h= m3_nut_h_tol+1, $fn=6);  
    
  // This is a triangle that it is barely supported by the hexagon
  // and it will support the circle above 
  // In a regular triangle the apotheme (in radius) is twice
  // the circumradius (r)
  // Intersection with the hexagon to take the vertexs away, because
  // they are outside the hexagon
    intersection () {  
      rotate([0,0,30])translate([0,0,m3_nut_h_tol])
        cylinder (r= m3_r_tol*2, h=h_layer3d, $fn=3);
      // take vetexs away:
      translate([0,0,m3_nut_h_tol])
        cylinder (r= m3_nut_r_tol, h= h_layer3d, $fn=6);    
    }
    
    // 1.15 is the relationship between the Radius and the Apothem
    // of the hexagon: sqrt(3)/2 . I make it slightly smaller
    translate([0,0,m3_nut_h_tol+h_layer3d])
      //rotate ([0,0,30])
      cylinder (r=m3_r_tol*1.15, h=h_layer3d, $fn=6);  
  }
}


// the hole for the bolt shank and the nut
module m4_halfboltnut_hole ()
{
  union () {
    // we make it all the way, although it is not necessary because
    // on the lower part it will be also the nut  
    translate([0,0,-1])
      cylinder (r= m4_r_tol, h= base_dim_z+2, $fa=1, $fs=0.5);
    translate([0,0,-1])
      cylinder (r= m4_nut_r_tol, h= m4_nut_h_tol+1, $fn=6);  
    
  // This is a triangle that it is barely supported by the hexagon
  // and it will support the circle above 
  // In a regular triangle the apotheme (in radius) is twice
  // the circumradius (r)
  // Intersection with the hexagon to take the vertexs away, because
  // they are outside the hexagon
    intersection () {  
      rotate([0,0,30])translate([0,0,m4_nut_h_tol])
        cylinder (r= m4_r_tol*2, h=h_layer3d, $fn=3);
      // take vetexs away:
      translate([0,0,m4_nut_h_tol])
        cylinder (r= m4_nut_r_tol, h= h_layer3d, $fn=6);    
    }
    
    // 1.15 is the relationship between the Radius and the Apothem
    // of the hexagon: sqrt(3)/2 . I make it slightly smaller
    translate([0,0,m4_nut_h_tol+h_layer3d])
      //rotate ([0,0,30])
      cylinder (r=m4_r_tol*1.15, h=h_layer3d, $fn=6);  
  }
}


difference () 
{
  //centered in X axis
  translate([base_pos_x,base_pos_y,base_pos_z])cube([base_dim_x, base_dim_y, base_dim_z]);

  // ---------------- Y rod -----------------------------
  // add 2 to the cylinder height to avoid non-manifold on
  // the difference
  translate ([0,dist_bearingax_y0, base_dim_z])
  rotate ([0,90,0])cylinder (r= yrod_diam_space/2, h= base_dim_x+2, center=true, $fa=1, $fs=0.5);
    
  // ----------------- Linear bearings

  translate ([(bearing_l_tol+bearing_sep)/2,dist_bearingax_y0, base_dim_z])
    rotate ([0,90,0])cylinder (r= bearing_d_tol/2, h= bearing_l_tol, center=true, $fa=1, $fs=0.5);

  translate ([-(bearing_l_tol+bearing_sep)/2,dist_bearingax_y0, base_dim_z])
    rotate ([0,90,0])cylinder (r= bearing_d_tol/2, h= bearing_l_tol, center=true, $fa=1, $fs=0.5);

  // -------------------------- X rods
  xrod_insert (x_pos = xrod_sep/2);
  xrod_insert (x_pos = -xrod_sep/2);

  // -------------------------- M3 shanks and nuts holes
    
  // on the lower Y lower X
  //translate ([base_dim_x/2-m3_bolts_yend,m3_bolts_yend,0]) 
  translate ([lowposx_m3,lowposy_m3,0])     
    rotate([0,0,15]) // this rotation is not necessary, but cool
    m3_halfboltnut_hole ();

  // on the lower Y higher X
  translate ([highposx_m3,lowposy_m3,0])     
    rotate([0,0,-15]) // this rotation is not necessary, but cool
    m3_halfboltnut_hole ();
    
  // on the lower Y middle 1
  translate ([mid1posx_m3,lowposy_m3,0]) 
    m3_halfboltnut_hole ();
    
  translate ([mid2posx_m3,lowposy_m3,0]) 
    m3_halfboltnut_hole ();

  // on the higher Y lower X
   translate ([lowposx_m3,highposy_m3,0])     
    rotate([0,0,-15]) // this rotation is not necessary, but cool
    m3_halfboltnut_hole ();

  // on the higher Y higher X
  translate ([highposx_m3,highposy_m3,0])     
    rotate([0,0,15]) // this rotation is not necessary, but cool
    m3_halfboltnut_hole ();
    
  // on the higher Y middle 1
  //translate ([mid1posx_m3,highposy_m3,0]) 
  translate ([-midposxhigh_m3,highposy_m3,0])   
    m3_halfboltnut_hole ();
    
  translate ([midposxhigh_m3,highposy_m3,0]) 
    m3_halfboltnut_hole ();    
    
  // M4 bolts for the idler pulleys

  translate ([dist_m4/2, posy_m4, 0])
    m4_halfboltnut_hole ();
    
  translate ([-dist_m4/2, posy_m4, 0])
    m4_halfboltnut_hole ();
        
    
  // ----------------------------- fillets
  // fillet is done on the 4 corners, vetically
  // Translation to the 4 corners:

  // The corner with the lowest X and Y: mxmy
  translate ([base_pos_x, base_pos_y, base_pos_z])
    redondeo_mxmy (r_fillet= base_fillet_radius, h_fillet=base_dim_z);

  // The corner with the lowest X and highest Y: mxy
  translate ([base_pos_x, base_pos_y+base_dim_y, base_pos_z])
    redondeo_mxy (r_fillet= base_fillet_radius, h_fillet=base_dim_z);

  // The corner with the highest X and lowest Y: xmy
  translate ([base_pos_x+base_dim_x, base_pos_y, base_pos_z])
    redondeo_xmy (r_fillet= base_fillet_radius, h_fillet=base_dim_z);

  // The corner with the highest X and highest Y: xy
  translate ([base_pos_x+base_dim_x, base_pos_y+base_dim_y, base_pos_z])
    redondeo_xy (r_fillet= base_fillet_radius, h_fillet=base_dim_z);


}

