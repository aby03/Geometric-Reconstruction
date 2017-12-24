function Ifinal=canny(img,sigma)

%img is the original image 
%sigma is standard deviation(used for smoothening) 
%default values of parameter
%sigma = 1;

if (nargin < 1)
  error('No. of arguments need to be passed..');
elseif (nargin ==1)
  sigma = 1;
end
img=imread('coins.jpeg');
origImage = img;

if (ndims(img)==3)
  img =double(rgb2gray(img));
end

%%%%% SMOOTHENING %%%%%%%%%%

%CONVOLUTION WITH DERIVATIVE OF GAUSSIAN

dG=dgauss(sigma);

grady = conv2(img, dG ,'same');
gradx = conv2(img, dG','same');

% norm of gradient
gradNorm = sqrt( gradx.^2 + grady.^2 );

[a,b]=size(gradNorm);
theta=zeros([a b]);
for i=1:a
      for j=1:b
            if(gradx(i,j)==0)
               theta(i,j)=atan(grady(i,j)/0.000000000001);
            else
                theta(i,j)=atan(grady(i,j)/gradx(i,j));
            end
      end
end
theta=theta*(180/3.14);

 % Handling negative directions  
  for i=1:a
      for j=1:b
            if(theta(i,j)<0)
               theta(i,j)= theta(i,j)-90;
            theta(i,j)=abs(theta(i,j));
            end
      end
 end
  for i=1:a
      for j=1:b
          if ((0<theta(i,j))&&(theta(i,j)<22.5))||((157.5<theta(i,j))&&(theta(i,j)<=180))
                theta(i,j)=0;
          elseif (22.5<theta(i,j))&&(theta(i,j)<67.5)
                 theta(i,j)=45;
          elseif (67.5<theta(i,j))&&(theta(i,j)<112.5)  
                  theta(i,j)=90;
          elseif (112.5<theta(i,j))&&(theta(i,j)<157.5)
                  theta(i,j)=135;
          end
      end
  end    

  %Non Maximal Supression
  
 [a1 b1]= size(theta);
Imgsup=zeros([a1 b1]);
gradNorm = padarray(gradNorm, [1 1]);
 [a b]=size(theta);
for i=2:a-1
    for j=2:b-1
      
           if (theta(i,j)==135)
                 if ((gradNorm(i-1,j+1)>gradNorm(i,j))||(gradNorm(i+1,j-1)>gradNorm(i,j)))
                      gradNorm(i,j)=0;
                  end
           elseif (theta(i,j)==45)   
                  if ((gradNorm(i+1,j+1)>gradNorm(i,j))||(gradNorm(i-1,j-1)>gradNorm(i,j)))
                       gradNorm(i,j)=0;
                  end
           elseif (theta(i,j)==90)   
                  if ((gradNorm(i,j+1)>gradNorm(i,j))||(gradNorm(i,j-1)>gradNorm(i,j)))
                      gradNorm(i,j)=0;
                  end
           elseif (theta(i,j)==0)   
                  if ((gradNorm(i+1,j)>gradNorm(i,j))||(gradNorm(i-1,j)>gradNorm(i,j)))
                      gradNorm(i,j)=0;
                  end
           end
    end
end
Imgsup=gradNorm;

Ie=im2uint8(Imgsup);

% Thresholding
Tl=115;
Th=180;
[a b]=size(Ie);
It=zeros([a b]);
for i = 1  : a
    for j = 1 : b
        if (Ie(i, j) < Tl)
            It(i, j) = 0;
        elseif (Ie(i, j) >= Th)
            It(i, j) = Ie(i,j);
        %Using 8-connected components
        elseif ( Ie(i+1,j)>Th || Ie(i-1,j)>Th || Ie(i,j+1)>Th || Ie(i,j-1)>Th || Ie(i-1, j-1)>Th || Ie(i-1, j+1)>Th || Ie(i+1, j+1)>Th || Ie(i+1, j-1)>Th)
            It(i,j) = Ie(i,j);
        end;
    end;
end;
Ifinal =It;

figure;
subplot(1,2,1);imshow(origImage);title('original image');
subplot(1,2,2);(imshow(Ifinal));title('Final Image');


