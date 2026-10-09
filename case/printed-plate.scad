side = "left";
$fn = 48;
include <parameters.scad>
include <geometry.scad>
include <plate-geometry.scad>

include <printed-parameters.scad>
data = side == "left" ? left_geometry : right_geometry;
outline = data[0];
keys = data[1];
bolts = data[2];

module rim() {
    difference() {
        perimeter();
        offset(delta=outline_expansion-rim_width) polygon(outline);
        bolt_holes(washer_diameter+1);
        key_holes(19);
    }
}
union() {
    linear_extrude(plate_thickness) plate();
    translate([0,0,plate_thickness]) linear_extrude(rim_height) rim();
}
