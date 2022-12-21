Name:           llvm-bolt
Version:        0
Release:        1.20211016.gitb72f753
Summary:        BOLT is a post-link optimizer developed to speed up large applications
License:        Apache 2.0
URL:            https://github.com/facebookincubator/BOLT
Source0:        %{name}-%{version}.tar.xz

BuildRequires:  gcc gcc-c++ cmake ninja-build libstdc++-static chrpath ncurses-devel zlib-devel
Requires:	glibc zlib ncurses-libs libstdc++ libgcc

%description
BOLT is a post-link optimizer developed to speed up large applications.
It achieves the improvements by optimizing application's code layout based
on execution profile gathered by sampling profiler, such as Linux perf tool.

%prep
%setup -q
mkdir -p _build
cd _build
%{__cmake} -G Ninja ../llvm -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLLVM_ENABLE_ASSERTIONS=ON \
    -DLLVM_ENABLE_PROJECTS="clang;lld;bolt" -DCMAKE_INSTALL_PREFIX=%{_usr} \
    -DLLVM_PARALLEL_LINK_JOBS=1 \
%ifarch %ix86 x86_64
    -DLLVM_TARGETS_TO_BUILD="X86"
%endif
%ifarch aarch64
    -DLLVM_TARGETS_TO_BUILD="AArch64"
%endif

%build
cd _build
%{ninja_build}

%install
%{ninja_install} -C _build
%global _bolt_install_dir %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/usr
# remove extera llvm files.
find %{_bolt_install_dir} ! -name "llvm-bolt" ! -name "merge-fdata" ! -name "perf2bolt" -type f,l -exec rm -f '{}' \;
# remove static libs.
rm -rf %{_buildrootdir}/root
# remove rpath
chrpath -d %{_bolt_install_dir}/bin/llvm-bolt
chrpath -d %{_bolt_install_dir}/bin/merge-fdata

%files
%license bolt/LICENSE.TXT
%doc bolt/docs/*
%exclude %{_includedir}/*
%exclude %{_datadir}/*
%exclude %{_builddir}/%{name}-%{version}/_build/*
%attr(0755,root,root) %{_bindir}/llvm-bolt
%attr(0755,root,root) %{_bindir}/merge-fdata
%attr(-,root,root) %{_bindir}/perf2bolt

%changelog
* Mon Dec 19 2022 liyancheng <412998149@qq.com> 0-1.20211016.gitb72f753
- Type:fix
- ID:NA
- SUG:NA
- DESC: Add debuginfo package and delete rpath in binary

* Mon Nov 29 2021 liyancheng <412998149@qq.com>
- Type:Init
- ID:NA
- SUG:NA
- DESC:Init llvm-bolt repository
