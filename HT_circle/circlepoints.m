function [x, y] = circlepoints(r)
x = [];
y = [];
for rad = r
    [xp, yp] = circlepoints1(rad);
    x = [x xp];
    y = [y yp];
end

end
    
function [x, y] = circlepoints1(r)    
% Get number of rows needed to cover 1/8 of the circle
m = round(r/sqrt(2));
if round(sqrt(r.^2 - m.^2)) < m   % if crosses diagonal
    m = m-1;
end
% generate coords for 1/8 of the circme, a dot on each row
x0 = 0:m;
y0 = round(sqrt(r.^2 - x0.^2));
% Check for overlap
if y0(end) == m
    m2 = m;
else
    m2 = m+1;
end
% assemble first quadrant
x = [x0 y0(m2:-1:2)]; 
y = [y0 x0(m2:-1:2)];
% add next quadrant
x0 = [x y];
y0 = [y -x];
% assemble full circle
x = [x0 -x0];
y = [y0 -y0];
end