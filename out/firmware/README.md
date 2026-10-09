# Firmware

These UF2 files target genuine nice!nano V2 modules.
The left half is the peripheral. The right half is the Bluetooth central.
The build revision and file hashes are recorded in `validation.json`.

Double-tap reset to enter the UF2 bootloader, then copy the matching file to its drive.
Use `left.uf2` for the left module and `right.uf2` for the right module.
For initial setup or split pairing recovery, flash `settings_reset.uf2` to both modules first, then flash their matching keyboard files.
Keep both halves powered while they pair. Connect the computer to `fridakeys` through the right half.

Build success does not prove the assembled keyboard works.
Complete the continuity, polarity, key, Bluetooth, and charging checks in `manufacturing/physical-tests.md` before normal battery use.
