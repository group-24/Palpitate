git clone https://github.com/FFmpeg/FFmpeg.git &&
cd FFmpeg &&
./configure --enable-nonfree --enable-gpl --enable-libx264 --enable-x11grab --enable-zlib &&
make  &&
make install
