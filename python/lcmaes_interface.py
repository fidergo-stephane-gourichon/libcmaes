"""usage (yet versatile):

    import lcmaes_interface as lci

    # setup input parameters
    myfun = lambda x: sum([xi**2 for xi in x])  # myfun accepts a list of numbers as input
    x0 = [2.1] * 10
    sigma0 = 0.1

    # run optimization via lci
    res = lci.lcmaes.pcmaes(lci.to_fitfunc(myfun),
                            lci.to_params(x0, sigma0,
                                str_algo=b'aipop', # b=bytes, unicode fails
                                restarts=2))
    lci.plot()  # plot from file set in lci.to_params

Details: for the time being `to_params` is based on `lcmaes.make_simple_parameters`,
but that might change in future.

"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import lcmaes
import cma_multiplt as cmaplt
fplot_current = b'lcmaes.dat'

def to_params(x0, sigma0, str_algo=b'acmaes', fplot=None, lbounds=None, ubounds=None, **kwargs):
    """return parameter object instance for `lcmaes.pcmaes`.

    Keys in `kwargs` must correspond to `name` in `set_name` attributes
    of `lcmaes.CMAParameters`, e.g. ``ftarget=1e-7``.

    Details: when `fplot is None` (default), the default output filename
    is used.
    """
    has_bounds = not lbounds==None and not ubounds == None
    p = None
    if has_bounds:
        gp = lcmaes.make_genopheno_pwqb(lbounds,ubounds,len(ubounds))
        p = lcmaes.make_parameters_pwqb(x0,sigma0,gp)
    else:
        p = lcmaes.make_simple_parameters(x0, sigma0)
    p.set_str_algo(str_algo)
    if fplot and fplot != True:  # then fplot must be filename
        global fplot_current
        fplot_current = fplot
    if fplot or fplot is None:  # 0 or False or '' or "" prevents writing
        p.set_fplot(fplot_current)
    for key, val in kwargs.items():
        setter = "set_" + key
        if not hasattr(p, setter):
            raise ValueError(setter + " is not known as method of CMAParameters")
        getattr(p, setter)(val)  # call setter with value
    return p

def pcmaes(fitfunc,p,has_bounds=False):
    if not has_bounds:
        return lcmaes.pcmaes(fitfunc,p)
    else:
        return lcmaes.pcmaes_pwqb(fitfunc,p)

def to_fitfunc(f):
    """return function for lcmaes from callable `f`, where `f` accepts a list of numbers as input."""
    return lcmaes.fitfunc_pbf.from_callable(lambda x, n: f(x))

def plot(file=None):
    cmaplt.plot(file if file else fplot_current)
