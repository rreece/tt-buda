import pybuda
from pybuda.verify.backend import verify_module
from pybuda import VerifyConfig
from pybuda.verify.config import TestKind

from transformers import AutoImageProcessor

import os
import requests
from PIL import Image
import pytest

import onnx


def get_sample_data(model_name):
    url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    image = Image.open(requests.get(url, stream=True).raw)

    image_processor = AutoImageProcessor.from_pretrained(model_name)
    pixel_values = image_processor(images=image, return_tensors="pt").pixel_values
    return pixel_values


variants_img_classification = [
    "nvidia/mit-b0",
    "nvidia/mit-b1",
    "nvidia/mit-b2",
    "nvidia/mit-b3",
]


@pytest.mark.parametrize("variant", variants_img_classification)
def test_segformer_imgcls_onnx_1(test_device, variant):

    # Set PyBuda configuration parameters
    compiler_cfg = pybuda.config._get_global_compiler_config()
    compiler_cfg.balancer_policy = "Ribbon"
    compiler_cfg.default_df_override = pybuda.DataFormat.Float16_b
    os.environ["PYBUDA_DISABLE_PADDING_PASS"] = "1"
    pcc_value = 0.99

    if test_device.arch == pybuda.BackendDevice.Wormhole_B0:

        if variant in [
            "nvidia/mit-b1",
            "nvidia/mit-b2",
            "nvidia/mit-b3",
        ]:
            os.environ["PYBUDA_FORCE_CONV_MULTI_OP_FRACTURE"] = "1"

        if (
            variant == "nvidia/mit-b0"
            and test_device.devtype == pybuda.BackendType.Silicon
        ):
            pcc_value = 0.97

    elif test_device.arch == pybuda.BackendDevice.Grayskull:
        if test_device.devtype == pybuda.BackendType.Silicon:
            if variant == "nvidia/mit-b1":
                pcc_value = 0.97
            elif variant == "nvidia/mit-b2":
                pcc_value = 0.96

    # Load the sample image
    pixel_values = get_sample_data(variant)

    onnx_model_path = (
        "third_party/confidential_customer_models/internal/segformer/files/onnx/imgcls/"
        + str(variant).split("/")[-1].replace("-", "_")
        + ".onnx"
    )
    model = onnx.load(onnx_model_path)
    onnx.checker.check_model(model)

    tt_model = pybuda.OnnxModule(
        str(variant).split("/")[-1].replace("-", "_"), model, onnx_model_path
    )

    # Run inference on Tenstorrent device
    verify_module(
        tt_model,
        input_shapes=[(pixel_values.shape,)],
        inputs=[(pixel_values,)],
        verify_cfg=VerifyConfig(
            arch=test_device.arch,
            devtype=test_device.devtype,
            devmode=test_device.devmode,
            test_kind=TestKind.INFERENCE,
            verify_pybuda_codegen_vs_framework=True,
            verify_tvm_compile=True,
            pcc=pcc_value,
        ),
    )
