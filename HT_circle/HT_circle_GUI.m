function varargout = HT_circle_GUI(varargin)
%HT_CIRCLE_GUI M-file for HT_circle_GUI.fig
%      HT_CIRCLE_GUI, by itself, creates a new HT_CIRCLE_GUI or raises the existing
%      singleton*.
%
%      H = HT_CIRCLE_GUI returns the handle to a new HT_CIRCLE_GUI or the handle to
%      the existing singleton*.
%
%      HT_CIRCLE_GUI('Property','Value',...) creates a new HT_CIRCLE_GUI using the
%      given property value pairs. Unrecognized properties are passed via
%      varargin to HT_circle_GUI_OpeningFcn.  This calling syntax produces a
%      warning when there is an existing singleton*.
%
%      HT_CIRCLE_GUI('CALLBACK') and HT_CIRCLE_GUI('CALLBACK',hObject,...) call the
%      local function named CALLBACK in HT_CIRCLE_GUI.M with the given input
%      arguments.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help HT_circle_GUI

% Last Modified by GUIDE v2.5 24-Dec-2017 20:53:44

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @HT_circle_GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @HT_circle_GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [], ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
   gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before HT_circle_GUI is made visible.
function HT_circle_GUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   unrecognized PropertyName/PropertyValue pairs from the
%            command line (see VARARGIN)

% Choose default command line output for HT_circle_GUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes HT_circle_GUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = HT_circle_GUI_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function nborxy_Callback(hObject, eventdata, handles)
% hObject    handle to nborxy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of nborxy as text
%        str2double(get(hObject,'String')) returns contents of nborxy as a double
global nhoodxy;
nhoodxy = str2num(get(hObject, 'String'));

% --- Executes during object creation, after setting all properties.
function nborxy_CreateFcn(hObject, eventdata, handles)
% hObject    handle to nborxy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
global nhoodxy;
set(hObject,'String',nhoodxy);



function nborrad_Callback(hObject, eventdata, handles)
% hObject    handle to nborrad (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of nborrad as text
%        str2double(get(hObject,'String')) returns contents of nborrad as a double
global nhoodrad;
nhoodrad = str2num(get(hObject, 'String'));


% --- Executes during object creation, after setting all properties.
function nborrad_CreateFcn(hObject, eventdata, handles)
% hObject    handle to nborrad (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
global nhoodrad;
set(hObject,'String',nhoodrad);



function threshold_Callback(hObject, eventdata, handles)
% hObject    handle to threshold (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of threshold as text
%        str2double(get(hObject,'String')) returns contents of threshold as a double
global thresh_val;
thresh_val = str2num(get(hObject, 'String'));


% --- Executes during object creation, after setting all properties.
function threshold_CreateFcn(hObject, eventdata, handles)
% hObject    handle to threshold (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
global thresh_val;
set(hObject,'String',thresh_val);



function npeaks_Callback(hObject, eventdata, handles)
% hObject    handle to npeaks (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of npeaks as text
%        str2double(get(hObject,'String')) returns contents of npeaks as a double
global noofpeaks;
noofpeaks = str2num(get(hObject, 'String'));


% --- Executes during object creation, after setting all properties.
function npeaks_CreateFcn(hObject, eventdata, handles)
% hObject    handle to npeaks (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
global noofpeaks;
set(hObject,'String',noofpeaks);


% --- Executes on button press in houghtrans.
function houghtrans_Callback(hObject, eventdata, handles)
% hObject    handle to houghtrans (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global img;global min_rad; global max_rad;
global wt_r;
global thresh_val;
global nhoodxy;
global nhoodrad;
global noofpeaks;
global e;
if size(img,3)==3
    imggray = rgb2gray(img);
else
    imggray = img;
end
e = edge(imggray, 'canny');
radii = min_rad:1:max_rad;          % Range of radii for circles to look for
h = hough(e, radii, wt_r);
peaks = houghpeaks(h, radii, thresh_val, nhoodxy, nhoodrad, noofpeaks);
imshow(img, 'Parent', handles.axes1);
hold on;
for peak = peaks
    [x, y] = circlepoints(peak(3));
    plot(x+peak(1), y+peak(2), 'g-','linewidth',3);
end
hold off
msgbox('Done...');

% --- Executes on button press in loadimage.
function loadimage_Callback(hObject, eventdata, handles)
% hObject    handle to loadimage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[a b] = uigetfile('*.*','All Files');
global img;
img = imread([b a]);
imshow(img,'Parent',handles.axes1);

function minrad_Callback(hObject, eventdata, handles)
% hObject    handle to minrad (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of minrad as text
%        str2double(get(hObject,'String')) returns contents of minrad as a double
global min_rad;
min_rad = str2num(get(hObject, 'String'));


% --- Executes during object creation, after setting all properties.
function minrad_CreateFcn(hObject, eventdata, handles)
% hObject    handle to minrad (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
global min_rad;
set(hObject,'String',min_rad);



function maxrad_Callback(hObject, eventdata, handles)
% hObject    handle to maxrad (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of maxrad as text
%        str2double(get(hObject,'String')) returns contents of maxrad as a double
global max_rad;
max_rad = str2num(get(hObject, 'String'));


% --- Executes during object creation, after setting all properties.
function maxrad_CreateFcn(hObject, eventdata, handles)
% hObject    handle to maxrad (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
global max_rad;
set(hObject,'String',max_rad);
