rm -rf source/ 
sphinx-apidoc -f -o source/ ../pytexit
make clean
make html
