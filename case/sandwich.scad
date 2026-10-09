side = "left";
part = "assembly";
exploded = 0;
$fn = 48;

include <parameters.scad>
include <geometry.scad>

data = side == "left" ? left_geometry : right_geometry;
outline = data[0];
keys = data[1];
bolts = data[2];
controller = data[3];
power = data[5];
limits = data[6];
battery = data[7];
plate_z = bottom_thickness + standoff_height + standoff_shim;
pcb_z = plate_z - plate_to_pcb_gap - pcb_thickness;
assert(pcb_z - bottom_thickness >= 13.9 + damping_thickness, "Insufficient battery and component clearance");

module pcb_shape() { polygon(outline); }
module perimeter() { offset(r = outline_expansion) pcb_shape(); }
module bolt_holes() { for (p = bolts) translate(p) circle(d = bolt_diameter); }
module key_holes() {
    for (key = keys) translate([key[0], key[1]]) rotate(key[2]) square(switch_cutout, center = true);
}
module side_access() {
    if (side == "left")
        translate([controller[0]-10, power[1]-4])
            square([limits[2]-controller[0]+outline_expansion+11, limits[3]-power[1]+outline_expansion+5]);
    else
        translate([limits[0]-outline_expansion-1, power[1]-4])
            square([controller[0]-limits[0]+outline_expansion+11, limits[3]-power[1]+outline_expansion+5]);
}
flange_x = limits[2] + outline_expansion + flange_clearance;
flange_length = flange_y_max - flange_y_min;
flat_edge_x = flange_x + flange_height + 2*bottom_thickness - bend_deduction;

module base_shape(flat = false) {
    union() {
        perimeter();
        for (sign = [-1,1]) scale([sign,1])
            translate([flange_x-10, flange_y_min])
                square([(flat ? flat_edge_x : flange_x-bend_radius)-(flange_x-10), flange_length]);
    }
}
module bottom_flat() { difference() { base_shape(true); bolt_holes(); } }
module damping() {
    difference() {
        perimeter();
        for (p = bolts) translate(p) circle(d=damping_bolt_diameter);
    }
}
module flange_profile() {
    r = bend_radius;
    t = bottom_thickness;
    polygon(concat(
        [[-(10-r),-r-t]],
        [for (i=[0:12]) let(a=-90+i*90/12) [(r+t)*cos(a),(r+t)*sin(a)]],
        [[r+t,flange_height-r],[r,flange_height-r]],
        [for (i=[0:12]) let(a=-i*90/12) [r*cos(a),r*sin(a)]],
        [[-(10-r),-r]]
    ));
}
module bottom() {
    difference() {
        union() {
            linear_extrude(bottom_thickness) base_shape();
            for (sign = [-1,1]) scale([sign,1,1])
                translate([flange_x-bend_radius,flange_y_max,bottom_thickness+bend_radius])
                    rotate([90,0,0]) linear_extrude(flange_length) flange_profile();
        }
        translate([0,0,-1]) linear_extrude(bottom_thickness+2) bolt_holes();
    }
}
module plate() {
    difference() {
        perimeter(); bolt_holes(); key_holes();
        translate(controller) square([20, 42], center = true);
        side_access();
    }
}
module assembly() {
    color([0.65,0.67,0.7]) bottom();
    color([0.1,0.1,0.1]) translate([0,0,bottom_thickness]) linear_extrude(damping_thickness) damping();
    color([0.25,0.3,0.4]) translate([battery[0]-30,battery[1]-18,bottom_thickness+damping_thickness+0.5]) cube([60,36,7]);
    color([0.97,0.97,0.97]) translate([0,0,pcb_z+exploded]) linear_extrude(pcb_thickness) pcb_shape();
    color([0.8,0.92,1,0.35]) translate([0,0,plate_z+2*exploded]) linear_extrude(plate_thickness) plate();
    for (p = bolts) color([0.25,0.25,0.25]) translate([p[0],p[1],bottom_thickness])
        cylinder(d=4,h=standoff_height);
    for (p = bolts) color([0.9,0.9,0.9]) translate([p[0],p[1],bottom_thickness+standoff_height])
        cylinder(d=4,h=standoff_shim);
}
if (part == "bottom") bottom();
else if (part == "bottom-flat") bottom_flat();
else if (part == "damping") damping();
else if (part == "plate") plate();
else if (part == "switch-fit-coupon") difference() {
    square([90,24],center=true);
    for (i=[0:3]) translate([-30+i*20,0]) square(13.9+i*0.1,center=true);
}
else if (part == "assembly") assembly();
else assert(false, "Expected bottom, bottom-flat, damping, plate, or assembly");
