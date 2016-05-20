%define		subver	2016-03-10
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		oauth
%define		php_min_version 5.3.0
%include	/usr/lib/rpm/macros.php
Summary:	Generic oAuth plugin to login via various services
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/cosmocode/dokuwiki-plugin-oauth/archive/master/%{plugin}-%{subver}.tar.gz
# Source0-md5:	0d744b1c3d46542d6f2bcbd97f620b20
URL:		https://www.dokuwiki.org/plugin:oauth
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	dokuwiki >= 20140929
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(pcre)
Requires:	php(session)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
Allow users to login through various oAuth1 and oAuth2 compatible
authentication providers.

%prep
%setup -qc
mv *-%{plugin}-*/{.??*,*} .
rm .travis.yml

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/README
%{__rm} -r $RPM_BUILD_ROOT%{plugindir}/_test

# use system pkg
%{__rm} -r $RPM_BUILD_ROOT%{plugindir}/phpoauthlib

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%dir %{plugindir}
%{plugindir}/*.less
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/classes
%{plugindir}/conf
%{plugindir}/images
