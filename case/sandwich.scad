side = "left";
part = "assembly";
exploded = 0;
bottom_thickness = 3;
spacer_height = 9;
plate_thickness = 1.5;
bezel_thickness = 3;
pcb_thickness = 1.6;
under_pcb_clearance = 4.9;
plate_to_pcb_gap = 3.5;
upper_gasket_height = 0.5;
switch_cutout = 14;
keycap_clearance = 18.8;
pcb_clearance = 0.8;
plate_expansion = 2.5;
wall_expansion = 9;
bolt_diameter = 2.2;
$fn = 48;

include <../build/case/geometry.scad>

data = side == "left" ? left_geometry : right_geometry;
outline = data[0];
keys = data[1];
bolts = data[2];
controller = data[3];
reset = data[4];
power = data[5];
limits = data[6];
pcb_z = bottom_thickness + under_pcb_clearance;
plate_z = pcb_z + pcb_thickness + plate_to_pcb_gap;
lower_gasket_height = plate_z - bottom_thickness - spacer_height;
bezel_z = plate_z + plate_thickness + upper_gasket_height;
assert(lower_gasket_height > 0);
assert(plate_expansion > pcb_clearance);
assert(wall_expansion > plate_expansion + 3);

module pcb_shape() {
    polygon(outline);
}

module perimeter(amount) {
    offset(r = amount) pcb_shape();
}

module bolt_holes() {
    for (p = bolts) translate(p) circle(d = bolt_diameter);
}

module key_holes(size) {
    for (key = keys) translate([key[0], key[1]]) rotate(key[2]) square(size, center = true);
}

module electronics_opening(extra = 0) {
    translate(controller) square([20 + 2 * extra, 42 + 2 * extra], center = true);
}

module side_access() {
    if (side == "left")
        translate([controller[0] - 10, power[1] - 4])
            square([limits[2] - controller[0] + wall_expansion + 11,
                    limits[3] - power[1] + wall_expansion + 5]);
    else
        translate([limits[0] - wall_expansion - 1, power[1] - 4])
            square([controller[0] - limits[0] + wall_expansion + 11,
                    limits[3] - power[1] + wall_expansion + 5]);
}

module bottom() {
    difference() {
        perimeter(wall_expansion);
        bolt_holes();
    }
}

module spacer() {
    difference() {
        perimeter(wall_expansion);
        perimeter(pcb_clearance);
        side_access();
        bolt_holes();
    }
}

module plate() {
    difference() {
        perimeter(plate_expansion);
        key_holes(switch_cutout);
        electronics_opening();
        side_access();
    }
}

module gasket() {
    intersection() {
        difference() {
            perimeter(plate_expansion);
            perimeter(pcb_clearance);
            electronics_opening();
            side_access();
        }
        spacer();
    }
}

module bezel() {
    difference() {
        perimeter(wall_expansion);
        key_holes(keycap_clearance);
        electronics_opening();
        side_access();
        bolt_holes();
    }
}

module layer(z, thickness, shade, index) {
    color(shade) translate([0, 0, z + index * exploded]) linear_extrude(thickness) children();
}

module assembly() {
    layer(0, bottom_thickness, [0.2, 0.2, 0.2, 0.65], 0) bottom();
    layer(bottom_thickness, spacer_height, [0.7, 0.7, 0.7, 0.45], 1) spacer();
    layer(pcb_z, pcb_thickness, [0.97, 0.97, 0.97], 2) pcb_shape();
    layer(bottom_thickness + spacer_height, lower_gasket_height, [0.15, 0.15, 0.15], 3) gasket();
    layer(plate_z, plate_thickness, [0.75, 0.77, 0.8], 4) plate();
    layer(plate_z + plate_thickness, upper_gasket_height, [0.15, 0.15, 0.15], 5) gasket();
    layer(bezel_z, bezel_thickness, [0.75, 0.77, 0.8], 6) bezel();
    for (p = bolts) color([0.3, 0.3, 0.3]) translate([p[0], p[1], bottom_thickness])
        cylinder(d = 4, h = bezel_z - bottom_thickness);
}

if (part == "bottom") bottom();
else if (part == "spacer") spacer();
else if (part == "plate") plate();
else if (part == "gasket") gasket();
else if (part == "bezel") bezel();
else if (part == "assembly") assembly();
else assert(false, "Unknown sandwich case part");
