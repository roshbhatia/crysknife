# Firmware

These UF2 files target genuine nice!nano V2 modules.
The left half is the peripheral. The right half is the Bluetooth central.
The build revision and file hashes are recorded in `validation.json`.

Double-tap reset to enter the UF2 bootloader, then copy the matching file to its drive.
Use `left.uf2` for the left module and `right.uf2` for the right module.
For initial setup or split pairing recovery, flash `settings_reset.uf2` to both modules first, then flash their matching keyboard files.
Keep both halves powered while they pair. Connect the computer to `crysknife` through the right half.

Both halves enter deep sleep after 15 minutes without activity while running on batteries.
Press a key on each sleeping half, then wait for Bluetooth to reconnect before typing.
The left half cannot wake a sleeping right central through Bluetooth.
The wake press may not reach the host. USB power prevents automatic deep sleep.
Pairing settings remain stored. Actual wake reliability needs the tests below.

Follow the [startup checks](../../manufacturing/physical-tests.md) for continuity, battery polarity, keys, Bluetooth, and charging.
