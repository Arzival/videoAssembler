#!/usr/bin/env sh
# Medios sintéticos para probar el editor y el render sin material propio (solo necesita ffmpeg).
#   sh ejemplo/generar.sh  →  ejemplo/medios/{toma1.mp4, toma2.mp4, voz.wav, musica.m4a}
set -e
cd "$(dirname "$0")"
mkdir -p medios
ff() { ffmpeg -nostdin -v error -y "$@"; }
# dos «tomas» verticales de 6 s a 60 fps (patrón de prueba y barras de color)
ff -f lavfi -i testsrc2=size=1080x1920:rate=60 -t 6 -c:v libx264 -pix_fmt yuv420p medios/toma1.mp4
ff -f lavfi -i smptehdbars=size=1080x1920:rate=60 -t 6 -c:v libx264 -pix_fmt yuv420p medios/toma2.mp4
# «voz»: 9 s de tonos con silencios (para probar cortes); «música»: un acorde suave de 20 s
ff -f lavfi -i "sine=frequency=330:duration=9,volume='if(lt(mod(t,3),2),1,0)':eval=frame" -ar 44100 medios/voz.wav
ff -f lavfi -i "sine=frequency=220:duration=20" -f lavfi -i "sine=frequency=277:duration=20" \
   -filter_complex "amix=inputs=2,volume=0.5" -c:a aac medios/musica.m4a
echo "listo: $(ls medios | tr '\n' ' ')"
