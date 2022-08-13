{
  description = "Stage production management";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    {
      # Nixpkgs overlay providing the application
      overlay = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (final: prev: {
          # The application
          fahrplanpp = prev.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
          };
        })
      ];
    }
    // (flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [self.overlay];
      };
    in {
      apps = {
        fahrplanpp = pkgs.fahrplanpp;
      };

      defaultApp = pkgs.fahrplanpp;

      devShells.default = let
        fahrplanppEnv = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          editablePackageSources = {
            fahrplanpp = ./src;
          };
        };
      in
        fahrplanppEnv.env.overrideAttrs (oldAttrs: {
          buildInputs = [pkgs.poetry];
        });
    }));
}
