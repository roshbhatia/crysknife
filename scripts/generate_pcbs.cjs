const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const yaml = require('js-yaml');
const ergogen = require('ergogen');

const root = path.resolve(__dirname, '..');
const library = process.env.ERGOGEN_FOOTPRINTS;
assert(library, 'Run this command in the repository Nix shell.');
const footprintNames = [
  'switch_mx', 'diode_tht_sod123', 'power_switch_smd_side',
  'reset_switch_smd_side', 'battery_connector_jst_ph_2', 'mounting_hole_npth',
];
for (const name of footprintNames) {
  const footprint = require(path.join(library, `${name}.js`));
  ergogen.inject(`ceoloide/${name}`, name === 'mounting_hole_npth'
    ? {...footprint, body: p => footprint.body({...p, ref_hide: 'hide'})}
    : footprint);
}
const controller = require(path.join(library, 'mcu_nice_nano.js'));
ergogen.inject('crysknife/nice_nano_socketed', require('../ergogen/controller_sockets.js')(controller));

async function main() {
  const config = yaml.load(fs.readFileSync(path.join(root, 'ergogen/layout.yaml'), 'utf8'));
  const layout = await ergogen.process(config, true);
  const pointNames = new Set(Object.keys(layout.points));
  config.points.mirror = 167.5;
  const originalOutlines = config.outlines;
  config.outlines = {};
  for (const side of ['left', 'right']) {
    for (const [name, parts] of Object.entries(originalOutlines)) {
      const copy = structuredClone(parts);
      for (const part of copy) {
        if (part.what === 'outline') {
          part.name = `${side}_${part.name}`;
        } else {
          if (part.where !== undefined) {
            if (side === 'right' && typeof part.where === 'string' && pointNames.has(part.where)) {
              part.where = `mirror_${part.where}`;
            } else {
              part.where = [[part.where, `meta.mirrored ~ ${side === 'right'}`]];
            }
          }
          if (side === 'right' && part.points) {
            for (const anchor of part.points) {
              if (anchor.ref) {
                assert(pointNames.has(anchor.ref), `Unknown outline anchor ${anchor.ref}`);
                anchor.ref = `mirror_${anchor.ref}`;
              }
            }
          }
        }
      }
      config.outlines[`${side}_${name}`] = copy;
    }
  }
  config.pcbs = yaml.load(fs.readFileSync(path.join(root, 'ergogen/pcb.yaml'), 'utf8')).pcbs;
  const result = await ergogen.process(config, true, console.log);
  const output = path.join(root, 'build/pcb');
  fs.mkdirSync(output, {recursive: true});
  fs.writeFileSync(path.join(output, 'config.yaml'), yaml.dump(config));
  for (const [name, board] of Object.entries(result.pcbs)) {
    assert.equal((board.match(/\(footprint "ceoloide:switch_mx"/g) || []).length, 21);
    assert.equal((board.match(/\(footprint "ceoloide:diode_tht_sod123"/g) || []).length, 21);
    fs.writeFileSync(path.join(output, `${name}.kicad_pcb`), board);
    console.log(`Wrote build/pcb/${name}.kicad_pcb`);
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
