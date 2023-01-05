# Converting video to frame
Logging here so i dont forget the commands again

```
docker pull jrottenberg/ffmpeg

docker run \
    -v /home/ernestlwt/Videos:/Videos \
jrottenberg/ffmpeg \
    -i /Videos/ships.mp4 -vf fps=1/5 /Videos/out%d.jpg

```