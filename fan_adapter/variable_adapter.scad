// A configurable fan size adapter
// Create by : Sherif Eid
// sherif.eid@gmail.com

// Here goes design variables, dimensions are in mm
t_wall = 2;      // wall thickness
d_fan1 = 30;     // fan 1 diameter
d_fan2 = 80;     // fan 2 diameter
angle_mani = 45; // manifold angle
d_screw = 3.4;   // M3 screw diameter

// other advanced variables
res_scale = 10;


// modules go here
module fanplate(diameter,screw_hole,thick) 
{
    difference()
    {
        difference()
        {
            difference()
            {
                difference()
                {
                    difference()
                        {
                        translate([diameter*0.1+diameter/-2,diameter*0.1+diameter/-2,0]) minkowski()
                        { 
                         cube([diameter-2*diameter*0.1,diameter-2*diameter*0.1,thick/2]);
                         cylinder(h=thick/2,r=diameter*0.1);
                        }
                        cylinder(thick,0.9*diameter/2,0.9*diameter/2);
                        }
                    translate([0.8*diameter/2,0.8*diameter/2,0]) cylinder(d=screw_hole,h=thick);
                }
                translate([-0.8*diameter/2,0.8*diameter/2,0]) cylinder(d=screw_hole,h=thick);
            }
            translate([-0.8*diameter/2,-0.8*diameter/2,0]) cylinder(d=screw_hole,h=thick);
        }
        translate([0.8*diameter/2,-0.8*diameter/2,0]) cylinder(d=screw_hole,h=thick);
    }
}



// body code goes here
scale(1/res_scale) fanplate(d_fan1*res_scale,d_screw*res_scale,t_wall*res_scale);
//fanplate(d_fan1,2,t_wall);