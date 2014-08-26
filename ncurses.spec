Summary:	Emulation of curses in System V Release 4.0
Name:		ncurses
Version:	5.9
Release:	9
License:	distributable
Group:		Core/Libraries
Source0:	ftp://dickey.his.com/ncurses/%{name}-%{version}.tar.gz
# Source0-md5:	8cb9c412e5f2d96bc6f459aa8c6282a1
Patch0:		ftp://dickey.his.com/ncurses/5.9/%{name}-5.9-20140308-patch.sh.bz2
Patch1:		%{name}-meta.patch
Patch2:		%{name}-gnome-terminal.patch
Patch3:		%{name}-urxvt.patch
URL:		http://dickey.his.com/ncurses/ncurses.html
BuildRequires:	automake
BuildRequires:	gpm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The curses library routines give the user a terminal-independent
method of updating character screens with reasonable optimization.
This implementation is ``new curses'' (ncurses) and is the approved
replacement for 4.4BSD classic curses, which is being discontinued.

%package -n terminfo
Summary:	Complete terminfo database
Group:		Applications/Terminal
Requires:	%{name} = %{version}-%{release}

%description -n terminfo
This package contains complete terminfo database. If you just use the
Linux console, xterm and VT100, you probably will not need this this -
a minimal %{_datadir}/terminfo tree for these terminal is already
included in the ncurses package.

%package devel
Summary:	Header files for develop ncurses based application
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package includes the header files and libraries necessary to
develop applications that use ncurses.

%package static
Summary:	Static libraries for ncurses
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package includes the static libraries necessary to develop
applications that use ncurses.

%package ext
Summary:	Additional ncurses libraries
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ext
This package contains addidion ncurses libraries like libforms,
libmenu and libpanel for easy making full screen curse application.

%package ext-devel
Summary:	Header files for additional ncurses libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-ext = %{version}-%{release}

%description ext-devel
Header files for additional ncurses libraries (form, menu, panel).

%package ext-static
Summary:	Static versions of additional ncurses libraries
Group:		Development/Libraries
Requires:	%{name}-ext-devel = %{version}-%{release}

%description ext-static
Static versions of additional ncurses libraries (form, menu, panel).

%package c++-devel
Summary:	Header files for develop C++ ncurses based application
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description c++-devel
This package includes the header files and libraries necessary to
develop applications that use C++ ncurses.

%package c++-static
Summary:	Static libraries for C++ ncurses
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
This package includes the static libraries necessary to develop
applications that use C++ ncurses.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
install -d build-ncurses{,w}
COMMONOPT=" \
%ifarch %{x8664}
	--with-chtype=long  \
%endif
	--with-normal	    \
	--with-pkg-config-libdir=%{_pkgconfigdir}   \
	--with-shared	    \
	--without-ada	    \
	--without-debug"

cd build-ncursesw
../%configure \
	--enable-ext-colors \
	--enable-pc-files   \
	--enable-widec	    \
	$COMMONOPT
%{__make}

cd ../build-ncurses
../%configure \
	$COMMONOPT
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd build-ncursesw
%{__make} install \
    DESTDIR=$RPM_BUILD_ROOT

for lib in ncurses form panel menu; do
    echo "INPUT(-l${lib}w)" > $RPM_BUILD_ROOT%{_libdir}/lib${lib}.so
done
for lib in ncurses ncurses++ form panel menu; do
    ln -s ${lib}w.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/${lib}.pc
done

echo "INPUT(-lncursesw)" > $RPM_BUILD_ROOT%{_libdir}/libcursesw.so
ln -s libncurses.so $RPM_BUILD_ROOT%{_libdir}/libcurses.so

cd ../build-ncurses
for lib in ncurses form panel menu; do
    install -Dm755 lib/lib${lib}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/lib${lib}.so.%{version}
    ln -s lib${lib}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/lib${lib}.so.5
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%post	ext -p /usr/sbin/ldconfig
%postun	ext -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE README
%attr(755,root,root) %{_bindir}/captoinfo
%attr(755,root,root) %{_bindir}/clear
%attr(755,root,root) %{_bindir}/infocmp
%attr(755,root,root) %{_bindir}/infotocap
%attr(755,root,root) %{_bindir}/reset
%attr(755,root,root) %{_bindir}/tabs
%attr(755,root,root) %{_bindir}/tic
%attr(755,root,root) %{_bindir}/toe
%attr(755,root,root) %{_bindir}/tput
%attr(755,root,root) %{_bindir}/tset

%attr(755,root,root) %ghost %{_libdir}/libncurses.so.5
%attr(755,root,root) %ghost %{_libdir}/libncursesw.so.6
%attr(755,root,root) %{_libdir}/libncurses.so.*.*
%attr(755,root,root) %{_libdir}/libncursesw.so.*.*

%{_datadir}/tabset

%dir %{_datadir}/terminfo
%{_datadir}/terminfo/E
%dir %{_datadir}/terminfo/[cdgklprsvx]

%{_datadir}/terminfo/c/cygwin*
%{_datadir}/terminfo/d/dumb
%{_datadir}/terminfo/g/gnome*
%{_datadir}/terminfo/k/klone+color
%{_datadir}/terminfo/k/konsole*
%{_datadir}/terminfo/l/linux*
%{_datadir}/terminfo/p/putty*
%{_datadir}/terminfo/r/rxvt*
%{_datadir}/terminfo/s/screen*
%{_datadir}/terminfo/v/vt100
%{_datadir}/terminfo/v/vt102
%{_datadir}/terminfo/v/vt220
%{_datadir}/terminfo/v/vt220-8
%{_datadir}/terminfo/v/vt52
%{_datadir}/terminfo/x/xterm*

%{_mandir}/man1/captoinfo.1m*
%{_mandir}/man1/clear.1*
%{_mandir}/man1/infocmp.1m*
%{_mandir}/man1/infotocap.1m*
%{_mandir}/man1/reset.1*
%{_mandir}/man1/tabs.1*
%{_mandir}/man1/tic.1m*
%{_mandir}/man1/toe.1m*
%{_mandir}/man1/tput.1*
%{_mandir}/man1/tset.1*
%{_mandir}/man5/term.5*
%{_mandir}/man5/terminfo.5*
%{_mandir}/man7/term.7*

%files -n terminfo
%defattr(644,root,root,755)
%{_datadir}/terminfo/[1-9ALMNPQXa-ce-jm-rt-uwz]
%{_datadir}/terminfo/[dklsvx]/*
%exclude %{_datadir}/terminfo/c/cygwin*
%exclude %{_datadir}/terminfo/d/dumb
%exclude %{_datadir}/terminfo/g/gnome*
%exclude %{_datadir}/terminfo/k/klone+color
%exclude %{_datadir}/terminfo/k/konsole*
%exclude %{_datadir}/terminfo/l/linux*
%exclude %{_datadir}/terminfo/p/putty*
%exclude %{_datadir}/terminfo/r/rxvt*
%exclude %{_datadir}/terminfo/s/screen*
%exclude %{_datadir}/terminfo/v/vt100
%exclude %{_datadir}/terminfo/v/vt102
%exclude %{_datadir}/terminfo/v/vt220
%exclude %{_datadir}/terminfo/v/vt220-8
%exclude %{_datadir}/terminfo/v/vt52
%exclude %{_datadir}/terminfo/x/xterm*

%files devel
%defattr(644,root,root,755)
%doc doc/html/ncurses-intro.html
%attr(755,root,root) %{_bindir}/ncursesw6-config
%attr(755,root,root) %{_libdir}/libcurses.so
%attr(755,root,root) %{_libdir}/libcursesw.so
%attr(755,root,root) %{_libdir}/libncurses.so
%attr(755,root,root) %{_libdir}/libncursesw.so

%dir %{_includedir}
%{_includedir}/curses.h
%{_includedir}/eti.h
%{_includedir}/nc_tparm.h
%{_includedir}/ncurses.h
%{_includedir}/ncurses_dll.h
%{_includedir}/term.h
%{_includedir}/term_entry.h
%{_includedir}/termcap.h
%{_includedir}/tic.h
%{_includedir}/unctrl.h
%{_pkgconfigdir}/ncurses.pc
%{_pkgconfigdir}/ncursesw.pc
%{_mandir}/man1/ncursesw6-config.1*
%{_mandir}/man3/BC.3x*
%{_mandir}/man3/COLORS.3x*
%{_mandir}/man3/COLOR_PAIR.3x*
%{_mandir}/man3/COLOR_PAIRS.3x*
%{_mandir}/man3/COLS.3x*
%{_mandir}/man3/ESCDELAY.3x*
%{_mandir}/man3/LINES.3x*
%{_mandir}/man3/PAIR_NUMBER.3x*
%{_mandir}/man3/PC.3x*
%{_mandir}/man3/SP.3x*
%{_mandir}/man3/TABSIZE.3x*
%{_mandir}/man3/UP.3x*
%{_mandir}/man3/_nc_*.3x*
%{_mandir}/man3/_trace*.3x*
%{_mandir}/man3/acs_map.3x*
%{_mandir}/man3/add*.3x*
%{_mandir}/man3/assume_default_colors*.3x*
%{_mandir}/man3/attr*.3x*
%{_mandir}/man3/baudrate*.3x*
%{_mandir}/man3/beep*.3x*
%{_mandir}/man3/bkgd*.3x*
%{_mandir}/man3/bkgrnd*.3x*
%{_mandir}/man3/bool*.3x*
%{_mandir}/man3/border*.3x*
%{_mandir}/man3/box*.3x*
%{_mandir}/man3/can_change_color*.3x*
%{_mandir}/man3/cbreak*.3x*
%{_mandir}/man3/ceiling_panel.3x*
%{_mandir}/man3/chgat.3x*
%{_mandir}/man3/clear*.3x*
%{_mandir}/man3/clrto*.3x*
%{_mandir}/man3/color_*.3x*
%{_mandir}/man3/copywin.3x*
%{_mandir}/man3/cur_term.3x*
%{_mandir}/man3/curs_*.3x*
%{_mandir}/man3/curscr.3x*
%{_mandir}/man3/curses_version.3x*
%{_mandir}/man3/def_*.3x*
%{_mandir}/man3/default_colors.3x*
%{_mandir}/man3/define_key*.3x*
%{_mandir}/man3/del_curterm*.3x*
%{_mandir}/man3/delay_output*.3x*
%{_mandir}/man3/delch.3x*
%{_mandir}/man3/deleteln.3x*
%{_mandir}/man3/delscreen.3x*
%{_mandir}/man3/delwin.3x*
%{_mandir}/man3/derwin.3x*
%{_mandir}/man3/doupdate*.3x*
%{_mandir}/man3/dupwin.3x*
%{_mandir}/man3/echo*.3x*
%{_mandir}/man3/endwin*.3x*
%{_mandir}/man3/erase*.3x*
%{_mandir}/man3/filter*.3x*
%{_mandir}/man3/flash*.3x*
%{_mandir}/man3/flushinp*.3x*
%{_mandir}/man3/get*.3x*
%{_mandir}/man3/ground_panel.3x*
%{_mandir}/man3/halfdelay*.3x*
%{_mandir}/man3/has_*.3x*
%{_mandir}/man3/hline*.3x*
%{_mandir}/man3/idcok.3x*
%{_mandir}/man3/idlok.3x*
%{_mandir}/man3/immedok.3x*
%{_mandir}/man3/in_*.3x*
%{_mandir}/man3/inch*.3x*
%{_mandir}/man3/init_color*.3x*
%{_mandir}/man3/init_pair*.3x*
%{_mandir}/man3/initscr.3x*
%{_mandir}/man3/innstr.3x*
%{_mandir}/man3/innwstr.3x*
%{_mandir}/man3/ins*.3x*
%{_mandir}/man3/intrflush*.3x*
%{_mandir}/man3/inwstr.3x*
%{_mandir}/man3/is_*.3x*
%{_mandir}/man3/isendwin*.3x*
%{_mandir}/man3/key*.3x*
%{_mandir}/man3/kill*.3x*
%{_mandir}/man3/leaveok.3x*
%{_mandir}/man3/legacy_coding.3x*
%{_mandir}/man3/longname.3x*
%{_mandir}/man3/mcprint*.3x*
%{_mandir}/man3/meta.3x*
%{_mandir}/man3/mouse*.3x*
%{_mandir}/man3/move.3x*
%{_mandir}/man3/mv*.3x*
%{_mandir}/man3/napms*.3x*
%{_mandir}/man3/ncurses.3x*
%{_mandir}/man3/new_prescr.3x*
%{_mandir}/man3/newpad*.3x*
%{_mandir}/man3/newscr.3x*
%{_mandir}/man3/newterm*.3x*
%{_mandir}/man3/newwin*.3x*
%{_mandir}/man3/nl*.3x*
%{_mandir}/man3/no*.3x*
%{_mandir}/man3/num*.3x*
%{_mandir}/man3/ospeed.3x*
%{_mandir}/man3/overlay.3x*
%{_mandir}/man3/overwrite.3x*
%{_mandir}/man3/pair_content*.3x*
%{_mandir}/man3/pecho*.3x*
%{_mandir}/man3/pnoutrefresh.3x*
%{_mandir}/man3/prefresh.3x*
%{_mandir}/man3/printw.3x*
%{_mandir}/man3/put*.3x*
%{_mandir}/man3/qiflush*.3x*
%{_mandir}/man3/raw*.3x*
%{_mandir}/man3/redrawwin.3x*
%{_mandir}/man3/refresh.3x*
%{_mandir}/man3/reset_*.3x*
%{_mandir}/man3/resetty*.3x*
%{_mandir}/man3/resize_term*.3x*
%{_mandir}/man3/resizeterm*.3x*
%{_mandir}/man3/restartterm*.3x*
%{_mandir}/man3/ripoffline*.3x*
%{_mandir}/man3/savetty*.3x*
%{_mandir}/man3/scanw.3x*
%{_mandir}/man3/scr_*.3x*
%{_mandir}/man3/scrl.3x*
%{_mandir}/man3/scroll*.3x*
%{_mandir}/man3/set_curterm*.3x*
%{_mandir}/man3/set_escdelay*.3x*
%{_mandir}/man3/set_tabsize*.3x*
%{_mandir}/man3/set_term.3x*
%{_mandir}/man3/setcchar.3x*
%{_mandir}/man3/setscrreg.3x*
%{_mandir}/man3/setsyx.3x*
%{_mandir}/man3/setterm.3x*
%{_mandir}/man3/setupterm.3x*
%{_mandir}/man3/slk_*.3x*
%{_mandir}/man3/stand*.3x*
%{_mandir}/man3/start_color*.3x*
%{_mandir}/man3/stdscr.3x*
%{_mandir}/man3/str*.3x*
%{_mandir}/man3/subpad.3x*
%{_mandir}/man3/subwin.3x*
%{_mandir}/man3/syncok.3x*
%{_mandir}/man3/term*.3x*
%{_mandir}/man3/tget*.3x*
%{_mandir}/man3/tgoto.3x*
%{_mandir}/man3/tiget*.3x*
%{_mandir}/man3/timeout.3x*
%{_mandir}/man3/tiparm.3x*
%{_mandir}/man3/touchline.3x*
%{_mandir}/man3/touchwin.3x*
%{_mandir}/man3/tparm.3x*
%{_mandir}/man3/tputs*.3x*
%{_mandir}/man3/trace.3x*
%{_mandir}/man3/ttytype.3x*
%{_mandir}/man3/typeahead*.3x*
%{_mandir}/man3/unctrl*.3x*
%{_mandir}/man3/unget*.3x*
%{_mandir}/man3/untouchwin.3x*
%{_mandir}/man3/use_*.3x*
%{_mandir}/man3/vid*.3x*
%{_mandir}/man3/vline*.3x*
%{_mandir}/man3/vw*.3x*
%{_mandir}/man3/wadd*.3x*
%{_mandir}/man3/wattr*.3x*
%{_mandir}/man3/wbkgd*.3x*
%{_mandir}/man3/wbkgrnd*.3x*
%{_mandir}/man3/wborder*.3x*
%{_mandir}/man3/wchgat.3x*
%{_mandir}/man3/wclear.3x*
%{_mandir}/man3/wclrto*.3x*
%{_mandir}/man3/wcolor_set.3x*
%{_mandir}/man3/wcursyncup.3x*
%{_mandir}/man3/wdel*.3x*
%{_mandir}/man3/wecho*.3x*
%{_mandir}/man3/wenclose.3x*
%{_mandir}/man3/werase.3x*
%{_mandir}/man3/wget*.3x*
%{_mandir}/man3/whline*.3x*
%{_mandir}/man3/win*.3x*
%{_mandir}/man3/wmouse_trafo.3x*
%{_mandir}/man3/wmove.3x*
%{_mandir}/man3/wnoutrefresh.3x*
%{_mandir}/man3/wprintw.3x*
%{_mandir}/man3/wredrawln.3x*
%{_mandir}/man3/wrefresh.3x*
%{_mandir}/man3/wresize.3x*
%{_mandir}/man3/wscanw.3x*
%{_mandir}/man3/wscrl.3x*
%{_mandir}/man3/wsetscrreg.3x*
%{_mandir}/man3/wstand*.3x*
%{_mandir}/man3/wsync*.3x*
%{_mandir}/man3/wtimeout.3x*
%{_mandir}/man3/wtouchln.3x*
%{_mandir}/man3/wunctrl*.3x*
%{_mandir}/man3/wvline*.3x*

%files ext
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libform.so.[56]
%attr(755,root,root) %ghost %{_libdir}/libformw.so.[56]
%attr(755,root,root) %ghost %{_libdir}/libmenu.so.[56]
%attr(755,root,root) %ghost %{_libdir}/libmenuw.so.[56]
%attr(755,root,root) %ghost %{_libdir}/libpanel.so.[56]
%attr(755,root,root) %ghost %{_libdir}/libpanelw.so.[56]
%attr(755,root,root) %{_libdir}/libform.so.*.*
%attr(755,root,root) %{_libdir}/libformw.so.*.*
%attr(755,root,root) %{_libdir}/libmenu.so.*.*
%attr(755,root,root) %{_libdir}/libmenuw.so.*.*
%attr(755,root,root) %{_libdir}/libpanel.so.*.*
%attr(755,root,root) %{_libdir}/libpanelw.so.*.*

%files ext-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libform.so
%attr(755,root,root) %{_libdir}/libmenu.so
%attr(755,root,root) %{_libdir}/libpanel.so
%attr(755,root,root) %{_libdir}/libformw.so
%attr(755,root,root) %{_libdir}/libmenuw.so
%attr(755,root,root) %{_libdir}/libpanelw.so
%{_includedir}/form.h
%{_includedir}/menu.h
%{_includedir}/panel.h
%{_pkgconfigdir}/form.pc
%{_pkgconfigdir}/formw.pc
%{_pkgconfigdir}/menu.pc
%{_pkgconfigdir}/menuw.pc
%{_pkgconfigdir}/panel.pc
%{_pkgconfigdir}/panelw.pc
%{_mandir}/man3/TYPE_ALNUM.3x*
%{_mandir}/man3/TYPE_ALPHA.3x*
%{_mandir}/man3/TYPE_ENUM.3x*
%{_mandir}/man3/TYPE_INTEGER.3x*
%{_mandir}/man3/TYPE_IPV4.3x*
%{_mandir}/man3/TYPE_NUMERIC.3x*
%{_mandir}/man3/TYPE_REGEXP.3x*
%{_mandir}/man3/bottom_panel.3x*
%{_mandir}/man3/current_field.3x*
%{_mandir}/man3/current_item.3x*
%{_mandir}/man3/data_ahead.3x*
%{_mandir}/man3/data_behind.3x*
%{_mandir}/man3/del_panel.3x*
%{_mandir}/man3/dup_field.3x*
%{_mandir}/man3/dynamic_field_info.3x*
%{_mandir}/man3/field_*.3x*
%{_mandir}/man3/form*.3x*
%{_mandir}/man3/free_*.3x*
%{_mandir}/man3/hide_panel.3x*
%{_mandir}/man3/item_*.3x*
%{_mandir}/man3/link_field*.3x*
%{_mandir}/man3/menu*.3x*
%{_mandir}/man3/mitem_*.3x*
%{_mandir}/man3/move_field.3x*
%{_mandir}/man3/move_panel.3x*
%{_mandir}/man3/new_field*.3x*
%{_mandir}/man3/new_form*.3x*
%{_mandir}/man3/new_item.3x*
%{_mandir}/man3/new_menu*.3x*
%{_mandir}/man3/new_page.3x*
%{_mandir}/man3/new_panel.3x*
%{_mandir}/man3/panel*.3x*
%{_mandir}/man3/pos_form_cursor.3x*
%{_mandir}/man3/pos_menu_cursor.3x*
%{_mandir}/man3/post_form.3x*
%{_mandir}/man3/post_menu.3x*
%{_mandir}/man3/replace_panel.3x*
%{_mandir}/man3/scale_form.3x*
%{_mandir}/man3/scale_menu.3x*
%{_mandir}/man3/set_current_field.3x*
%{_mandir}/man3/set_current_item.3x*
%{_mandir}/man3/set_field*.3x*
%{_mandir}/man3/set_form_*.3x*
%{_mandir}/man3/set_item_*.3x*
%{_mandir}/man3/set_max_field.3x*
%{_mandir}/man3/set_menu_*.3x*
%{_mandir}/man3/set_new_page.3x*
%{_mandir}/man3/set_panel_userptr.3x*
%{_mandir}/man3/set_top_row.3x*
%{_mandir}/man3/show_panel.3x*
%{_mandir}/man3/top_panel.3x*
%{_mandir}/man3/top_row.3x*
%{_mandir}/man3/unpost_form.3x*
%{_mandir}/man3/unpost_menu.3x*
%{_mandir}/man3/update_panels*.3x*

%files c++-devel
%defattr(644,root,root,755)
%doc c++/{demo.cc,README-first,NEWS,PROBLEMS}
%{_includedir}/cursesapp.h
%{_includedir}/cursesf.h
%{_includedir}/cursesm.h
%{_includedir}/cursesp.h
%{_includedir}/cursesw.h
%{_includedir}/etip.h
%{_includedir}/cursslk.h
%{_pkgconfigdir}/ncurses++.pc
%{_pkgconfigdir}/ncurses++w.pc

