from .run_node import CheckbinStartRunNode
from .bin_node import (
    CheckbinGetImageBinNode,
    CheckbinGetStringBinNode,
    CheckbinSaveImageBinNode,
    CheckbinSaveStringBinNode,
    CheckbinSubmitBinNode,
)

NODE_CLASS_MAPPINGS = {
    "Checkbin Start Run": CheckbinStartRunNode,
    "Checkbin Get Image Bin": CheckbinGetImageBinNode,
    "Checkbin Get String Bin": CheckbinGetStringBinNode,
    "Checkbin Save Image Bin": CheckbinSaveImageBinNode,
    "Checkbin Save String Bin": CheckbinSaveStringBinNode,
    "Checkbin Submit Bin": CheckbinSubmitBinNode,
}
__all__ = ["NODE_CLASS_MAPPINGS"]
