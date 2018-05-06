# axn-cam
Poor man's action camera using Raspberry Pi Zero

## Installation

1. Create directory:`sudo mkdir /opt/axn_cam`
1. Copy `start.py`: `cp start.py /opt/axn_cam/start`
1. Make it executable: `sudo chmod 755 /opt/axn_cam/startup`
1. Copy the index file to the same directory: `cp index /opt/axn_cam/`
1. Create the log file: `sudo touch /var/log/axn_cam.log`
1. Copy the startup script `axn_cam_startup` to `/etc/init.d/`
1. Make it executable: `sudo chmod 755 /etc/init.d/axn_cam_startup`
1. Test starting the program: `sudo /etc/init.d/axn_cam_startup start`
1. Test stopping the program `sudo /etc/init.d/axn_cam_startup stop`
1. Register script to be run at start-up `sudo update-rc.d axn_cam_startup defaults`
1. If you ever want to remove the script from start-up, run: `sudo update-rc.d -f  axn_cam_startup remove`

## Troubleshooting
1. Access issues can be resolved by adding write permissions to the index file, log file and the `/opt/axn_cam` directory
1. Make sure `/opt/axn_cam/start` and `/etc/init.d/axn_cam_startup` are executable
1. The camera is known to 'freeze' while recording. The status LED stays on and doesn't respond to the toggle switch. I have a hunch that this is due to overheating (I could be wrong). I don't know of a workaround yet (except for restarting the Pi)
