import kfp.components as comp
from kfp import dsl
from kfp.dsl import Dataset, Input, Metrics, Output


@dsl.component(base_image='python:3.8')
def write_data(output_path: Output[Dataset], metrics_path: Output[Metrics]):
    with open(output_path.path, 'w') as f:
        f.write("Hello, Kubeflow!")
    with open(metrics_path.path, 'w') as f:
        f.write('{"metrics": [{"name": "example_metric", "numberValue": 0.9}]}')


@dsl.component(base_image='python:3.8')
def read_data(input_path: Input[Dataset], metrics_path: Output[Metrics]):
    with open(input_path.path, 'r') as f:
        data = f.read()
        print(f"Read data: {data}")
    with open(metrics_path.path, 'w') as f:
        f.write('{"metrics": [{"name": "example_metric", "numberValue": 0.95}]}')


@dsl.pipeline(name="metrics-passing-pipeline")
def metrics_passing_pipeline():
    write_op = write_data()
    read_op = read_data(input_path=write_op.outputs['output_path'])


if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(metrics_passing_pipeline, 'metrics_passing_pipeline.yaml')
