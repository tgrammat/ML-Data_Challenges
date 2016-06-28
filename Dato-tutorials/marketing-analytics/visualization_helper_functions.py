# libraries required
import graphlab.aggregate as agg
from matplotlib import pyplot as plt
import seaborn as sns

def item_freq_plot(data_sf, item_column, hue=None, topk=None, pct_threshold=None ,reverse=False,
                    seaborn_style='whitegrid', seaborn_palette='deep', color='b', **kwargs):
    '''Function for topk item frequency plot:
    
    Parameters
    ----------
    data_sf: SFrame
        SFrame for plotting. If x and y are absent, this is interpreted as wide-form. 
        Otherwise it is expected to be long-form.
    item_column: string
        The attribute name the frequency counts of which we want to visualize
    hue: seaborn barplot name of variable in vector data, optional
        Inputs for plotting long-form data. See seaborn examples for interpretation.
    topk: int, optional
        The number of most frequent items
    pct_threshold: float in [0,100] range, optional
        Lower frequency limit below which all the grouby counted items will be ignored.
    seaborn_style: dict, None, or one of {darkgrid, whitegrid, dark, white, ticks}
        Set the aesthetic style of the plots through the seaborn module.
        A dictionary of parameters or the name of a preconfigured set.
    seaborn_palette: {deep, muted, pastel, dark, bright, colorblind}
        Change how matplotlib color shorthands are interpreted.
        Calling this will change how shorthand codes like 'b' or 'g' 
        are interpreted by matplotlib in subsequent plots.
    color: matplotlib color, optional
        Color for all of the elements, or seed for light_palette() 
        when using hue nesting in seaborn.barplot().
    kwargs : key, value mappings
        Other keyword arguments which are passed through (a)seaborn.countplot API 
        and/or (b)plt.bar at draw time.
    '''    
    # set seaborn style
    sns.set(style=seaborn_style)
    
    # compute the item counts: (1) apply groupby count operation,
    # (2) check whether a nested grouping exist or not
    if hue is not None:
        item_counts = data_sf.groupby([item_column,hue], agg.COUNT())
        hue_order = list(data_sf[hue].unique())
        hue_length = len(hue_order)
    else:
        item_counts = data_sf.groupby(item_column, agg.COUNT())
        hue_order=None
        hue_length=1
    # compute frequencies
    pcts = (item_counts['Count'] / float(item_counts['Count'].sum())) * 100
    item_counts['Percent'] = pcts
    
    # apply a percentage threshold if any
    if((pct_threshold is not None) & (pct_threshold < 100)):
        item_counts = item_counts[item_counts['Percent'] >= pct_threshold]
    elif((pct_threshold is not None) & (pct_threshold >=1)):
        print 'The frequency threshold was unacceptably high.',\
        'and have been removed from consideration.',\
        'If you want to use this flag please choose a value lower than one.'
    
    # print the number of remaining item counts
    print 'Number of Unique Items: %d' % len(item_counts)
    
    # determine the ysize per item 
    ysize_per_item = 0.5 * hue_length
    
    # apply topk/sort operations
    if((topk is not None) & (topk < len(item_counts))):
        item_counts = item_counts.topk('Percent', k=topk, reverse=reverse)
        ysize = ysize_per_item * topk
        print 'Number of Most Frequent Items, Visualized: %d' % topk
    else:
        item_counts = item_counts.sort('Percent', ascending=False)
        ysize = ysize_per_item * len(item_counts)
        print 'Number of Most Frequent Items, Visualized: %d' % len(item_counts)
           
    # transform the item_counts SFrame into a Pandas DataFrame
    item_counts_df = item_counts.to_dataframe()
    
    # initialize the matplotlib figure
    ax = plt.figure(figsize=(7, ysize))
    
    # plot the Freq Percentages of the topk Items
    ax = sns.barplot(x='Percent', y=item_column, hue=hue, data=item_counts_df, 
                     order=list(item_counts_df[item_column]), hue_order=hue_order,
                     orient='h', color='b', palette='deep')
    
    # add informative axis labels
    # make final plot adjustments
    xmax = max(item_counts['Percent'])    
    ax.set(xlim=(0, xmax),
           ylabel= item_column,
           xlabel='Most Frequent Items\n(% of total occurences)')
    if hue is not None:
        ax.legend(ncol=hue_length, loc="lower right", frameon=True)
    sns.despine(left=True, bottom=True)


def segments_countplot(data_sf, x=None, y=None, hue=None, 
                       order=None, hue_order=None, figsize_tuple= None, title=None,
                       seaborn_style='whitegrid', seaborn_palette='deep', color='b', 
                       **kwargs):
    '''Function for fancy seaborn barplot:
    
    Parameters
    ----------
    data_sf: SFrame
        SFrame for plotting. If x and y are absent, this is interpreted as wide-form.
        Otherwise it is expected to be long-form.
    x, y, hue: seaborn countplot names of variables in data or vector data, optional
        Inputs for plotting long-form data. See examples for interpretation.
    order, hue_order: seaborn countplot lists of strings, optional
        Order to plot the categorical levels in, otherwise the levels are inferred from the data objects.
    figsize_tuple: tuple of integers, optional, default: None
        width, height in inches. If not provided, defaults to rc figure.figsize.
    title: string
        Provides the countplot title.
    seaborn_style: dict, None, or one of {darkgrid, whitegrid, dark, white, ticks}
        Set the aesthetic style of the plots through the seaborn module.
        A dictionary of parameters or the name of a preconfigured set.
    seaborn_palette: {deep, muted, pastel, dark, bright, colorblind}
        Change how matplotlib color shorthands are interpreted.
        Calling this will change how shorthand codes like 'b' or 'g' 
        are interpreted by matplotlib in subsequent plots.
    color: matplotlib color, optional
        Color for all of the elements, or seed for light_palette() 
        when using hue nesting in seaborn.barplot().
    kwargs : key, value mappings
        Other keyword arguments which are passed through (a)seaborn.countplot API 
        and/or (b)plt.bar at draw time.
    '''
    # define the plotting style
    sns.set(style=seaborn_style)
    
    # initialize the matplotlib figure
    plt.figure(figsize=figsize_tuple)
    
    # transform the SFrame into a Pandas DataFrame
    data_df = data_sf.to_dataframe()

    # plot the segments counts
    ax = sns.countplot(x=x, y=y, hue=hue, data=data_df, order=order, hue_order=hue_order,
                       orient='v', palette=seaborn_palette, color=color, **kwargs)
    
    # add informative axis labels, title
    # make final plot adjustments
    plt.title(title, {'fontweight': 'bold'})
    sns.despine(left=True, bottom=True)
    plt.show()


def univariate_summary_statistics_plot(data_sf, attribs_list, nsubplots_inrow=3, subplots_wspace=0.5, 
                                       seaborn_style='whitegrid', seaborn_palette='deep', color='b',
                                       **kwargs):
    '''Function for fancy univariate summary plot:
    
    Parameters
    ----------
    data_sf: SFrame 
        SFrame of interest
    attribs_list: list of strings
        Provides the list of SFrame attributes the univariate plots of which we want to draw
    nsubplots_inrow: int
        Determines the desired number of subplots per row.
    seaborn_style: dict, None, or one of {darkgrid, whitegrid, dark, white, ticks}
        Set the aesthetic style of the plots through the seaborn module.
        A dictionary of parameters or the name of a preconfigured set.
    seaborn_palette: {deep, muted, pastel, dark, bright, colorblind}
        Change how matplotlib color shorthands are interpreted.
        Calling this will change how shorthand codes like 'b' or 'g' 
        are interpreted by matplotlib in subsequent plots.
    color: matplotlib color, optional
        Color for all of the elements, or seed for light_palette() 
        when using hue nesting in seaborn.barplot().
    '''
    import graphlab as gl
    
    # transform the SFrame into a Pandas DataFrame
    if isinstance(data_sf, gl.data_structures.sframe.SFrame):
        data_df = data_sf.to_dataframe()
    else:
        data_df = data_sf
        
    # define the plotting style
    sns.set(style=seaborn_style)
    
    # remove any offending attributes for a univariate summary statistics
    # filtering function
    def is_appropriate_attrib(attrib):
        if(data_df[attrib].dtype != 'datetime64[ns]'):
            return True
        else:
            return False
    
    # apply the filtering function
    attribs_list_before = attribs_list
    attribs_list = list(filter(is_appropriate_attrib, attribs_list))
    xattribs_list =list([attrib for\
                         attrib in attribs_list_before if(attrib not in attribs_list)])
    if(len(xattribs_list) !=0):
        print 'These attributes are not appropriate for a univariate summary statistics,',\
        'and have been removed from consideration:'
        print xattribs_list, '\n'
    
    # initialize the matplotlib figure
    nattribs = len(attribs_list)
    # compute the sublots nrows
    nrows = ((nattribs-1)/nsubplots_inrow) + 1
    # compute the subplots ncols
    if(nattribs >= nsubplots_inrow):
        ncols = nsubplots_inrow
    else:
        ncols = nattribs
    # compute the subplots ysize
    row_ysize = 9
    ysize =  nrows * row_ysize
    # set figure dimensions
    plt.rcParams['figure.figsize'] = (14, ysize)
    #fig = plt.figure(figsize=(14, ysize))
        
    # draw the relavant univariate plots for each attribute of interest
    num_plot = 1
    for attrib in attribs_list:
        if(data_df[attrib].dtype == object):
            plt.subplot(nrows, ncols, num_plot)
            sns.countplot(y=attrib, data=data_df, 
                          palette=seaborn_palette, color=color, **kwargs)
            plt.xticks(rotation=45)
            plt.ylabel(attrib, {'fontweight': 'bold'})
        elif((data_df[attrib].dtype == float) | (data_df[attrib].dtype == int)):
            plt.subplot(nrows, ncols, num_plot)
            sns.boxplot(y=attrib, data=data_df, 
                        palette=seaborn_palette, color=color, **kwargs)
            plt.ylabel(attrib, {'fontweight': 'bold'})
        num_plot +=1
    
    # final plot adjustments
    sns.despine(left=True, bottom=True)
    if subplots_wspace < 0.2:
        print 'Subplots White Space was less than default, 0.2.'
        print 'The default vaule is going to be used: \'subplots_wspace=0.2\''
        subplots_wspace =0.2
    plt.subplots_adjust(wspace=subplots_wspace)
    plt.show()
    
    # print the corresponding summary statistic
    print '\n', 'Univariate Summary Statistics:\n'
    summary = data_df[attribs_list].describe(include='all')
    print summary
    

def plot_time_series(timestamp, values, title, **kwargs):
    plt.rcParams['figure.figsize'] = 14, 7
    plt.plot_date(timestamp, values, fmt='g-', tz='utc', **kwargs)
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Dollars per Barrel')
    plt.rcParams.update({'font.size': 16})
