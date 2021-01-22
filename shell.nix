{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    (pkgs.python3.withPackages (p: with p;[
      flask
      psutil
      mpd2
      requests
    ]))
  ];
}

