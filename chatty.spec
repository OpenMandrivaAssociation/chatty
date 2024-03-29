%global _build_id_links none
%global __requires_exclude ^libjabber\\.so.*$
%global libcmatrix_commit 702b894675f12ecd43439b3b3eee66cc74899b82

Name: chatty
Version: 0.8.1
Release: 1
Summary: A libpurple messaging client
Group:   Networking/Instant messaging
License: GPL-3.0-or-later
URL: https://gitlab.gnome.org/World/Chatty
Source0: https://gitlab.gnome.org/World/Chatty/-/archive/v%{version}/Chatty-v%{version}.tar.bz2
Source1: https://source.puri.sm/Librem5/libcmatrix/-/archive/%{libcmatrix_commit}/libcmatrix-%{libcmatrix_commit}.tar.gz

# From Fedora
# Chatty links against a libpurple private library (libjabber).
# Obviously, Fedora build tooling doesn't support that, so we have to use
# some kind of workaround. This seemed simplest.
# We do not want to provide a private library, which is from another
# project, to be used in other packages.
Patch0:  0001-hacky-hack.patch

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  dbus-daemon
BuildRequires:  dbus-x11
BuildRequires:  itstool
BuildRequires:  pkgconfig(libebook-contacts-1.2)
BuildRequires:  pkgconfig(libebook-1.2) >= 3.42.0
BuildRequires:  pkgconfig(libfeedback-0.0)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.2
BuildRequires:  pkgconfig(gtk4) >= 4.10
BuildRequires:  pkgconfig(gio-2.0) >= 2.66
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.62
BuildRequires:  pkgconfig(purple)
BuildRequires:  pkgconfig(sqlite3) >= 3.26.0
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(folks)
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
BuildRequires:  pkgconfig(gnome-desktop-4) >= 43
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(mm-glib) >= 1.12.0
BuildRequires:  pkgconfig(gspell-1)
BuildRequires:  pkgconfig(olm)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  cmake(libphonenumber)
BuildRequires:  cmake(protobuf)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  appstream-util
BuildRequires:  desktop-file-utils
BuildRequires:  /usr/bin/xvfb-run
BuildRequires:  /usr/bin/xauth
BuildRequires:  at-spi2-core

Requires: hicolor-icon-theme

# Those packages may be dynamically loaded, but they depend on libsoup-2.4
# libsoup-2.4 and libsoup-3.0 can't exist in the same process
# Better to create a conflict, so user doesn't get a hard to debug error
Conflicts: purple-chime <= 1.4.1
Conflicts: purple-sipe <= 1.25.0

%description
Chatty is a libpurple based messaging client for mobile phones,
works best with the phosh mobile DE.

%prep
# Copy private libjabber library in so we can build against it
cp `pkg-config --variable=plugindir purple`/libjabber.so.0 /tmp/libjabber.so

%setup -a1 -n Chatty-v%{version}
%patch -P 0 -p1

rm -rf subprojects/libcmatrix
mv libcmatrix-%{libcmatrix_commit} subprojects/libcmatrix

%build
%meson
%meson_build

%install
%meson_install

# Adding libjabber to link against
mkdir -p %{buildroot}%{_libdir}
cp `pkg-config --variable=plugindir purple`/libjabber.so.0 %{buildroot}%{_libdir}

# Adding ld.so.conf.d in order to use the libjabber at runtime
mkdir -p %{buildroot}/%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/chatty" > %{buildroot}/%{_sysconfdir}/ld.so.conf.d/chatty.conf

%find_lang purism-chatty

# The mesa vulkan bug breaks tests
# https://bugzilla.redhat.com/show_bug.cgi?id=1911130

%files -f purism-chatty.lang
%{_bindir}/chatty
%{_sysconfdir}/xdg/autostart/sm.puri.Chatty-daemon.desktop
%{_datadir}/glib-2.0/schemas/sm.puri.Chatty.gschema.xml
%{_datadir}/applications/sm.puri.Chatty.desktop
%{_datadir}/icons/hicolor/*/apps/sm.puri.Chatty*.svg
%{_metainfodir}/sm.puri.Chatty.metainfo.xml
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/chatty
%{_datadir}/help/C/chatty/index.page
%{_libdir}/libjabber.so.0
%{_sysconfdir}/ld.so.conf.d/chatty.conf
%doc README.md
%license COPYING
