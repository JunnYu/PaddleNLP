# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from collections import OrderedDict

huggingface_to_paddle = {
    "embeddings.LayerNorm": "embeddings.layer_norm",
    "encoder.layer": "encoder.layers",
    "attention.self.query.": "self_attn.q_proj.",
    "attention.self.key.": "self_attn.k_proj.",
    "attention.self.value.": "self_attn.v_proj.",
    "attention.output.dense.": "self_attn.out_proj.",
    "intermediate.dense": "linear1",
    "output.dense": "linear2",
    "attention.output.LayerNorm": "norm1",
    "output.LayerNorm": "norm2",
    "attention.self.key_conv_attn_layer": "self_attn.key_conv_attn_layer",
    "attention.self.conv_kernel_layer": "self_attn.conv_kernel_layer",
    "attention.self.conv_out_layer": "self_attn.conv_out_layer",
}

skip_weights = ["embeddings.position_ids"]
dont_transpose = ["attention.self.key_conv_attn_layer", "_embeddings.weight", "LayerNorm."]


def convert_pytorch_checkpoint_to_paddle(pytorch_checkpoint_path, paddle_dump_path):
    import paddle
    import torch

    pytorch_state_dict = torch.load(pytorch_checkpoint_path, map_location="cpu")
    paddle_state_dict = OrderedDict()
    for k, v in pytorch_state_dict.items():
        if k in skip_weights:
            continue
        if k[-7:] == ".weight":
            if not any([w in k for w in dont_transpose]):
                if v.ndim == 2:
                    v = v.transpose(0, 1)
        if "self.key_conv_attn_layer.bias" in k:
            v = v.squeeze(-1)

        oldk = k
        for huggingface_name, paddle_name in huggingface_to_paddle.items():
            k = k.replace(huggingface_name, paddle_name)

        print(f"Converting: {oldk} => {k}")
        paddle_state_dict[k] = v.data.numpy()

    paddle.save(paddle_state_dict, paddle_dump_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pytorch_checkpoint_path",
        default="./conv-bert-base/pytorch_model.bin",
        type=str,
        required=False,
        help="Path to the Pytorch checkpoint path.",
    )
    parser.add_argument(
        "--paddle_dump_path",
        default="./convbert-base/model_state.pdparams",
        type=str,
        required=False,
        help="Path to the output Paddle model.",
    )
    args = parser.parse_args()
    convert_pytorch_checkpoint_to_paddle(args.pytorch_checkpoint_path, args.paddle_dump_path)
