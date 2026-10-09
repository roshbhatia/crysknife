module.exports = {
  params: {
    designator: 'TP',
    DATA: {type: 'net', value: 'TP_DATA'},
    CLK: {type: 'net', value: 'TP_CLK'},
    RST: {type: 'net', value: 'TP_RST'},
    VCC: {type: 'net', value: 'VCC'},
    GND: {type: 'net', value: 'GND'},
  },
  body: p => {
    const nets = [p.DATA, p.RST, null, null, null, p.CLK, p.GND, p.VCC];
    const signals = nets.map((net, i) => `
      (pad "${i+1}" smd rect (at ${i-3.5} 0 ${p.r}) (size 0.6 1.3)
        (layers "F.Cu" "F.Paste" "F.Mask") ${net ? net.str : ''})`).join('');
    return `
    (footprint "fridakeys:Hirose_FH12-8S-1SH" (layer "F.Cu") ${p.at}
      (property "Reference" "${p.ref}" (at 0 2 ${p.r}) (layer "F.Fab")
        (effects (font (size 1 1) (thickness 0.15))))
      (property "Value" "FH12-8S-1SH(55)" (at 0 7 ${p.r}) (layer "F.Fab")
        (effects (font (size 1 1) (thickness 0.15))))
      (attr smd)
      (fp_rect (start -6.3 -0.65) (end 6.3 5.75)
        (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab"))
      (fp_rect (start -7.05 -0.9) (end 7.05 6)
        (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
      ${signals}
      (pad "" smd rect (at -5.9 3.25 ${p.r}) (size 1.8 2.2) (layers "F.Cu" "F.Paste" "F.Mask"))
      (pad "" smd rect (at 5.9 3.25 ${p.r}) (size 1.8 2.2) (layers "F.Cu" "F.Paste" "F.Mask"))
    )`;
  },
};
