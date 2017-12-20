im = imread('coins.png');
e = edge(im, 'canny');
figure;
imshow(e);
radii = 15:1:40;          % Range of radii for circles to look for
h = hough(e, radii);
npeaks = []; threshold = [];
peaks = houghpeaks(h, radii, threshold, npeaks);
figure;
imshow(im);
hold on;
for peak = peaks2
    [x, y] = circlepoints(peak(3));
    plot(x+peak(1), y+peak(2), 'g-');
end
hold off