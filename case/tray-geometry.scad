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

module control_openings(clearance=0) {
    translate([controller[0],controller[1]+12,pcb_z-controller_gap-0.5])
        rotate([-90,0,0]) linear_extrude(40)
            offset(delta=clearance)
                hull() for (x=[-7,7],y=[-2.5,2.5])
                    translate([x,y]) circle(r=2);
    translate([reset[0]-7-clearance,reset[1]-4-clearance,pcb_z-1-clearance])
        cube([14+2*clearance,40+2*clearance,20+clearance]);
    translate([power[0]+(side=="left"?-4:-26)-clearance,
               power[1]-7-clearance,pcb_z-2-clearance])
        cube([30+2*clearance,14+2*clearance,20+clearance]);
}
