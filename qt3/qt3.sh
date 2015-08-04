# Qt initialization script (sh)

qt_prefix=`/usr/bin/pkg-config --variable=prefix qt-mt`

if [ -z "$QTDIR" ] ; then
	QTDIR="$qt_prefix"
	QTINC="$qt_prefix/include"
	QTLIB="$qt_prefix/lib"
fi

export QTDIR QTINC QTLIB
