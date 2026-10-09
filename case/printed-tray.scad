side = "left";
$fn = 48;
include <tray-geometry.scad>

difference() {
    linear_extrude(tray_height) offset(delta=outline_expansion) polygon(outline);
    translate([0,0,bottom_thickness]) linear_extrude(tray_height)
        offset(delta=pcb_clearance) polygon(outline);
    for (p=bolts) translate([p[0],p[1],-0.1])
        cylinder(d=bolt_diameter,h=bottom_thickness+0.2);
    control_openings();
}
