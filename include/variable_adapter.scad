// A configurable fan size adapter
// Create by : Sherif Eid
// sherif.eid@gmail.com

// Here goes design variables, dimensions are in mm

// fans' parameters
t_wall = 2;      // wall thickness
d_fan1 = 30;     // fan 1: diameter
ls_fan1 = 24;    // fan 1: distance between screw openings
ds_fan1 = 3.4;   // fan 1: screw opening diameters
d_fan2 = 80;     // fan 2: diameter
ls_fan2 = 71.5;  // fan 2: distance between screw openings
ds_fan2 = 4.5;   // fan 2: screw opening diameters
// manifold parameters
l_mani = 30;     // length to manifold elbow  
a_mani = 60;     // manifold angle
az_mani = -0;     // z-axis rotation angle of the manifold elbow
// internal parameters
n_pipe = 0.9;      // pipe reduction ratio relative to fan 1 diameter

// other advanced variables
$fn = 50;        // used to control the resolution of all arcs 

// modules library
use <../include/fan_modules.scad>;

// body code goes here

difference() // fan 1 plate + pipe 
{
    union()
    {
        fanplate(d=d_fan1,ds=ds_fan1,t=t_wall,ls=ls_fan1);  // fan 1 plate
        cylinder(d=n_pipe*d_fan1,h=l_mani+t_wall);    // fan 1 pipe length
    }
    cylinder(d=n_pipe*d_fan1-2*t_wall,h=l_mani+t_wall);
}
translate([0,0,l_mani+t_wall]) mani_elbow(d=n_pipe*d_fan1,a=a_mani,t=t_wall,az=az_mani);

translate([n_pipe*d_fan1*(cos(a_mani)-1),0,t_wall+l_mani+n_pipe*d_fan1*sin(a_mani)]) rotate([0,-1*a_mani,0]) difference()
{
union()
{
    cylinder(d1=n_pipe*d_fan1,d2=n_pipe*d_fan2,l_mani);
    translate([0,0,l_mani]) fanplate(d=d_fan2,ds=ds_fan2,t=t_wall,ls=ls_fan2);  // fan 1 plate
}
cylinder(d1=n_pipe*d_fan1-t_wall,d2=n_pipe*d_fan2-t_wall,l_mani+t_wall);
}

