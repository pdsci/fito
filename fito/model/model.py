from collections import defaultdict
from itertools import product

from fito import Operation
from fito.specs.base import PrimitiveField, _no_default, BaseSpecField, SpecField, Field, Spec
from sklearn.grid_search import ParameterGrid


class ModelParameter(PrimitiveField):
    def __init__(self, grid, pos=None, default=_no_default, *args, **kwargs):
        super(ModelParameter, self).__init__(pos, default, *args, **kwargs)
        self.grid = grid


class Model(Operation):
    @classmethod
    def get_primitive_param_grid(cls):
        res = {}
        for field_name, field_spec in cls.get_fields():
            if isinstance(field_spec, ModelParameter):
                res[field_name] = field_spec.grid
        return ParameterGrid(res)

    @classmethod
    def get_hyper_parameters_grid(cls):
        submodels_params = defaultdict(list)

        for field_name, field_spec in cls.get_fields():
            if not isinstance(field_spec, BaseSpecField): continue
            if field_spec.base_type is None: continue
            if not issubclass(field_spec.base_type, Model): continue

            for impl in field_spec.base_type._get_all_subclasses():
                # This check has to be done because SpecField creates subclasses
                if issubclass(impl, Field): continue

                submodels_params[field_name].extend(impl.get_hyper_parameters_grid())

        res = []

        if len(submodels_params) > 0:
            submodel_fields, submodels_params = zip(*submodels_params.iteritems())

        for model_fields_combination in cls.get_primitive_param_grid():

            if len(submodels_params) > 0:
                # If there are submodels, let's combine them
                for params in product(*submodels_params):

                    params = map(Spec.dict2spec, params)
                    model_fields_combination.update(dict(zip(submodel_fields, params)))

                    res.append(
                        cls(**model_fields_combination).to_dict()
                    )
            else:
                res.append(
                    cls(**model_fields_combination).to_dict()
                )

        return res


def ModelField(pos=None, default=_no_default, base_type=None):
    if base_type is None: raise ValueError("ModelField needs to have base_type")
    return SpecField(pos=pos, default=default, base_type=base_type)

