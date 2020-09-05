# Portfolio Theory - Constructing an Optimal Portfolio
##### Last Updated: 2020-01-19

As someone who wants to take charge of his own finance, I decided to work on this small project to create an optimal portfolio based on Harry Markowitz portfoliot theory.

My goal is to apply the results of this directly to my own portfolio.

### Data source
Stock price data are taken from Alpha Advantage throug the pandas.DataReader wrapper.

### Modules
retrieveDumpData.py has six functions to retrieve stock price data, calculate returns and dump the output to a pickle file. All functions are documented.

### Example

Below is a frontier for five different ETF: 'VTI', 'BAR', 'VCE.TRT', 'VGK', 'SCHH'


![Frontier](https://github.com/tdkcumberland/portfolio_theory_python/blob/master/Example.png)