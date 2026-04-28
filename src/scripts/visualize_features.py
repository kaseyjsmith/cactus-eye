"""
Phase 0, Step 3: Visualize intermediate feature maps of a CNN.

Hooks into layers of a pretrained YOLOv8n backbone and plots feature maps
at early, middle, and deep layers on a real camera image.

Goal: see that early layers detect edges/textures, deep layers detect
higher-level structures like vehicle shapes.

Usage:
    python -m src.scripts.visualize_features [image_path]
    python -m src.scripts.visualize_features  # uses a default image
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torchvision.transforms as T
from PIL import Image
from ultralytics import YOLO


def get_default_image() -> Path:
    images = sorted(Path("data/1209").glob("*.jpg"))
    if not images:
        raise FileNotFoundError("No images found in data/1209/")
    return images[len(images) // 2]  # pick one from the middle


def register_hooks(model_sequential, layer_indices: list[int]):
    """
    Register forward hooks on specific layers of the backbone.
    Returns a dict that gets populated with activations during forward pass.
    """
    activations = {}

    def make_hook(name):
        def hook(module, input, output):
            activations[name] = output.detach()

        return hook

    for idx in layer_indices:
        layer = model_sequential[idx]
        layer_type = layer.__class__.__name__
        name = f"layer_{idx} ({layer_type})"
        layer.register_forward_hook(make_hook(name))

    return activations


def plot_feature_maps(activations: dict, num_maps: int = 8):
    """
    For each hooked layer, plot the first `num_maps` feature maps.
    Each feature map is one channel of the layer's output — it shows
    where in the image that particular learned filter activated strongly.
    """
    num_layers = len(activations)
    fig, axes = plt.subplots(
        num_layers,
        num_maps + 1,
        figsize=(2.5 * (num_maps + 1), 3 * num_layers),
    )
    if num_layers == 1:
        axes = [axes]

    for row, (name, feat) in enumerate(activations.items()):
        # feat shape: (batch, channels, h, w)
        feat = feat.squeeze(0)  # remove batch dim → (channels, h, w)
        num_channels = feat.shape[0]
        spatial = f"{feat.shape[1]}x{feat.shape[2]}"

        # first column: mean across all channels (overall activation)
        axes[row][0].imshow(feat.mean(dim=0).cpu(), cmap="viridis")
        axes[row][0].set_title(
            f"{name}\n{num_channels}ch @ {spatial}\n(mean)", fontsize=8
        )
        axes[row][0].axis("off")

        # remaining columns: individual feature maps
        for col in range(num_maps):
            ax = axes[row][col + 1]
            if col < num_channels:
                ax.imshow(feat[col].cpu(), cmap="viridis")
                ax.set_title(f"ch {col}", fontsize=8)
            ax.axis("off")

    plt.suptitle(
        "CNN Feature Maps: Early → Deep\n"
        "Each row is a layer. Each column is one filter's activation map.\n"
        "Bright = strong activation. Notice how spatial detail decreases with depth.",
        fontsize=11,
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig("feature_maps.png", dpi=150, bbox_inches="tight")
    print("Saved to feature_maps.png")
    plt.show()


def main():
    img_path = Path(sys.argv[1]) if len(sys.argv) > 1 else get_default_image()
    print(f"Using image: {img_path}")

    # Load pretrained YOLOv8n and extract the PyTorch backbone
    yolo = YOLO("yolov8n.pt")
    backbone = yolo.model.model  # nn.Sequential of all layers

    # Print the architecture so you can see what each layer index is
    print("\n--- YOLOv8n Architecture ---")
    for idx, layer in enumerate(backbone):
        print(f"  [{idx:2d}] {layer.__class__.__name__}")
    print("---\n")

    # The backbone is layers 0-9 (before the neck/head which has Concat skip connections).
    # We'll run through these sequentially and capture outputs at key layers.
    #
    # Layer 0: Conv       — first conv (edges, gradients)
    # Layer 2: C2f        — early block (textures, simple shapes)
    # Layer 4: C2f        — middle block (parts, repeated patterns)
    # Layer 6: C2f        — deep block (object-level features)
    # Layer 9: SPPF       — Spatial Pyramid Pooling (highest-level summary)
    capture_indices = {0, 2, 4, 6, 9}
    activations = {}

    # Preprocess image the same way the model expects
    img = Image.open(img_path).convert("RGB")
    transform = T.Compose(
        [
            T.Resize((640, 640)),
            T.ToTensor(),
        ]
    )
    tensor = transform(img).unsqueeze(0)  # add batch dim

    # Forward pass through backbone only (layers 0-9), capturing activations
    x = tensor
    with torch.no_grad():
        for idx in range(10):  # layers 0 through 9
            layer = backbone[idx]
            x = layer(x)
            if idx in capture_indices:
                layer_type = layer.__class__.__name__
                name = f"layer_{idx} ({layer_type})"
                activations[name] = x.detach()

    print(f"Captured activations from {len(activations)} layers:")
    for name, feat in activations.items():
        print(f"  {name}: {feat.shape}")

    # Show original image alongside feature maps
    fig_orig, ax_orig = plt.subplots(1, 1, figsize=(6, 6))
    ax_orig.imshow(img)
    ax_orig.set_title(f"Original: {img_path.name}")
    ax_orig.axis("off")
    plt.show()

    plot_feature_maps(activations)


if __name__ == "__main__":
    main()
