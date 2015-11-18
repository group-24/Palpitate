/*===========================================================
//// Copyright (C) 2014, Akshay Asthana, all rights reserved.
//// * Do not redistribute without permission.
//// * Strictly for academic and non-commerial purpose only.
//// * Use at your own risk.
////
//// Please cite the follwing paper if you use this code:
//// *	Incremental Face Alignment in the Wild.
////	A. Asthana, S. Zafeiriou, S. Cheng and M. Pantic.
////	In Proc. of IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2014), June 2014.
////
//// Contact:
//// akshay.asthana@gmail.com
////
//// Version:
//// Chehra 0.1 (29 May 2014)
===========================================================*/

#ifndef __Chehra_Linker_h_
#define __Chehra_Linker_h_

#include <iostream>
#include <fstream>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"
// #include <windows.h>
#include "eigen/Eigen/Eigen"
#include "opencv2/core/eigen.hpp"
#include <stdint.h>

using namespace cv;

typedef uint8_t BYTE;
typedef uint32_t DWORD;
typedef int32_t LONG;
typedef int64_t LONGLONG;

typedef union _LARGE_INTEGER {
    struct {
        DWORD LowPart;
        LONG  HighPart;
    };
    struct {
        DWORD LowPart;
        LONG  HighPart;
    } u;
    LONGLONG QuadPart;
} LARGE_INTEGER, *PLARGE_INTEGER;

namespace Chehra_Tracker
{
  class Chehra_Linker{

  public:

	Mat     _bestFaceShape;	//Current Face Shape
	Mat     _bestEyeShape;	//Current Eye Shape
    float	_PitchDeg;		//Pose Pitch in degrees
	float	_YawDeg;		//Pose Yaw in degrees
	float	_RollDeg;		//Pose Roll in degrees

	virtual int TrackFrame(Mat im, int fcheck_interval, float fcheck_treshold, int fcheck_fail_treshold, CascadeClassifier face_cascade) = 0;
	virtual void Reinitialize(void) = 0;
  };

  Chehra_Linker * CreateChehraLinker(const char* reg_fname);
}

#endif
