import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data - 过滤掉前2.5%和后2.5%的异常值
# 假设CSV文件的列名是 'value'，如果不是，可能需要调整
column_name = df.columns[0]  # 获取第一列的名称
df = df[
    (df[column_name] >= df[column_name].quantile(0.025)) & 
    (df[column_name] <= df[column_name].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(14, 6))
    column_name = df.columns[0]  # 获取数据列名
    ax.plot(df.index, df[column_name], color='red', linewidth=1)
    
    # 设置标题和轴标签
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # 优化布局
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    column_name = df.columns[0]  # 获取数据列名
    
    # 添加年份和月份列
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    # 计算每年每月的平均页面浏览量
    df_bar = df_bar.groupby(['year', 'month'])[column_name].mean().unstack()
    
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 创建条形图
    df_bar.plot(kind='bar', ax=ax, figsize=(12, 8))
    
    # 设置标题和轴标签
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('')
    
    # 设置图例
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    ax.legend(month_names, title='Months')
    
    # 设置x轴标签为年份
    ax.set_xticklabels([str(year) for year in df_bar.index], rotation=0)
    
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # 获取数据列名
    column_name = [col for col in df_box.columns if col not in ['date', 'year', 'month']][0]

    # 临时解决numpy兼容性问题
    original_float = getattr(np, 'float', None)
    if not hasattr(np, 'float'):
        np.float = float
    
    try:
        # Draw box plots (using Seaborn with numpy fix)
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Year-wise Box Plot (Trend)
        sns.boxplot(data=df_box, x='year', y=column_name, ax=axes[0])
        axes[0].set_title('Year-wise Box Plot (Trend)')
        axes[0].set_xlabel('Year')
        axes[0].set_ylabel('Page Views')
        
        # Month-wise Box Plot (Seasonality)
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        sns.boxplot(data=df_box, x='month', y=column_name, ax=axes[1], order=month_order)
        axes[1].set_title('Month-wise Box Plot (Seasonality)')
        axes[1].set_xlabel('Month')
        axes[1].set_ylabel('Page Views')
        
        plt.tight_layout()
        
    finally:
        # 恢复原始状态
        if original_float is None and hasattr(np, 'float'):
            delattr(np, 'float')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig