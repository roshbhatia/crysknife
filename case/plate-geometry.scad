module perimeter() { offset(delta=outline_expansion) polygon(outline); }
module bolt_holes(d=bolt_diameter) { for (p=bolts) translate(p) circle(d=d); }
module key_holes(size=switch_cutout) {
    for (key=keys) translate([key[0],key[1]]) rotate(key[2]) square(size,center=true);
}
module plate() { difference() { perimeter(); bolt_holes(); key_holes(); } }
