import torch
import numpy as np
from torch import nn
import torch.autograd.profiler as profiler

class MyModule(nn.Module):
    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super(MyModule, self).__init__()
        self.linear = nn.Linear(in_features, out_features, bias)

    def forward(self, input, mask):
        with profiler.record_function("LINEAR"):
            out = self.linear(input)

        with profiler.record_function("MASK INDICES"):
            threshold = out.sum(axis=1).mean().item()
            # hi_idx = (mask > threshold).nonzero(as_tuple=True)
            hi_idx = np.argwhere(mask.cpu().numpy() > threshold)
            hi_idx = torch.from_numpy(hi_idx)

        return out, hi_idx

torch.set_default_device('mps')
# device = torch.device('mps')

model = MyModule(500, 10)
input = torch.rand(128, 500)
mask = torch.rand((500, 500, 500), dtype=torch.float32)

# warm-up
# prof = torch.autograd.profiler.profile(profile_memory=False, record_shapes=True, with_stack=True)
prof = torch.profiler.profile(profile_memory=True, record_shapes=True, with_stack=True)

model(input, mask) # warm-up

prof.start()
out, idx = model(input, mask)
prof.step()

prof.stop()

print(prof.key_averages(group_by_stack_n=5).table(sort_by='cpu_memory_usage', row_limit=-1))
# print(prof.key_averages(group_by_stack_n=5).table(sort_by="cpu_memory_usage", row_limit=-1))
prof.export_chrome_trace("trace.json")