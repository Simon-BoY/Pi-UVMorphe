import torch
import torch.nn as nn
from models.transformer_blocks import ViT


class DeepUVModel(nn.Module):
    def __init__(self,
                 tabular_input_dim=4,
                 tabular_hidden_dims=[128, 64],
                 image_size=224,
                 patch_size=16,
                 vit_dim=768,
                 vit_depth=12,
                 vit_heads=12,
                 vit_mlp_dim=3072,
                 num_classes=2):
        super(DeepUVModel, self).__init__()

        # 1. Tabular分支：MLP
        self.tabular_mlp = self._build_mlp(tabular_input_dim, tabular_hidden_dims)
        tabular_output_dim = tabular_hidden_dims[-1] if tabular_hidden_dims else tabular_input_dim

        # 2. Image分支：ViT
        self.vit = ViT(
            image_size=image_size,
            patch_size=patch_size,
            dim=vit_dim,
            depth=vit_depth,
            heads=vit_heads,
            mlp_dim=vit_mlp_dim,
            channels=3
        )

        # 3. 融合层
        fusion_input_dim = tabular_output_dim + vit_dim
        self.fusion_layer = nn.Sequential(
            nn.Linear(fusion_input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )

    def _build_mlp(self, input_dim, hidden_dims):
        layers = []
        prev_dim = input_dim
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
            prev_dim = hidden_dim
        return nn.Sequential(*layers)

    def forward(self, tabular, image):
        tabular_features = self.tabular_mlp(tabular)
        image_features = self.vit(image)
        combined = torch.cat([tabular_features, image_features], dim=1)
        output = self.fusion_layer(combined)
        return output