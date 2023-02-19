import glob
import argparse
import cv2
import os
import numpy as np
import _init_paths
import models
import torch
import torch.nn.functional as F
from PIL import Image

mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

color_map = [(255,255,255),
             (244, 35,232),
             ( 70, 70, 70),
             (102,102,156),
             (190,153,153),
             (153,153,153),
             (250,170, 30),
             (220,220,  0),
             (107,142, 35),
             (152,251,152),
             ( 70,130,180),
             (220, 20, 60),
             (255,  0,  0),
             (  0,  0,142),
             (  0,  0, 70),
             (  0, 60,100),
             (  0, 80,100),
             (  0,  0,230),
             (119, 11, 32)]

def parse_args():
    parser = argparse.ArgumentParser(description='Custom Input')
    
    parser.add_argument('--a', help='pidnet-s, pidnet-m or pidnet-l', default='pidnet-s', type=str)
    parser.add_argument('--c', help='cityscapes pretrained or not', type=bool, default=True)
    #parser.add_argument('--p', help='dir for pretrained model', default='./pretrained_models/cityscapes/PIDNet_S_Cityscapes_test.pt', type=str)
    parser.add_argument('--p', help='dir for pretrained model', default='C:/Users/Dun/Desktop/nghiencuctrenleb/PID_Net/pretrained_models/cityscapes/PIDNet_S_Cityscapes_test.pt', type=str)
    #parser.add_argument('--r', help='root or dir for input images', default='./data/', type=str)
    parser.add_argument('--r', help='root or dir for input images', default='C:/Users/Dun/Desktop/nghiencuctrenleb/PID_Net/data/', type=str)
    parser.add_argument('--t', help='the format of input images (.jpg, .png, ...)', default='.jpg', type=str)

    args = parser.parse_args()

    return args

def input_transform(image):
    image = image.astype(np.float32)[:, :, ::-1]
    image = image / 255.0
    image -= mean
    image /= std
    return image

def load_pretrained(model, pretrained):
    pretrained_dict = torch.load(pretrained, map_location=lambda storage, loc: storage)
    if 'state_dict' in pretrained_dict:
        pretrained_dict = pretrained_dict['state_dict']
    model_dict = model.state_dict()
    pretrained_dict = {k[6:]: v for k, v in pretrained_dict.items() if (k[6:] in model_dict and v.shape == model_dict[k[6:]].shape)}
    msg = 'Loaded {} parameters!'.format(len(pretrained_dict))
    print('Attention!!!')
    print(msg)
    print('Over!!!')
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict, strict = False)
    return model

if __name__ == '__main__':
    args = parse_args()
    images_list = glob.glob(args.r+'/inputs/*'+args.t)
    sv_path = args.r+'outputs/'
    
    model = models.pidnet.get_pred_model(args.a, 19 if args.c else 11)
    model = load_pretrained(model, args.p).cuda()
    model.eval()
    with torch.no_grad():
        for img_path in images_list:
            img_name = img_path.split("\\")[-1]
            img = cv2.imread(os.path.join(args.r+'/inputs/', img_name),
                               cv2.IMREAD_COLOR)
            sv_img = np.zeros_like(img).astype(np.uint8)
            img = input_transform(img)
            img = img.transpose((2, 0, 1)).copy()
            img = torch.from_numpy(img).unsqueeze(0).cuda()
            pred = model(img)
            pred = F.interpolate(pred, size=img.size()[-2:], 
                                 mode='bilinear', align_corners=True)
            pred = torch.argmax(pred, dim=1).squeeze(0).cpu().numpy()

            for j in range(3):
                sv_img[:, :, j][pred == 0] = color_map[0][j]

            if not os.path.exists(sv_path):
                os.mkdir(sv_path)
            cv2.imwrite(sv_path+img_name, sv_img)