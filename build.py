import papermill as pm
from pathlib import Path
import logging

logger = logging.getLogger()

def print_notebooks_to_build(workflow_stages):
    """
    pretty-print the list of notebooks that will be considered

    Parameters
    ----------
    workflow_stages: Dict[str, List[Path]]
        dictionary of workflow stage name mapped to list of notebooks within it. 
    """
    print("======== BUILDING: ===========")
    for directory, files in workflow_stages.items():
        print(directory, ":")
        for nb in files:
            print(" - ", nb)

def build_notebooks(stage, notebook_paths, build_dir):
    """ 
    Build a list of notebooks

    Parameters
    ----------
    stage: str
        name of stage (just for identification purposes)
    notebook_paths: List[Path]
        list of paths to notebooks
    build_dir: Path
        path to top-level of output directory
    """
    logger.info("Building Stage '%s'", stage)
    for path in notebook_paths:
        output_path = build_dir/path
        output_path.parents[0].mkdir(parents=True, exist_ok=True)
        logger.debug("Created %s", path.parents[0])
        pm.execute_notebook(
            str(path),
            str(output_path),
            #parameters = dict(alpha=0.6, ratio=0.1)
        )
    
            
if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    
    build_dir = Path("BUILD")
    build_dir.mkdir(exist_ok=True)
    logging.info("Build directory:", build_dir.resolve())
    
    dirs_to_build = ['Preparation', 'Benchmarks', 'Summaries']
    workflow_stages = {x: list(Path(f'./{x}').rglob("*.ipynb"))
                       for x in dirs_to_build}
    print_notebooks_to_build(workflow_stages)

    for stage, paths in workflow_stages.items():
        build_notebooks(stage, paths, build_dir)
