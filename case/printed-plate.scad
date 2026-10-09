side = "left";
$fn = 48;
include <parameters.scad>
include <geometry.scad>
include <plate-geometry.scad>

data = side == "left" ? left_geometry : right_geometry;
outline = data[0];
keys = data[1];
bolts = data[2];
reinforced_plate();
