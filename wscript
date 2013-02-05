# -*- python -*-
# automatically generated wscript

import waflib.Logs as msg

PACKAGE = {
    'name': 'PhysicsAnalysis/PATJobTransforms',
    'author': ["atlas collaboration"], 
}

def pkg_deps(ctx):
    # put your package dependencies here.
    # e.g.:
    # ctx.use_pkg('AtlasPolicy')
    ctx.use_pkg('AtlasPolicy')
    ctx.use_pkg('External/AtlasPython')
    ctx.use_pkg('Tools/PyJobTransformsCore')
    ctx.use_pkg('Reconstruction/RecJobTransforms')
    return

def configure(ctx):
    msg.debug('[configure] package name: '+PACKAGE['name'])
    return

def build(ctx):
    ctx.build_pymodule(source=['python/*.py'])
    ctx.install_joboptions(source=['share/*.py'])
    ctx.install_scripts(source=['scripts/*_trf.py'])

    #FIXME: implement ctx.declare_alias(dst='Reco_trf', src='Reco_trf.py')
    #FIXME: implement makeTrfSignature
    #FIXME: implement install_pickle_dependencies
    return
