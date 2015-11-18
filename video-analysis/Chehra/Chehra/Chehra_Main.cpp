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

#include "Chehra_Linker.h"

using namespace std;
using namespace cv;
using namespace Chehra_Tracker;

void Chehra_Plot(Mat &img,Mat &pts,Mat &eyes, bool p_flag, bool e_flag);
void Chehra_Plot_Pose(Mat img, Chehra_Linker& ChehraObj, int frate);
void Chehra_Plot_Connections(Mat &img,Mat pts);

void QueryPerformanceCounter(LARGE_INTEGER*);
void QueryPerformanceFrequency(LARGE_INTEGER*);

int main()
{
	//use webcam or video
	//0: Video
	//1: Webcam
	int webcam = 0;

	//video path
	string videofile;
	if(webcam==0)
		videofile="test/test.avi";

	//save results
	//0: No
	//1:Yes
	int savedata=0;
	string savepath;
	if(savedata==1)
		savepath="test/";

	//set other tracking parameters

	//Failure Checker Interval <integer>
	int fcheck_interval=5; //Failure checker to be executed after every 5 frames

	//Failure Checker Score Treshold [-1,1]
	float fcheck_score_treshold=-0.25;	//threshold for detecting tracking failure

	//Number of Consecutive Frames Failed To Activate Redetection
	int fcheck_fail_treshold=2;	//reinitialize after failure on 2 consecutive frames

	//models
	char regFile[256],fdFile[256];
	strcpy(regFile,"model/Chehra_t1.0.model");
	strcpy(fdFile,"model/haarcascade_frontalface_alt_tree.xml");

	//loading opencv's face detector model
	CascadeClassifier face_cascade;
	if(!face_cascade.load(fdFile))
	{
		cout<<"--(!)Error Loading Face Detector Model\n";
		return -1;
	}

	//load chehra model
	std::auto_ptr<Chehra_Tracker::Chehra_Linker> pModel(Chehra_Tracker::CreateChehraLinker(regFile));
	Chehra_Tracker::Chehra_Linker &ChehraObj = *pModel.get();

	cout << "CHEHRA Face & Eyes Tracker (Version 0.1) - Akshay Asthana (May 2014)" << endl << endl;
	cout << "####### USAGE: #######"<< endl
	<< " ->  Esc - Close"			<< endl
	<< " ->  r   - Reinitialize"	<< endl
	<< " ->  i   - Activate Incremental Tracking (Coming Soon..)" << endl
	<< " ->  e   - Toggle Eyes Points"<< endl
	<< " ->  h   - Toggle Head Pose"<< endl
	<< " ->  p   - Toggle Points/Line Visualization"<< endl
	<< "#########################"	<< endl;

	//activate camera
	CvCapture* cam;
	if(webcam==1)
		cam = cvCaptureFromCAM(0);
	else
		cam = cvCaptureFromAVI(videofile.c_str());

	if(!cam)return -1;

	string tname="CHEHRA (Version 0.1)";
	namedWindow(tname);
	int i,c;

	LARGE_INTEGER start1, end1, freq1;
	QueryPerformanceFrequency(&freq1);
	int frate1;

	string temp;char tmpp[255];
	ofstream file;
	long int file_count=0;
	Mat gimg, img;
	bool p_flag = true;	bool e_flag=true; bool h_flag=false;

	while(1)
	{
		//get frame
		IplImage* I = cvQueryFrame(cam);
		if(!I)
			break;
		img = I;

		sprintf(tmpp,"%05ld",file_count);
		string tmp(tmpp);
		if(webcam==1 && savedata==1)
		{
			temp=savepath+tmp+".jpg";

            auto imageCast = (IplImage)img;

			try{::cvSaveImage(temp.c_str(), &imageCast);}
			catch (runtime_error& ex){fprintf(stderr, "Exception converting image to JPG format: %s\n", ex.what());}
		}

		cvtColor(img,gimg,CV_BGR2GRAY);

		if(h_flag)
			QueryPerformanceCounter(&start1);

		//main tracking function
		if(ChehraObj.TrackFrame(gimg,fcheck_interval,fcheck_score_treshold,fcheck_fail_treshold,face_cascade) == 0)
		{
			if(h_flag)
			{
				QueryPerformanceCounter(&end1);
				frate1=(end1.QuadPart-start1.QuadPart)*1000/freq1.QuadPart;
			}

			Chehra_Plot(img,ChehraObj._bestFaceShape,ChehraObj._bestEyeShape, p_flag, e_flag);

			if(h_flag)
				Chehra_Plot_Pose(img,ChehraObj,frate1);

			if(savedata==1)
			{
				temp=savepath+tmp+".data";
				file.open(temp);
				file<<ChehraObj._PitchDeg<<" "<<ChehraObj._YawDeg<<" "<<ChehraObj._RollDeg<<"\n";
				for(i=1;i<6;i++)
					file<<ChehraObj._bestEyeShape.at<float>(i,0)<<" "<<ChehraObj._bestEyeShape.at<float>(i+14,0)<<" ";
				for(i = 8; i < 13; i++)
					file<<ChehraObj._bestEyeShape.at<float>(i,0)<<" "<<ChehraObj._bestEyeShape.at<float>(i+14,0)<<" ";
				file<<"\n";

				for(i=0;i<49;i++)
					file<<ChehraObj._bestFaceShape.at<float>(i,0)<<" "<<ChehraObj._bestFaceShape.at<float>(i+49,0)<<" ";
				file<<"\n";

				file.close();
			}
		}
		else
			ChehraObj.Reinitialize();

		//show results
		file_count++;
		imshow(tname,img);
		c = cvWaitKey(1);

		if(c == 27) {break;}
		else if(char(c) == 'r') {ChehraObj.Reinitialize();}
		else if(char(c) == 'e') {e_flag = !e_flag;}
		else if(char(c) == 'h') {h_flag = !h_flag;}
		else if(char(c) == 'p') {p_flag = !p_flag;}

    }

::cvReleaseCapture(&cam);
::cvDestroyAllWindows();

return 0;
}

//-----------------------------------------------------------------//
//-----------------------------------------------------------------//

/*
	Supporting Functions
*/

void Chehra_Plot(Mat &img,Mat &pts,Mat &eyes, bool p_flag, bool e_flag)
{

	int i,n=49,m=14;
	Point p1; Scalar c;

	if (p_flag == true)
	{
		c = CV_RGB(0,255,0);
		for(i = 0; i < 49; i++)
		{
			p1 = Point(pts.at<float>(i,0),pts.at<float>(i+n,0));
			circle(img,p1,1,c,-1);
		}
	}
	else
		Chehra_Plot_Connections(img,pts);

	if (e_flag == true)
	{
		c = CV_RGB(255,0,0);
		p1 = Point(0.2*(eyes.at<float>(1,0)+eyes.at<float>(2,0)+eyes.at<float>(3,0)+eyes.at<float>(4,0)+eyes.at<float>(5,0)),0.2*(eyes.at<float>(1+m,0)+eyes.at<float>(2+m,0)+eyes.at<float>(3+m,0)+eyes.at<float>(4+m,0)+eyes.at<float>(5+m,0)));
		circle(img,p1,2,c,-1);

		p1 = Point(0.2*(eyes.at<float>(8,0)+eyes.at<float>(9,0)+eyes.at<float>(10,0)+eyes.at<float>(11,0)+eyes.at<float>(12,0)),0.2*(eyes.at<float>(8+m,0)+eyes.at<float>(9+m,0)+eyes.at<float>(10+m,0)+eyes.at<float>(11+m,0)+eyes.at<float>(12+m,0)));
		circle(img,p1,2,c,-1);
	}

}


void Chehra_Plot_Pose(Mat img, Chehra_Linker& ChehraObj, int frate)
{
	CvFont font;  cvInitFont(&font, CV_FONT_HERSHEY_DUPLEX, 0.4, 0.4, 0.0, 1, CV_AA);
	char buff[50]; Scalar color(0,255,0);
	IplImage image(img);
	sprintf(buff, "%d msec", frate);
	cvPutText(&image,buff,Point(10,20),&font,color);
	sprintf(buff, "Pitch : %.1f", ChehraObj._PitchDeg);
	cvPutText(&image,buff,Point(10,40),&font,color);
	sprintf(buff, "Yaw : %.1f", ChehraObj._YawDeg);
	cvPutText(&image,buff,Point(10,60),&font,color);
	sprintf(buff, "Roll : %.1f", ChehraObj._RollDeg);
	cvPutText(&image,buff,Point(10,80),&font,color);
}


void Chehra_Plot_Connections(Mat &img,Mat pts)
{
	int i,n=49; Point p1,p2; Scalar c,d;
	c = CV_RGB(0,255,0);
	d = CV_RGB(255,0,0);

	for(i = 0; i < n; i++)
	{
		if((i!=4)&&(i!=9)&&(i!=13)&&(i!=18)&&(i!=24)&&(i!=30)&&(i!=42)&&(i!=45)&&(i!=n-1))
		{
			p1 = Point(pts.at<float>(i,0),pts.at<float>(i+n,0));
			p2 = Point(pts.at<float>(i+1,0),pts.at<float>(i+1+n,0));
			line(img,p1,p2,c,1,CV_AA);
		}
		if(i==13)
		{
			p1 = Point(pts.at<float>(13,0),pts.at<float>(13+n,0));
			p2 = Point(pts.at<float>(16,0),pts.at<float>(16+n,0));
			line(img,p1,p2,c,1,CV_AA);
		}
		if(i==19)
		{
			p1 = Point(pts.at<float>(19,0),pts.at<float>(19+n,0));
			p2 = Point(pts.at<float>(24,0),pts.at<float>(24+n,0));
			line(img,p1,p2,c,1,CV_AA);
		}
		if(i==25)
		{
			p1 = Point(pts.at<float>(25,0),pts.at<float>(25+n,0));
			p2 = Point(pts.at<float>(30,0),pts.at<float>(30+n,0));
			line(img,p1,p2,c,1,CV_AA);
		}
		if(i==31)
		{
			p1 = Point(pts.at<float>(31,0),pts.at<float>(31+n,0));
			p2 = Point(pts.at<float>(42,0),pts.at<float>(42+n,0));
			line(img,p1,p2,c,1,CV_AA);
			p1 = Point(pts.at<float>(31,0),pts.at<float>(31+n,0));
			p2 = Point(pts.at<float>(43,0),pts.at<float>(43+n,0));
			line(img,p1,p2,c,1,CV_AA);
			p1 = Point(pts.at<float>(31,0),pts.at<float>(31+n,0));
			p2 = Point(pts.at<float>(48,0),pts.at<float>(48+n,0));
			line(img,p1,p2,c,1,CV_AA);
		}
		if(i==37)
		{
			p1 = Point(pts.at<float>(37,0),pts.at<float>(37+n,0));
			p2 = Point(pts.at<float>(45,0),pts.at<float>(45+n,0));
			line(img,p1,p2,c,1,CV_AA);
			p1 = Point(pts.at<float>(37,0),pts.at<float>(37+n,0));
			p2 = Point(pts.at<float>(46,0),pts.at<float>(46+n,0));
			line(img,p1,p2,c,1,CV_AA);
		}
		p1 = Point(pts.at<float>(i,0),pts.at<float>(i+n,0));
		circle(img,p1,1,d,-1);
	}
}


void QueryPerformanceCounter(LARGE_INTEGER* i)
{
}

void QueryPerformanceFrequency(LARGE_INTEGER* i)
{
}
