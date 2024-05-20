from kfp import dsl
from kfp.compiler import compiler


@dsl.component
def add(value_1: int, value_2: int) -> int:
    ret = value_1 + value_2
    return ret


@dsl.component
def subtract(value_1: int, value_2: int) -> int:
    ret = value_1 - value_2
    return ret


@dsl.component
def multiply(value_1: int, value_2: int) -> int:
    ret = value_1 * value_2
    return ret


@dsl.pipeline(name="add example")
def my_pipeline(value_1: int, value_2: int):
    task_1 = add(value_1=value_1, value_2=value_2)
    task_2 = subtract(value_1=value_1, value_2=value_2)
    task_3 = multiply(value_1=task_1.output, value_2=task_2.output)


compiler.Compiler().compile(my_pipeline, 'pipeline.yaml')
