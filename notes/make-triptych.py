"""Create a triptych image of all three cobweb gradient spectrograms."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def make_triptych():
    labels = ['period-2', 'period-4', 'chaotic']
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=150)

    for ax, label in zip(axes, labels):
        img = plt.imread(f'./assets/cobweb-gradient-{label}-spec.png')
        ax.imshow(img)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('./assets/cobweb-gradient-triptych.png',
                facecolor='black', edgecolor='none', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved cobweb-gradient-triptych.png")

if __name__ == "__main__":
    make_triptych()
