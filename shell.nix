{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3.pkgs;
buildPythonPackage {
  name = "env";
  src = ./.;
  propagatedBuildInputs = [
    requests
    flask
    mpd2
    psutil
  ];
  checkInputs = [ black jq ];
}

