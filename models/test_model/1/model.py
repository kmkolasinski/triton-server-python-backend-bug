import json
from typing import List
import numpy as np
import triton_python_backend_utils as pb_utils
import sys
import logging


LOGGER = logging.getLogger("APP")
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(logging.StreamHandler(stream=sys.stdout))


class TritonPythonModel:
    def initialize(self, args):
        LOGGER.info("Initialized model")
        LOGGER.info(sys.version)
    def predict(self, request):
        tensor = pb_utils.get_input_tensor_by_name(request, "input_bytes")
        image_bytes = tensor.as_numpy()[0, 0]

        outputs_str = []
        outputs_float = []

        for i in range(min(len(image_bytes), 50000)):
            vector = np.random.rand(1000)
            some_float = float((vector * vector).sum())
            some_str = str(hash(image_bytes[i]))
            outputs_str.append(some_str)
            outputs_float.append(some_float)

        output = {"outputs_str": outputs_str, "outputs_float": outputs_float}

        output = np.array([json.dumps(output).encode()])

        LOGGER.info(f"Processed num bytes: {len(outputs_float)}")

        output = pb_utils.Tensor("output_bytes", output)
        return pb_utils.InferenceResponse(output_tensors=[output])

    def execute(self, requests):
        LOGGER.info(f"Got N requests: {len(requests)}")
        responses = []
        for request in requests:
            responses.append(self.predict(request))
        return responses
