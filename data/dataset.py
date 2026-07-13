import torch
from torch.utils.data import Dataset
import numpy as np
from PIL import Image
import torchvision.transforms as transforms


class MassSpecDataset(Dataset):
    def __init__(self, df, transform=None, tabular_columns=['Mass', 'Intensity', 'Charge', 'mz']):
        self.df = df.reset_index(drop=True)
        self.transform = transform
        self.tabular_columns = tabular_columns

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        tabular_features = row[self.tabular_columns].values.astype(np.float32)
        tabular_features = torch.from_numpy(tabular_features)
        image_path = row['image_path']
        return {
            'tabular': tabular_features,
            'image_path': image_path,
            'label': torch.tensor(row['label'], dtype=torch.long)
        }


class CustomDataset(Dataset):
    def __init__(self, data_list, target_size=(224, 224), transform=None):
        self.data = data_list
        self.target_size = target_size

        if transform is None:
            self.transform = transforms.Compose([
                transforms.Lambda(lambda x: x.convert('RGB')),
                transforms.Resize(target_size),
                transforms.ToTensor(),
            ])
        else:
            self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        tabular = item['tabular'].float()
        image_path = item['image_path']
        label = item['label'].long()

        try:
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image_tensor = self.transform(image)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            image_tensor = torch.zeros(4, self.target_size[0], self.target_size[1])

        return tabular, image_tensor, label