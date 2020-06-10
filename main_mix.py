import base64 #line:2
import math #line:3
import sys #line:4
from io import BytesIO #line:5
import numpy as np #line:7
from PIL import Image #line:8
import cv2 #line:9
import dlib #line:10
from flask import request ,Flask ,jsonify #line:11
app =Flask (__name__ )#line:13
detector =dlib .get_frontal_face_detector ()#line:14
predictor =dlib .shape_predictor ('./shape_predictor_68_face_landmarks.dat')#line:15
font =cv2 .FONT_HERSHEY_SIMPLEX #line:16
mask =Image .open ('pic/Mask5.png')#line:17
def drawDot (O0O0OOOO00O000O0O ,OOOO00OOOOO00O00O ):#line:19
    if len (OOOO00OOOOO00O00O )!=0 :#line:21
        for OO00OOOO0O0000OOO in range (len (OOOO00OOOOO00O00O )):#line:23
            O0O00O0O0O0O0OO00 =np .matrix ([[OO00O00O0O00000O0 .x ,OO00O00O0O00000O0 .y ]for OO00O00O0O00000O0 in predictor (O0O0OOOO00O000O0O ,OOOO00OOOOO00O00O [OO00OOOO0O0000OOO ]).parts ()])#line:25
            for O0OOO00O0OO00O000 ,OOOOO0OO0000O0O0O in enumerate (O0O00O0O0O0O0OO00 ):#line:26
                O00000000OOO0O000 =(OOOOO0OO0000O0O0O [0 ,0 ],OOOOO0OO0000O0O0O [0 ,1 ])#line:28
                cv2 .circle (O0O0OOOO00O000O0O ,O00000000OOO0O000 ,2 ,color =(139 ,0 ,0 ))#line:31
                cv2 .putText (O0O0OOOO00O000O0O ,str (O0OOO00O0OO00O000 +1 ),O00000000OOO0O000 ,font ,0.2 ,(187 ,255 ,255 ),1 ,cv2 .LINE_AA )#line:33
        cv2 .putText (O0O0OOOO00O000O0O ,"faces: "+str (len (OOOO00OOOOO00O00O )),(20 ,50 ),font ,1 ,(0 ,0 ,0 ),1 ,cv2 .LINE_AA )#line:35
    else :#line:36
        cv2 .putText (O0O0OOOO00O000O0O ,"no face",(20 ,50 ),font ,1 ,(0 ,0 ,0 ),1 ,cv2 .LINE_AA )#line:38
    return O0O0OOOO00O000O0O #line:39
def calc_angle (O0OO00000OO0OO0OO ,OOOO00O0O00OO00O0 ,OO000OO000O00O000 ,OOOOO00O0OO0000O0 ):#line:43
    O00O0000OO0O0OOO0 =abs (O0OO00000OO0OO0OO -OO000OO000O00O000 )#line:44
    OOO0O00O0OO0O0OOO =abs (OOOO00O0O00OO00O0 -OOOOO00O0OO0000O0 )#line:45
    O00OO000000OO00OO =math .sqrt (O00O0000OO0O0OOO0 *O00O0000OO0O0OOO0 +OOO0O00O0OO0O0OOO *OOO0O00O0OO0O0OOO )#line:46
    OOOOOO000O00OOOO0 =round (math .asin (OOO0O00O0OO0O0OOO /O00OO000000OO00OO )/math .pi *180 )#line:47
    return OOOOOO000O00OOOO0 #line:48
def rotate_bound (O0O00O0OOO00OOO0O ,O0OOOO00O00O000O0 ):#line:52
    (O000O0O0OOOO00OOO ,O00OOOOOOOOOOOOO0 )=O0O00O0OOO00OOO0O .shape [:2 ]#line:55
    (O0OO0O00O0000O0OO ,OO0OO000O00O0OOOO )=(O00OOOOOOOOOOOOO0 /2 ,O000O0O0OOOO00OOO /2 )#line:56
    OOOO0O00OO00OOO0O =cv2 .getRotationMatrix2D ((O0OO0O00O0000O0OO ,OO0OO000O00O0OOOO ),-O0OOOO00O00O000O0 ,1.0 )#line:59
    O0000000O0OO0OO0O =np .abs (OOOO0O00OO00OOO0O [0 ,0 ])#line:60
    O0O00O00OO0O0O0O0 =np .abs (OOOO0O00OO00OOO0O [0 ,1 ])#line:61
    OOO00OO0000OO00O0 =int ((O000O0O0OOOO00OOO *O0O00O00OO0O0O0O0 )+(O00OOOOOOOOOOOOO0 *O0000000O0OO0OO0O ))#line:64
    OO00O0OOO0OOO0OOO =int ((O000O0O0OOOO00OOO *O0000000O0OO0OO0O )+(O00OOOOOOOOOOOOO0 *O0O00O00OO0O0O0O0 ))#line:65
    OOOO0O00OO00OOO0O [0 ,2 ]+=(OOO00OO0000OO00O0 /2 )-O0OO0O00O0000O0OO #line:68
    OOOO0O00OO00OOO0O [1 ,2 ]+=(OO00O0OOO0OOO0OOO /2 )-OO0OO000O00O0OOOO #line:69
    return cv2 .warpAffine (O0O00O0OOO00OOO0O ,OOOO0O00OO00OOO0O ,(OOO00OO0000OO00O0 ,OO00O0OOO0OOO0OOO ))#line:71
def make_mask (OOO00000OO0OO0OO0 ,OOOOOO00O0O00OOOO ,O0OOOOOOO00OO0000 ):#line:74
    OOO000OO00OO00OOO =cv2 .cvtColor (OOO00000OO0OO0OO0 ,cv2 .COLOR_BGR2GRAY )#line:75
    O000000OOOO0O0O00 =detector (OOO000OO00OO00OOO ,0 )#line:76
    for O00OOO0O000000000 ,OO00O0OOOO0000000 in enumerate (O000000OOOO0O0O00 ):#line:77
        OOOOO000O00O000O0 =[]#line:78
        O000000O0O0OOO000 =[]#line:79
        O0OOO000OO0OO00O0 =OO00O0OOOO0000000 .bottom ()-OO00O0OOOO0000000 .top ()#line:81
        OOOO0OO0OO00OOOO0 =OO00O0OOOO0000000 .right ()-OO00O0OOOO0000000 .left ()#line:83
        O0000O0OO0OOOO00O =predictor (OOO000OO00OO00OOO ,OO00O0OOOO0000000 )#line:84
        for OOO0OO00000OO00OO in range (48 ,68 ):#line:86
            OOOOO000O00O000O0 .append (O0000O0OO0OOOO00O .part (OOO0OO00000OO00OO ).x )#line:87
            O000000O0O0OOO000 .append (O0000O0OO0OOOO00O .part (OOO0OO00000OO00OO ).y )#line:88
        OOOOOOO0000O0OOOO =int (max (O000000O0O0OOO000 )+O0OOO000OO0OO00O0 /3 )#line:90
        O0O00O0O00OO0OO0O =int (min (O000000O0O0OOO000 )-O0OOO000OO0OO00O0 /3 )#line:91
        OOOO0O0OO0OO0O00O =int (max (OOOOO000O00O000O0 )+OOOO0OO0OO00OOOO0 /3 )#line:92
        OO000OO00OOO00O0O =int (min (OOOOO000O00O000O0 )-OOOO0OO0OO00OOOO0 /3 )#line:93
        OOO000OO00O000OOO =((OOOO0O0OO0OO0O00O -OO000OO00OOO00O0O ),(OOOOOOO0000O0OOOO -O0O00O0O00OO0OO0O ))#line:94
        OO0O0OO0O0OOOOO00 =mask .resize (OOO000OO00O000OOO )#line:95
        OOOOOOOO00OO0OO00 =calc_angle (O0000O0OO0OOOO00O .part (48 ).x ,O0000O0OO0OOOO00O .part (48 ).y ,O0000O0OO0OOOO00O .part (54 ).x ,O0000O0OO0OOOO00O .part (54 ).y )#line:96
        if 0 !=OOOOOOOO00OO0OO00 :#line:98
            if O0000O0OO0OOOO00O .part (48 ).y <O0000O0OO0OOOO00O .part (54 ).y :#line:99
                OOOOOOOO00OO0OO00 =-OOOOOOOO00OO0OO00 #line:100
            OO0O0OO0O0OOOOO00 =OO0O0OO0O0OOOOO00 .rotate (OOOOOOOO00OO0OO00 )#line:101
        O00OOOO00OO0OO000 =Image .fromarray (OOO00000OO0OO0OO0 [:,:,::-1 ])#line:108
        O00OOOO00OO0OO000 .paste (OO0O0OO0O0OOOOO00 ,(OO000OO00OOO00O0O ,O0O00O0O00OO0OO0O ),OO0O0OO0O0OOOOO00 )#line:110
        OO0O000O0000OOO0O =BytesIO ()#line:111
        O00OOOO00OO0OO000 .save (OO0O000O0000OOO0O ,format ='PNG')#line:112
        O00000O0O0O000000 =base64 .b64encode (OO0O000O0000OOO0O .getvalue ())#line:113
        OO0O00O0O00OOOO00 =O00000O0O0O000000 .decode ()#line:114
        return jsonify ({"code":200 ,"format":"PNG","data":OO0O00O0O00OOOO00 })#line:115
    return None #line:116
@app .route ('/shape',methods =["POST"])#line:119
def shape ():#line:120
    OO0O00OOOO00O00O0 =request .files .get ('face')#line:121
    if OO0O00OOOO00O00O0 :#line:122
        O0OO0OOOOOOO0O000 =OO0O00OOOO00O00O0 .read ()#line:123
        OO0000OOO0OO00000 =cv2 .imdecode (np .frombuffer (O0OO0OOOOOOO0O000 ,np .uint8 ),cv2 .IMREAD_COLOR )#line:124
        OOO00OO0000OOOO00 =cv2 .cvtColor (OO0000OOO0OO00000 ,cv2 .COLOR_BGR2GRAY )#line:125
        O0OOO0O0OOO00O0O0 =detector (OOO00OO0000OOOO00 ,0 )#line:126
        OOOOOO0OOOO00O00O =drawDot (OO0000OOO0OO00000 ,O0OOO0O0OOO00O0O0 )#line:127
        OO0O00O000OO0OO0O =Image .fromarray (OOOOOO0OOOO00O00O [:,:,::-1 ])#line:128
        O0O000000OOOO0OO0 =BytesIO ()#line:129
        OO0O00O000OO0OO0O .save (O0O000000OOOO0OO0 ,format ='PNG')#line:130
        OOOO0OO00OOO000OO =base64 .b64encode (O0O000000OOOO0OO0 .getvalue ())#line:131
        O0OO0O0O00O0O00OO =OOOO0OO00OOO000OO .decode ()#line:132
        return jsonify (O0OO0O0O00O0O00OO )#line:133
    return jsonify ({"code":400 })#line:134
@app .route ('/make',methods =["POST"])#line:137
def make ():#line:138
    O00O000O0OOOO0000 =request .files .get ('face')#line:139
    OOOO00O0O0OO00O00 =None #line:140
    if O00O000O0OOOO0000 :#line:141
        try :#line:142
            OO0OO00OOO0OOOO0O =O00O000O0OOOO0000 .read ()#line:143
            O0OOOO000OO00OO0O =np .frombuffer (OO0OO00OOO0OOOO0O ,np .uint8 )#line:144
            OO0000O0OOOO0OOO0 =cv2 .imdecode (O0OOOO000OO00OO0O ,cv2 .IMREAD_COLOR )#line:145
            O000OO0O000O00OOO ,O00OOO00O0O00OO00 ,OOO0O000000O00OOO =OO0000O0OOOO0OOO0 .shape #line:147
            OOOO00O0O0OO00O00 =make_mask (OO0000O0OOOO0OOO0 ,O00OOO00O0O00OO00 ,O000OO0O000O00OOO )#line:148
            if None is OOOO00O0O0OO00O00 :#line:149
                for OO0OO0O0OOOO0000O in range (1 ,4 ):#line:150
                    OOO0000OO000O0O00 =cv2 .getRotationMatrix2D ((O00OOO00O0O00OO00 /2 ,O000OO0O000O00OOO /2 ),OO0OO0O0OOOO0000O *-90 ,1 )#line:153
                    O00OOOOO0OOOO0O00 =cv2 .warpAffine (OO0000O0OOOO0OOO0 ,OOO0000OO000O0O00 ,(O00OOO00O0O00OO00 ,O000OO0O000O00OOO ))#line:155
                    OOOO00O0O0OO00O00 =make_mask (O00OOOOO0OOOO0O00 ,O00OOO00O0O00OO00 ,O000OO0O000O00OOO )#line:156
                    if None is not OOOO00O0O0OO00O00 :#line:157
                        break #line:158
        except ():#line:159
            return jsonify ({"code":500 })#line:160
    if None is not OOOO00O0O0OO00O00 :#line:161
        return OOOO00O0O0OO00O00 #line:162
    else :#line:163
        return jsonify ({"code":400 })#line:164
if __name__ =='__main__':#line:167
    port =1234 #line:168
    argv =sys .argv #line:169
    if len (argv )>1 :#line:170
        port =int (argv [1 ])#line:171
    app .run (host ='0.0.0.0',port =port )#line:173
