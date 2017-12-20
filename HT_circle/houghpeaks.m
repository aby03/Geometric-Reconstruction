function peaks = houghpeaks(h, radii, threshold, npeaks)

% set threshold
if isempty(threshold)
    threshold = 0.5 * max(h(:));
end

% First approach to peak finding: local maxima
% find the maxima
maxarr = imregionalmax(h);
maxarr = maxarr & maxarr >= threshold;
% get 3d array indices from linear
peakind = find(maxarr);
[y, x, rind] = ind2sub(size(h), peakind);
peaks = [x'; y'; radii(rind)];
% get strongest peaks
if ~isempty(npeaks) && npeaks < size(peaks,2)
    [~, ind] = sort(h(peakind), 'descend');
    ind = ind(1:npeaks);
    peaks = peaks(:, ind);
end