#!/usr/bin/env bash
# install_dinos.sh: pretend package manager for a toy box (never runs)
set -euo pipefail

PACKAGES=(stegosaurus triceratops t-rex brachiosaurus)
TOYBOX="${HOME}/toybox"

spinner() {
  local frames='▖▘▝▗'
  printf '%s resolving %s...' "${frames:$1:1}" "$2"
}

for pkg in "${PACKAGES[@]}"; do
  echo "→ fetching ${pkg} from the dino registry"
  mkdir -p "${TOYBOX}/${pkg}"
done

echo "✔ ${#PACKAGES[@]} dinosaurs installed, 0 vulnerabilities, 3 roars"

# ── output ────────────────────────────────────────────
▖ resolving dinosaurs...
▘ resolving dinosaurs...
▝ resolving dinosaurs...
▗ resolving dinosaurs...
▖ resolving dinosaurs...
▘ resolving dinosaurs...
▝ resolving dinosaurs...
▗ resolving dinosaurs...
▖ resolving dinosaurs...
▘ resolving dinosaurs...
▖ resolving dinosaurs...
▘ resolving dinosaurs...
→ fetching stegosaurus from the dino registry
[--------------------]   0%  unpacking stegosaurus, triceratops
[#-------------------]   5%  unpacking stegosaurus, triceratops
[##------------------]  10%  unpacking stegosaurus, triceratops
[###-----------------]  15%  unpacking stegosaurus, triceratops
[####----------------]  20%  unpacking stegosaurus, triceratops
[#####---------------]  25%  unpacking stegosaurus, triceratops
[######--------------]  30%  unpacking stegosaurus, triceratops
[#######-------------]  35%  unpacking stegosaurus, triceratops
[########------------]  40%  unpacking stegosaurus, triceratops
[#########-----------]  45%  unpacking stegosaurus, triceratops
[##########----------]  50%  unpacking stegosaurus, triceratops
[###########---------]  55%  unpacking stegosaurus, triceratops
[############--------]  60%  unpacking stegosaurus, triceratops
[#############-------]  65%  unpacking stegosaurus, triceratops
[##############------]  70%  unpacking stegosaurus, triceratops
[###############-----]  75%  unpacking stegosaurus, triceratops
[################----]  80%  unpacking stegosaurus, triceratops
[#################---]  85%  unpacking stegosaurus, triceratops
[##################--]  90%  unpacking stegosaurus, triceratops
[###################-]  95%  unpacking stegosaurus, triceratops
[####################] 100%  unpacking stegosaurus, triceratops
✔ unpacked 4 dinosaur eggs
▖ linking t-rex arms (they are short)...
▘ linking t-rex arms (they are short)...
▝ linking t-rex arms (they are short)...
▗ linking t-rex arms (they are short)...
▖ linking t-rex arms (they are short)...
▘ linking t-rex arms (they are short)...
▝ linking t-rex arms (they are short)...
▗ linking t-rex arms (they are short)...
✔ t-rex arms linked
[--------------------]   0%  building brachiosaurus neck
[##------------------]  10%  building brachiosaurus neck
[####----------------]  20%  building brachiosaurus neck
[######--------------]  30%  building brachiosaurus neck
[########------------]  40%  building brachiosaurus neck
[##########----------]  50%  building brachiosaurus neck
[############--------]  60%  building brachiosaurus neck
[##############------]  70%  building brachiosaurus neck
[################----]  80%  building brachiosaurus neck
[##################--]  90%  building brachiosaurus neck
[####################] 100%  building brachiosaurus neck
✔ 4 dinosaurs installed, 0 vulnerabilities, 3 roars
