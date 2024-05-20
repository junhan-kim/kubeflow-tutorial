from kfp import dsl
from kfp.dsl import Dataset, Input, Output


@dsl.component(base_image='python:3.8')
def write_data(output_path: Output[Dataset]):
    with open(output_path.path, 'w') as f:
        f.write("Hello, Kubeflow!")


@dsl.component(base_image='python:3.8')
def read_data(input_path: Input[Dataset]):
    with open(input_path.path, 'r') as f:
        data = f.read()
        print(f"Read data: {data}")


@dsl.pipeline(name="file-passing-pipeline")
def file_passing_pipeline():
    write_op = write_data()
    read_op = read_data(input_path=write_op.outputs['output_path'])


if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(file_passing_pipeline, 'file_passing_pipeline.yaml')
