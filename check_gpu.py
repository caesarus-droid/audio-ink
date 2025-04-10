import torch

def check_cuda():
    cuda_available = torch.cuda.is_available()
    if cuda_available:
        print("CUDA GPU detected!")
        print(f"Device: {torch.cuda.get_device_name(0)}")
        return True
    else:
        print("No CUDA GPU detected. Using CPU only.")
        return False

if __name__ == "__main__":
    check_cuda() 