@echo off
set mypath=%~dp0
pushd %mypath%
bash cccp %*
popd
