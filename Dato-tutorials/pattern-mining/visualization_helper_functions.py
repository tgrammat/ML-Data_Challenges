def item_freq_plot(data_sf, item_column, ndigits=3, topk=10, style=None, palette='deep', color='b'):
    '''Function for topk item frequency plot:
    
    Parameters
    ----------
    data_sf : SFrame 
        SFrame of interest
    item_column: string
        The frequency counts of which want to visualize
    ndigits: int, optional
        The number of decimal points to keep for the item frequencies
    topk: int, optional
        The number of most frequent items
    style: : dict, None, or one of {darkgrid, whitegrid, dark, white, ticks}
        Set the aesthetic style of the plots through the seaborn module.
        A dictionary of parameters or the name of a preconfigured set.
    palette : {deep, muted, pastel, dark, bright, colorblind}
        Change how matplotlib color shorthands are interpreted.
        Calling this will change how shorthand codes like 'b' or 'g' 
        are interpreted by matplotlib in subsequent plots.
    color : matplotlib color, optional
        Color for all of the elements, or seed for light_palette() 
        when using hue nesting in seaborn.barplot().
    '''
    
    import graphlab.aggregate as agg
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style=style)
    
    # compute the item frequencies
    item_counts = data_sf.groupby(item_column, agg.COUNT())
    print 'Number of Unique Items: %d' % len(item_counts)
    pcts = (item_counts['Count'] / item_counts['Count'].sum()) * 100
    pcts = pcts.apply(lambda x: round(x,ndigits))
    item_counts['Percent'] = pcts
    item_counts = item_counts.topk('Count', k=topk)
    item_counts = item_counts.to_dataframe()
    print 'Number of Most Frequent Items, Visualized: %d' % topk
    
    # initialize the matplotlib figure
    ylength_per_item = 0.5
    
    if topk < len(item_counts):
        ysize = ylength_per_item * topk
    else:
        ysize = ylength_per_item * len(item_counts)
        
    ax = plt.figure(figsize=(8, ysize))
    
    # plot the Freq Counts of the topk Items
    sns.set_color_codes(palette)
    ax = sns.barplot(x='Percent', y='Item', data=item_counts,
                     label="Item Frequency", color=color)
    
    # add informative axis labels
    xmax = max(item_counts['Percent'])
    ax.set(xlim=(0, xmax), 
           ylabel='Items',
           xlabel='Most Frequent Items')
    
    sns.despine(left=True, bottom=True)
    
    
def seaborn_barplot(data_sf, ref_column, item_column, style=None, palette='deep', color='b'):
    '''Function for fancy seaborn barplot:
    
    Parameters
    ----------
    data_sf : SFrame 
        SFrame of interest
    ref_column: string
        The reference categorical variable across the values of which
        we want to draw the barplot.
    item_column: string
        The counts we want to visualize
    style: : dict, None, or one of {darkgrid, whitegrid, dark, white, ticks}
        Set the aesthetic style of the plots through the seaborn module.
        A dictionary of parameters or the name of a preconfigured set.
    palette : {deep, muted, pastel, dark, bright, colorblind}
        Change how matplotlib color shorthands are interpreted.
        Calling this will change how shorthand codes like 'b' or 'g' 
        are interpreted by matplotlib in subsequent plots.
    color : matplotlib color, optional
        Color for all of the elements, or seed for light_palette() 
        when using hue nesting in seaborn.barplot().
    '''
    
    import graphlab.aggregate as agg
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style=style)
    
    # transform SFrame to Pandas DataFrame
    data_df = data_sf.to_dataframe()
    
    # initialize the matplotlib figure
    xlength_per_item = 3
    segments = len(data_df[ref_column].unique())
    xsize = xlength_per_item * segments
    ax = plt.figure(figsize=(xsize, 7))
    
    # plot the item_column counts
    sns.set_color_codes(palette)
    ax = sns.barplot(x=ref_column, y=item_column, data=data_df,
                     label='Counts', color=color)
    
    # add informative axis labels
    #xmax = max(item_counts['Percent'])
    ax.set(ylabel=item_column,
           xlabel=ref_column)
    
    sns.despine(left=True, bottom=True)
    