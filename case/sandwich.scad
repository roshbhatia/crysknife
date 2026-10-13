side = "left";
part = "assembly";
exploded = 0;
rf_window = true;
$fn = 48;

include <parameters.scad>
include <geometry.scad>
include <battery.scad>
include <plate-geometry.scad>

data = side == "left" ? left_geometry : right_geometry;
outline = data[0];
keys = data[1];
bolts = data[2];
controller = data[3];
battery = data[7];
plate_z = bottom_thickness + standoff_height + standoff_shim + pcb_thickness + plate_to_pcb_gap;
pcb_z = plate_z - plate_to_pcb_gap - pcb_thickness;
assert(plate_to_pcb_gap == upper_spacer_height + upper_spacer_shim, "Upper spacer height differs from plate gap");
assert(controller_gap > controller_component_height, "Controller components intersect carrier");
assert(pcb_z - controller_gap - controller_board_thickness > bottom_thickness + damping_thickness + 0.5, "Controller intersects the floor");
assert(pcb_z - bottom_thickness >= battery_reserved[2] + battery_component_reservation + battery_foam + battery_cover + damping_thickness, "Insufficient battery and component clearance");

module pcb_shape() {
    difference() {
        polygon(outline);
        for (p = bolts) translate(p) circle(d=data[8]);
    }
}
module rf_profile() { translate([controller[0]-14,controller[1]-23]) square([28,46]); }
module rf_insert() { offset(delta=-0.25) intersection() { perimeter(); rf_profile(); } }
module bottom_flat() { difference() { perimeter(); bolt_holes(); if (rf_window) rf_profile(); } }
module damping() {
    difference() {
        perimeter();
        for (p = bolts) translate(p) circle(d=damping_bolt_diameter);
    }
}
module bottom() { linear_extrude(bottom_thickness) bottom_flat(); }
module spacer(d, h, faces = 48) {
    difference() {
        cylinder(d=d,h=h,$fn=faces);
        translate([0,0,-0.01]) cylinder(d=bolt_diameter,h=h+0.02);
    }
}
module assembly() {
    if (part == "sleeved-assembly") color([0.65,0.8,0.9,0.6])
        import(str("../manufacturing/jlc3dp/",side,"-sleeve.stl"));
    color([0.12,0.12,0.12]) bottom();
    if (rf_window) color([0.8,0.92,1,0.5]) linear_extrude(bottom_thickness) rf_insert();
    color([0.1,0.1,0.1]) translate([0,0,bottom_thickness]) linear_extrude(damping_thickness) damping();
    color([0.25,0.3,0.4]) translate([battery[0]+(side=="left"?-1:1)*(battery_reserved[0]-battery_protected[0])/2-battery_protected[0]/2,battery[1]+(battery_reserved[1]-battery_protected[1])/2-battery_protected[1]/2,bottom_thickness+damping_thickness+battery_foam]) cube(battery_protected);
    color([0.97,0.97,0.97]) translate([0,0,pcb_z+exploded]) linear_extrude(pcb_thickness) pcb_shape();
    color([0.15,0.2,0.3]) translate([controller[0]-controller_width/2,controller[1]-controller_length/2,pcb_z-controller_gap-controller_board_thickness])
        cube([controller_width,controller_length,controller_board_thickness]);
    color([0.7,0.7,0.7]) translate([controller[0]-4.5,controller[1]+10,pcb_z-controller_gap])
        cube([9,7,controller_component_height]);
    color([0.8,0.92,1,0.35]) translate([0,0,plate_z+2*exploded])
        if (part == "sleeved-assembly") reinforced_plate();
        else linear_extrude(plate_thickness) plate();
    for (p = bolts) color([0.25,0.25,0.25]) translate([p[0],p[1],bottom_thickness])
        spacer(standoff_across_flats/cos(30),standoff_height,6);
    for (p = bolts) color([0.9,0.9,0.9]) translate([p[0],p[1],bottom_thickness+standoff_height])
        spacer(standoff_shim_diameter,standoff_shim);
    for (p = bolts) color([0.9,0.9,0.9]) translate([p[0],p[1],pcb_z+pcb_thickness])
        spacer(washer_diameter,upper_spacer_shim);
    for (p = bolts) color([0.9,0.9,0.9]) translate([p[0],p[1],pcb_z+pcb_thickness+upper_spacer_shim])
        spacer(upper_spacer_diameter,upper_spacer_height);
}
if (part == "bottom") bottom();
else if (part == "bottom-flat") bottom_flat();
else if (part == "rf-insert") rf_insert();
else if (part == "damping") damping();
else if (part == "plate") plate();
else if (part == "plate-solid") linear_extrude(plate_thickness) plate();
else if (part == "switch-fit-coupon") difference() {
    square([90,24],center=true);
    for (i=[0:3]) translate([-30+i*20,0]) square(13.9+i*0.1,center=true);
}
else if (part == "assembly" || part == "sleeved-assembly") assembly();
else assert(false, "Expected bottom, bottom-flat, damping, plate, or assembly");
