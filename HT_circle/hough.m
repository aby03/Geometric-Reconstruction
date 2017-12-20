function [h, margin] = hough(b, rrange)
[featR, featC] = find(b);           % indices of points in detected edges
[nr, nc] = size(b);                 % size of image
nradii = length(rrange);            % no of radii
margin = ceil(max(rrange));         % max radius
nrh = nr + 2*margin;                % increase size of accumulator
nch = nc + 2*margin;

h = zeros(nrh*nch*nradii, 1, 'uint32');

tempR = []; tempC = []; tempRad = [];
for i = 1:nradii
    [tR, tC] = circlepoints(rrange(i));
    tempR = [tempR tR]; 
    tempC = [tempC tC];
    tempRad = [tempRad repmat(i, 1, length(tR))];
end

% index is rows->columns->radius
tempInd = uint32( tempR+margin + nrh*(tempC+margin-1) + nrh*nch*(tempRad-1) );
featInd = uint32( featR' + nrh*(featC-1)' );

% Loop over features
for f = featInd
    % shift template to be centred on this feature
    incI = tempInd + f;
    % and update the accumulator
    h(incI) = h(incI) + 1;
end

% Reshape h, convert to double, and apply options
h = reshape(double(h), nrh, nch, nradii);
% Bring to original size without margin
h = h(1+margin:end-margin, 1+margin:end-margin, :);
end