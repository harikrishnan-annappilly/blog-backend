import functools
from model.base import BaseModel


def get_one_or_404(Model: BaseModel, **kwargs):
    def inner_func(func):
        @functools.wraps(func)
        def validate_and_return(*args):
            model = Model.find_one(**kwargs)
            if model is None:
                return {'message': 'object not found', 'model': Model.__name__, 'data': kwargs}, 404
            args += (model,)
            return func(*args)

        return validate_and_return

    return inner_func
