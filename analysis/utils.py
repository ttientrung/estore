import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_hist(data, column_name, title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.hist(data[column_name], bins=8)
    plt.title(title)
    plt.subplot(1, 2, 2)
    sns.histplot(data[column_name], bins=8)
    plt.title(title)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_box(data, column_name, title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.boxplot(data[column_name])
    plt.title(title)
    plt.subplot(1, 2, 2)
    sns.boxplot(data=data[column_name])
    plt.title(title)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_bar(data, x_name, y_name, title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.bar(data[x_name], data[y_name])    
    plt.xticks(rotation=45)
    plt.title(title)
    plt.subplot(1, 2, 2)
    bar2 = sns.barplot(data=data, x=x_name, y=y_name)
    bar2.set_xticklabels(bar2.get_xticklabels(), rotation=45)
    plt.title(title)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_plot(data, title, x=1, y=1):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(data)        
    plt.title(title)
    plt.subplot(2, 1, 2)
    sns.lineplot(data=data)
    plt.title(title)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_pie(x, labels, title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.pie(x, labels=labels, counterclock=False, shadow=True, autopct='%.0f%%')
    plt.title(title, fontsize=16, color = 'b')
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_scatter(data, x, y, title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.scatter(data[x], data[y])
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.subplot(1, 2, 2)
    sns.regplot(x=x, y=y, data=data)
    plt.title(title)
    plt.tight_layout()
    graph = get_graph()
    return graph



