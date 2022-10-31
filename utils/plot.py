import math
import matplotlib.pyplot as plt

def build_grid_plot(configs):
    cols = 2 if len(configs) <= 4 else 3
    rows = math.ceil(len(configs) / cols)
    fig_dims = (rows, cols)
    fig = plt.figure(figsize=(20, rows * 5))
    fig.subplots_adjust(hspace=0.2, wspace=0.2)

    for i, config in enumerate(configs):
        if i == len(configs) - 1 and len(configs) % cols == 1 and cols % 2 == 1:
            plt.subplot2grid(fig_dims, (i // cols, cols // 2))
        else:
            plt.subplot2grid(fig_dims, (i // cols, i % cols))
        if config['type'] == 'hist':
            config['column'].hist(bins=int(math.log2(len(config['column'])) + 1))
            plt.title(config['title'])
        elif config['type'] == 'bar':
            config['column'].value_counts().plot(kind='bar', title=config['title'])
            if ('rotation' in config) and config['rotation']:
                plt.xticks(rotation=0)
        elif config['type'] == 'boxplot':
            config['df'].boxplot(column=config['columns'])
        if 'xscale' in config:
            plt.xscale(config['xscale'])
        if 'yscale' in config:
            plt.yscale(config['yscale'])
        
    plt.show()