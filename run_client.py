from dataclasses import dataclass
import json
from tqdm import tqdm
import numpy as np
import tritonclient.grpc as triton_server


@dataclass(frozen=True)
class TritonClient:
    url: str = "localhost:8001"
    model_name: str = "test_model"

    @property
    def triton_client(self) -> triton_server.InferenceServerClient:
        return triton_server.InferenceServerClient(url=self.url, verbose=False)

    def predict(self, image: bytes):
        input_image = triton_server.InferInput("input_bytes", [1, 1], "BYTES")
        input_image.set_data_from_numpy(np.array([[image]]))

        results = self.triton_client.infer(
            model_name=self.model_name,
            model_version="1",
            inputs=[input_image],
        )

        return json.loads(results.as_numpy("output_bytes")[0].decode())


if __name__ == "__main__":
    client = TritonClient()

    print("FIRST RUN:", client.predict(b"Initial Run Check"))

    for num_bytes in tqdm([1000, 10000, 100000, 1000000, 5000000]):
        for path in tqdm(range(10), desc=f"N={num_bytes:>10}"):
            some_bytes = b"a" * num_bytes
            client = TritonClient()
            client.predict(some_bytes)
