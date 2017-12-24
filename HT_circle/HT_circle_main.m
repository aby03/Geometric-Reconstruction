% im = imread('coins.png');
% e = edge(im, 'canny');
% figure;
% imshow(e);
% radii = 15:1:40;          % Range of radii for circles to look for
% h = hough(e, radii);
% npeaks = [30]; threshold = [];
% [peaks,marr] = houghpeaks(h, radii, threshold, npeaks);
% figure;
% imshow(im);
% hold on;
% for peak = peaks
%     [x, y] = circlepoints(peak(3));
%     plot(x+peak(1), y+peak(2), 'g-');
% end
% hold off
global t1;
global t2;global t3;
global img;
global thresh_val;
global nhoodxy;
global nhoodrad;
global noofpeaks;
global min_rad;
global max_rad;
global wt_r;
global e;
global t5;
wt_r = 0.5;
img = imread('coins.png');
thresh_val = 0.5;
nhoodxy = 1;
nhoodrad = 1;
noofpeaks = 10;
min_rad = 1;
max_rad = 100;

HT_circle_GUI({nhoodxy, nhoodrad, noofpeaks, min_rad, max_rad, thresh_val});