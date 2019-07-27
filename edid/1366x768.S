/* "1366x768"     76.42   1366 1434 1479 1592    768  772  779  800 -hsync -vsync */

/* EDID */
#define VERSION 1
#define REVISION 3

/* Display */
#define CLOCK 76420 /* kHz */
#define XPIX 1366
#define YPIX 768
#define XY_RATIO XY_RATIO_16_9
#define XBLANK 226
#define YBLANK  32
#define XOFFSET 68
#define XPULSE 45
#define YOFFSET 4 /* 4 */
#define YPULSE  7 /* 7 */
#define DPI 96
#define VFREQ 60 /* Hz */
#define TIMING_NAME "Linux WXGA"
#define HSYNC_POL 0
#define VSYNC_POL 0
#define CRC 0x5f

#include "edid.S"