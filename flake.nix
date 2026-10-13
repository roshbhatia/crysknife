{
  description = "crysknife keyboard design tools";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.footprints = {
    url = "github:ceoloide/ergogen-footprints/48935f54b456ff1503d78d6b17d9d146b54e8ade";
    flake = false;
  };

  outputs = { nixpkgs, footprints, ... }:
    let
      systems = [ "aarch64-darwin" "x86_64-darwin" "aarch64-linux" "x86_64-linux" ];
    in {
      devShells = nixpkgs.lib.genAttrs systems (system:
        let pkgs = import nixpkgs { inherit system; };
        in {
          enclosures = pkgs.mkShell {
            packages = [ pkgs.python312 pkgs.uv pkgs.openscad ];
          };
          default = pkgs.mkShell {
            packages = [
              pkgs.nodejs_24
              pkgs.bun
              (pkgs.python3.withPackages (ps: [ ps.pillow ps.shapely ]))
              pkgs.librsvg
              pkgs.poppler-utils
              pkgs.openscad
            ];
            ERGOGEN_FOOTPRINTS = footprints;
          };
        });
    };
}
