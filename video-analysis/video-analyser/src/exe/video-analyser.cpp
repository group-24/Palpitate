#include "opencv2/opencv.hpp"
#include <FaceTracker/Tracker.h>
#include <iostream>

void Draw(cv::Mat &image,cv::Mat &shape,cv::Mat &con,cv::Mat &tri,cv::Mat &visi)
{
  int i,n = shape.rows/2; cv::Point p1,p2; cv::Scalar c;

  //draw triangulation
  c = CV_RGB(0,0,0);
  for(i = 0; i < tri.rows; i++){
    if(visi.at<int>(tri.at<int>(i,0),0) == 0 ||
       visi.at<int>(tri.at<int>(i,1),0) == 0 ||
       visi.at<int>(tri.at<int>(i,2),0) == 0)continue;
    p1 = cv::Point(shape.at<double>(tri.at<int>(i,0),0),
		   shape.at<double>(tri.at<int>(i,0)+n,0));
    p2 = cv::Point(shape.at<double>(tri.at<int>(i,1),0),
		   shape.at<double>(tri.at<int>(i,1)+n,0));
    cv::line(image,p1,p2,c);
    p1 = cv::Point(shape.at<double>(tri.at<int>(i,0),0),
		   shape.at<double>(tri.at<int>(i,0)+n,0));
    p2 = cv::Point(shape.at<double>(tri.at<int>(i,2),0),
		   shape.at<double>(tri.at<int>(i,2)+n,0));
    cv::line(image,p1,p2,c);
    p1 = cv::Point(shape.at<double>(tri.at<int>(i,2),0),
		   shape.at<double>(tri.at<int>(i,2)+n,0));
    p2 = cv::Point(shape.at<double>(tri.at<int>(i,1),0),
		   shape.at<double>(tri.at<int>(i,1)+n,0));
    cv::line(image,p1,p2,c);
  }
  //draw connections
  c = CV_RGB(0,0,255);
  for(i = 0; i < con.cols; i++){
    if(visi.at<int>(con.at<int>(0,i),0) == 0 ||
       visi.at<int>(con.at<int>(1,i),0) == 0)continue;
    p1 = cv::Point(shape.at<double>(con.at<int>(0,i),0),
		   shape.at<double>(con.at<int>(0,i)+n,0));
    p2 = cv::Point(shape.at<double>(con.at<int>(1,i),0),
		   shape.at<double>(con.at<int>(1,i)+n,0));
    cv::line(image,p1,p2,c,1);
  }
  //draw points
  for(i = 0; i < n; i++){
    if(visi.at<int>(i,0) == 0)continue;
    p1 = cv::Point(shape.at<double>(i,0),shape.at<double>(i+n,0));
    c = CV_RGB(255,0,0); cv::circle(image,p1,2,c);
  }return;
}


int main(int argc, char** argv)
{
    using namespace cv;
    using namespace std;

    if (argc < 2) {
        cout << "No arguments specified\n";
        return -1;
    }
    cout << "getting arguments\n";

    const char* pathToVideo = argv[1];
    cout << "path: " << pathToVideo << "\n";

    VideoCapture cap(pathToVideo); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;

    //set other tracking parameters

    std::vector<int> wSize1(1); wSize1[0] = 7;
    std::vector<int> wSize2(3); wSize2[0] = 11; wSize2[1] = 9; wSize2[2] = 7;

    cout << "getting stuff\n";
    // int nIter = 5; double clamp=3,fTol=0.01;
    FACETRACKER::Tracker model("../model/face2.tracker");
    cout << "loaded model\n";
    cv::Mat tri=FACETRACKER::IO::LoadTri("../model/face.tri");
    cv::Mat con=FACETRACKER::IO::LoadCon("../model/face.con");


    Mat gray, frame, im;
    bool failed = true; // If failed previouse frame, be more lenient next time
    namedWindow("Face Tracker",1);
    cout << "starting loop\n";
    for(int i = 0; true; ++i)
    {
        // if (i % 3 != 0) {
        //     continue;
        // }

        cap >> frame;
        cvtColor(frame, gray, CV_BGR2GRAY);
        im = frame;

        std::vector<int> wSize;
        if(failed){
            wSize = wSize2;
        } else {
            wSize = wSize1;
        }

        if(model.Track(gray,wSize, 1, 5) == 0){
            failed = false;
            int idx = model._clm.GetViewIdx();
            cout << "WIN!";
            Draw(im,model._shape,con,tri,model._clm._visi[idx]);
        } else {
            failed = true;
            cout << "failed";
            model.FrameReset();
        }
        imshow("Face Tracker",im);
        if(waitKey(10) >= 0) break;
    }
    return 0;

}
