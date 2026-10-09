const assert = require('node:assert/strict');

module.exports = controller => ({
  params: {...controller.params, socket_side: 'B'},
  body: p => {
    assert.equal(p.reversible, false);
    assert.equal(p.include_extra_pins, false);
    assert(p.r === 0, 'Socket adapter requires an unrotated controller');
    let outline = controller.body(p);
    const pads = [];
    for (const match of outline.matchAll(/\(pad\s/g)) {
      let depth = 0;
      let quoted = false;
      let end = match.index;
      for (; end < outline.length; end++) {
        const character = outline[end];
        if (character === '"' && outline[end-1] !== '\\') quoted = !quoted;
        if (!quoted) {
          if (character === '(') depth++;
          if (character === ')' && --depth === 0) break;
        }
      }
      assert(end < outline.length);
      pads.push(outline.slice(match.index, end+1));
    }
    assert.equal(pads.length, 24);
    assert(pads.every(pad => pad.includes('(drill 1)')));
    for (const pad of pads) outline = outline.replace(pad, '');
    const at = p.at.match(/\(at ([\d.e+-]+) ([\d.e+-]+) -?0\)/);
    assert(at);
    const textJustify = p.socket_side === 'B' ? '(justify mirror)' : '';
    const sockets = [-7.62, 7.62].map((x, index) => {
      const contacts = pads.filter(pad => Number(pad.match(/\(at ([\d.e+-]+)/)[1]) === x);
      assert.equal(contacts.length, 12);
      const relocated = contacts.map(pad => pad.replace(/\(at [\d.e+-]+ ([\d.e+-]+) 0\)/,
        (_, y) => `(at 0 ${(Number(y)-1.27).toFixed(6)} 0)`)).join('\n');
      return `(footprint "crysknife:MillMax_315_1x12" (layer "${p.socket_side}.Cu")
        (at ${Number(at[1])+x} ${Number(at[2])+1.27} 0)
        (property "Reference" "${p.ref}${index === 0 ? 'A' : 'B'}" (at 0 -16 0) (layer "${p.socket_side}.Fab")
          (effects (font (size 1 1) (thickness 0.15)) ${textJustify}))
        (property "Value" "315-43-112-41-003000" (at 0 16 0) (layer "${p.socket_side}.Fab")
          (effects (font (size 1 1) (thickness 0.15)) ${textJustify}))
        (attr through_hole)
        (fp_rect (start -1.27 -15.24) (end 1.27 15.24)
          (stroke (width 0.1) (type default)) (fill none) (layer "${p.socket_side}.Fab"))
        (fp_rect (start -1.52 -15.49) (end 1.52 15.49)
          (stroke (width 0.05) (type default)) (fill none) (layer "${p.socket_side}.CrtYd"))
        ${relocated})`;
    });
    return outline+sockets.join('\n');
  },
});
