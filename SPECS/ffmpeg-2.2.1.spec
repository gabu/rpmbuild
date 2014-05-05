# Simple static build for ffmpeg, ffprobe with x264 and fdk-aac

%define _unpackaged_files_terminate_build 0

Summary:        Digital VCR and streaming server
Name:           ffmpeg
Version:        2.2.1
Release:        1%{?dist}
License:        GPLv2+
URL:            http://ffmpeg.org/
Source0:        http://ffmpeg.org/releases/ffmpeg-%{version}.tar.gz

%description
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.

%prep
%setup -q -n ffmpeg-%{version}
# fix -O3 -g in host_cflags
sed -i "s/-O3 -g/$RPM_OPT_FLAGS/" configure

%build
./configure \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --datadir=%{_datadir}/%{name} \
  --incdir=%{_includedir}/%{name} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --arch=%{_target_cpu} \
  --optflags="$RPM_OPT_FLAGS" \
  --enable-pthreads \
  --enable-gpl \
  --enable-nonfree \
  --enable-libfdk_aac \
  --enable-libx264 \
  --disable-shared \
  --enable-static \
  --disable-ffserver \
  --disable-ffplay \
  --extra-cflags=-I%{_includedir}/%{name} \
  --extra-ldflags=-L%{_libdir} \
  --extra-libs=-ldl \
  --disable-debug

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT V=1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}/ffmpeg
%{_bindir}/ffprobe
%{_mandir}/man1/ffmpeg*.1*
%{_mandir}/man1/ffprobe*.1*

