#!/bin/sh
@PYTHON3@ -c "import PyQt4" &> /dev/null
if [ $? -eq 0 ]; then
  exec @PYTHON3@ -m PyQt4.uic.pyuic ${1+"$@"}
else
  exec @PYTHON2@ -m PyQt4.uic.pyuic ${1+"$@"}
fi
