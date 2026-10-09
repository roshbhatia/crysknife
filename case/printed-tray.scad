side = "left";
$fn = 48;
include <parameters.scad>
include <geometry.scad>

data = side == "left" ? left_geometry : right_geometry;
outline = data[0];
bolts = data[2];
controller = data[3];
reset = data[4];
power = data[5];
pcb_z = bottom_thickness + standoff_height + standoff_shim;
plate_z = pcb_z + pcb_thickness + plate_to_pcb_gap;
tray_height = plate_z - 0.3;
pcb_clearance = 0.6;

module usb_opening() {
    translate([controller[0],controller[1]+12,pcb_z-controller_gap-0.5])
        rotate([-90,0,0]) linear_extrude(40)
            hull() for (x=[-7,7],y=[-2.5,2.5])
                translate([x,y]) circle(r=2);
}

difference() {
    linear_extrude(tray_height) offset(delta=outline_expansion) polygon(outline);
    translate([0,0,bottom_thickness]) linear_extrude(tray_height)
        offset(delta=pcb_clearance) polygon(outline);
    for (p=bolts) translate([p[0],p[1],-0.1])
        cylinder(d=bolt_diameter,h=bottom_thickness+0.2);
    usb_opening();
    translate([reset[0]-7,reset[1]-4,pcb_z-1]) cube([14,40,20]);
    translate([power[0]+(side=="left"?-4:-26),power[1]-7,pcb_z-2])
        cube([30,14,20]);
}
