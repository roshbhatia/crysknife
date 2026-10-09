side = "left";
$fn = 48;
include <sleeve-geometry.scad>
include <plate-geometry.scad>
keys = data[1];

sleeve_clearance = 0.5;
sleeve_wall = 2;
sleeve_floor = 4.1;
screw_recess_diameter = 8;
screw_recess_depth = 2.5;
lip_clearance = 0.3;
lip_height = 1.6;
lip_overlap = 1.8;
keycap_keepout = 20;
lip_z = plate_z + plate_thickness + lip_clearance;
opening_clearance = 1;
inner_expansion = outline_expansion + sleeve_clearance;
outer_expansion = inner_expansion + sleeve_wall;

difference() {
    union() {
        difference() {
            translate([0,0,-sleeve_floor])
                linear_extrude(lip_z+sleeve_floor)
                    offset(delta=outer_expansion) polygon(outline);
            translate([0,0,-0.01]) linear_extrude(lip_z+1)
                offset(delta=inner_expansion) polygon(outline);
            for (p=bolts) translate([p[0],p[1],-screw_recess_depth])
                cylinder(d=screw_recess_diameter,h=screw_recess_depth+0.02);
        }
        translate([0,0,lip_z]) linear_extrude(lip_height)
            difference() {
                offset(delta=outer_expansion) polygon(outline);
                offset(delta=outline_expansion-lip_overlap) polygon(outline);
                bolt_holes(washer_diameter+1.5);
            }
    }
    control_openings(opening_clearance);
    translate([0,0,plate_z]) linear_extrude(lip_z+lip_height-plate_z+1)
        key_holes(keycap_keepout);
}
