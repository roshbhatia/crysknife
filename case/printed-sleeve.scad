side = "left";
$fn = 48;
include <tray-geometry.scad>

sleeve_clearance = 0.5;
sleeve_wall = 2;
sleeve_floor = 4.1;
screw_recess_diameter = 8;
screw_recess_depth = 2.5;
sleeve_top_gap = 0.3;
opening_clearance = 1;
grip_interference = 0.2;
grip_height = 4;
grip_z = 5.3;
inner_expansion = outline_expansion + sleeve_clearance;
outer_expansion = inner_expansion + sleeve_wall;

difference() {
    union() {
        difference() {
            translate([0,0,-sleeve_floor])
                linear_extrude(tray_height-sleeve_top_gap+sleeve_floor)
                    offset(delta=outer_expansion) polygon(outline);
            translate([0,0,-0.01]) linear_extrude(tray_height+1)
                offset(delta=inner_expansion) polygon(outline);
            for (p=bolts) translate([p[0],p[1],-screw_recess_depth])
                cylinder(d=screw_recess_diameter,h=screw_recess_depth+0.02);
        }
        translate([0,0,grip_z]) linear_extrude(grip_height)
            difference() {
                offset(delta=inner_expansion+0.01) polygon(outline);
                offset(delta=outline_expansion-grip_interference) polygon(outline);
            }
    }
    control_openings(opening_clearance);
}
