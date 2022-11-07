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
        elif config['type'] == 'scatter':
            columns = config['df'].columns
            x_index = config['x_index']
            y_index = config['y_index']
            centers = config['centers']
            plt.scatter(config['df'][columns[x_index]], config['df'][columns[y_index]], c=config['labels'], s=20)
            plt.scatter(centers[:, x_index], centers[:, y_index], s=100, marker='*', c='r')
            plt.xlabel(columns[x_index])
            plt.ylabel(columns[y_index])

        if 'xscale' in config:
            plt.xscale(config['xscale'])
        if 'yscale' in config:
            plt.yscale(config['yscale'])
        if 'ylim_inf' in config and 'ylim_sup' in config:
            plt.ylim(config['ylim_inf'], config['ylim_sup'])
            
        
    plt.show()