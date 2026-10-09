module perimeter() { offset(delta=outline_expansion) polygon(outline); }
module bolt_holes(d=bolt_diameter) { for (p=bolts) translate(p) circle(d=d); }
module key_holes(size=switch_cutout) {
    for (key=keys) translate([key[0],key[1]]) rotate(key[2]) square(size,center=true);
}
module plate() { difference() { perimeter(); bolt_holes(); key_holes(); } }

module reinforced_plate(rim_width=1.6, rim_height=1) {
    linear_extrude(plate_thickness) plate();
    translate([0,0,-rim_height]) linear_extrude(rim_height)
        difference() {
            perimeter();
            offset(delta=outline_expansion-rim_width) polygon(outline);
            key_holes(20);
            bolt_holes(washer_diameter+1.5);
        }
}
