import os
import torch

# Kiểm tra xem có GPU hỗ trợ CUDA không
if torch.cuda.is_available():
    # In thông báo cho biết đang sử dụng GPU
    print('\n' + '\n' + 'Co su dung card do hoa')
else:
    # In thông báo cho biết không sử dụng GPU
    print('khong su dung card do hoa')

# In trạng thái của cuDNN
print(torch.backends.cudnn.enabled)

# In phiên bản của PyTorch
print('\n' + '\n' + 'phien ban torch :' + torch.__version__)

# In phiên bản của CUDA Toolkit
print('\n' + '\n' + 'phien ban cuda toolkit :')
os.system('nvcc --version')

# In phiên bản của NVIDIA System Management Interface
print('\n' + '\n' + 'phien ban card do hoa :')
os.system('nvidia-smi')

# In danh sách đầy đủ phiên bản của tất cả các thư viện và công cụ được cài đặt trên hệ thống mà PyTorch phụ thuộc vào
print('\n' + '\n' + 'phien ban day du tren thu vien :')
os.system('python -m torch.utils.collect_env  ')

# In thông báo cho biết đang sử dụng chức năng của CUDA
print('da su dung chuc nang cua card')
print(torch.zeros(1).cuda())