module.exports = {
  params: {
    designator: 'R',
    value: '',
    from: {type: 'net', value: ''},
    to: {type: 'net', value: ''},
  },
  body: p => `
    (footprint "fridakeys:Passive_0603" (layer "F.Cu") ${p.at}
      (property "Reference" "${p.ref}" (at 0 -1.5 ${p.r}) (layer "F.Fab")
        (effects (font (size 1 1) (thickness 0.15))))
      (property "Value" "${p.value}" (at 0 1.5 ${p.r}) (layer "F.Fab")
        (effects (font (size 1 1) (thickness 0.15))))
      (attr smd)
      (fp_rect (start -1.5 -0.85) (end 1.5 0.85)
        (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
      (pad "1" smd rect (at -0.825 0 ${p.r}) (size 0.8 0.95)
        (layers "F.Cu" "F.Paste" "F.Mask") ${p.from.str})
      (pad "2" smd rect (at 0.825 0 ${p.r}) (size 0.8 0.95)
        (layers "F.Cu" "F.Paste" "F.Mask") ${p.to.str})
    )`,
};
