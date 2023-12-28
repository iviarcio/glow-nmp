# Copyright (c) Glow Contributors. See CONTRIBUTORS file.
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

from __future__ import absolute_import, division, print_function, unicode_literals

import random

import torch
from tests import utils


class SimplePixelShuffleModel(torch.nn.Module):
    def __init__(self, upscale_factor):
        super(SimplePixelShuffleModel, self).__init__()
        self.upscale_factor = upscale_factor
        self.ps = torch.nn.PixelShuffle(self.upscale_factor)

    def forward(self, tensor):
        return self.ps(tensor)


class TestPixelShuffle(utils.TorchGlowTestCase):
    def test_pixel_shuffle(self):
        """Test of the PyTorch pixel_shuffle Node on Glow."""

        for _ in range(20):
            c = random.randint(1, 3)
            r = random.randint(2, 5)
            w = random.randint(1, 100)
            h = random.randint(1, 100)
            b = random.randint(1, 10)

            utils.compare_tracing_methods(
                SimplePixelShuffleModel(r),
                torch.randn(b, c * r * r, w, h),
                fusible_ops={"aten::pixel_shuffle"},
            )
