import checkbin
import tempfile
import requests
import torch
import os
import numpy as np
from PIL import Image


class CheckbinGetImageBinNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"bin": ("CHECKBIN",), "name": ("STRING",)},
        }

    RETURN_TYPES = ("CHECKBIN", "IMAGE")
    RETURN_NAMES = ("bin", "image")
    CATEGORY = "comparison"
    FUNCTION = "get_image"

    def get_image(self, bin: checkbin.Bin, name: str):
        file_url = bin.get_input_file_url(name)

        if file_url is None:
            raise ValueError(f"No file found with name: {name}")

        suffix = os.path.splitext(file_url)[1].lower()
        with tempfile.NamedTemporaryFile(suffix=suffix) as tmp_file:
            response = requests.get(file_url)
            response.raise_for_status()
            tmp_file.write(response.content)
            tmp_file.flush()

            image = Image.open(tmp_file.name)
            image = image.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
        return (bin, image)


class CheckbinGetStringBinNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"bin": ("CHECKBIN",), "name": ("STRING",)},
        }

    RETURN_TYPES = ("CHECKBIN", "STRING")
    RETURN_NAMES = ("bin", "string")
    CATEGORY = "comparison"
    FUNCTION = "get_string"

    def get_string(self, bin: checkbin.Bin, name: str):
        string = bin.get_input_data(name)

        if string is None:
            raise ValueError(f"No data found with name: {name}")

        if not isinstance(string, str):
            raise ValueError(f"Data is not a string: {type(string)}")

        return (bin, string)


class CheckbinSaveImageBinNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bin": ("CHECKBIN",),
                "image": ("IMAGE",),
                "name": ("STRING",),
            },
        }

    RETURN_TYPES = ("CHECKBIN", "IMAGE")
    RETURN_NAMES = ("bin", "image")
    CATEGORY = "comparison"
    FUNCTION = "save_image"

    def save_image(self, bin: checkbin.Bin, image: torch.Tensor, name: str):
        bin.checkin(name)
        pil_image = 255.0 * image[0].cpu().numpy()
        pil_image = Image.fromarray(np.clip(pil_image, 0, 255).astype(np.uint8))
        bin.upload_image(name, pil_image)
        return (bin, image)


class CheckbinSaveStringBinNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bin": ("CHECKBIN",),
                "string": ("STRING",),
                "name": ("STRING",),
            },
        }

    RETURN_TYPES = ("CHECKBIN", "STRING")
    RETURN_NAMES = ("bin", "string")
    CATEGORY = "comparison"
    FUNCTION = "save_string"

    def save_string(self, bin: checkbin.Bin, string: str, name: str):
        bin.checkin(name)
        bin.add_state(name, string)
        return (bin, string)


class CheckbinSubmitBinNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bin": ("CHECKBIN",),
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True

    CATEGORY = "comparison"
    FUNCTION = "submit_bin"

    def submit_bin(self, bin: checkbin.Bin):
        bin.submit()
        return ()
