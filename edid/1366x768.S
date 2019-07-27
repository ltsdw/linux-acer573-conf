/*
   1024x768.S: EDID data set for standard 1024x768 60 Hz monitor

   Copyright (C) 2011 Carsten Emde <C.Emde@osadl.org>

   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License
   as published by the Free Software Foundation; either version 2
   of the License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.
*/

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
#define No ESTABLISHED_TIMING3_BITS 0x00 */
#define HSYNC_POL 0
#define VSYNC_POL 0
#define CRC 0x5f

#include "edid.S"