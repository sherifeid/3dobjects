module fanplate(d,ls,t,ds) 
{
    /*
    d   : diameter of the fan
    ls  : distance between screws
    t   : wall thickness
    ds  : diameter of screws 
    */
    difference()
    {
        difference()
        {
            difference()
            {
                difference()
                {
                    //translate([d*0.1+d/-2,d*0.1+d/-2,0]) minkowski()
                    translate([-0.45*d,-0.45*d,0]) minkowski()
                        { 
                         //cube([d-2*d*0.1,d-2*d*0.1,t/2]);
                         cube([d*0.9,d*0.9,t/2]);
                         cylinder(h=t/2,r=d*0.1);
                        }
                    translate([ls/2,ls/2,0]) cylinder(d=ds,h=t);
                }
                translate([ls/-2,ls/2,0]) cylinder(d=ds,h=t);
            }
            translate([ls/-2,ls/-2,0]) cylinder(d=ds,h=t);
        }
        translate([ls/2,ls/-2,0]) cylinder(d=ds,h=t);
    }
}

module mani_elbow(a,d,t,az)
{
    // this is the manifold elbow
    // a  : angle of the elbow
    // d  : diameter of the elbow
    // t  : wall thickness
    
    rotate([0,0,az]) translate([-1*d,0,0]) rotate([-90,0,0]) difference()
    {
        difference()
        {  
            difference()
            {
                rotate_extrude() translate([d,0,0]) circle(r = d/2);
                rotate_extrude() translate([d,0,0]) circle(r = (d-2*t)/2);
            }
            translate([-2*d,0,-2*d]) cube([4*d,4*d,4*d]);
        }
        rotate([0,0,90-a]) translate([-4*d,-2*d,-2*d]) cube([4*d,4*d,4*d]);
    }
}