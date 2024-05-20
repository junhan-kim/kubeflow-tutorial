import kfp
from kfp import dsl
from kfp.dsl import component


@component(base_image='python:3.8')
def generate_random_op(minimum: int, maximum: int) -> int:
    import random

    result = random.randint(minimum, maximum)
    print(f"Random Integer is : {result}")
    return result


@component(base_image='python:3.8')
def small_num_op(num: int):
    print(f"{num} is Small!")


@component(base_image='python:3.8')
def large_num_op(num: int):
    print(f"{num} is Large!")


@dsl.pipeline(
    name='Conditional pipeline',
    description='Small or Large'
)
def conditional_pipeline(minimum: int = 0, maximum: int = 100):
    number = generate_random_op(minimum=minimum, maximum=maximum).output

    with dsl.If(number < 30):
        small_num_op(num=number)
    with dsl.If(number >= 30):
        large_num_op(num=number)


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        conditional_pipeline,
        "./conditional_pipeline.yaml"
    )
